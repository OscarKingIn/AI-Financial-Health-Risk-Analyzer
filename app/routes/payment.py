import os
from flask import Blueprint, request, jsonify, redirect, url_for
from models import db, Report, Payment
from app.services.stripe_service import create_checkout_session, verify_payment_session
import stripe

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/create-checkout-session/<int:report_id>', methods=['POST'])
def create_session(report_id):
    report = Report.query.get_or_404(report_id)
    
    success_url = url_for('report.get_report', report_id=report_id, _external=True) + "?success=true&session_id={CHECKOUT_SESSION_ID}"
    cancel_url = url_for('report.get_report', report_id=report_id, _external=True) + "?cancelled=true"
    
    session = create_checkout_session(report_id, success_url, cancel_url)
    
    if session:
        report.stripe_session_id = session.id
        db.session.commit()
        return jsonify({"checkout_url": session.url})
    
    return jsonify({"error": "Failed to create payment session"}), 500

@payment_bp.route('/webhook', methods=['POST'])
def stripe_webhook():
    payload = request.get_data()
    sig_header = request.headers.get('STRIPE_SIGNATURE')

    try:
        from app.services.stripe_service import construct_event
        event = construct_event(payload, sig_header)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        report_id = session.get('metadata', {}).get('report_id')
        
        if report_id:
            report = Report.query.get(report_id)
            if report and not report.paid: # Added 'and not report.paid'
                report.paid = True
                payment = Payment(
                    report_id=report.id,
                    stripe_payment_intent_id=session.payment_intent,
                    amount=session.amount_total / 100,
                    status="completed"
                )
                db.session.add(payment)
                db.session.commit()

    return jsonify({"status": "success"}), 200
