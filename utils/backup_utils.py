import os
from config import UPLOAD_FOLDER

def list_backups():
    """Função para listar todos os backups disponíveis."""
    backups = os.listdir(UPLOAD_FOLDER)
    return backups

def get_backup_size(filename):
    """Função para obter o tamanho de um backup específico."""
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    return os.path.getsize(file_path)

def get_backup_path(filename):
    """Função para obter o caminho completo de um backup."""
    return os.path.join(UPLOAD_FOLDER, filename)

def upload_backup(file):
    """Função para fazer upload de um arquivo de backup."""
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    return True

def delete_backup(filename):
    """Função para deletar um backup específico."""
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False
