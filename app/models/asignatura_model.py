from app import mysql
import MySQLdb.cursors

# ---------------- Obtener todas las asignaturas activas ----------------
def obtener_asignaturas():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = "SELECT * FROM asignatura WHERE estado = 'activo'"
    cursor.execute(query)
    asignaturas = cursor.fetchall()
    cursor.close()
    return asignaturas

# ---------------- Obtener asignaturas inactivas ----------------
def obtener_asignaturas_inactivas():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = "SELECT * FROM asignatura WHERE estado = 'inactivo'"
    cursor.execute(query)
    asignaturas = cursor.fetchall()
    cursor.close()
    return asignaturas

# ---------------- Crear una nueva asignatura ----------------
def crear_asignatura(nombre):
    cursor = mysql.connection.cursor()
    query = "INSERT INTO asignatura (nombre, estado) VALUES (%s, 'activo')"
    cursor.execute(query, (nombre,))
    mysql.connection.commit()
    cursor.close()

# ---------------- Obtener una asignatura por ID ----------------
def obtener_asignatura_por_id(asignatura_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = "SELECT * FROM asignatura WHERE id = %s"
    cursor.execute(query, (asignatura_id,))
    asignatura = cursor.fetchone()
    cursor.close()
    return asignatura

# ---------------- Actualizar asignatura ----------------
def actualizar_asignatura(asignatura_id, nombre, estado):
    cursor = mysql.connection.cursor()
    query = "UPDATE asignatura SET nombre=%s, estado=%s WHERE id=%s"
    cursor.execute(query, (nombre, estado, asignatura_id))
    mysql.connection.commit()
    cursor.close()

# ---------------- Eliminar lógico (inactivar asignatura) ----------------
def eliminar_asignatura(asignatura_id):
    cursor = mysql.connection.cursor()
    query = "UPDATE asignatura SET estado = 'inactivo' WHERE id=%s"
    cursor.execute(query, (asignatura_id,))
    mysql.connection.commit()
    cursor.close()

# ---------------- Reactivar asignatura ----------------
def reactivar_asignatura(asignatura_id):
    cursor = mysql.connection.cursor()
    query = "UPDATE asignatura SET estado = 'activo' WHERE id=%s"
    cursor.execute(query, (asignatura_id,))
    mysql.connection.commit()
    cursor.close()
