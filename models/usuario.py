from models.database import db
from utils.criptografia_senha import criptografada

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    ativo = db.Column(db.Boolean, default=True)
    
    # Relacionamentos
    contas = db.relationship('Conta', backref='usuario', lazy=True)
    
    @property
    def senha(self):
        raise AttributeError('senha não é um atributo legível')
    
    @senha.setter
    def senha(self, senha):
        self.senha_hash = criptografada.gerar_hash_senha(senha)
    
    def verificar_senha(self, senha):
        from utils.criptografia_senha import criptografada
        return criptografada.verificar_senha(self.senha_hash, senha)