from flask import Blueprint, jsonify
from models import Report, User, Payment

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/stats')
def get_stats():
    total_users = User.query.count()
    total_reports = Report.query.count()
    paid_reports = Report.query.filter_by(paid=True).count()
    total_revenue = sum(p.amount for p in Payment.query.all())
    
    return jsonify({
        "total_users": total_users,
        "total_reports": total_reports,
        "paid_reports": paid_reports,
        "total_revenue": total_revenue
    })

@admin_bp.route('/admin/reports')
def list_reports():
    reports = Report.query.order_by(Report.created_at.desc()).limit(50).all()
    return jsonify([{
        "id": r.id,
        "user": r.user.email,
        "score": r.risk_score,
        "is_paid": r.paid,
        "created_at": r.created_at.isoformat()
    } for r in reports])
