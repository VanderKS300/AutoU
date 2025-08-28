from flask import Blueprint, jsonify, request
from src.models.user import db, User

# Cria um Blueprint para as rotas de usuário.
user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['GET'])
def get_users():
    """
    Rota para listar todos os usuários cadastrados.
    Retorna uma lista de usuários em formato JSON.
    """
    try:
        # Busca todos os usuários no banco de dados
        users = User.query.all()
        
        # Converte a lista de objetos User para uma lista de dicionários
        user_list = [{"id": user.id, "username": user.username, "email": user.email} for user in users]
        
        return jsonify(user_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/users', methods=['POST'])
def create_user():
    """
    Rota para criar um novo usuário.
    Recebe os dados do usuário via JSON e os adiciona ao banco de dados.
    """
    try:
        # Obtém os dados do corpo da requisição
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')

        # Verifica se os campos obrigatórios estão presentes
        if not username or not email:
            return jsonify({'error': 'Nome de usuário e email são obrigatórios'}), 400

        # Cria uma nova instância do modelo User
        new_user = User(username=username, email=email)
        
        # Adiciona e comita o novo usuário ao banco de dados
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({'message': 'Usuário criado com sucesso!', 'user_id': new_user.id}), 201
    except Exception as e:
        # Em caso de erro, reverte a transação e retorna uma mensagem de erro
        db.session.rollback()
        return jsonify({'error': 'Erro ao criar usuário: ' + str(e)}), 500

