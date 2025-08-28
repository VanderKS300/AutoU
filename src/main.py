import os
import sys

# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from src.models.user import db
from src.routes.user import user_bp
from src.routes.email_classifier_simple import email_classifier_bp

# Define a pasta estática como a subpasta 'static'
static_folder = os.path.join(os.path.dirname(__file__), 'static')
app = Flask(__name__, static_folder=static_folder)
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Comente todas as linhas relacionadas ao banco de dados para evitar o erro de permissão.
# app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db.init_app(app)
# with app.app_context():
#     db.create_all()

# Registra os Blueprints (conjuntos de rotas) na aplicação
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(email_classifier_bp, url_prefix='/api')

@app.route('/', defaults={'path': ''})
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

