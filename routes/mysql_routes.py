# routes/mysql_routes.py
from flask import Blueprint, render_template, session, redirect, url_for, jsonify
from utils.mysql_utils import get_mysql_info, get_mysql_table_data
from config import mysql_credentials

import plotly.graph_objs as go
import plotly.express as px

mysql_bp = Blueprint('mysql', __name__)

@mysql_bp.route('/mysql')
def mysql_route():
    """Rota para exibir informações do MySQL."""
    # Verifica se o usuário está autenticado
    if not session.get('logged_in'):
        return redirect(url_for('auth.login'))

    # Recupera as informações do MySQL
    mysql_info = get_mysql_info()

    # Exemplo de dados de tabela (substitua pelo seu próprio método)
    table_data = get_mysql_table_data()

    # Exemplo de gráfico Plotly (substitua pelo seu próprio método)
    fig = px.bar(table_data, x='column_x', y='column_y', title='Exemplo de Gráfico')

    return render_template('mysql.html', mysql_info=mysql_info, table_data=table_data, plot_div=fig.to_html(include_plotlyjs='cdn'))

@mysql_bp.route('/api/mysql-info')
def api_mysql_info():
    """API para obter informações do MySQL."""
    # Verifica se o usuário está autenticado
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401

    # Autentica o usuário com base no nome de usuário apenas
    if session.get('username') != mysql_credentials['user']:
        return jsonify({'error': 'Unauthorized'}), 401

    # Recupera as informações do MySQL
    mysql_info = get_mysql_info()
    return jsonify(mysql_info)

@mysql_bp.route('/test_mysql_connection', methods=['GET'])
def test_mysql():
    """Rota para testar a conexão com o MySQL."""
    # Recupera as informações do MySQL
    mysql_info = get_mysql_info()
    if mysql_info['server_version'] != 'Erro ao obter informações do MySQL':
        print("Postman conectado ao MySQL com sucesso!")  # Apenas para debug no console
        return jsonify({'message': 'Conexão com MySQL estabelecida e informações obtidas com sucesso!', 'mysql_info': mysql_info}), 200
    else:
        print("Erro ao conectar ou obter informações do MySQL.")
        return jsonify({'error': 'Falha ao conectar ou obter informações do MySQL.'}), 500
