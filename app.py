import os
from flask import Flask, render_template
from dotenv import load_dotenv
from models import db
from flask_migrate import Migrate

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-123')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    Migrate(app, db)

    # Register Blueprints
    from app.routes.upload import upload_bp
    from app.routes.payment import payment_bp
    from app.routes.report import report_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(upload_bp)
    app.register_blueprint(payment_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(admin_bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/report-page/<int:report_id>')
    def report_page(report_id):
        return render_template('report.html')

    @app.route('/processing/<int:report_id>')
    def processing_page(report_id):
        return render_template('processing.html', report_id=report_id)

    @app.route('/admin/dashboard')
    def admin_dashboard_page():
        return render_template('admin.html')

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true')
