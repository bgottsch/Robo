#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 00:03:39 2018

@author: Beno
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from Robo.scheduler import Scheduler
from Robo.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
scheduler = Scheduler()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'danger'


def create_app(config_class=Config):
    
    app = Flask(__name__)
    app.config.from_object(Config)

    with app.app_context():
        db.init_app(app)
        
    bcrypt.init_app(app)
    login_manager.init_app(app)
    
    scheduler.init_app(app)
    scheduler.start()

    from Robo.users.routes import users
    from Robo.dashboard.routes import dashboard
    from Robo.logs.routes import logs
    from Robo.settings.routes import settings
    
    app.register_blueprint(users)
    app.register_blueprint(dashboard)
    app.register_blueprint(logs)
    app.register_blueprint(settings)

    return app
