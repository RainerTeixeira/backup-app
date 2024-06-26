from flask import render_template, redirect, url_for, session, jsonify
from . import mysql_bp
from utils.mysql_utils import get_mysql_info

@mysql_bp.route('/mysql')
def mysql():
    """Rota para exibir informações do MySQL."""
    if not session.get('logged_in'):
        return redirect(url_for('auth.login'))
    mysql_info = get_mysql_info()
    return render_template('mysql.html', mysql_info=mysql_info)

@mysql_bp.route('/api/mysql-info')
def api_mysql_info():
    """API para obter informações do MySQL."""
    if not session.get('logged_in'):
        return redirect(url_for('auth.login'))
    return jsonify(get_mysql_info())
