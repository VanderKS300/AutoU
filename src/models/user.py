from flask_sqlalchemy import SQLAlchemy

# Instância do banco de dados SQLAlchemy
# Isso permite que os modelos de dados interajam com o banco de dados
db = SQLAlchemy()

class User(db.Model):
    """
    Modelo de dados para a tabela 'user'.
    Define a estrutura da tabela no banco de dados.
    """
    # A coluna 'id' é a chave primária da tabela.
    # Ela é um número inteiro que é gerado automaticamente e é único para cada usuário.
    id = db.Column(db.Integer, primary_key=True)
    
    # A coluna 'username' armazena o nome de usuário.
    # É uma string de até 80 caracteres e deve ser única para cada usuário.
    username = db.Column(db.String(80), unique=True, nullable=False)
    
    # A coluna 'email' armazena o email do usuário.
    # É uma string de até 120 caracteres e deve ser única para cada usuário.
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        """
        Representação em string do objeto User, útil para debugging.
        """
        return f'<User {self.username}>'

