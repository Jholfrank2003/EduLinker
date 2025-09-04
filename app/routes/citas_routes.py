
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import mysql
import MySQLdb.cursors
from app.models.citas_model import (
    obtener_citas_usuario, 
    obtener_registro_citas_usuario,
    cancelar_cita,
    obtener_citas_docente,
    obtener_citas_pendientes_docente,
    obtener_docente_id_por_usuario,
    obtener_registro_citas_docente,
    aprobar_cita_docente,
    rechazar_cita_docente,
    finalizar_cita_docente
)

citas_bp = Blueprint("citas", __name__, url_prefix="/citas")

@citas_bp.route("/mis-citas")
@login_required
def mis_citas():
    usuario_id = current_user.id
    citas = obtener_citas_usuario(usuario_id)
    return render_template("citas/mis_citas.html", citas=citas)

@citas_bp.route("/cancelar/<int:cita_id>")
@login_required
def cancelar_cita_route(cita_id):
    usuario_id = current_user.id
    ok, msg = cancelar_cita(cita_id, usuario_id)
    flash(msg, "success" if ok else "danger")
    return redirect(url_for("citas.mis_citas"))


citas_bp = Blueprint("citas", __name__, url_prefix="/citas")
@citas_bp.route("/mis-citas")
@login_required
def mis_citas():
    usuario_id = current_user.id
    estado = request.args.get("estado")
    citas = obtener_citas_usuario(usuario_id, estado)
    return render_template("citas/mis_citas.html", citas=citas, estado_filtro=estado)


@citas_bp.route("/cancelar/<int:cita_id>", methods=["POST"])
@login_required
def cancelar_cita_route(cita_id):
    motivo = request.form.get("motivo", "").strip()
    if not motivo:
        flash("⚠️ Debes ingresar un motivo para cancelar la cita.", "warning")
        return redirect(url_for("citas.mis_citas"))

    exito, mensaje = cancelar_cita(cita_id, current_user.id, motivo)
    flash(mensaje, "success" if exito else "danger")
    return redirect(url_for("citas.registros_citas"))


@citas_bp.route("/registros")
@login_required
def registros_citas():
    usuario_id = current_user.id
    estado = request.args.get("estado") 
    registros = obtener_registro_citas_usuario(usuario_id, estado)
    return render_template("citas/registro_citas.html", registros=registros, estado_filtro=estado)



#Rutas Docente

@citas_bp.route("/docente/mis-citas")
@login_required
def mis_citas_docente():
    if current_user.rol != "docente":
        flash("⚠️ Solo los docentes pueden acceder a esta sección.", "warning")
        return redirect(url_for("citas.mis_citas"))

    docente_id = obtener_docente_id_por_usuario(current_user.id)
    if not docente_id:
        flash("⚠️ No se encontró el docente asociado.", "danger")
        return redirect(url_for("citas.mis_citas"))

    estado = request.args.get("estado")
    citas = obtener_citas_docente(docente_id, estado)
    return render_template("citas/mis_citas_docente.html", citas=citas, estado_filtro=estado)


@citas_bp.route("/docente/aprobar/<int:cita_id>", methods=["POST"])
@login_required
def aprobar_cita_docente_route(cita_id):
    if current_user.rol != "docente":
        flash("⚠️ Acción no permitida.", "danger")
        return redirect(url_for("citas.mis_citas_docente"))

    docente_id = obtener_docente_id_por_usuario(current_user.id)
    exito, mensaje = aprobar_cita_docente(cita_id, docente_id)
    flash(mensaje, "success" if exito else "danger")
    return redirect(url_for("citas.mis_citas_docente"))


@citas_bp.route("/docente/rechazar/<int:cita_id>", methods=["POST"])
@login_required
def rechazar_cita_docente_route(cita_id):
    if current_user.rol != "docente":
        flash("⚠️ Acción no permitida.", "danger")
        return redirect(url_for("citas.mis_citas_docente"))

    motivo = request.form.get("motivo", "").strip()
    if not motivo:
        flash("⚠️ Debes ingresar un motivo para rechazar la cita.", "warning")
        return redirect(url_for("citas.mis_citas_docente"))

    docente_id = obtener_docente_id_por_usuario(current_user.id)
    exito, mensaje = rechazar_cita_docente(cita_id, docente_id, motivo)
    flash(mensaje, "success" if exito else "danger")
    return redirect(url_for("citas.mis_citas_docente"))


@citas_bp.route("/pendientes-count")
@login_required
def pendientes_count():
    if current_user.rol != "docente":
        return jsonify({"success": False, "count": 0, "citas": []})

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT id FROM docente WHERE usuario_id=%s", (current_user.id,))
    docente = cur.fetchone()
    cur.close()

    if not docente:
        return jsonify({"success": False, "count": 0, "citas": []})

    docente_id = docente['id']
    citas = obtener_citas_pendientes_docente(docente_id)

    return jsonify({
        "success": True,
        "count": len(citas),
        "citas": citas
    })
    
@citas_bp.route("/docente/finalizar/<int:cita_id>", methods=["POST"])
@login_required
def finalizar_cita_docente_route(cita_id):
    if current_user.rol != "docente":
        flash("⚠️ Acción no permitida.", "danger")
        return redirect(url_for("citas.mis_citas_docente"))

    motivo = request.form.get("motivo", "").strip()
    if not motivo:
        motivo = "Cita finalizada correctamente."  

    docente_id = obtener_docente_id_por_usuario(current_user.id)
    exito, mensaje = finalizar_cita_docente(cita_id, docente_id, motivo)
    flash(mensaje, "success" if exito else "danger")
    return redirect(url_for("citas.mis_citas_docente"))


@citas_bp.route("/docente/historial")
@login_required
def historial_citas_docente():
    if current_user.rol != "docente":
        flash("⚠️ Solo los docentes pueden acceder a esta sección.", "warning")
        return redirect(url_for("main.home"))
    
    docente_id = obtener_docente_id_por_usuario(current_user.id)
    if not docente_id:
        flash("⚠️ No se encontró el docente asociado.", "danger")
        return redirect(url_for("citas.mis_citas"))

    estado = request.args.get("estado") 

    registros = obtener_registro_citas_docente(docente_id, estado)
    return render_template(
        "citas/registro_citas_docente.html",
        registros=registros,
        estado_filtro=estado
    )




