# Importações do Flask para funcionalidades web
from flask import Blueprint, render_template, session, request, flash, send_file, redirect, url_for
from mega import Mega  # Importação da biblioteca Mega
import os

# Importação da configuração de pasta de upload
from config import UPLOAD_FOLDER

# Importações dos utilitários de backup
from utils.backup_utils import list_backups, get_backup_size, get_backup_path, upload_backup, delete_backup
# Importações dos utilitários do Mega
from utils.mega_utils import upload_backup_to_mega

# Blueprint para rotas relacionadas à página backup
backup_bp = Blueprint('backup', __name__)

##############################################################
#       Rota para exibir a página principal de backups      #
##############################################################
@backup_bp.route('/backup')
def backup_page():
    """Rota para exibir a página principal de backups."""
    if not session.get('logged_in'):
        return redirect(url_for('auth.login'))

    backups = list_backups()
    backup_cards = []
    for filename in backups:
        size = get_backup_size(filename)
        path = get_backup_path(filename)
        backup_cards.append({
            'filename': filename,
            'size': size,
            'path': path
        })

    return render_template('backup.html', backup_cards=backup_cards)

##############################################################
#           Rota para baixar um backup específico           #
##############################################################
@backup_bp.route('/download/<filename>')
def download_backup(filename):
    """Rota para baixar um backup específico."""
    if not session.get('logged_in'):
        return redirect(url_for('auth.login'))

    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        flash('Arquivo não encontrado', 'error')
        return redirect(url_for('backup.backup_page'))

##############################################################
#                   Rota para listar backups                 #
##############################################################
@backup_bp.route('/list')
def list_backups_route():
    """Rota para listar backups."""
    if not session.get('logged_in'):
        return redirect(url_for('auth.login'))

    backups = list_backups()
    return render_template('backup_list.html', backups=backups)

###########################################################
#             Rota para fazer upload de um backup         #
###########################################################
@backup_bp.route('/upload', methods=['POST'])
def upload_backup_route():
    """Rota para fazer upload de um backup."""
    if not session.get('logged_in'):
        return redirect(url_for('auth.login'))

    if 'file' not in request.files:
        flash('Nenhum arquivo selecionado', 'error')
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        flash('Nenhum arquivo selecionado', 'error')
        return redirect(request.url)

    upload_backup(file)
    flash('Upload realizado com sucesso', 'success')
    return redirect(url_for('backup.list_backups_route'))

############################################################
#       Rota para deletar um backup específico             #
############################################################
@backup_bp.route('/delete/<filename>', methods=['POST'])
def delete_backup_route(filename):
    """Rota para deletar um backup específico."""
    if not session.get('logged_in'):
        return redirect(url_for('auth.login'))

    delete_backup(filename)
    flash('Backup deletado com sucesso', 'success')
    return redirect(url_for('backup.list_backups_route'))

#############################################################
#     Rota para fazer upload de backup para o Mega.nz       #
#############################################################
@backup_bp.route('/upload_backup_to_mega', methods=['POST'])
def upload_backup_to_mega_route():
    """Rota para fazer upload de backup para o Mega.nz."""
    if not session.get('logged_in'):
        return redirect(url_for('auth.login'))

    if 'backup_file' not in request.files:
        flash('Nenhum arquivo selecionado', 'error')
        return redirect(request.url)

    file = request.files['backup_file']
    if file.filename == '':
        flash('Nenhum arquivo selecionado', 'error')
        return redirect(request.url)

    result = upload_backup_to_mega(file)
    if result:
        flash('Backup enviado para o Mega.nz com sucesso', 'success')
    else:
        flash('Erro ao enviar backup para o Mega.nz', 'error')

    return redirect(url_for('backup.backup_page'))

##############################################################
# Rota para exibir informações de armazenamento do Mega.nz  #
##############################################################
@backup_bp.route('/mega_storage_info')
def mega_storage_info():
    """Rota para exibir informações de armazenamento do Mega.nz."""
    if not session.get('logged_in'):  # Verifica se o usuário está logado
        return redirect(url_for('auth.login'))  # Redireciona para a página de login se não estiver logado

    storage_info = get_mega_storage_info()  # Obtém informações de armazenamento do Mega.nz
    return render_template('mega_storage.html', storage_info=storage_info)  # Renderiza o template HTML com as informações de armazenamento

##############################################################
#           Rota para cancelar um backup diário              #
##############################################################
@backup_bp.route('/cancel_daily_backup', methods=['POST'])
def cancel_daily_backup():
    """Rota para cancelar um backup diário."""
    if not session.get('logged_in'):
        return redirect(url_for('auth.login'))

    # Implemente a lógica para cancelar o backup diário aqui

    flash('Backup diário cancelado com sucesso', 'success')
    return redirect(url_for('backup.backup_page'))
