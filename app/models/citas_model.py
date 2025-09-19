import datetime
from app import mysql
import MySQLdb.cursors

# ---------------- Consultas Usuario ----------------

def obtener_citas_usuario(usuario_id, estado=None):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = """
        SELECT c.id, c.fecha, c.hora_inicio, c.hora_fin, c.estado,
               u.nombre AS docente_nombre, u.apellido AS docente_apellido,
               r.nombre AS docente_rol
        FROM citas c
        INNER JOIN docente d ON c.docente_id = d.id
        INNER JOIN usuarios u ON d.usuario_id = u.id
        INNER JOIN roles r ON u.rol_id = r.id
        WHERE c.usuario_id = %s
    """
    params = [usuario_id]

    if estado in ("pendiente", "aprobada", "cancelada", "rechazada", "finalizada"):
        sql += " AND c.estado = %s"
        params.append(estado)

    sql += " ORDER BY c.fecha DESC, c.hora_inicio ASC"
    cur.execute(sql, params)
    citas = cur.fetchall()
    cur.close()

    for cita in citas:
        if isinstance(cita["fecha"], datetime.date):
            cita["fecha"] = cita["fecha"].strftime("%d/%m/%Y")
        if isinstance(cita["hora_inicio"], datetime.time):
            cita["hora_inicio"] = cita["hora_inicio"].strftime("%H:%M")
        if isinstance(cita["hora_fin"], datetime.time):
            cita["hora_fin"] = cita["hora_fin"].strftime("%H:%M")

    return citas

def cancelar_cita(cita_id, usuario_id, motivo):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("""
        SELECT * FROM citas WHERE id = %s AND usuario_id = %s AND estado = 'pendiente'
    """, (cita_id, usuario_id))
    cita = cur.fetchone()

    if not cita:
        cur.close()
        return False, "❌ No se encontró la cita o no está en estado pendiente."

    cur.execute("""
        INSERT INTO registro_citas
        (usuario_id, docente_id, slot_id, fecha, hora_inicio, hora_fin, estado, motivo)
        VALUES (%s, %s, %s, %s, %s, %s, 'cancelada', %s)
    """, (cita["usuario_id"], cita["docente_id"], cita["slot_id"],
          cita["fecha"], cita["hora_inicio"], cita["hora_fin"], motivo))

    cur.execute("UPDATE slots SET estado='libre' WHERE id=%s", (cita["slot_id"],))
    cur.execute("DELETE FROM citas WHERE id=%s", (cita_id,))
    mysql.connection.commit()
    cur.close()
    return True, "✅ La cita fue cancelada y registrada con motivo."

def obtener_registro_citas_usuario(usuario_id, estado=None):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = """
        SELECT r.id, r.fecha, r.hora_inicio, r.hora_fin, r.estado, r.motivo,
               u.nombre AS docente_nombre, u.apellido AS docente_apellido,
               ro.nombre AS docente_rol,
               r.fecha_registro
        FROM registro_citas r
        INNER JOIN docente d ON r.docente_id = d.id
        INNER JOIN usuarios u ON d.usuario_id = u.id
        INNER JOIN roles ro ON u.rol_id = ro.id
        WHERE r.usuario_id = %s
    """
    params = [usuario_id]

    if estado in ("cancelada", "finalizada", "rechazada"):
        sql += " AND r.estado = %s"
        params.append(estado)

    sql += " ORDER BY r.fecha_registro DESC"
    cur.execute(sql, params)
    registros = cur.fetchall()
    cur.close()

    for reg in registros:
        if isinstance(reg["fecha"], datetime.date):
            reg["fecha"] = reg["fecha"].strftime("%d/%m/%Y")
        if isinstance(reg["hora_inicio"], datetime.time):
            reg["hora_inicio"] = reg["hora_inicio"].strftime("%H:%M")
        if isinstance(reg["hora_fin"], datetime.time):
            reg["hora_fin"] = reg["hora_fin"].strftime("%H:%M")
        if isinstance(reg["fecha_registro"], datetime.datetime):
            reg["fecha_registro"] = reg["fecha_registro"].strftime("%d/%m/%Y %H:%M")

    return registros

# ---------------- Consultas Docente ----------------

