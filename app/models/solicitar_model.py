from datetime import datetime, timedelta
from app import mysql
import MySQLdb.cursors


# ---------------- Filtrar Docente por Asignatura ----------------

# Obtener todas las asignaturas
def obtener_asignaturas():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, nombre FROM asignatura")
    asignaturas = cur.fetchall()
    cur.close()
    return asignaturas

# Obtener docentes que dictan una asignatura
def obtener_docentes_por_asignatura(asignatura_id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)  
    query = """
        SELECT d.id AS id, u.nombre AS nombre, u.apellido AS apellido
        FROM docente d
        JOIN usuarios u ON d.usuario_id = u.id
        JOIN docente_asignatura da ON d.id = da.docente_id
        WHERE da.asignatura_id = %s
    """
    cur.execute(query, (asignatura_id,))
    docentes = cur.fetchall()
    cur.close()
    return docentes


# ---------------- Obtener todos los Slots de un Docente----------------
def obtener_slots_docente(docente_id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("""
        SELECT s.id, s.hora_inicio, s.hora_fin, d.dia, s.estado
        FROM slots s
        JOIN disponibilidad d ON s.disponibilidad_id = d.id
        WHERE d.docente_id = %s
    """, (docente_id,))
    slots = cur.fetchall()
    cur.close()

    for s in slots:
        if isinstance(s["hora_inicio"], timedelta):
            s["hora_inicio"] = (datetime.min + s["hora_inicio"]).time()
        if isinstance(s["hora_fin"], timedelta):
            s["hora_fin"] = (datetime.min + s["hora_fin"]).time()

    return slots


# ---------------- Crear unaCita y Cambiar el Estado del Slots a Ocupado ----------------
def crear_cita(usuario_id, docente_id, slot_id, fecha, hora_inicio, hora_fin):
   
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    try:
        if isinstance(fecha, str):
            fecha_cita = datetime.strptime(fecha, "%Y-%m-%d").date()
        elif isinstance(fecha, datetime):
            fecha_cita = fecha.date()
        else:
            fecha_cita = fecha 

        inicio_semana = fecha_cita - timedelta(days=fecha_cita.weekday())  # lunes
        fin_semana = inicio_semana + timedelta(days=6)                     # domingo

# ---------------- Validar si ya tienes una Cita esa Semana ----------------
        cur.execute("""
            SELECT id FROM citas
            WHERE usuario_id = %s
              AND fecha BETWEEN %s AND %s
              AND estado IN ('pendiente', 'aprobada')
        """, (usuario_id, inicio_semana, fin_semana))

        if cur.fetchone():
            cur.close()
            return False, "⚠️ Ya tienes una cita en esta semana."
        
        cur.execute("UPDATE slots SET estado='ocupado' WHERE id=%s", (slot_id,))
        
        cur.execute("""
            INSERT INTO citas (usuario_id, docente_id, slot_id, fecha, hora_inicio, hora_fin, estado)
            VALUES (%s, %s, %s, %s, %s, %s, 'pendiente')
        """, (usuario_id, docente_id, slot_id, fecha_cita, hora_inicio, hora_fin))
        
        mysql.connection.commit()
        cur.close()
        return True, "✅ Cita registrada correctamente."
    
    except Exception as e:
        cur.close()
        return False, f"Error al registrar la cita: {e}"






