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
            r.nombre AS rol,  -- ahora traemos el nombre desde la tabla roles
            u.estado,
            e.grado_id,
            g.nombre AS grado,
            e.fecha_nacimiento
        FROM estudiante e
        INNER JOIN usuarios u ON e.usuario_id = u.id
        INNER JOIN grado g ON e.grado_id = g.id
        INNER JOIN roles r ON u.rol_id = r.id
        WHERE u.estado = 'activo'
    """
    cursor.execute(query)
    estudiantes = cursor.fetchall()
    cursor.close()
    return estudiantes


# ---------------- Obtener todos los Estudiantes Inactivos ----------------
def obtener_estudiantes_inactivos():
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
            e.grado_id,
            e.fecha_nacimiento
        FROM estudiante e
        INNER JOIN usuarios u ON e.usuario_id = u.id
        INNER JOIN roles r ON u.rol_id = r.id
        WHERE u.estado = 'inactivo'
    """
    cursor.execute(query)
    estudiantes = cursor.fetchall()
    cursor.close()
    return estudiantes


# ---------------- Obtener Estudiante por ID ----------------
def obtener_estudiante_por_id(estudiante_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = """
        SELECT 
            u.id, 
            u.nombre, 
            u.apellido, 
            u.correo, 
            u.telefono, 
            u.rol_id, 
            r.nombre AS rol,
            u.estado,
            u.contrasena,
            e.grado_id,
            e.fecha_nacimiento
        FROM estudiante e
        INNER JOIN usuarios u ON e.usuario_id = u.id
        INNER JOIN roles r ON u.rol_id = r.id
        WHERE u.id = %s
    """
    cursor.execute(query, (estudiante_id,))
    estudiante = cursor.fetchone()
    cursor.close()
    return estudiante


# ---------------- Actualizar Datos del Estudiante ----------------
def actualizar_estudiante(estudiante_id, nombre, apellido, correo, telefono, rol_id, contrasena, grado_id, fecha_nacimiento):
    cursor = mysql.connection.cursor()
    
    if contrasena:
        query = """
            UPDATE usuarios u
            INNER JOIN estudiante e ON u.id = e.usuario_id
            SET u.nombre=%s, u.apellido=%s, u.correo=%s, u.telefono=%s,
                u.rol_id=%s, u.contrasena=%s,
                e.grado_id=%s, e.fecha_nacimiento=%s
            WHERE u.id=%s
        """
        cursor.execute(query, (nombre, apellido, correo, telefono, rol_id, contrasena, grado_id, fecha_nacimiento, estudiante_id))
    else:
        query = """
            UPDATE usuarios u
            INNER JOIN estudiante e ON u.id = e.usuario_id
            SET u.nombre=%s, u.apellido=%s, u.correo=%s, u.telefono=%s,
                u.rol_id=%s,
                e.grado_id=%s, e.fecha_nacimiento=%s
            WHERE u.id=%s
        """
        cursor.execute(query, (nombre, apellido, correo, telefono, rol_id, grado_id, fecha_nacimiento, estudiante_id))
    
    mysql.connection.commit()
    cursor.close()


# ---------------- Obtener Todos los grados ----------------
def obtener_grados():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = "SELECT id, nombre FROM grado"
    cursor.execute(query)
    grados = cursor.fetchall()
    cursor.close()
    return grados

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
