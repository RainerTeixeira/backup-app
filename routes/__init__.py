# routes/__init__.py

from flask import Blueprint          
from .backup_routes import backup_bp        #importação correta para Backup
from .auth_routes import auth_bp
from .mysql_routes import mysql_bp          #importação correta para mysql_bp
from .system_routes import system_bp        #importação correta para system_bp
from .home_routes import home_bp            #importação correta para home_bp


def register_blueprints(app):
    app.register_blueprint(backup_bp, url_prefix='/backup')
    app.register_blueprint(mysql_bp, url_prefix='/mysql')
    app.register_blueprint(system_bp, url_prefix='/system')
    app.register_blueprint(home_bp, url_prefix='/home')
