# app.py

from flask import Flask, render_template, send_file, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from google.oauth2 import service_account
from googleapiclient.discovery import build
import mysql.connector
import psutil

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/home/ubuntu/backup-app/backupSQL'
app.secret_key = 'sua_chave_secreta_aqui'

backup_dir = app.config['UPLOAD_FOLDER']
credentials_path = '/home/ubuntu/backup-app/backup-Chave-Google-427505-7e5ba27b4500.json'

login_manager = LoginManager()
login_manager.init_app(app)

scheduler = BackgroundScheduler()
scheduler.start()

# Usuário de exemplo para autenticação
class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'ubuntu' and password == 'ubuntu':  # Simples validação de usuário
            user = User(id=1)
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Credenciais inválidas')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Upload para o Google Drive
def upload_to_google_drive(filename):
    scopes = ['https://www.googleapis.com/auth/drive.file']
    credentials = service_account.Credentials.from_service_account_file(credentials_path, scopes=scopes)
    service = build('drive', 'v3', credentials=credentials)

    file_metadata = {'name': os.path.basename(filename)}
    media = {'mimeType': 'application/octet-stream', 'body': open(filename, 'rb')}
    service.files().create(body=file_metadata, media_body=media).execute()

# Agendamento de backups
def schedule_backup():
    scheduler.add_job(upload_to_google_drive, CronTrigger(hour=11, minute=0), args=[latest_backup()])

def latest_backup():
    backups = os.listdir(backup_dir)
    if backups:
        backups.sort(key=lambda x: os.path.getmtime(os.path.join(backup_dir, x)), reverse=True)
        return os.path.join(backup_dir, backups[0])
    else:
        return None

# Informações do MySQL
def get_mysql_info():
    try:
        connection = mysql.connector.connect(
            user='venda', password='Vend@171!', host='192.168.1.250', database='dbrsvendas'
        )
        cursor = connection.cursor()
        cursor.execute("SHOW STATUS")
        status = cursor.fetchall()
        return status
    except mysql.connector.Error as err:
        return {'error': str(err)}
    finally:
        if connection:
            connection.close()

# Informações do sistema
def get_system_info():
    disk_usage = psutil.disk_usage('/')
    memory_info = psutil.virtual_memory()
    cpu_info = psutil.cpu_percent(interval=1)
    return {
        'disk_usage': disk_usage._asdict(),
        'memory_info': memory_info._asdict(),
        'cpu_info': cpu_info
    }

@app.route('/')
@login_required
def index():
    return render_template('home.html')

@app.route('/mysql')
@login_required
def mysql():
    mysql_info = get_mysql_info()
    return render_template('mysql.html', mysql_info=mysql_info)

@app.route('/system-info')
@login_required
def system_info():
    system_info = get_system_info()
    return render_template('system_info.html', system_info=system_info)

@app.route('/backup')
@login_required
def backup():
    backups = os.listdir(backup_dir)
    return render_template('backup.html', backups=backups)

@app.route('/download/<filename>')
@login_required
def download_backup(filename):
    file_path = os.path.join(backup_dir, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        flash('Arquivo não encontrado')
        return redirect(url_for('backup'))

@app.route('/upload', methods=['POST'])
@login_required
def upload_backup():
    if 'file' not in request.files:
        flash('Nenhum arquivo selecionado')
        return redirect(url_for('backup'))

    file = request.files['file']
    if file.filename == '':
        flash('Nenhum arquivo selecionado')
        return redirect(url_for('backup'))

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    flash('Backup enviado com sucesso')
    return redirect(url_for('backup'))

# API para informações do sistema (AJAX)
@app.route('/api/system-info')
@login_required
def api_system_info():
    return jsonify(get_system_info())

# API para informações do MySQL (AJAX)
@app.route('/api/mysql-info')
@login_required
def api_mysql_info():
    return jsonify(get_mysql_info())

# Iniciar o agendamento de backups
schedule_backup()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
