from flask import Flask

from .extensions import db, migrate, login_manager, bcrypt, settings, qrcode
from .error.error import page_not_found, forbidden, internal_server_error
from .models import User
from .admin.views import admin
from .api.views import api
from .auth.views import auth
from .dashboard.views import dashboard
from .home.views import home
from .media_uploader.views import media_uploader
from .membership.views import membership

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    app.config["SECRET_KEY"] = settings["SECRET_KEY"]
    app.config["UPLOAD_FOLDER"] = "media/"
    app.url_map.strict_slashes = False
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(403, forbidden)
    app.register_error_handler(500, internal_server_error)

    db.init_app(app)
    with app.app_context():
        db.create_all()
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    qrcode.init_app(app)
    
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "warning"

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    app.register_blueprint(admin)
    app.register_blueprint(api)
    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
    app.register_blueprint(home)
    app.register_blueprint(media_uploader)
    app.register_blueprint(membership)

    return app