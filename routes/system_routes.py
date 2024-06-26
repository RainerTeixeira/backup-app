from flask import render_template, redirect, url_for, session, jsonify
from . import system_bp
from utils.system_utils import get_system_info

@system_bp.route('/system-info')
def system_info():
    """Rota para exibir informações do sistema."""
    if not session.get('logged_in'):
        return redirect(url_for('auth.login'))
    system_info = get_system_info()
    return render_template('system_info.html', system_info=system_info)

@system_bp.route('/api/system-info')
def api_system_info():
    """API para obter informações do sistema."""
    if not session.get('logged_in'):
        return redirect(url_for('auth.login'))
    return jsonify(get_system_info())
