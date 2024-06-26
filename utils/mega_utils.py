import config
from mega import Mega

mega_email = config.mega_credentials['email']
mega_password = config.mega_credentials['password']
mega = Mega()
mega_client = mega.login(mega_email, mega_password)

def get_mega_storage_info():
    """Função para obter informações de armazenamento do MEGA."""
    try:
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
