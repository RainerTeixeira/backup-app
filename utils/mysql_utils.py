import mysql.connector
import config

def get_mysql_connection():
    """Função para obter a conexão com o banco de dados MySQL."""
    try:
        connection = mysql.connector.connect(
            user=config.mysql_credentials['user'], 
            password=config.mysql_credentials['password'], 
            host=config.mysql_credentials['host'], 
            database=config.mysql_credentials['database']
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao MySQL: {err}")
        return None

def get_mysql_info():
    """Função para obter informações de status do MySQL."""
    connection = get_mysql_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SHOW STATUS")
            status = cursor.fetchall()
            return status
        except mysql.connector.Error as err:
            print(f"Erro ao executar consulta MySQL: {err}")
            return {'error': str(err)}
        finally:
            connection.close()
    else:
        return {'error': 'Não foi possível conectar ao MySQL'}
