from app import mysql
import MySQLdb.cursors

def obtener_relaciones():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = """
        SELECT r.id, 
               ua.nombre AS acudiente_nombre, ua.apellido AS acudiente_apellido,
               ue.nombre AS estudiante_nombre, ue.apellido AS estudiante_apellido,
               g.nombre AS grado,
               r.parentesco
        FROM acudiente_estudiante r
        INNER JOIN acudiente a ON a.id = r.acudiente_id
        INNER JOIN usuarios ua ON ua.id = a.usuario_id
        INNER JOIN estudiante e ON e.id = r.estudiante_id
        INNER JOIN usuarios ue ON ue.id = e.usuario_id
        INNER JOIN grado g ON e.grado_id = g.id
        GROUP BY r.id
    """
    cursor.execute(query)
    relaciones = cursor.fetchall()
    cursor.close()
    return relaciones

def existe_relacion(acudiente_id, estudiante_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = """
        SELECT 1 
        FROM acudiente_estudiante 
        WHERE acudiente_id = %s AND estudiante_id = %s
        LIMIT 1
    """
    cursor.execute(query, (acudiente_id, estudiante_id))
    existe = cursor.fetchone() is not None
    cursor.close()
    return existe





def crear_relacion(acudiente_id, estudiante_id, parentesco):
    cursor = mysql.connection.cursor()
    query = "INSERT INTO acudiente_estudiante (acudiente_id, estudiante_id, parentesco) VALUES (%s, %s, %s)"
    cursor.execute(query, (acudiente_id, estudiante_id, parentesco))
    mysql.connection.commit()
    cursor.close()

def eliminar_relacion(relacion_id):
    cursor = mysql.connection.cursor()
    query = "DELETE FROM acudiente_estudiante WHERE id = %s"
    cursor.execute(query, (relacion_id,))
    mysql.connection.commit()
    cursor.close()

def obtener_estudiantes():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = """
        SELECT e.id, u.nombre, u.apellido, g.nombre AS grado
        FROM estudiante e
        INNER JOIN usuarios u ON e.usuario_id = u.id
        INNER JOIN grado g ON e.grado_id = g.id
        WHERE u.estado = 'activo'
    """
    cursor.execute(query)
    estudiantes = cursor.fetchall()
    cursor.close()
    return estudiantes


def obtener_acudientes():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = """
        SELECT a.id, u.nombre, u.apellido, u.correo
        FROM acudiente a
        INNER JOIN usuarios u ON a.usuario_id = u.id
        WHERE u.estado = 'activo'
    """
    cursor.execute(query)
    acudientes = cursor.fetchall()
    cursor.close()
    return acudientes


# ---------------- Obtener valores ENUM de parentesco ----------------
def obtener_parentescos():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SHOW COLUMNS FROM acudiente_estudiante LIKE 'parentesco'")
    row = cursor.fetchone()
    cursor.close()

    if row and "enum(" in row["Type"]:
        valores = row["Type"].replace("enum(", "").replace(")", "").replace("'", "")
        lista_parentescos = [v.strip() for v in valores.split(",")]
        return sorted(lista_parentescos)
    return []

