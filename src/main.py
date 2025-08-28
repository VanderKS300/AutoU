import os
import sys

# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
# Importa o db da nova classe de modelo
from src.models.user import db
# Importa as novas rotas de usuário
from src.routes.user import user_bp
from src.routes.email_classifier_simple import email_classifier_bp

# Define a pasta estática como a subpasta 'static'
static_folder = os.path.join(os.path.dirname(__file__), 'static')
app = Flask(__name__, static_folder=static_folder)
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Configura o banco de dados SQLite para criar o arquivo app.db
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o banco de dados com a aplicação
db.init_app(app)
with app.app_context():
    # Cria as tabelas do banco de dados, se ainda não existirem
    db.create_all()

# Registra os Blueprints (conjuntos de rotas) na aplicação
# Registra as rotas de usuário
app.register_blueprint(user_bp, url_prefix='/api')
# Registra as rotas do classificador de e-mails
app.register_blueprint(email_classifier_bp, url_prefix='/api')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    """
    Serve os arquivos estáticos, incluindo o index.html como padrão.
    """
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        index_path = os.path.join(app.static_folder, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(app.static_folder, 'index.html')
        else:
            return "index.html not found", 404

# A linha abaixo é usada para rodar localmente. No Render, o servidor WSGI (Gunicorn)
# irá carregar a aplicação diretamente.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

