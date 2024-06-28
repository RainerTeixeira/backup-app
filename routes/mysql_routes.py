# routes/mysql_routes.py

from flask import Blueprint, render_template, session, redirect, url_for, jsonify
from utils.mysql_utils import get_mysql_info
from config import mysql_credentials

mysql_bp = Blueprint('mysql', __name__)

@mysql_bp.route('/mysql')
def mysql_route():
    """Rota para exibir informações do MySQL."""
    if not session.get('logged_in'):
        return redirect(url_for('auth.login'))

    # Autentica o usuário com base nas credenciais em config.py
    if session.get('username') != mysql_credentials['user'] or session.get('password') != mysql_credentials['password']:
        return redirect(url_for('auth.login'))

    mysql_info = get_mysql_info()
    return render_template('mysql.html', mysql_info=mysql_info)

@mysql_bp.route('/api/mysql-info')
def api_mysql_info():
    """API para obter informações do MySQL."""
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401

    # Autentica o usuário com base nas credenciais em config.py
    if session.get('username') != mysql_credentials['user'] or session.get('password') != mysql_credentials['password']:
        return jsonify({'error': 'Unauthorized'}), 401

    mysql_info = get_mysql_info()
    return jsonify(mysql_info)
