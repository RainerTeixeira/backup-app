from flask import redirect, url_for, flash, request, session, render_template
from app import app
import app.config as config

@app.route('/')
def root():
    """Rota raiz, redireciona para a página de login."""
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
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

@app.route('/home')
def home():
    """Rota para a página inicial."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/logout')
def logout():
    """Rota para logout, redireciona para a página de login."""
    session.pop('logged_in', None)
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('login'))

# Outras rotas relacionadas à autenticação podem ser adicionadas aqui
