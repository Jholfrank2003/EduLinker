from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.relaciones_model import (
    obtener_relaciones,
    crear_relacion,
    eliminar_relacion,
    obtener_acudientes,
    obtener_estudiantes,
    obtener_parentescos,
    existe_relacion
)

relaciones_bp = Blueprint('relaciones', __name__, url_prefix="/relaciones")

@relaciones_bp.route("/")
def lista_relaciones():
    relaciones = obtener_relaciones()
    return render_template("relaciones/lista_relaciones.html", relaciones=relaciones)

@relaciones_bp.route("/crear", methods=["GET", "POST"])
def crear_relaciones():
    acudientes = obtener_acudientes()
    estudiantes = obtener_estudiantes()
    parentescos = obtener_parentescos()

    if request.method == "POST":
        acudiente_id = request.form["acudiente_id"]
        estudiante_id = request.form["estudiante_id"]
        parentesco = request.form["parentesco"]

        # ✅ validación antes de insertar
        if existe_relacion(acudiente_id, estudiante_id):
            flash("⚠️ Ya existe una relación entre este acudiente y este estudiante.", "warning")
        else:
            crear_relacion(acudiente_id, estudiante_id, parentesco)
            flash("Relación creada correctamente ✅", "success")

        return redirect(url_for("relaciones.crear_relaciones"))

    return render_template(
        "relaciones/crear_relaciones.html",
        acudientes=acudientes,
        estudiantes=estudiantes,
        parentescos=parentescos
    )

@relaciones_bp.route("/eliminar/<int:relacion_id>", methods=["POST"])
def eliminar(relacion_id):
    eliminar_relacion(relacion_id)
    flash("Relación eliminada correctamente", "warning")
    return redirect(url_for("relaciones.lista_relaciones"))
