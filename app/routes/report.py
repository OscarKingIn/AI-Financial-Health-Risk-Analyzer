from flask import Blueprint, jsonify, send_file, request
from models import Report, Transaction
from app.services.pdf_service import generate_report_pdf

report_bp = Blueprint('report', __name__)

@report_bp.route('/report/<int:report_id>')
def get_report(report_id):
    report = Report.query.get_or_404(report_id)
    
    # Check if payment was just completed (polling fallback)
    session_id = request.args.get('session_id')
    if session_id and not report.paid:
        from app.services.stripe_service import verify_payment_session
        if verify_payment_session(session_id):
            report.paid = True
            from models import db
            db.session.commit()

    return jsonify({
        "id": report.id,
        "score": report.risk_score,
        "is_paid": report.paid,
        "summary": report.summary_data
    })

@report_bp.route('/report/<int:report_id>/download')
def download_report(report_id):
    report = Report.query.get_or_404(report_id)
    
    if not report.paid:
        return jsonify({"error": "Payment required"}), 402
    
    transactions = Transaction.query.filter_by(report_id=report.id).all()
    pdf_path = generate_report_pdf(report, transactions)
    
    return send_file(
        pdf_path,
        as_attachment=True,
        download_name=f"Financial_Report_{report.id}.pdf"
    )
