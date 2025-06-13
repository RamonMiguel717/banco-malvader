from models.database import db
from datetime import datetime

class Transacao(db.Model):
    __tablename__ = 'transacoes'
    
    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Float, nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # 'deposito', 'saque', 'transferencia'
    descricao = db.Column(db.String(200))
    data = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    conta_id = db.Column(db.Integer, db.ForeignKey('contas.id'), nullable=False)
    conta_destino_id = db.Column(db.Integer, db.ForeignKey('contas.id')))
    
    # Relacionamentos
    conta_destino = db.relationship('Conta', foreign_keys=[conta_destino_id])