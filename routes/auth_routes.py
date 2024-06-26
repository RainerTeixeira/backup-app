from flask import render_template, redirect, url_for, flash, request, session
from . import auth_bp
import config

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Rota para login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == config.user_credentials['username'] and password == config.user_credentials['password']:
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            flash('Usuário ou senha incorretos.', 'error')
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    """Rota para logout, redireciona para a página de login."""
    session.pop('logged_in', None)
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('auth.login'))
