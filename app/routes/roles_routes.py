from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.roles_model import (
    obtener_roles,
    obtener_roles_inactivos,
    crear_rol,
    obtener_rol_por_id,
    actualizar_rol,
    eliminar_rol,
    reactivar_rol
)
from app.utils.validaciones import validar_rol

roles_bp = Blueprint("roles", __name__, url_prefix="/roles")

@roles_bp.route("/")
def lista_roles():
    roles = obtener_roles()
    return render_template("roles/roles.html", roles=roles)

@roles_bp.route("/crear", methods=["GET", "POST"])
def crear():
    if request.method == "POST":
        nombre = request.form["nombre"]
        descripcion = request.form["descripcion"]

        valido, error = validar_rol(nombre, descripcion)
        if not valido:
            flash(error, "danger")
            return render_template("roles/crear_rol.html", form_data=request.form)

        crear_rol(nombre, descripcion)
        flash("Rol creado exitosamente ✅", "success")
        return redirect(url_for("roles.lista_roles"))

    return render_template("roles/crear_rol.html")

@roles_bp.route("/editar/<int:rol_id>", methods=["GET", "POST"])
def editar(rol_id):
    rol = obtener_rol_por_id(rol_id)

    if request.method == "POST":
        nombre = request.form["nombre"]
        descripcion = request.form["descripcion"]

        valido, error = validar_rol(nombre, descripcion)
        if not valido:
            flash(error, "danger")
            return render_template("roles/editar_rol.html", rol=rol, form_data=request.form)

        actualizar_rol(rol_id, nombre, descripcion)
        flash("Rol actualizado correctamente ✅", "success")
        return redirect(url_for("roles.lista_roles"))

    return render_template("roles/editar_rol.html", rol=rol)

@roles_bp.route("/eliminar/<int:rol_id>", methods=["POST"])
def eliminar(rol_id):
    eliminar_rol(rol_id)
    flash("Rol desactivado ⚠️", "warning")
    return redirect(url_for("roles.lista_roles"))

@roles_bp.route("/inactivos")
def inactivos():
    roles = obtener_roles_inactivos()
    return render_template("roles/borrados_roles.html", roles=roles)

@roles_bp.route("/reactivar/<int:rol_id>", methods=["POST"])
def reactivar(rol_id):
    reactivar_rol(rol_id)
    flash("Rol reactivado correctamente ✅", "success")
    return redirect(url_for("roles.inactivos"))
