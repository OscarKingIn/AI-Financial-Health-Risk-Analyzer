from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reports = db.relationship('Report', backref='user', lazy=True)

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    risk_score = db.Column(db.Integer)
    total_income = db.Column(db.Float, default=0.0)
    total_expense = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    paid = db.Column(db.Boolean, default=False)
    
    # SaaS Extensions (Stripe integration)
    stripe_session_id = db.Column(db.String(255))
    summary_data = db.Column(db.JSON) 
    transactions = db.relationship('Transaction', backref='report', lazy=True)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey('report.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100))

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey('report.id'), nullable=False)
    stripe_payment_intent_id = db.Column(db.String(255))
    amount = db.Column(db.Float)
    status = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
