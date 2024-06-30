# Importações do Flask
from flask import session, redirect, url_for, Blueprint, render_template

# Importa as credenciais do Mega.nz
from config import mega_credentials

# Importa a classe Mega da biblioteca mega.py
from mega import Mega

# Inicialização da instância do Mega.nz
mega = Mega()
m = mega.login(mega_credentials['email'], mega_credentials['password'])

# Importações adicionais do Flask
from flask import session  # Importa sessão para gerenciamento de estado do usuário
from flask import redirect  # Importa redirecionamento de URLs
from flask import url_for  # Importa construção de URLs
from flask import Blueprint  # Importa Blueprint para definição de rotas
from flask import render_template  # Importa renderização de templates HTML

###################################################################
#         FUNÇÃO PARA EXIBIR INFORMAÇÃO DO MEGA.NZ               #
###################################################################

def get_mega_storage_info():
    """Função para obter informações de armazenamento do Mega.nz."""
    storage_info = m.get_storage_space()
    total_storage = storage_info['total'] / (1024**3)  # Convertendo bytes para GB
    used_storage = storage_info['used'] / (1024**3)    # Convertendo bytes para GB
    free_storage = total_storage - used_storage        # Convertendo bytes para GB
    return {
        'total_storage': f'{total_storage:.2f} GB',
        'used_storage': f'{used_storage:.2f} GB',
        'free_storage': f'{free_storage:.2f} GB'
    }

###################################################################
#         FUNÇÃO PARA UPLOAD DE BACKUP NO MEGA.NZ                #
###################################################################

def upload_backup_to_mega(file_path):
    """Função para fazer upload de um arquivo de backup para o Mega.nz."""
    try:
        file = m.upload(file_path)
        file_link = m.get_link(file)
        return file_link
    except Exception as e:
        print(f"Erro ao fazer upload do backup: {e}")
        return None
