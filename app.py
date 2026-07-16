from flask import Flask, redirect, url_for
from config import Config
from extensions import db, login_manager
from models import User
from werkzeug.security import generate_password_hash

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from routes.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from routes.dashboard import bp as dashboard_bp
    app.register_blueprint(dashboard_bp)

    from routes.revenue import bp as revenue_bp
    app.register_blueprint(revenue_bp, url_prefix='/revenue')

    from routes.expenses import bp as expenses_bp
    app.register_blueprint(expenses_bp, url_prefix='/expenses')

    from routes.clients import bp as clients_bp
    app.register_blueprint(clients_bp, url_prefix='/clients')

    from routes.projects import bp as projects_bp
    app.register_blueprint(projects_bp, url_prefix='/projects')

    from routes.settings import bp as settings_bp
    app.register_blueprint(settings_bp, url_prefix='/settings')

    from routes.reports import bp as reports_bp
    app.register_blueprint(reports_bp, url_prefix='/reports')
    
    from routes.transfers import bp as transfers_bp
    app.register_blueprint(transfers_bp, url_prefix='/transfers')

    @app.route('/')
    def index():
        return redirect(url_for('dashboard.index'))
        
    @app.cli.command("init-db")
    def init_db():
        with app.app_context():
            db.create_all()
            from models import Setting
            if not Setting.query.first():
                setting = Setting(opening_cash=0, opening_online=0)
                db.session.add(setting)
            if not User.query.filter_by(username=app.config['ADMIN_USERNAME']).first():
                admin = User(
                    username=app.config['ADMIN_USERNAME'],
                    password=app.config['ADMIN_PASSWORD']
                )
                db.session.add(admin)
            db.session.commit()
            print("Database initialized.")

    return app

# Expose app at the top level for Vercel
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)