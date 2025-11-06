from flask import Flask
from app.extensions import db, jwt, cors
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Inicializar extensiones
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)
    
    # Registrar blueprints
    from app.routes.alineacion_routes import alineacion_bp
    app.register_blueprint(alineacion_bp, url_prefix='/api/alineaciones')
    
    return app