from flask import render_template, redirect, url_for, flash, request, session, send_file
from . import backup_bp
import os
import config

backup_dir = config.app_config['UPLOAD_FOLDER']

@backup_bp.route('/backup')
def backup():
    """Rota para exibir a lista de backups."""
    if not session.get('logged_in'):
        return redirect(url_for('auth.login'))
    backups = os.listdir(backup_dir)
    return render_template('backup.html', backups=backups)

@backup_bp.route('/download/<filename>')
def download_backup(filename):
    """Rota para baixar um backup específico."""
    if not session.get('logged_in'):
        return redirect(url_for('auth.login'))
    file_path = os.path.join(backup_dir, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        flash('Arquivo não encontrado')
        return redirect(url_for('backup.backup'))

@backup_bp.route('/upload', methods=['POST'])
def upload_backup():
    """Rota para fazer upload de um backup."""
    if not session.get('logged_in'):
        return redirect(url_for('auth.login'))
    if 'file' not in request.files:
        flash('Nenhum arquivo selecionado')
        return redirect(url_for('backup.backup'))

    file = request.files['file']
    if file.filename == '':
        flash('Nenhum arquivo selecionado')
        return redirect(url_for('backup.backup'))

    file_path = os.path.join(backup_dir, file.filename)
    file.save(file_path)
    flash('Backup enviado com sucesso', 'success')
    return redirect(url_for('backup.backup'))

@backup_bp.route('/delete/<filename>', methods=['POST'])
def delete_backup(filename):
    """Rota para deletar um backup específico."""
    if not session.get('logged_in'):
        return redirect(url_for('auth.login'))
    file_path = os.path.join(backup_dir, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        flash(f'Backup {filename} excluído com sucesso', 'success')
    else:
        flash('Backup não encontrado', 'error')
    return redirect(url_for('backup.backup'))
