# app/__init__.py

import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    with app.app_context():
        # Import parts of our application
        from . import models

        # Import and register blueprints
        # This line imports the variables we defined in app/routes/__init__.py
        from app.routes import auth_bp, admin_bp, patient_bp, doctor_bp

        app.register_blueprint(auth_bp)
        app.register_blueprint(admin_bp)
        app.register_blueprint(patient_bp)
        app.register_blueprint(doctor_bp) # <-- This line registers our new module

        # Create database tables for our models
        db.create_all()

    @app.route('/')
    def index():
        return render_template('index.html')

    return app