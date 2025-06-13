from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Carrega variáveis de ambiente
load_dotenv()

def create_app():
   app = Flask(__name__)
   CORS(app)

   # Configurações
   app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
   app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
   app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

   # Inicializa extensões
   from models.database import db
   db.init_app(app)

   # Registra blueprints
   from controllers.auth_controller import auth_bp
   from controllers.conta_controller import conta_bp
   from controllers.cliente_routes import cliente_bp
   from controllers.agencia_routes import agencia_bp
   from controllers.usuario_routes import usuario_bp
   from controllers.endereco_routes import endereco_bp

   app.register_blueprint(auth_bp)
   app.register_blueprint(conta_bp)
   app.register_blueprint(cliente_bp)
   app.register_blueprint(agencia_bp)
   app.register_blueprint(usuario_bp)
   app.register_blueprint(endereco_bp)

   return app

if __name__ == '__main__':
   app = create_app()
   app.run(debug=True)