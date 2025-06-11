from flask import Flask
from controllers.cliente_routes import cliente_bp
from controllers.usuario_routes import usuario_bp

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

   # Register blueprints
app = Flask(__name__)
app.register_blueprint(usuario_bp)

if __name__ == "__main__":
    app.run(debug=True)
   