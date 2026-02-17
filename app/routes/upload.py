import pandas as pd
from flask import Blueprint, request, jsonify
from models import db, User, Transaction, Report
from app.services.ai_service import categorize_transactions
from app.services.risk_engine import calculate_risk_score, aggregate_report_data
import io

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    email = request.form.get('email')
    
    if not email or not file:
        return jsonify({"error": "Email and file are required"}), 400

    try:
        # Get or create user
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(email=email)
            db.session.add(user)
            db.session.commit()

        # Parse CSV
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        df = pd.read_csv(stream)
        
        # Expecting columns: Date, Description, Amount
        # Basic mapping to handle different CSV headers
        df.columns = [c.strip().lower() for c in df.columns]
        
        required_cols = {'date', 'description', 'amount'}
        if not required_cols.issubset(set(df.columns)):
            return jsonify({"error": f"CSV must contain: {required_cols}"}), 400

        raw_transactions = df.to_dict('records')
        
        # Categorize via AI
        categorized_txs = categorize_transactions(raw_transactions)
        
        # Create Report
        report = Report(user_id=user.id)
        db.session.add(report)
        db.session.commit()
        
        # Save Transactions and calculate income flag
        db_txs = []
        for tx in categorized_txs:
            try:
                # Basic parsing handle
                amount = float(str(tx['amount']).replace('$', '').replace(',', ''))
                is_income = amount > 0
                
                new_tx = Transaction(
                    report_id=report.id,
                    date=pd.to_datetime(tx['date']).date(),
                    description=tx['description'],
                    amount=amount,
                    category=tx['category']
                )
                db_txs.append(new_tx)
                db.session.add(new_tx)
            except Exception as e:
                print(f"Skipping row due to error: {e}")

        db.session.commit()

        # Calculate Score and Aggregate Data
        summary = aggregate_report_data(db_txs)
        risk_data = calculate_risk_score(db_txs)
        
        report.risk_score = risk_data['score']
        report.total_income = summary.get('total_income', 0)
        report.total_expense = summary.get('total_expenses', 0)
        
        # Enrich summary with risk analysis
        summary['risk_analysis'] = risk_data['analysis']
        summary['risk_level'] = risk_data['risk_level']
        summary['metrics'] = risk_data['metrics']
        
        report.summary_data = summary
        db.session.commit()

        return jsonify({
            "message": "Report generated successfully",
            "report_id": report.id,
            "score": report.risk_score,
            "risk_level": risk_data['risk_level']
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
