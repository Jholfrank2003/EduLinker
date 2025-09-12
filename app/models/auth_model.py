from flask_login import UserMixin
from app import mysql
import MySQLdb.cursors

class User(UserMixin):
    def __init__(self, id, nombre, apellido, correo, rol, estado, contrasena=None):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.rol = rol
        self.estado = estado
        self.contrasena = contrasena

    def get_id(self):
        return str(self.id)



def get_user_by_id(user_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""
        SELECT u.id, u.nombre, u.apellido, u.correo, u.estado, u.contrasena,
               r.nombre AS rol
        FROM usuarios u
        JOIN roles r ON u.rol_id = r.id
        WHERE u.id = %s
    """, (user_id,))
    user = cursor.fetchone()
    cursor.close()

    if user:
        return User(
            id=user["id"],
            nombre=user["nombre"],
            apellido=user["apellido"],
            correo=user["correo"],
            rol=user["rol"],  # aquí ya es r.nombre
            estado=user["estado"],
            contrasena=user["contrasena"]
        )
    return None


def get_user_by_email(correo):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""
        SELECT u.id, u.nombre, u.apellido, u.correo, u.estado, u.contrasena,
               r.nombre AS rol
        FROM usuarios u
        JOIN roles r ON u.rol_id = r.id
        WHERE u.correo = %s
    """, (correo,))
    user = cursor.fetchone()
    cursor.close()

    if user:
        return User(
            id=user["id"],
            nombre=user["nombre"],
            apellido=user["apellido"],
            correo=user["correo"],
            rol=user["rol"],  # ahora funciona porque viene de roles.nombre
            estado=user["estado"],
            contrasena=user["contrasena"]
        )
    return None


