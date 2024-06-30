
# Importações do Flask para funcionalidades web
from flask import Blueprint         # Blueprint para definição de rotas
from flask import render_template   # Renderização de templates HTML
from flask import session           # Gerenciamento de sessões de usuário
from flask import redirect          # Redirecionamento de URLs
from flask import url_for           # Construção de URLs
from flask import jsonify           # Serialização de objetos para JSON

# Importações do Flask para funcionalidades web
from flask import Blueprint, render_template, session, redirect, url_for, jsonify

# Importações de utilitários do sistema
from utils.system_utils import get_system_info   # Função para obter informações do sistema


# Blueprint para rotas relacionadas ao sistema
system_bp = Blueprint('system', __name__)

###################################################################
# Rota para exibir informações do sistema.
###################################################################
@system_bp.route('/system-info')
def system_info():
    """Rota para exibir informações do sistema."""
    if not session.get('logged_in'):
        return redirect(url_for('auth.login'))
    system_info_data = get_system_info()
    return render_template('system_info.html', system_info_data=system_info_data)

###################################################################
# API para obter informações do sistema.
###################################################################
@system_bp.route('/api/system-info')
def api_system_info():
    """API para obter informações do sistema."""
    if not session.get('logged_in'):
        return redirect(url_for('auth.login'))
    return jsonify(get_system_info())

