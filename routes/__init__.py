# routes/__init__.py

from flask import Blueprint

# Importando os blueprints de cada módulo
from .backup_routes import backup_bp
from .auth_routes import auth_bp
from .mysql_routes import mysql_bp
from .system_routes import system_bp
from .home_routes import home_bp

def register_blueprints(app):
    # Registrando cada blueprint com um prefixo de URL específico
    app.register_blueprint(backup_bp, url_prefix='/backup')
    app.register_blueprint(mysql_bp, url_prefix='/mysql')
    app.register_blueprint(system_bp, url_prefix='/system')
    app.register_blueprint(home_bp, url_prefix='/home')
