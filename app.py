from flask import Flask, render_template, redirect, url_for, flash, request, session, send_file, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from mega import Mega
import mysql.connector
import os
from pytz import timezone
import app.config as config  # Importar as configurações

# Inicializa a aplicação Flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = config.app_config['UPLOAD_FOLDER']
app.secret_key = config.app_config['SECRET_KEY']

# Configurações do diretório de backup e credenciais do MEGA
backup_dir = app.config['UPLOAD_FOLDER']
mega_email = config.mega_credentials['email']
mega_password = config.mega_credentials['password']

# Inicializa o cliente MEGA
mega_instance = Mega()
mega_client = mega_instance.login(mega_email, mega_password)

# Configura o fuso horário para 'America/Sao_Paulo'
os.environ['TZ'] = 'America/Sao_Paulo'

# Inicializa o agendador de tarefas
scheduler = BackgroundScheduler()
scheduler.start()

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

@app.route('/mysql')
def mysql_route():
    """Rota para exibir informações do MySQL."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    mysql_info = get_mysql_info()
    return render_template('mysql.html', mysql_info=mysql_info)

@app.route('/system-info')
def system_info():
    """Rota para exibir informações do sistema."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    system_info_data = get_system_info()
    return render_template('system_info.html', system_info=system_info_data)

@app.route('/backup')
def backup():
    """Rota para exibir a lista de backups."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    backups = os.listdir(backup_dir)
    return render_template('backup.html', backups=backups)

@app.route('/logout')
def logout():
    """Rota para logout, redireciona para a página de login."""
    session.pop('logged_in', None)
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('login'))

def get_mysql_connection():
    """Função para obter a conexão com o banco de dados MySQL."""
    try:
        connection = mysql.connector.connect(
            user=config.mysql_credentials['user'], 
            password=config.mysql_credentials['password'], 
            host=config.mysql_credentials['host'], 
            database=config.mysql_credentials['database']
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao MySQL: {err}")
        return None

def get_mysql_info():
    """Função para obter informações de status do MySQL."""
    connection = get_mysql_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SHOW STATUS")
            status = cursor.fetchall()
            return status
        except mysql.connector.Error as err:
            print(f"Erro ao executar consulta MySQL: {err}")
            return {'error': str(err)}
        finally:
            connection.close()
    else:
        return {'error': 'Não foi possível conectar ao MySQL'}

def get_mega_storage_info():
    """Função para obter informações de armazenamento do MEGA."""
    try:
        # Logar no Mega com as credenciais definidas anteriormente
        account_info = mega_client.get_user()

        # Calcular o espaço disponível
        total_space = account_info['total_space']
        used_space = account_info['used_space']
        free_space = total_space - used_space

        # Formatar os valores para exibição
        total_space_gb = total_space / (1024 * 1024 * 1024)
        used_space_gb = used_space / (1024 * 1024 * 1024)
        free_space_gb = free_space / (1024 * 1024 * 1024)

        return {
            'total_space': total_space_gb,
            'used_space': used_space_gb,
            'free_space': free_space_gb
        }
    except Exception as e:
        print(f"Erro ao obter informações do Mega: {str(e)}")
        return None

def get_system_info():
    """Função para obter informações do sistema."""
    return {
        'disk_usage': {'total': 0, 'used': 0, 'free': 0},  # Substitua com lógica real se necessário
        'memory_info': {'total': 0, 'used': 0, 'free': 0},  # Substitua com lógica real se necessário
        'cpu_info': 0  # Substitua com lógica real se necessário
    }

@app.route('/download/<filename>')
def download_backup(filename):
    """Rota para baixar um backup específico."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    file_path = os.path.join(backup_dir, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        flash('Arquivo não encontrado')
        return redirect(url_for('backup'))

@app.route('/upload', methods=['POST'])
def upload_backup():
    """Rota para fazer upload de um backup."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if 'file' not in request.files:
        flash('Nenhum arquivo selecionado')
        return redirect(url_for('backup'))

    file = request.files['file']
    if file.filename == '':
        flash('Nenhum arquivo selecionado')
        return redirect(url_for('backup'))

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    flash('Backup enviado com sucesso', 'success')
    return redirect(url_for('backup'))

@app.route('/api/system-info')
def api_system_info():
    """API para obter informações do sistema."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return jsonify(get_system_info())

@app.route('/api/mysql-info')
def api_mysql_info():
    """API para obter informações do MySQL."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return jsonify(get_mysql_info())

@app.route('/delete/<filename>', methods=['POST'])
def delete_backup(filename):
    """Rota para deletar um backup específico."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        flash(f'Backup {filename} excluído com sucesso', 'success')
    else:
        flash('Backup não encontrado', 'error')
    return redirect(url_for('backup'))

def upload_to_mega(file_path):
    """Função para fazer upload de um arquivo para o MEGA."""
    try:
        mega_client.upload(file_path)
        print(f'{file_path} enviado para o MEGA com sucesso.')
    except Exception as e:
        print(f'Erro ao enviar {file_path} para o MEGA: {str(e)}')

@app.route('/trigger-backup', methods=['POST'])
def trigger_backup():
    """Rota para iniciar manualmente um backup."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    latest_backup = max([os.path.join(backup_dir, f) for f in os.listdir(backup_dir)], key=os.path.getctime)
    if latest_backup:
        upload_to_mega(latest_backup)
        flash('Backup iniciado manualmente', 'info')
    else:
        flash('Nenhum backup encontrado para enviar.', 'error')
    return redirect(url_for('backup'))

@app.route('/test-mysql')
def test_mysql_connection():
    """Rota para testar a conexão com o MySQL."""
    try:
        connection = get_mysql_connection()
        if connection:
            return 'Conexão MySQL funcionando corretamente!'
        else:
            return 'Erro ao conectar ao MySQL. Verifique as configurações.'
    except Exception as e:
        return f"Erro ao testar a conexão MySQL: {str(e)}"

@app.route('/upload-favicon', methods=['GET'])
def upload_favicon_to_mega():
    """Rota para fazer upload do favicon para o MEGA."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    try:
        file_path = '/home/ubuntu/backup-app/static/img/Favicon.png'
        if not os.path.exists(file_path):
            return 'Arquivo não encontrado'
        upload_to_mega(file_path)
        return 'Favicon enviado para o MEGA com sucesso.'
    except Exception as e:
        return f'Erro ao enviar favicon para o MEGA: {str(e)}'

@app.route('/upload-backup-to-mega', methods=['POST'])
def upload_backup_to_mega():
    """Rota para fazer upload de um backup para o MEGA."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    try:
        if 'backup_file' not in request.files:
            return 'Nenhum arquivo enviado'

        backup_file = request.files['backup_file']
        if backup_file.filename == '':
            return 'Nome de arquivo inválido'

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], backup_file.filename)
        backup_file.save(file_path)
        
        upload_to_mega(file_path)

        return 'Upload bem-sucedido para o Mega.nz'
    except Exception as e:
        return f'Ocorreu um erro: {str(e)}'

@app.route('/api/mega-info')
def api_mega_info():
    """API para obter informações de armazenamento do MEGA."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    storage_info = get_mega_storage_info()
    if storage_info:
        return jsonify(storage_info)
    else:
        return jsonify({'error': 'Não foi possível obter informações do Mega.nz'})

if __name__ == '__main__':
    app.run(debug=True, host='192.168.1.250', port=80)
