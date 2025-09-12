from app import mysql
import MySQLdb.cursors

# ---------------- Obtener todos los roles activos ----------------
def obtener_roles():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = "SELECT * FROM roles WHERE estado = 'activo'"
    cursor.execute(query)
    roles = cursor.fetchall()
    cursor.close()
    return roles

# ---------------- Obtener roles inactivos ----------------
def obtener_roles_inactivos():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = "SELECT * FROM roles WHERE estado = 'inactivo'"
    cursor.execute(query)
    roles = cursor.fetchall()
    cursor.close()
    return roles

# ---------------- Crear un nuevo rol ----------------
def crear_rol(nombre, descripcion):
    cursor = mysql.connection.cursor()
    query = "INSERT INTO roles (nombre, descripcion, estado) VALUES (%s, %s, 'activo')"
    cursor.execute(query, (nombre, descripcion))
    mysql.connection.commit()
    cursor.close()

# ---------------- Obtener un rol por ID ----------------
def obtener_rol_por_id(rol_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = "SELECT * FROM roles WHERE id = %s"
    cursor.execute(query, (rol_id,))
    rol = cursor.fetchone()
    cursor.close()
    return rol

# ---------------- Actualizar rol ----------------
def actualizar_rol(rol_id, nombre, descripcion, ):
    cursor = mysql.connection.cursor()
    query = "UPDATE roles SET nombre=%s, descripcion=%s WHERE id=%s"
    cursor.execute(query, (nombre, descripcion, rol_id))
    mysql.connection.commit()
    cursor.close()

# ---------------- Eliminar lógico (inactivar rol) ----------------
def eliminar_rol(rol_id):
    cursor = mysql.connection.cursor()
    query = "UPDATE roles SET estado = 'inactivo' WHERE id=%s"
    cursor.execute(query, (rol_id,))
    mysql.connection.commit()
    cursor.close()

# ---------------- Reactivar rol ----------------
def reactivar_rol(rol_id):
    cursor = mysql.connection.cursor()
    query = "UPDATE roles SET estado = 'activo' WHERE id=%s"
    cursor.execute(query, (rol_id,))
    mysql.connection.commit()
    cursor.close()
