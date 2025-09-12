from flask import Blueprint, render_template, request, redirect, url_for, flash
# from werkzeug.security import generate_password_hash
from app.models.estudiante_model import (
    obtener_estudiantes,
    obtener_estudiantes_inactivos,
    obtener_estudiante_por_id,
    actualizar_estudiante,
    inactivar_estudiante,
    reactivar_estudiante,
    obtener_grados
)

estudiante_bp = Blueprint('estudiante', __name__, url_prefix="/estudiante")


@estudiante_bp.route('/')
def lista_estudiantes():
    estudiantes = obtener_estudiantes()
    return render_template("estudiante/estudiante.html", estudiantes=estudiantes)


@estudiante_bp.route('/inactivos')
def lista_estudiantes_inactivos():
    estudiantes = obtener_estudiantes_inactivos()
    return render_template("estudiante/borrados_estudiantes.html", estudiantes=estudiantes)


@estudiante_bp.route('/editar/<int:estudiante_id>', methods=['GET', 'POST'])
def editar_estudiante(estudiante_id):
    estudiante = obtener_estudiante_por_id(estudiante_id)
    grados = obtener_grados()

    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo = request.form['correo']
        telefono = request.form['telefono']
        grado_id = request.form['grado_id']
        fecha_nacimiento = request.form['fecha_nacimiento']
        contrasena = request.form.get('contrasena')
        
        rol_id = estudiante["rol_id"]

        actualizar_estudiante(estudiante_id, nombre, apellido, correo, telefono, rol_id, contrasena, grado_id, fecha_nacimiento)
        flash("Estudiante actualizado correctamente", "success")
        return redirect(url_for('estudiante.lista_estudiantes'))

    return render_template("estudiante/editar_estudiante.html", estudiante=estudiante, grados=grados)



@estudiante_bp.route('/eliminar/<int:estudiante_id>')
def eliminar_estudiante(estudiante_id):
    inactivar_estudiante(estudiante_id)
    flash("Estudiante marcado como inactivo", "warning")
    return redirect(url_for('estudiante.lista_estudiantes'))


@estudiante_bp.route('/reactivar/<int:estudiante_id>')
def reactivar(estudiante_id):
    reactivar_estudiante(estudiante_id)
    flash("Estudiante reactivado correctamente", "success")
    return redirect(url_for('estudiante.lista_estudiantes_inactivos'))
