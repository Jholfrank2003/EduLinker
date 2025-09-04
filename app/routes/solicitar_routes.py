from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.models.solicitar_model import (
    obtener_asignaturas,
    obtener_docentes_por_asignatura,
    obtener_slots_docente,
    crear_cita
)

solicitar_bp = Blueprint("solicitar", __name__, url_prefix="/solicitar")

@solicitar_bp.route("/solicitar", methods=["GET"])
def solicitar_cita():
    asignaturas = obtener_asignaturas()
    return render_template("disponibilidad/solicitar_cita.html", asignaturas=asignaturas)

@solicitar_bp.route("/docentes/<int:asignatura_id>")
def listar_docentes(asignatura_id):
    docentes = obtener_docentes_por_asignatura(asignatura_id)
    return jsonify([{"id": d["id"], "nombre": f"{d['nombre']} {d['apellido']}"} for d in docentes])

@solicitar_bp.route("/disponibilidad/<int:docente_id>")
def listar_slots(docente_id):
    slots = obtener_slots_docente(docente_id)

    dias_map = {"lunes":1, "martes":2, "miercoles":3, "jueves":4, "viernes":5}

    eventos = []
    for s in slots:
        slot_day = dias_map[s["dia"].lower()]
        if s["estado"] == "libre":
            eventos.append({
                "id": s["id"],
                "title": "Libre",
                "daysOfWeek": [slot_day],
                "startTime": s["hora_inicio"].strftime("%H:%M:%S"),
                "endTime": s["hora_fin"].strftime("%H:%M:%S"),
                "color": "#28a745",  
                "estado": "libre"
            })
        else:
            eventos.append({
                "id": s["id"],
                "title": "Ocupado",
                "daysOfWeek": [slot_day],
                "startTime": s["hora_inicio"].strftime("%H:%M:%S"),
                "endTime": s["hora_fin"].strftime("%H:%M:%S"),
                "color": "#007bff",  
                "estado": "ocupado",
                "overlap": False
            })

    return jsonify(eventos)

@solicitar_bp.route("/confirmar", methods=["POST"])
@login_required
def confirmar_cita():
    data = request.json

    usuario_id = current_user.id
    docente_id = data.get("docente_id")
    slot_id = data.get("slot_id")
    fecha = data.get("fecha")  
    hora_inicio = data.get("hora_inicio")
    hora_fin = data.get("hora_fin")

    exito, mensaje = crear_cita(usuario_id, docente_id, slot_id, fecha, hora_inicio, hora_fin)
    return jsonify({"success": exito, "message": mensaje})


