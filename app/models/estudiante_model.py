from app import mysql
import MySQLdb.cursors

# ---------------- Obtener todos los Estudiantes Activos ----------------
def obtener_estudiantes():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = """
        SELECT 
            u.id, 
            u.nombre, 
            u.apellido, 
            u.correo, 
            u.telefono, 
            u.rol, 
            u.estado,
            e.grado_id,
            g.nombre AS grado,
            e.fecha_nacimiento
        FROM estudiante e
        INNER JOIN usuarios u ON e.usuario_id = u.id
        INNER JOIN grado g ON e.grado_id = g.id
        WHERE u.estado = 'activo'
    """
    cursor.execute(query)
    estudiantes = cursor.fetchall()
    cursor.close()
    return estudiantes

# ---------------- Obtener Todos los grados ----------------
def obtener_grados():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = "SELECT id, nombre FROM grado"
    cursor.execute(query)
    grados = cursor.fetchall()
    cursor.close()
    return grados


# ---------------- Obtener todos los Estudiantyes Inactivos ----------------
def obtener_estudiantes_inactivos():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = """
        SELECT 
            u.id, 
            u.nombre, 
            u.apellido, 
            u.correo, 
            u.telefono, 
            u.rol, 
            u.estado,
            e.grado_id,
            e.fecha_nacimiento
        FROM estudiante e
        INNER JOIN usuarios u ON e.usuario_id = u.id
        WHERE u.estado = 'inactivo'
    """
    cursor.execute(query)
    estudiantes = cursor.fetchall()
    cursor.close()
    return estudiantes


# ---------------- Obtenerl el estudiante del Usuario  ----------------
def obtener_estudiante_por_id(estudiante_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = """
        SELECT 
            u.id, 
            u.nombre, 
            u.apellido, 
            u.correo, 
            u.telefono, 
            u.rol, 
            u.estado,
            u.contrasena,
            e.grado_id,
            e.fecha_nacimiento
        FROM estudiante e
        INNER JOIN usuarios u ON e.usuario_id = u.id
        WHERE u.id = %s
    """
    cursor.execute(query, (estudiante_id,))
    estudiante = cursor.fetchone()
    cursor.close()
    return estudiante


# ---------------- Actualizar Datos del Estudiante ----------------
def actualizar_estudiante(estudiante_id, nombre, apellido, correo, telefono, rol, contrasena, grado_id, fecha_nacimiento):
    cursor = mysql.connection.cursor()
    
    if contrasena:
        query = """
            UPDATE usuarios u
            INNER JOIN estudiante e ON u.id = e.usuario_id
            SET u.nombre=%s, u.apellido=%s, u.correo=%s, u.telefono=%s,
                u.rol=%s, u.contrasena=%s,
                e.grado_id=%s, e.fecha_nacimiento=%s
            WHERE u.id=%s
        """
        cursor.execute(query, (nombre, apellido, correo, telefono, rol, contrasena, grado_id, fecha_nacimiento, estudiante_id))
    else:
        query = """
            UPDATE usuarios u
            INNER JOIN estudiante e ON u.id = e.usuario_id
            SET u.nombre=%s, u.apellido=%s, u.correo=%s, u.telefono=%s,
                u.rol=%s,
                e.grado_id=%s, e.fecha_nacimiento=%s
            WHERE u.id=%s
        """
        cursor.execute(query, (nombre, apellido, correo, telefono, rol, grado_id, fecha_nacimiento, estudiante_id))
    
    mysql.connection.commit()
    cursor.close()


# ---------------- Cambiar el estado del Estudiante a Inactivo ----------------
def inactivar_estudiante(estudiante_id):
    cursor = mysql.connection.cursor()
    query = "UPDATE usuarios SET estado = 'inactivo' WHERE id = %s"
    cursor.execute(query, (estudiante_id,))
    mysql.connection.commit()
    cursor.close()


# ---------------- Reactivar Estudiante ----------------
def reactivar_estudiante(estudiante_id):
    cursor = mysql.connection.cursor()
    query = "UPDATE usuarios SET estado = 'activo' WHERE id = %s"
    cursor.execute(query, (estudiante_id,))
    mysql.connection.commit()
    cursor.close()
