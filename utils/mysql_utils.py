# Importações do Flask
from flask import Blueprint  # Blueprint para rotas
from flask import render_template  # Renderização de templates HTML
from flask import session  # Sessões para armazenar informações do usuário
from flask import request  # Manipulação de requisições HTTP
from flask import flash  # Exibição de mensagens flash
from flask import redirect  # Redirecionamento de URLs
from flask import url_for  # Construção de URLs
from flask import send_file  # Envio de arquivos


# Importações gerais do Python
import os  # Funções do sistema operacional

# Importações de configuração
from config import (
    UPLOAD_FOLDER,  # Diretório de uploads
    mysql_credentials  # Credenciais de conexão com o MySQL
)

# Importação do cursor do MySQL para consultas
import pymysql.cursors

# Definição do Blueprint para rotas relacionadas a backup
backup_bp = Blueprint('backup', __name__)

###################################################################
#                        FUNÇÕES MYSQL                            #
###################################################################

# Função para conectar ao servidor MySQL
def get_mysql_connection():
    """Função para conectar ao servidor MySQL."""
    try:
        connection = pymysql.connect(
            host=mysql_credentials['host'],
            user=mysql_credentials['user'],
            password=mysql_credentials['password'],
            database=mysql_credentials['database'],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except pymysql.MySQLError as e:
        print(f"Erro ao conectar ao MySQL: {str(e)}")
        return None

# Função para obter informações gerais do MySQL
def get_mysql_info():
    """Função para obter informações gerais do MySQL."""
    connection = get_mysql_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT VERSION()")
                version = cursor.fetchone()
                cursor.execute("SHOW DATABASES")
                databases = cursor.fetchall()
            
            mysql_info = {
                'Versão': version['VERSION()'],
                'Databases': [db['Database'] for db in databases]
            }
            
            return mysql_info
        except pymysql.MySQLError as e:
            print(f"Erro ao obter informações do MySQL: {str(e)}")
            return {}
        finally:
            connection.close()
    return {}

# Função para obter informações das tabelas do MySQL
def get_mysql_tables_info():
    """Função para obter informações das tabelas do MySQL."""
    connection = get_mysql_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SHOW TABLE STATUS")
                tables_info = cursor.fetchall()
            
            tables = []
            for table_info in tables_info:
                table = {
                    'Nome da Tabela': table_info['Name'],
                    'Número de Registros': table_info['Rows'],
                    'Tamanho Aproximado (KB)': table_info['Data_length'] / 1024,
                    'Tipo de Armazenamento': table_info['Engine']
                }
                tables.append(table)
            
            return tables
        except pymysql.MySQLError as e:
            print(f"Erro ao obter informações das tabelas do MySQL: {str(e)}")
            return []
        finally:
            connection.close()
    return []


###################################################################
#                   FUNÇÕES TABELA CONTAS A RECEBER                #
###################################################################

# Função para obter contas a receber do MySQL
def get_mysql_accounts_receivable():
    """Função para obter contas a receber do MySQL."""
    connection = get_mysql_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM contas_a_receber WHERE status = 'pendente'")
                accounts_receivable = cursor.fetchall()
            
            accounts = []
            for account in accounts_receivable:
                account_data = {
                    'ID': account['id'],
                    'Cliente': account['cliente'],
                    'Valor': account['valor'],
                    'Status': account['status']
                }
                accounts.append(account_data)
            
            return accounts
        except pymysql.MySQLError as e:
            print(f"Erro ao obter contas a receber: {str(e)}")
            return []
        finally:
            connection.close()
    return []

###################################################################
#                   FUNÇÕES TABELA CONTAS A PAGAR                 #
###################################################################

# Função para obter contas a pagar do MySQL
def get_mysql_accounts_payable():
    """Função para obter contas a pagar do MySQL."""
    connection = get_mysql_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM contas_a_pagar WHERE status = 'pendente'")
                accounts_payable = cursor.fetchall()
            
            accounts = []
            for account in accounts_payable:
                account_data = {
                    'ID': account['id'],
                    'Fornecedor': account['fornecedor'],
                    'Valor': account['valor'],
                    'Status': account['status']
                }
                accounts.append(account_data)
            
            return accounts
        except pymysql.MySQLError as e:
            print(f"Erro ao obter contas a pagar: {str(e)}")
            return []
        finally:
            connection.close()
    return []

###################################################################
#                   FUNÇÕES TABELA VENDAS                          #
###################################################################

# Função para obter produtos com baixo estoque do MySQL
def get_mysql_low_stock_products():
    """Função para obter produtos com baixo estoque do MySQL."""
    connection = get_mysql_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM produtos WHERE estoque < 10")
                low_stock_products = cursor.fetchall()
            
            products = []
            for product in low_stock_products:
                product_data = {
                    'ID': product['id'],
                    'Nome': product['nome'],
                    'Estoque': product['estoque'],
                    'Preço': product['preco']
                }
                products.append(product_data)
            
            return products
        except pymysql.MySQLError as e:
            print(f"Erro ao obter produtos com baixo estoque: {str(e)}")
            return []
        finally:
            connection.close()
    return []

# Função para obter as 20 maiores vendas do mês com a forma de pagamento usada
def get_sales_by_payment_method():
    """Função para obter as 20 maiores vendas do mês com a forma de pagamento usada."""
    connection = get_mysql_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                query = """
                    SELECT valor_venda, forma_pagamento
                    FROM vendas
                    ORDER BY valor_venda DESC
                    LIMIT 20
                """
                cursor.execute(query)
                result = cursor.fetchall()
            
            return result
        except pymysql.MySQLError as e:
            print(f"Erro ao obter as maiores vendas por forma de pagamento: {str(e)}")
            return []
        finally:
            connection.close()
    return []

# Função para obter vendas recentes do MySQL
def get_mysql_recent_sales():
    """Função para obter vendas recentes do MySQL."""
    connection = get_mysql_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM vendas ORDER BY data_venda DESC LIMIT 10")
                recent_sales = cursor.fetchall()
            
            sales = []
            for sale in recent_sales:
                sale_data = {
                    'ID': sale['id'],
                    'Data da Venda': sale['data_venda'],
                    'Valor da Venda': sale['valor_venda'],
                    'Forma de Pagamento': sale['forma_pagamento']
                }
                sales.append(sale_data)
            
            return sales
        except pymysql.MySQLError as e:
            print(f"Erro ao obter vendas recentes: {str(e)}")
            return []
        finally:
            connection.close()
    return []

###################################################################
#                   FUNÇÕES RELACIONADAS A FORNECEDOR              #
###################################################################

# Função para obter informações dos fornecedores
def get_mysql_suppliers():
    """Função para obter informações dos fornecedores do MySQL."""
    connection = get_mysql_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM fornecedores")
                suppliers = cursor.fetchall()
            
            supplier_list = []
            for supplier in suppliers:
                supplier_data = {
                    'ID': supplier['id'],
                    'Nome': supplier['nome'],
                    'Contato': supplier['contato'],
                    'Email': supplier['email']
                }
                supplier_list.append(supplier_data)
            
            return supplier_list
        except pymysql.MySQLError as e:
            print(f"Erro ao obter informações dos fornecedores: {str(e)}")
            return []
        finally:
            connection.close()
    return []


