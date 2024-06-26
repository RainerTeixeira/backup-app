from mega import Mega
import app.config as config

def login_mega():
    """Realiza login no MEGA e retorna o cliente MEGA."""
    mega_email = config.mega_credentials['email']
    mega_password = config.mega_credentials['password']
    mega_instance = Mega()
    mega_client = mega_instance.login(mega_email, mega_password)
    return mega_client

def upload_to_mega(file_path):
    """Faz upload de um arquivo para o MEGA."""
    try:
        mega_client = login_mega()
        mega_client.upload(file_path)
        print(f'{file_path} enviado para o MEGA com sucesso.')
    except Exception as e:
        print(f'Erro ao enviar {file_path} para o MEGA: {str(e)}')

def get_mega_storage_info():
    """Obtém informações de armazenamento do MEGA."""
    try:
        mega_client = login_mega()
        account_info = mega_client.get_user()

        total_space = account_info['total_space']
        used_space = account_info['used_space']
        free_space = total_space - used_space

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
