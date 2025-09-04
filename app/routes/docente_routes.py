from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.docente_model import (
    obtener_docentes,
    obtener_docentes_inactivos,
    obtener_docente_por_id,
    actualizar_docente,
    eliminar_docente,
    reactivar_docente,
    obtener_asignaturas
)

docente_bp = Blueprint('docente', __name__, url_prefix="/docente")


@docente_bp.route('/')
def lista_docentes():
    docentes = obtener_docentes()
    return render_template("docente/docente.html", docentes=docentes)


@docente_bp.route('/inactivos')
def lista_docentes_inactivos():
    docentes = obtener_docentes_inactivos()
    return render_template("docente/borrados_docentes.html", docentes=docentes)


@docente_bp.route('/editar/<int:docente_id>', methods=["GET", "POST"])
def editar_docente(docente_id):
    docente = obtener_docente_por_id(docente_id)
    asignaturas = obtener_asignaturas()

    if request.method == "POST":
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        correo = request.form["correo"]
        telefono = request.form["telefono"]
        rol = request.form.get("rol", "docente")
        profesion = request.form["profesion"]
        contrasena = request.form.get("contrasena")
        asignaturas_ids = request.form.getlist("asignaturas")

        actualizar_docente(docente_id, nombre, apellido, correo, telefono, rol, profesion, contrasena, asignaturas_ids)
        flash("Docente actualizado correctamente", "success")
        return redirect(url_for("docente.lista_docentes"))

    return render_template("docente/editar_docente.html", docente=docente, asignaturas=asignaturas)


@docente_bp.route('/eliminar/<int:docente_id>', methods=['POST'])
def eliminar_docente_route(docente_id):
    eliminar_docente(docente_id)
    flash("Docente desactivado correctamente", "warning")
    return redirect(url_for("docente.lista_docentes"))


@docente_bp.route('/reactivar/<int:docente_id>',methods=['POST'])
def reactivar(docente_id):
    reactivar_docente(docente_id)
    flash("Docente reactivado correctamente", "success")
    return redirect(url_for("docente.lista_docentes_inactivos"))
