from flask import Flask
from controllers.cliente_routes import cliente_bp

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

# Registrando rotas (blueprints)
app.register_blueprint(cliente_bp, url_prefix="/clientes")

if __name__ == "__main__":
    app.run(debug=True)
