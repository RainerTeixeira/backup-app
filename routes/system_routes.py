# routes/system_routes.py

from flask import Blueprint, render_template, session, redirect, url_for, jsonify
from utils.system_utils import get_system_info

system_bp = Blueprint('system', __name__)

@system_bp.route('/system-info')
def system_info():
    """Rota para exibir informações do sistema."""
    if not session.get('logged_in'):
        return redirect(url_for('auth.login'))
    system_info_data = get_system_info()
    return render_template('system_info.html', system_info=system_info_data)

@system_bp.route('/api/system-info')
def api_system_info():
    """API para obter informações do sistema."""
    if not session.get('logged_in'):
        return redirect(url_for('auth.login'))
    return jsonify(get_system_info())
