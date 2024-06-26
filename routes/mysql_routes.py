from flask import redirect, url_for, flash, session, render_template, jsonify
from app import app
from routes.utils import get_system_info

@app.route('/system-info')
def system_info():
    """Rota para exibir informações do sistema."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    system_info_data = get_system_info()
    return render_template('system_info.html', system_info=system_info_data)

@app.route('/api/system-info')
def api_system_info():
    """API para obter informações do sistema."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return jsonify(get_system_info())

# Outras rotas relacionadas às informações do sistema podem ser adicionadas aqui
