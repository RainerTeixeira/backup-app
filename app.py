# app.py

from flask import Flask, redirect, url_for, session
from routes.auth_routes import auth_bp, logout as auth_logout
from routes.home_routes import home_bp
from routes.mysql_routes import mysql_bp
from routes.backup_routes import backup_bp
from routes.system_routes import system_bp
from routes import register_blueprints
from config import app_config


app = Flask(__name__)
app.config['SECRET_KEY'] = app_config['SECRET_KEY']

# Registro dos blueprints
app.register_blueprint(backup_bp, url_prefix='/backup')
app.register_blueprint(mysql_bp, url_prefix='/mysql')
app.register_blueprint(auth_bp)
app.register_blueprint(home_bp, url_prefix='/home')  # Verifique se usa o mesmo prefixo '/home'
app.register_blueprint(system_bp, url_prefix='/system')



# Rota para logout, redireciona para a página de login
@app.route('/logout')
def logout():
    """Rota para logout, redireciona para a página de login."""
    return auth_logout()

if __name__ == '__main__':
    app.run(debug=True, host='192.168.1.250', port=8000)
