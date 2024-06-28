# routes/home_routes.py

from flask import Blueprint, render_template
from routes.auth_routes import login_required
from utils.system_utils import get_system_info

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
@login_required
def home():
    """Rota para a página inicial."""
    system_info_data = get_system_info()
    return render_template('home.html', system_info=system_info_data)
