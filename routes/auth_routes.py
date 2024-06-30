# routes/auth_routes.py

import logging
from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from config import user_credentials

logger = logging.getLogger(__name__)
auth_bp = Blueprint('auth', __name__)


def login_required(func):
    """
    Decorator que verifica se o usuário está logado antes de acessar a rota.

    Este decorator verifica se a chave 'logged_in' está presente na sessão do usuário.
    Se não estiver presente, redireciona para a página de login e exibe uma mensagem de erro.
    Caso contrário, permite o acesso à rota decorada.

    Returns:
        function: Função decorada que requer autenticação.
    """
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not session.get('logged_in'):
            flash('É necessário estar logado para acessar esta página.', 'error')
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    return decorated_view


############################################
#             Rota para login.             #
############################################
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Rota para login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == user_credentials['username'] and password == user_credentials['password']:
            session['logged_in'] = True
            logger.info(f'Usuário {username} fez login com sucesso.')
            return redirect(url_for('home.home'))  # Corrigido para 'home.home'

        else:
            flash('Usuário ou senha incorretos.', 'error')
            logger.warning(f'Tentativa de login falhou para o usuário {username}.')
    
    # Se o método for GET ou se houver erro no login, renderiza o template de login
    return render_template('login.html')

############################################
#     ROTA REDIRECIONAR PARA LOGOUT        #
############################################

@auth_bp.route('/logout')
@login_required
def logout():
    """Rota para logout, redireciona para a página de login."""
    session.pop('logged_in', None)
    flash('Você foi desconectado.', 'info')
    logger.info('Usuário desconectado.')
    return redirect(url_for('auth.login'))

###################################################
#  Rota raiz, redireciona para a página de login  #
###################################################

@auth_bp.route('/')
def root():
    if session.get('logged_in'):
        # Redireciona para a página inicial do site após o login
        return redirect(url_for('home.home'))
    else:
        # Se não estiver logado, redireciona para a página de login
        return redirect(url_for('auth.login'))
