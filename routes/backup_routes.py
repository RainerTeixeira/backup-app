from flask import redirect, url_for, flash, session, render_template, send_file, request
from app import app, backup_dir
import os

@app.route('/backup')
def backup():
    """Rota para exibir a lista de backups."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    backups = os.listdir(backup_dir)
    return render_template('backup.html', backups=backups)

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

# Outras rotas relacionadas a backups podem ser adicionadas aqui