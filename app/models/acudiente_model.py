from app import mysql
import MySQLdb.cursors
from werkzeug.security import generate_password_hash

# ---------------- Obtener todos los acudientes activos ----------------
def obtener_acudientes():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = """
        SELECT 
            u.id, 
            u.nombre, 
            u.apellido, 
            u.correo, 
            u.telefono, 
            r.nombre AS rol,
            u.estado,
            a.ocupacion
        FROM acudiente a
        INNER JOIN usuarios u ON a.usuario_id = u.id
        INNER JOIN roles r ON u.rol_id = r.id
        WHERE u.estado = 'activo'
    """
    cursor.execute(query)
    acudientes = cursor.fetchall()
    cursor.close()
    return acudientes


# ---------------- Obtener un acudiente por ID ----------------
def obtener_acudiente_por_id(acudiente_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = """
        SELECT 
            u.id, 
            u.nombre, 
            u.apellido, 
            u.correo, 
            u.telefono, 
            r.id AS rol_id,
            r.nombre AS rol,
            u.estado,
            a.ocupacion
        FROM acudiente a
        INNER JOIN usuarios u ON a.usuario_id = u.id
        INNER JOIN roles r ON u.rol_id = r.id
        WHERE u.id = %s
    """
    cursor.execute(query, (acudiente_id,))
    acudiente = cursor.fetchone()
    cursor.close()
    return acudiente


# ---------------- Actualizar acudiente ----------------
def actualizar_acudiente(acudiente_id, nombre, apellido, correo, telefono, rol_id, ocupacion, password=None):
    cursor = mysql.connection.cursor()

    if password:  
        hashed_password = generate_password_hash(password)
        query_usuario = """
            UPDATE usuarios
            SET nombre=%s, apellido=%s, correo=%s, telefono=%s, rol_id=%s, contraseña=%s
            WHERE id=%s
        """
        cursor.execute(query_usuario, (nombre, apellido, correo, telefono, rol_id, hashed_password, acudiente_id))
    else:  
        query_usuario = """
            UPDATE usuarios
            SET nombre=%s, apellido=%s, correo=%s, telefono=%s, rol_id=%s
            WHERE id=%s
        """
        cursor.execute(query_usuario, (nombre, apellido, correo, telefono, rol_id, acudiente_id))

    query_acudiente = """
        UPDATE acudiente
        SET ocupacion=%s
        WHERE usuario_id=%s
    """
    cursor.execute(query_acudiente, (ocupacion, acudiente_id))

    mysql.connection.commit()
    cursor.close()



# ---------------- Cambiar estado a inactivo (Eliminar lógico) ----------------
def eliminar_acudiente(acudiente_id):
    cursor = mysql.connection.cursor()
    query = "UPDATE usuarios SET estado = 'inactivo' WHERE id = %s"
    cursor.execute(query, (acudiente_id,))
    mysql.connection.commit()
    cursor.close()


# ---------------- Obtener acudientes inactivos ----------------
def obtener_acudientes_inactivos():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = """
        SELECT 
            u.id, 
            u.nombre, 
            u.apellido, 
            u.correo, 
            u.telefono, 
            r.nombre AS rol,
            u.estado,
            a.ocupacion
        FROM acudiente a
        INNER JOIN usuarios u ON a.usuario_id = u.id
        INNER JOIN roles r ON u.rol_id = r.id
        WHERE u.estado = 'inactivo'
    """
    cursor.execute(query)
    acudientes = cursor.fetchall()
    cursor.close()
    return acudientes

def reactivar_acudiente(acudiente_id):
    cursor = mysql.connection.cursor()
    query = "UPDATE usuarios SET estado='activo' WHERE id=%s"
    cursor.execute(query, (acudiente_id,))
    mysql.connection.commit()
    cursor.close()
