from config import mysql_credentials
import pymysql

def get_mysql_connection():
    """Função para obter e retornar uma conexão ao servidor MySQL."""
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
    except Exception as e:
        print(f"Erro ao conectar ao MySQL: {str(e)}")
        return None

def get_mysql_info():
    """Função para obter informações do MySQL."""
    connection = get_mysql_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "SELECT @@version AS server_version, ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS database_size, COUNT(*) AS tables_count FROM information_schema.tables WHERE table_schema = %s"
                cursor.execute(sql, (mysql_credentials['database'],))
                result = cursor.fetchone()

                mysql_info = {
                    'server_version': result['server_version'],
                    'database_size': f"{result['database_size']} MB",
                    'tables_count': result['tables_count'],
                    # Adicione mais informações conforme necessário
                }

            return mysql_info

        except Exception as e:
            print(f"Erro ao obter informações do MySQL: {str(e)}")
            return {
                'server_version': 'Erro ao obter informações do MySQL',
                'database_size': 'N/A',
                'tables_count': 'N/A',
                # Adicione mais informações de erro conforme necessário
            }
        finally:
            connection.close()  # Fechar a conexão apenas uma vez aqui

    else:
        return {
            'server_version': 'Erro ao conectar ao MySQL',
            'database_size': 'N/A',
            'tables_count': 'N/A',
            # Adicione mais informações de erro conforme necessário
        }
