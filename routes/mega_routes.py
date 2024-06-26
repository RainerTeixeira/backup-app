from flask import jsonify
from . import mega_bp
from utils.mega_utils import get_mega_storage_info

@mega_bp.route('/api/mega-info')
def api_mega_info():
    """API para obter informações de armazenamento do MEGA."""
    storage_info = get_mega_storage_info()
    if storage_info:
        return jsonify(storage_info)
    else:
        return jsonify({'error': 'Não foi possível obter informações do Mega.nz'})
