from flask import Flask, redirect, url_for
from apscheduler.schedulers.background import BackgroundScheduler
import os
import config  # Importar as configurações
from routes import register_blueprints

# Inicializa a aplicação Flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = config.app_config['UPLOAD_FOLDER']
app.secret_key = config.app_config['SECRET_KEY']

# Configura o fuso horário para 'America/Sao_Paulo'
os.environ['TZ'] = 'America/Sao_Paulo'

# Inicializa o agendador de tarefas
scheduler = BackgroundScheduler()
scheduler.start()

# Registra os blueprints
register_blueprints(app)

@app.route('/')
def root():
    """Rota raiz, redireciona para a página de login."""
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    app.run(debug=True, host='192.168.1.250', port=80)
