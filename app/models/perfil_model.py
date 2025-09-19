from app import mysql
import MySQLdb.cursors
from werkzeug.security import generate_password_hash

# ---------------- Obtener datos generales ----------------
def obtener_usuario(usuario_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""
        SELECT u.id, u.nombre, u.apellido, u.correo, u.telefono,
               u.rol_id, r.nombre AS rol, u.estado
        FROM usuarios u
        INNER JOIN roles r ON u.rol_id = r.id
        WHERE u.id = %s
    """, (usuario_id,))
    usuario = cursor.fetchone()
    cursor.close()
    return usuario or {}

# ---------------- Datos por rol ----------------
def obtener_datos_docente(usuario_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""
        SELECT d.profesion,
               GROUP_CONCAT(a.id SEPARATOR ',') AS asignaturas_ids,
               GROUP_CONCAT(a.nombre SEPARATOR ', ') AS asignaturas_nombres
        FROM docente d
        LEFT JOIN docente_asignatura da ON d.id = da.docente_id
        LEFT JOIN asignatura a ON da.asignatura_id = a.id
        WHERE d.usuario_id = %s
        GROUP BY d.id
    """, (usuario_id,))
    datos = cursor.fetchone()
    cursor.close()

    if datos:
        if datos.get("asignaturas_ids"):
            datos["asignaturas_list"] = [int(x) for x in datos["asignaturas_ids"].split(',')]
        else:
            datos["asignaturas_list"] = []

        datos["asignaturas"] = datos.get("asignaturas_nombres", None)
    else:
        datos = {"asignaturas_list": [], "asignaturas": None}

    return datos

def obtener_id_docente(usuario_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT id FROM docente WHERE usuario_id = %s", (usuario_id,))
    result = cursor.fetchone()
    cursor.close()
    if result:
        return result["id"]
    return None



def obtener_todas_asignaturas():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT id, nombre FROM asignatura ORDER BY nombre")
    asignaturas = cursor.fetchall()
    cursor.close()
    return asignaturas or []


def obtener_datos_estudiante(usuario_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""
        SELECT e.grado_id, g.nombre AS grado_nombre,
               e.fecha_nacimiento,
               GROUP_CONCAT(CONCAT(u.nombre, ' ', u.apellido, ' (', ae.parentesco, ')') 
                            SEPARATOR ', ') AS acudientes
        FROM estudiante e
        LEFT JOIN grado g ON e.grado_id = g.id
        LEFT JOIN acudiente_estudiante ae ON e.id = ae.estudiante_id
        LEFT JOIN acudiente a ON ae.acudiente_id = a.id
        LEFT JOIN usuarios u ON a.usuario_id = u.id
        WHERE e.usuario_id = %s
        GROUP BY e.id, g.nombre, e.fecha_nacimiento
    """, (usuario_id,))
    datos = cursor.fetchone()
    cursor.close()

    if datos:
        datos["acudientes"] = datos["acudientes"] or "No tiene acudientes asignados"

        if datos.get("fecha_nacimiento"):
            datos["fecha_nacimiento"] = datos["fecha_nacimiento"].strftime("%Y-%m-%d")
    else:
        datos = {
            "grado_id": None,
            "grado_nombre": None,
            "fecha_nacimiento": "",
            "acudientes": "No tiene acudientes asignados"
        }

    return datos



def obtener_datos_acudiente(usuario_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""
        SELECT a.ocupacion,
               GROUP_CONCAT(CONCAT(u.nombre,' ',u.apellido,' (',ae.parentesco,')') SEPARATOR ', ') AS estudiantes
        FROM acudiente a
        LEFT JOIN acudiente_estudiante ae ON a.id = ae.acudiente_id
        LEFT JOIN estudiante e ON ae.estudiante_id = e.id
        LEFT JOIN usuarios u ON e.usuario_id = u.id
        WHERE a.usuario_id = %s
        GROUP BY a.id
    """, (usuario_id,))
    datos = cursor.fetchone()
    cursor.close()

    if datos:
        datos["estudiantes"] = datos["estudiantes"] or "No tiene estudiantes asignados"
    else:
        datos = {"ocupacion": "", "estudiantes": "No tiene estudiantes asignados"}

    return datos


# ---------------- Actualizar datos ----------------
def actualizar_perfil(usuario_id, nombre, apellido, correo, telefono, contrasena=None):
    cursor = mysql.connection.cursor()
    if contrasena:
        hashed = generate_password_hash(contrasena)
        cursor.execute("""
            UPDATE usuarios
            SET nombre=%s, apellido=%s, correo=%s, telefono=%s, contraseña=%s
            WHERE id=%s
        """, (nombre, apellido, correo, telefono, hashed, usuario_id))
    else:
        cursor.execute("""
            UPDATE usuarios
            SET nombre=%s, apellido=%s, correo=%s, telefono=%s
            WHERE id=%s
        """, (nombre, apellido, correo, telefono, usuario_id))
    mysql.connection.commit()
    cursor.close()

def actualizar_docente(usuario_id, profesion):
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE docente SET profesion=%s WHERE usuario_id=%s", (profesion, usuario_id))
    mysql.connection.commit()
    cursor.close()
    
def actualizar_asignaturas_docente(docente_id, lista_asignaturas_ids):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM docente_asignatura WHERE docente_id = %s", (docente_id,))
    for asignatura_id in lista_asignaturas_ids:
        cursor.execute(
            "INSERT INTO docente_asignatura (docente_id, asignatura_id) VALUES (%s, %s)",
            (docente_id, asignatura_id)
        )
    mysql.connection.commit()
    cursor.close()


def actualizar_estudiante(usuario_id, grado_id, fecha_nacimiento):
    cursor = mysql.connection.cursor()
    if grado_id is not None:
        cursor.execute(
            "UPDATE estudiante SET grado_id=%s, fecha_nacimiento=%s WHERE usuario_id=%s",
            (grado_id, fecha_nacimiento, usuario_id)
        )
    else:
        cursor.execute(
            "UPDATE estudiante SET fecha_nacimiento=%s WHERE usuario_id=%s",
            (fecha_nacimiento, usuario_id)
        )
    mysql.connection.commit()
    cursor.close()


def actualizar_acudiente(usuario_id, ocupacion):
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE acudiente SET ocupacion=%s WHERE usuario_id=%s", (ocupacion, usuario_id))
    mysql.connection.commit()
    cursor.close()
