from flask import Flask
import app.config as config

# Inicializa a aplicação Flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = config.app_config['UPLOAD_FOLDER']
app.secret_key = config.app_config['SECRET_KEY']

if __name__ == '__main__':
    app.run(debug=True, host='192.168.1.250', port=80)
