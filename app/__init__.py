from flask import Flask
from flask_mysqldb import MySQL
from flask_login import LoginManager
from .config import Config

mysql = MySQL()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar conexión MySQL
    mysql.init_app(app)

    # Inicializar login_manager
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # Importar aquí, después de crear mysql
    from .models.auth_model import get_user_by_id

    @login_manager.user_loader
    def load_user(user_id):
        return get_user_by_id(user_id)

    # Importar y registrar Blueprints existentes
    from .routes.main_routes import main_bp
    app.register_blueprint(main_bp)

    from .routes.registro_routes import registro_bp
    app.register_blueprint(registro_bp)

    from .routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)

    from .routes.usuario_routes import usuario_bp
    app.register_blueprint(usuario_bp)

    from .routes.estudiante_routes import estudiante_bp
    app.register_blueprint(estudiante_bp)

    from .routes.acudiente_routes import acudiente_bp
    app.register_blueprint(acudiente_bp)

    from .routes.docente_routes import docente_bp
    app.register_blueprint(docente_bp)
    
    from .routes.roles_routes import roles_bp
    app.register_blueprint(roles_bp)
    
    from .routes.asignatura_routes import asignatura_bp
    app.register_blueprint(asignatura_bp)
    
    from .routes.relaciones_routes import relaciones_bp
    app.register_blueprint(relaciones_bp)
    
    #disponibilidad
    from .routes.disponibilidad_routes import disponibilidad_bp
    app.register_blueprint(disponibilidad_bp)
    
    from app.routes.solicitar_routes import solicitar_bp
    app.register_blueprint(solicitar_bp)
    
    #citas
    from app.routes.citas_routes import citas_bp
    app.register_blueprint(citas_bp)

    return app
