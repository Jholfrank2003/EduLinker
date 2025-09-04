from flask import Blueprint, jsonify, render_template, request
from flask_login import login_required, current_user
from app import mysql
import MySQLdb.cursors
from datetime import datetime, timedelta

disponibilidad_bp = Blueprint("disponibilidad", __name__, url_prefix="/disponibilidad")

dias_map = {
    "lunes": 1,
    "martes": 2,
    "miercoles": 3,
    "jueves": 4,
    "viernes": 5
}

ESTADO_COLORES = {
    "disponible": "#28a745",   # Verde
    "vacaciones": "#6c757d",   # Gris oscuro
    "incapacitado": "#dc3545", # Rojo
    "inactivo": "#d3d3d3"      # Gris claro
}

ESTADOS_VALIDOS = set(ESTADO_COLORES.keys())

def format_time(td):
    if td is None:
        return None
    if isinstance(td, str):
        return td
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def actualizar_slots(cur, disponibilidad_id, nuevo_inicio, nuevo_fin, estado):
    from datetime import datetime, timedelta

    formato = "%H:%M:%S"
    inicio_dt = datetime.strptime(nuevo_inicio, formato)
    fin_dt = datetime.strptime(nuevo_fin, formato)

    cur.execute("""
        SELECT id, hora_inicio, hora_fin, estado
        FROM slots
        WHERE disponibilidad_id = %s
    """, (disponibilidad_id,))
    slots_existentes = cur.fetchall()

    for s in slots_existentes:
        s['hora_inicio_dt'] = datetime.strptime(str(s['hora_inicio']), formato)
        s['hora_fin_dt'] = datetime.strptime(str(s['hora_fin']), formato)

    if estado in ("vacaciones", "incapacitado", "inactivo"):
        for s in slots_existentes:
            if s['estado'] == "libre":
                cur.execute("DELETE FROM slots WHERE id = %s", (s['id'],))
        return

    for s in slots_existentes:
        if s['estado'] == "libre" and (s['hora_inicio_dt'] < inicio_dt or s['hora_fin_dt'] > fin_dt):
            cur.execute("DELETE FROM slots WHERE id = %s", (s['id'],))

    if estado == "disponible":
        horarios_existentes = {s['hora_inicio_dt'].strftime(formato) for s in slots_existentes if s['estado'] in ("libre", "ocupado")}
        tiempo_actual = inicio_dt
        while tiempo_actual < fin_dt:
            hora_str = tiempo_actual.strftime(formato)
            if hora_str not in horarios_existentes:
                cur.execute("""
                    INSERT INTO slots (disponibilidad_id, hora_inicio, hora_fin, estado)
                    VALUES (%s, %s, %s, 'libre')
                """, (disponibilidad_id, hora_str, (tiempo_actual + timedelta(hours=1)).strftime(formato)))
            tiempo_actual += timedelta(hours=1)



# Vista del calendario
@disponibilidad_bp.route("/")
@login_required
def disponibilidad_docente():
    return render_template("disponibilidad/disponibilidad_docente.html")

# API: lista de eventos
@disponibilidad_bp.route("/data")
@login_required
def disponibilidad_data():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT id FROM docente WHERE usuario_id = %s", (current_user.id,))
    docente = cur.fetchone()
    if not docente:
        cur.close()
        return jsonify([])

    docente_id = docente["id"]
    cur.execute("""
        SELECT id, dia, hora_inicio, hora_fin, estado
        FROM disponibilidad
        WHERE docente_id = %s
    """, (docente_id,))
    rows = cur.fetchall()
    cur.close()

    eventos = []
    for row in rows:
        estado = (row["estado"] or "").lower()
        color = ESTADO_COLORES.get(estado, "#007bff")

        if estado in ["vacaciones", "incapacitado"]:
            eventos.append({
                "id": row["id"],
                "title": estado.capitalize(),
                "estado": estado,
                "daysOfWeek": [dias_map.get(row["dia"], 1)],
                "startTime": "00:00:00",
                "endTime": "23:59:59",
                "color": color
            })
        else:
            inicio = format_time(row["hora_inicio"]) or "00:00:00"
            fin = format_time(row["hora_fin"]) or "23:59:59"
            eventos.append({
                "id": row["id"],
                "title": estado.capitalize() if estado else "",
                "estado": estado,
                "daysOfWeek": [dias_map.get(row["dia"], 1)],
                "startTime": inicio,
                "endTime": fin,
                "color": color
            })

    return jsonify(eventos)

@disponibilidad_bp.route("/update", methods=["POST"])
@login_required
def disponibilidad_update():
    data = request.get_json(silent=True) or {}
    disponibilidad_id = data.get("id")
    hora_inicio = data.get("hora_inicio")
    hora_fin = data.get("hora_fin")
    estado = (data.get("estado") or "").lower()

    if not all([disponibilidad_id, hora_inicio, hora_fin, estado]):
        return jsonify({"success": False, "msg": "Datos incompletos"})

    if estado not in ESTADOS_VALIDOS:
        return jsonify({"success": False, "msg": "Estado no válido"})

    if estado in ("disponible", "inactivo") and hora_inicio >= hora_fin:
        return jsonify({"success": False, "msg": "La hora de inicio debe ser menor que la hora de fin"})

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    formato = "%H:%M:%S"

    try:
        cur.execute("""
            UPDATE disponibilidad
            SET hora_inicio = %s, hora_fin = %s, estado = %s
            WHERE id = %s
        """, (hora_inicio, hora_fin, estado, disponibilidad_id))

        inicio_dt = datetime.strptime(hora_inicio, formato)
        fin_dt = datetime.strptime(hora_fin, formato)

        cur.execute("""
            SELECT id, hora_inicio, hora_fin, estado
            FROM slots
            WHERE disponibilidad_id = %s
        """, (disponibilidad_id,))
        slots_existentes = cur.fetchall()

        for s in slots_existentes:
            s['hora_inicio_dt'] = datetime.strptime(str(s['hora_inicio']), formato)
            s['hora_fin_dt'] = datetime.strptime(str(s['hora_fin']), formato)

        if estado in ("vacaciones", "incapacitado", "inactivo"):
            for s in slots_existentes:
                if s['estado'] == "libre":
                    cur.execute("DELETE FROM slots WHERE id = %s", (s['id'],))
        else:
            for s in slots_existentes:
                if s['estado'] == "libre" and (s['hora_inicio_dt'] < inicio_dt or s['hora_fin_dt'] > fin_dt):
                    cur.execute("DELETE FROM slots WHERE id = %s", (s['id'],))

            horarios_existentes = {s['hora_inicio_dt'].strftime(formato) for s in slots_existentes if s['estado'] in ("libre", "ocupado")}
            tiempo_actual = inicio_dt
            while tiempo_actual < fin_dt:
                hora_str = tiempo_actual.strftime(formato)
                if hora_str not in horarios_existentes:
                    cur.execute("""
                        INSERT INTO slots (disponibilidad_id, hora_inicio, hora_fin, estado)
                        VALUES (%s, %s, %s, 'libre')
                    """, (disponibilidad_id, hora_str, (tiempo_actual + timedelta(hours=1)).strftime(formato)))
                tiempo_actual += timedelta(hours=1)

        mysql.connection.commit()
    except Exception as e:
        cur.close()
        return jsonify({"success": False, "msg": f"Error al actualizar disponibilidad: {e}"})
    
    cur.close()
    return jsonify({"success": True})


