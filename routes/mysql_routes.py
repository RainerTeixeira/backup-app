# Importações do Flask para funcionalidades web
from flask import Blueprint         # Blueprint para definição de rotas
from flask import render_template   # Renderização de templates HTML
from flask import session           # Gerenciamento de sessões de usuário
from flask import redirect         # Redirecionamento de URLs
from flask import url_for          # Construção de URLs
from flask import jsonify          # Serialização de objetos para JSON

# Importações de utilitários MySQL
from utils.mysql_utils import get_mysql_info        # Função para obter informações do MySQL
from utils.mysql_utils import get_mysql_tables_info  # Função para obter informações das tabelas do MySQL

# Configurações do MySQL
from config import mysql_credentials   # Credenciais de acesso ao MySQL

# Importações para gráficos com Plotly
import plotly.graph_objs as go   # Módulo para criação de gráficos interativos

# Blueprint para rotas relacionadas ao MySQL
mysql_bp = Blueprint('mysql', __name__)



###################################################################
# Rota para exibir informações do MySQL.                         #
###################################################################
@mysql_bp.route('/mysql')
def mysql_route():
    """Rota para exibir informações do MySQL."""
    # Verifica se o usuário está autenticado
    if not session.get('logged_in'):
        return redirect(url_for('auth.login'))  # Redireciona para login se não estiver logado

    # Recupera as informações do MySQL
    mysql_info = get_mysql_info()

    # Recupera os dados das tabelas do MySQL
    table_data = get_mysql_tables_info()

    # Preparação dos dados para o gráfico de barras com Plotly
    if table_data:
        table_names = [table['Nome da Tabela'] for table in table_data]
        table_sizes = [table['Tamanho Aproximado (KB)'] / 1024 for table in table_data]  # Convertendo para MB
        update_times = [table.get('Última Atualização', 'N/A') for table in table_data]

        # Criação do gráfico de barras com Plotly
        fig = go.Figure()
        fig.add_trace(go.Bar(x=table_names, y=table_sizes, name='Tamanho (MB)', marker_color='blue'))
        fig.update_layout(title='Tamanhos das Tabelas do MySQL', xaxis_title='Tabelas', yaxis_title='Tamanho (MB)', barmode='group', bargap=0.15)
        plot_div = fig.to_html(include_plotlyjs='cdn')
    else:
        plot_div = ""

    return render_template('mysql.html', mysql_info=mysql_info, table_data=table_data, plot_div=plot_div)

###################################################################
#              API para obter informações do MySQL.               #
###################################################################
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

###################################################################
#             Rota para testar a conexão com o MySQL.             #
###################################################################
@mysql_bp.route('/test_mysql_connection', methods=['GET'])
def test_mysql():
    """Rota para testar a conexão com o MySQL."""
    # Recupera as informações do MySQL
    mysql_info = get_mysql_info()
    if mysql_info.get('server_version') and mysql_info['server_version'] != 'Erro ao obter informações do MySQL':
        print("Postman conectado ao MySQL com sucesso!")  # Apenas para debug no console
        return jsonify({'message': 'Conexão com MySQL estabelecida e informações obtidas com sucesso!', 'mysql_info': mysql_info}), 200
    else:
        print("Erro ao conectar ou obter informações do MySQL.")
        return jsonify({'error': 'Falha ao conectar ou obter informações do MySQL.'}), 500
