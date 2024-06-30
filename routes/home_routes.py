# Importações do Flask para funcionalidades web
from flask import Blueprint         # Blueprint para definição de rotas
from flask import render_template   # Renderização de templates HTML

# Importação de decorador para autenticação
from routes.auth_routes import login_required   # Decorador para exigir autenticação

# Blueprint para rotas relacionadas à página inicial (home)
home_bp = Blueprint('home', __name__)


##################################################
#     Rota para a página inicial da aplicação    #     
##################################################

@home_bp.route('/')
@login_required
def home():
    """Rota para a página inicial."""
    return render_template('home.html')

