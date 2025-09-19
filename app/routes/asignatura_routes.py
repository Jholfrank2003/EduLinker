from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.asignatura_model import (
    obtener_asignaturas,
    obtener_asignaturas_inactivas,
    crear_asignatura,
    obtener_asignatura_por_id,
    actualizar_asignatura,
    eliminar_asignatura,
    reactivar_asignatura
)
from app.utils.validaciones import validar_asignatura

asignatura_bp = Blueprint("asignatura", __name__, url_prefix="/asignaturas")

@asignatura_bp.route("/")
def lista_asignaturas():
    asignaturas = obtener_asignaturas()
    return render_template("asignatura/asignaturas.html", asignaturas=asignaturas)

@asignatura_bp.route("/crear", methods=["GET", "POST"])
def crear():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()

        valido, error = validar_asignatura(nombre)
        if not valido:
            flash(error, "danger")
            return render_template("asignatura/crear_asignatura.html", nombre=nombre)

        crear_asignatura(nombre)
        flash("Asignatura creada exitosamente.", "success")
        return redirect(url_for("asignatura.lista_asignaturas"))

    return render_template("asignatura/crear_asignatura.html")

@asignatura_bp.route("/editar/<int:asignatura_id>", methods=["GET", "POST"])
def editar(asignatura_id):
    asignatura = obtener_asignatura_por_id(asignatura_id)

    if request.method == "POST":
        nombre = request.form["nombre"]
        estado = request.form["estado"]

        valido, error = validar_asignatura(nombre)
        if not valido:
            flash(error, "danger")
            return render_template("asignatura/editar_asignatura.html", asignatura=asignatura, form_data=request.form)

        actualizar_asignatura(asignatura_id, nombre, estado)
        flash("Asignatura actualizada correctamente ✅", "success")
        return redirect(url_for("asignatura.lista_asignaturas"))

    return render_template("asignatura/editar_asignatura.html", asignatura=asignatura)

@asignatura_bp.route("/eliminar/<int:asignatura_id>", methods=["POST"])
def eliminar(asignatura_id):
    eliminar_asignatura(asignatura_id)
    flash("Asignatura desactivada ⚠️", "warning")
    return redirect(url_for("asignatura.lista_asignaturas"))

@asignatura_bp.route("/inactivas")
def inactivas():
    asignaturas = obtener_asignaturas_inactivas()
    return render_template("asignatura/borrados_asignaturas.html", asignaturas=asignaturas)

@asignatura_bp.route("/reactivar/<int:asignatura_id>", methods=["POST"])
def reactivar(asignatura_id):
    reactivar_asignatura(asignatura_id)
    flash("Asignatura reactivada correctamente ✅", "success")
    return redirect(url_for("asignatura.inactivas"))
