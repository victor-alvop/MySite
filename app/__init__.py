from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    db.init_app(app)

    from app.routes.home import home_bp
    from app.routes.home import store_warehouse_bp
    from app.routes.datashake import datashake_bp
    from app.routes.cryptoInfo import crypto_info_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(datashake_bp)
    app.register_blueprint(crypto_info_bp, url_prefix='/crypto')
    app.register_blueprint(store_warehouse_bp)

    return app





