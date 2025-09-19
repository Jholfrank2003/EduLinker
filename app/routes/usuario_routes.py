from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.usuario_model import (
    obtener_administradores,
    obtener_administrador_por_id,
    actualizar_administrador,
    eliminar_administrador,
    obtener_administradores_inactivos,
    reactivar_administrador
)

from app.utils.validaciones import validar_admin_form


usuario_bp = Blueprint('usuario', __name__, url_prefix="/usuario")


@usuario_bp.route('/')
def lista_administradores():
    administradores = obtener_administradores()
    return render_template("usuario/usuario.html", administradores=administradores)


@usuario_bp.route('/editar/<int:admin_id>', methods=['GET', 'POST'])
def editar_administrador(admin_id):
    admin = obtener_administrador_por_id(admin_id)

    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo = request.form['correo']
        telefono = request.form['telefono']
        estado = request.form['estado']
        password = request.form['password']

        valido, error_msg = validar_admin_form(nombre, apellido, correo, telefono, password if password else None)
        if not valido:
            flash(error_msg, "danger")
            return render_template("usuario/editar_usuario.html", admin=admin)

        actualizar_administrador(admin_id, nombre, apellido, correo, telefono, estado, password if password else None)

        flash("Administrador actualizado correctamente.", "success")
        return redirect(url_for('usuario.lista_administradores'))

    return render_template("usuario/editar_usuario.html", admin=admin)



@usuario_bp.route('/eliminar/<int:admin_id>', methods=['POST'])
def eliminar_administrador_route(admin_id):
    eliminar_administrador(admin_id)
    flash("El administrador ha sido desactivado.", "warning")
    return redirect(url_for('usuario.lista_administradores'))


@usuario_bp.route('/borrados')
def lista_administradores_inactivos():
    administradores = obtener_administradores_inactivos()
    return render_template("usuario/borrados_usuarios.html", administradores=administradores)


@usuario_bp.route('/reactivar/<int:admin_id>', methods=['POST'])
def reactivar(admin_id):
    reactivar_administrador(admin_id)
    flash("Administrador reactivado correctamente.", "success")
    return redirect(url_for('usuario.lista_administradores_inactivos'))
