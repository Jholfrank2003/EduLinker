from app import mysql
import MySQLdb.cursors

# ---------------- Obtener todos los Docentes activos con sus Asignaturas ----------------
def obtener_docentes():
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
            d.profesion,
            GROUP_CONCAT(a.nombre SEPARATOR ', ') AS asignaturas
        FROM docente d
        INNER JOIN usuarios u ON d.usuario_id = u.id
        INNER JOIN roles r ON u.rol_id = r.id
        LEFT JOIN docente_asignatura da ON d.id = da.docente_id
        LEFT JOIN asignatura a ON da.asignatura_id = a.id
        WHERE u.estado = 'activo'
        GROUP BY u.id, u.nombre, u.apellido, u.correo, u.telefono, r.nombre, u.estado, d.profesion
    """
    cursor.execute(query)
    docentes = cursor.fetchall()
    cursor.close()
    return docentes



# ---------------- Obtener los Docentes Inactivos ----------------
def obtener_docentes_inactivos():
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
            d.profesion,
            GROUP_CONCAT(a.nombre SEPARATOR ', ') AS asignaturas
        FROM docente d
        INNER JOIN usuarios u ON d.usuario_id = u.id
        INNER JOIN roles r ON u.rol_id = r.id
        LEFT JOIN docente_asignatura da ON d.id = da.docente_id
        LEFT JOIN asignatura a ON da.asignatura_id = a.id
        WHERE u.estado = 'inactivo'
        GROUP BY u.id, u.nombre, u.apellido, u.correo, u.telefono, r.nombre, u.estado, d.profesion
    """
    cursor.execute(query)
    docentes = cursor.fetchall()
    cursor.close()
    return docentes


def obtener_docente_por_id(docente_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = """
        SELECT u.*, d.id AS docente_pk, d.profesion, r.nombre AS rol
        FROM docente d
        INNER JOIN usuarios u ON d.usuario_id = u.id
        INNER JOIN roles r ON u.rol_id = r.id
        WHERE u.id = %s
    """
    cursor.execute(query, (docente_id,))
    docente = cursor.fetchone()

    query_asignaturas = "SELECT asignatura_id FROM docente_asignatura WHERE docente_id = %s"
    cursor.execute(query_asignaturas, (docente["docente_pk"],))
    asignaturas = [row["asignatura_id"] for row in cursor.fetchall()]
    docente["asignaturas"] = asignaturas

    cursor.close()
    return docente



# ---------------- Actualizar Datos del Docente ----------------
def actualizar_docente(docente_id, nombre, apellido, correo, telefono, rol_id, profesion, contrasena, asignaturas):
    cursor = mysql.connection.cursor()

    # Actualizar usuario (con o sin contraseña)
    if contrasena:
        query = """
            UPDATE usuarios
            SET nombre=%s, apellido=%s, correo=%s, telefono=%s, rol_id=%s, contrasena=SHA2(%s,256)
            WHERE id=%s
        """
        cursor.execute(query, (nombre, apellido, correo, telefono, rol_id, contrasena, docente_id))
    else:
        query = """
            UPDATE usuarios
            SET nombre=%s, apellido=%s, correo=%s, telefono=%s, rol_id=%s
            WHERE id=%s
        """
        cursor.execute(query, (nombre, apellido, correo, telefono, rol_id, docente_id))

    # Verificar que el docente existe
    cursor.execute("SELECT id FROM docente WHERE usuario_id=%s", (docente_id,))
    docente_row = cursor.fetchone()

    if not docente_row:
        mysql.connection.rollback()
        cursor.close()
        raise Exception("El docente no existe en la tabla docente")

    docente_pk = docente_row[0] if isinstance(docente_row, tuple) else docente_row["id"]

    # Actualizar profesión
    cursor.execute("UPDATE docente SET profesion=%s WHERE usuario_id=%s", (profesion, docente_id))

    # Actualizar asignaturas (eliminar las viejas y agregar las nuevas)
    cursor.execute("DELETE FROM docente_asignatura WHERE docente_id=%s", (docente_pk,))
    for asignatura_id in asignaturas:
        cursor.execute(
            "INSERT INTO docente_asignatura (docente_id, asignatura_id) VALUES (%s, %s)",
            (docente_pk, asignatura_id)
        )

    mysql.connection.commit()
    cursor.close()




# ---------------- Cambiar el estado del Docente a Inactivo ----------------
def eliminar_docente(docente_id):
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE usuarios SET estado='inactivo' WHERE id=%s", (docente_id,))
    mysql.connection.commit()
    cursor.close()

# ---------------- Reactivar Docente ----------------
def reactivar_docente(docente_id):
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE usuarios SET estado='activo' WHERE id=%s", (docente_id,))
    mysql.connection.commit()
    cursor.close()

# ---------------- Obtener Todas las Asignaturas ----------------
def obtener_asignaturas():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT id, nombre FROM asignatura")
    asignaturas = cursor.fetchall()
    cursor.close()
    return asignaturas
