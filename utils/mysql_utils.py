import pymysql.cursors
from config import mysql_credentials

def get_mysql_connection():
    """Função para conectar ao servidor MySQL."""
    try:
        connection = pymysql.connect(host=mysql_credentials['host'],
                                     user=mysql_credentials['user'],
                                     password=mysql_credentials['password'],
                                     database=mysql_credentials['database'],
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        return connection
    except pymysql.MySQLError as e:
        print(f"Erro ao conectar ao MySQL: {str(e)}")
        return None

def get_mysql_variables():
    """Função para obter variáveis do MySQL."""
    try:
        connection = get_mysql_connection()
        with connection.cursor() as cursor:
            cursor.execute("SHOW VARIABLES")
            variables = cursor.fetchall()
        return variables
    except pymysql.MySQLError as e:
        print(f"Erro ao obter variáveis do MySQL: {str(e)}")
        return []

def get_mysql_status():
    """Função para obter status do MySQL."""
    try:
        connection = get_mysql_connection()
        with connection.cursor() as cursor:
            cursor.execute("SHOW STATUS")
            status = cursor.fetchall()
        return status
    except pymysql.MySQLError as e:
        print(f"Erro ao obter status do MySQL: {str(e)}")
        return []

def get_mysql_databases():
    """Função para obter databases do MySQL."""
    try:
        connection = get_mysql_connection()
        with connection.cursor() as cursor:
            cursor.execute("SHOW DATABASES")
            databases = cursor.fetchall()
        return databases
    except pymysql.MySQLError as e:
        print(f"Erro ao obter databases do MySQL: {str(e)}")
        return []

def get_mysql_tables():
    """Função para obter tabelas do MySQL."""
    try:
        connection = get_mysql_connection()
        with connection.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
        return tables
    except pymysql.MySQLError as e:
        print(f"Erro ao obter tabelas do MySQL: {str(e)}")
        return []

def get_mysql_table_data(table_name):
    """Função para obter os dados de uma tabela específica do MySQL."""
    try:
        connection = get_mysql_connection()
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {table_name}")
            table_data = cursor.fetchall()
        return table_data
    except pymysql.MySQLError as e:
        print(f"Erro ao obter dados da tabela {table_name}: {str(e)}")
        return []

def get_mysql_info():
    """Função para obter informações detalhadas do MySQL."""
    try:
        variables = get_mysql_variables()
        status = get_mysql_status()
        databases = get_mysql_databases()
        tables = get_mysql_tables()

        mysql_info = {
            'variables': variables,
            'status': status,
            'databases': databases,
            'tables': tables
        }
        return mysql_info

    except Exception as e:
        print(f"Erro ao obter informações do MySQL: {str(e)}")
        return {'error': 'Erro ao obter informações do MySQL'}
    finally:
        if connection:
            connection.close()
