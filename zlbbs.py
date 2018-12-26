from flask import Flask
import config
from exts import db,mail
from flask_wtf import CSRFProtect

from apps.cms import bp as cms_bp
from apps.common import bp as common_bp
from apps.front import bp as front_bp



def create_app():
    app = Flask(__name__)
    app.register_blueprint(cms_bp)
    app.register_blueprint(front_bp)
    app.register_blueprint(common_bp)
    app.config.from_object(config)
    CSRFProtect(app)
    db.init_app(app)
    mail.init_app(app)
    return app


if __name__ == '__main__':
    # Captcha.gene_graph_captcha()
    app=create_app()
    app.run()
