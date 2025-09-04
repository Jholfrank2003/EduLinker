from app import mysql
import MySQLdb.cursors
from werkzeug.security import generate_password_hash


# ---------------- Registrar un Nuevo Usuario ----------------
def crear_usuario(nombre, apellido, correo, telefono, contrasena, rol):
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO usuarios (nombre, apellido, correo, telefono, contrasena, rol)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (nombre, apellido, correo, telefono, contrasena, rol))
    mysql.connection.commit()
    usuario_id = cur.lastrowid
    cur.close()
    return usuario_id

def registrar_estudiante(usuario_id, grado_id, fecha_nacimiento):
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO estudiante (usuario_id, grado_id, fecha_nacimiento)
        VALUES (%s, %s, %s)
    """, (usuario_id, grado_id, fecha_nacimiento))
    mysql.connection.commit()
    cur.close()

def registrar_acudiente(usuario_id, ocupacion):
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO acudiente (usuario_id, ocupacion)
        VALUES (%s, %s)
    """, (usuario_id, ocupacion))
    mysql.connection.commit()
    cur.close()

def registrar_docente(usuario_id, profesion, asignaturas):
    cur = mysql.connection.cursor()

    cur.execute("""
        INSERT INTO docente (usuario_id, profesion)
        VALUES (%s, %s)
    """, (usuario_id, profesion))
    docente_id = cur.lastrowid

    for asignatura_id in asignaturas:
        cur.execute("""
            INSERT INTO docente_asignatura (docente_id, asignatura_id)
            VALUES (%s, %s)
        """, (docente_id, asignatura_id))

# ---------------- Crear Disponibilidad de Luves a Viernes con estado Inactivo ----------------
    dias = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes']
    for dia in dias:
        estado_inicial = 'inactivo' 
        hora_inicio = '07:00:00'
        hora_fin = '15:00:00'

        cur.execute("""
            INSERT INTO disponibilidad (docente_id, dia, hora_inicio, hora_fin, estado)
            VALUES (%s, %s, %s, %s, %s)
        """, (docente_id, dia, hora_inicio, hora_fin, estado_inicial))

    mysql.connection.commit()
    cur.close()
    return docente_id


# ---------------- Obtener todos los Grados ----------------
def obtener_grados():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, nombre FROM grado")
    grados = cur.fetchall()
    cur.close()
    return grados

# ---------------- Obtener todas las Aisgnaturas ----------------
def obtener_asignaturas():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, nombre FROM asignatura")
    asignaturas = cur.fetchall()
    cur.close()
    return asignaturas


# Administrador

# ---------------- Obtener todos los Administradores Activos ----------------
def obtener_administradores():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = """
        SELECT 
            id, nombre, apellido, correo, telefono, rol, estado
        FROM usuarios
        WHERE rol = 'admin' AND estado = 'activo'
    """
    cursor.execute(query)
    administradores = cursor.fetchall()
    cursor.close()
    return administradores

# ---------------- Obtener Administrador del Usuario ----------------
def obtener_administrador_por_id(admin_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = """
        SELECT 
            id, nombre, apellido, correo, telefono, rol, estado
        FROM usuarios
        WHERE id = %s AND rol = 'admin'
    """
    cursor.execute(query, (admin_id,))
    admin = cursor.fetchone()
    cursor.close()
    return admin

# ---------------- Actualizar Datos del Administrador ----------------
def actualizar_administrador(admin_id, nombre, apellido, correo, telefono, estado, password=None):
    cursor = mysql.connection.cursor()

    if password:
        hashed_password = generate_password_hash(password)
        query = """
            UPDATE usuarios
            SET nombre=%s, apellido=%s, correo=%s, telefono=%s, estado=%s, contrasena=%s
            WHERE id=%s AND rol='admin'
        """
        cursor.execute(query, (nombre, apellido, correo, telefono, estado, hashed_password, admin_id))
    else:
        query = """
            UPDATE usuarios
            SET nombre=%s, apellido=%s, correo=%s, telefono=%s, estado=%s
            WHERE id=%s AND rol='admin'
        """
        cursor.execute(query, (nombre, apellido, correo, telefono, estado, admin_id))

    mysql.connection.commit()
    cursor.close()


# ---------------- Obtener el Registro de Citas del Usuario ----------------
def eliminar_administrador(admin_id):
    cursor = mysql.connection.cursor()
    query = "UPDATE usuarios SET estado='inactivo' WHERE id=%s AND rol='admin'"
    cursor.execute(query, (admin_id,))
    mysql.connection.commit()
    cursor.close()

# ---------------- Cambiar el estado del Administrador a Inactivo ----------------
def obtener_administradores_inactivos():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = """
        SELECT 
            id, nombre, apellido, correo, telefono, rol, estado
        FROM usuarios
        WHERE rol = 'admin' AND estado = 'inactivo'
    """
    cursor.execute(query)
    administradores = cursor.fetchall()
    cursor.close()
    return administradores


# ---------------- Reactivar el Administrador ----------------
def reactivar_administrador(admin_id):
    cursor = mysql.connection.cursor()
    query = "UPDATE usuarios SET estado='activo' WHERE id=%s AND rol='admin'"
    cursor.execute(query, (admin_id,))
    mysql.connection.commit()
    cursor.close()
