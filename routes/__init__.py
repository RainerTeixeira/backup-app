from flask import Blueprint

auth_bp = Blueprint('auth', __name__)
backup_bp = Blueprint('backup', __name__)
mega_bp = Blueprint('mega', __name__)
mysql_bp = Blueprint('mysql', __name__)
system_bp = Blueprint('system', __name__)

# Importar as rotas
from . import auth_routes, backup_routes, mega_routes, mysql_routes, system_routes

def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(backup_bp)
    app.register_blueprint(mega_bp)
    app.register_blueprint(mysql_bp)
    app.register_blueprint(system_bp)
