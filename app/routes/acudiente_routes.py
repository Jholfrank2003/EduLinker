from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.acudiente_model import (
    obtener_acudientes, 
    obtener_acudiente_por_id, 
    actualizar_acudiente, 
    eliminar_acudiente, 
    obtener_acudientes_inactivos,
    reactivar_acudiente
)

from app.utils.validaciones import validar_acudiente

acudiente_bp = Blueprint('acudiente', __name__, url_prefix="/acudiente")

@acudiente_bp.route('/')
def lista_acudientes():
    acudientes = obtener_acudientes()
    return render_template("acudiente/acudiente.html", acudientes=acudientes)


@acudiente_bp.route('/editar/<int:acudiente_id>', methods=['GET', 'POST'])
def editar_acudiente(acudiente_id):
    acudiente = obtener_acudiente_por_id(acudiente_id)

    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo = request.form['correo']
        telefono = request.form['telefono']
        ocupacion = request.form['ocupacion']
        
        contrasena = request.form.get('contrasena')

        valido, error = validar_acudiente(nombre, apellido, correo, telefono, ocupacion, contrasena)
        if not valido:
            flash(error, "danger")
            return render_template("acudiente/editar_acudiente.html", acudiente=acudiente)

        rol_id = acudiente['rol_id']
        actualizar_acudiente(acudiente_id, nombre, apellido, correo, telefono, rol_id, ocupacion, contrasena)
        flash("Acudiente actualizado correctamente", "success")
        return redirect(url_for('acudiente.lista_acudientes'))

    return render_template("acudiente/editar_acudiente.html", acudiente=acudiente)




@acudiente_bp.route('/eliminar/<int:acudiente_id>', methods=['POST'])
def eliminar_acudiente_route(acudiente_id):
    eliminar_acudiente(acudiente_id)
    flash("El acudiente ha sido desactivado.", "warning")
    return redirect(url_for('acudiente.lista_acudientes'))


@acudiente_bp.route('/borrados')
def lista_acudientes_inactivos():
    acudientes = obtener_acudientes_inactivos()
    return render_template("acudiente/borrados_acudientes.html", acudientes=acudientes)


@acudiente_bp.route('/reactivar/<int:acudiente_id>', methods=['POST'])
def reactivar(acudiente_id):
    reactivar_acudiente(acudiente_id)
    flash("Acudiente reactivado correctamente.", "success")
    return redirect(url_for('acudiente.lista_acudientes_inactivos'))
