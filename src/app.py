import os
from flask import Flask, request, jsonify, url_for, send_from_directory
from flask_migrate import Migrate
from flask_swagger import swagger
from api.utils import APIException, generate_sitemap
from api.models import db, BlockedToken
from api.routes import api
from api.admin import setup_admin
from api.commands import setup_commands
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../dist/')

# 1. Configuración de Base de Datos (Corrigiendo el error de Postgres)
db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 2. Configuración de Seguridad
app.config["JWT_SECRET_KEY"] = os.getenv("FLASK_APP_KEY", "super-secret-key")

# 3. Inicialización de extensiones
db.init_app(app)
jwt = JWTManager(app)

# register a callback function that will check if a JWT exists in the blocklist
@jwt.token_in_blocklist_loader
# jwt_header and jwt_payload are provided by flask_jwt_extended when verifying tokens
# return True if token has been revoked/blocked (i.e. should be treated as invalid)
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload.get("jti")
    # look up the jti in our BlockedToken table
    return BlockedToken.query.filter_by(jti=jti).first() is not None

bcrypt = Bcrypt(app)
MIGRATE = Migrate(app, db, compare_type=True)

# 4. Configuración de utilidades (Admin y Comandos)
setup_admin(app)
setup_commands(app)

# 5. Registro del Blueprint (UNA SOLA VEZ)
app.register_blueprint(api, url_prefix='/api')

# --- Manejo de Errores y Rutas Estáticas ---

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    if os.getenv("FLASK_DEBUG") == "1":
        return generate_sitemap(app)
    return send_from_directory(static_file_dir, 'index.html')

@app.route('/<path:path>', methods=['GET'])
def serve_any_other_file(path):
    if not os.path.isfile(os.path.join(static_file_dir, path)):
        path = 'index.html'
    response = send_from_directory(static_file_dir, path)
    response.cache_control.max_age = 0
    return response

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3001))
    app.run(host='0.0.0.0', port=PORT, debug=True)