def obtener_docente_id_por_usuario(usuario_id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT id FROM docente WHERE usuario_id = %s", (usuario_id,))
    docente = cur.fetchone()
    cur.close()
    if docente:
        return docente["id"]
    return None

def obtener_citas_docente(docente_id, estado=None):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = """
        SELECT c.id, c.fecha, c.hora_inicio, c.hora_fin, c.estado,
               u.nombre, u.apellido, u.correo, u.telefono,
               r.nombre AS usuario_rol
        FROM citas c
        INNER JOIN usuarios u ON c.usuario_id = u.id
        INNER JOIN roles r ON u.rol_id = r.id
        WHERE c.docente_id = %s
    """
    params = [docente_id]

    if estado in ("pendiente", "aprobada"):
        sql += " AND c.estado = %s"
        params.append(estado)

    sql += " ORDER BY c.fecha DESC, c.hora_inicio ASC"
    cur.execute(sql, params)
    citas = cur.fetchall()
    cur.close()

    for cita in citas:
        if isinstance(cita["fecha"], datetime.date):
            cita["fecha"] = cita["fecha"].strftime("%d/%m/%Y")
        if isinstance(cita["hora_inicio"], datetime.time):
            cita["hora_inicio"] = cita["hora_inicio"].strftime("%H:%M")
        if isinstance(cita["hora_fin"], datetime.time):
            cita["hora_fin"] = cita["hora_fin"].strftime("%H:%M")

    return citas

def obtener_citas_pendientes_docente(docente_id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("""
        SELECT c.id, c.fecha, c.hora_inicio, c.hora_fin,
               u.nombre, u.apellido, r.nombre AS usuario_rol
        FROM citas c
        INNER JOIN usuarios u ON c.usuario_id = u.id
        INNER JOIN roles r ON u.rol_id = r.id
        WHERE c.docente_id = %s AND c.estado = 'pendiente'
        ORDER BY c.fecha ASC, c.hora_inicio ASC
    """, (docente_id,))
    citas = cur.fetchall()
    cur.close()

    for cita in citas:
        if isinstance(cita["fecha"], datetime.date):
            cita["fecha"] = cita["fecha"].strftime("%d/%m/%Y")
        if isinstance(cita["hora_inicio"], datetime.time):
            cita["hora_inicio"] = cita["hora_inicio"].strftime("%H:%M")
        if isinstance(cita["hora_fin"], datetime.time):
            cita["hora_fin"] = cita["hora_fin"].strftime("%H:%M")
    return citas

def aprobar_cita_docente(cita_id, docente_id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("""
        SELECT * FROM citas WHERE id = %s AND docente_id = %s AND estado = 'pendiente'
    """, (cita_id, docente_id))
    cita = cur.fetchone()

    if not cita:
        cur.close()
        return False, "❌ No se encontró la cita o ya fue atendida."

    cur.execute("UPDATE citas SET estado = 'aprobada' WHERE id = %s", (cita_id,))
    mysql.connection.commit()
    cur.close()
    return True, "✅ Cita aprobada correctamente."

def rechazar_cita_docente(cita_id, docente_id, motivo):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("""
        SELECT * FROM citas WHERE id = %s AND docente_id = %s AND estado = 'pendiente'
    """, (cita_id, docente_id))
    cita = cur.fetchone()

    if not cita:
        cur.close()
        return False, "❌ No se encontró la cita o no está pendiente."

    cur.execute("""
        INSERT INTO registro_citas
        (usuario_id, docente_id, slot_id, fecha, hora_inicio, hora_fin, estado, motivo)
        VALUES (%s, %s, %s, %s, %s, %s, 'rechazada', %s)
    """, (cita["usuario_id"], cita["docente_id"], cita["slot_id"],
          cita["fecha"], cita["hora_inicio"], cita["hora_fin"], motivo))

    cur.execute("UPDATE slots SET estado='libre' WHERE id=%s", (cita["slot_id"],))
    cur.execute("DELETE FROM citas WHERE id=%s", (cita_id,))
    mysql.connection.commit()
    cur.close()
    return True, "✅ La cita fue rechazada y registrada con motivo."

def finalizar_cita_docente(cita_id, docente_id, motivo):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("""
        SELECT * FROM citas WHERE id = %s AND docente_id = %s AND estado = 'aprobada'
    """, (cita_id, docente_id))
    cita = cur.fetchone()

    if not cita:
        cur.close()
        return False, "❌ No se encontró la cita o no está en estado aprobado."

    cur.execute("""
        INSERT INTO registro_citas
        (usuario_id, docente_id, slot_id, fecha, hora_inicio, hora_fin, estado, motivo)
        VALUES (%s, %s, %s, %s, %s, %s, 'finalizada', %s)
    """, (cita["usuario_id"], cita["docente_id"], cita["slot_id"],
          cita["fecha"], cita["hora_inicio"], cita["hora_fin"], motivo))

    cur.execute("UPDATE slots SET estado='libre' WHERE id=%s", (cita["slot_id"],))
    cur.execute("DELETE FROM citas WHERE id=%s", (cita_id,))
    mysql.connection.commit()
    cur.close()
    return True, "✅ La cita fue finalizada y registrada."

def obtener_registro_citas_docente(docente_id, estado=None):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = """
        SELECT r.id, r.fecha, r.hora_inicio, r.hora_fin, r.estado, r.motivo,
               u.nombre, u.apellido, u.correo, u.telefono,
               ro.nombre AS usuario_rol
        FROM registro_citas r
        INNER JOIN usuarios u ON r.usuario_id = u.id
        INNER JOIN roles ro ON u.rol_id = ro.id
        WHERE r.docente_id = %s
    """
    params = [docente_id]

    if estado in ("finalizada", "rechazada", "cancelada"):
        sql += " AND r.estado = %s"
        params.append(estado)

    sql += " ORDER BY r.fecha_registro DESC"
    cur.execute(sql, params)
    registros = cur.fetchall()
    cur.close()

    for reg in registros:
        if isinstance(reg["fecha"], datetime.date):
            reg["fecha"] = reg["fecha"].strftime("%d/%m/%Y")
        if isinstance(reg["hora_inicio"], datetime.time):
            reg["hora_inicio"] = reg["hora_inicio"].strftime("%H:%M")
        if isinstance(reg["hora_fin"], datetime.time):
            reg["hora_fin"] = reg["hora_fin"].strftime("%H:%M")
    return registros
