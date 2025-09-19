from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from app import mysql
from app.models.usuario_model import (
    crear_usuario, 
    registrar_estudiante,
    registrar_acudiente,
    registrar_docente, 
    obtener_roles, 
    obtener_nombre_rol, 
    manejar_error,
    obtener_grados,
    obtener_asignaturas
)
from app.utils.validaciones import (
    validar_usuario, 
    validar_estudiante, 
    validar_acudiente, 
    validar_docente
)
import datetime

registro_bp = Blueprint('registro', __name__)

@registro_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    roles = obtener_roles()
    grados = obtener_grados()
    asignaturas = obtener_asignaturas()

    if request.method == 'POST':
        try:
            nombre = request.form['nombre'].strip()
            apellido = request.form['apellido'].strip()
            correo = request.form['correo'].strip()
            telefono = request.form['telefono'].strip()
            contrasena = request.form['contraseña'].strip()
            rol_id = int(request.form['rol_id'])

            valido, error_msg = validar_usuario(nombre, apellido, correo, telefono, contrasena)
            if not valido:
                return manejar_error(error_msg, roles, grados, asignaturas, request.form, request.form.getlist('asignatura_id'))

            contrasena_hash = generate_password_hash(contrasena)
            usuario_id = crear_usuario(nombre, apellido, correo, telefono, contrasena_hash, rol_id)
            rol_nombre = obtener_nombre_rol(rol_id)

            if rol_nombre.lower() == 'estudiante':
                fecha_nacimiento = request.form['fecha_nacimiento'].strip()
                grado_id = request.form['grado_id'].strip()

                valido, error_msg = validar_estudiante(nombre, apellido, correo, telefono, grado_id, fecha_nacimiento)
                if not valido:
                    return manejar_error(error_msg, roles, grados, asignaturas, request.form)

                fecha_nacimiento_obj = datetime.datetime.strptime(fecha_nacimiento, "%Y-%m-%d").date()
                grado_id_int = int(grado_id)

                registrar_estudiante(usuario_id, grado_id_int, fecha_nacimiento_obj)

            elif rol_nombre.lower() == 'acudiente':
                ocupacion = request.form['ocupacion'].strip()

                valido, error_msg = validar_acudiente(nombre, apellido, correo, telefono, ocupacion)
                if not valido:
                    return manejar_error(error_msg, roles, grados, asignaturas, request.form)

                registrar_acudiente(usuario_id, ocupacion)

            elif rol_nombre.lower() == 'docente':
                profesion = request.form['profesion'].strip()
                asignaturas_seleccionadas = request.form.getlist('asignatura_id')

                valido, error_msg = validar_docente(nombre, apellido, correo, telefono, profesion, asignaturas_seleccionadas)
                if not valido:
                    return manejar_error(error_msg, roles, grados, asignaturas, request.form, asignaturas_seleccionadas)

                asignaturas_int = [int(aid) for aid in asignaturas_seleccionadas if aid]
                registrar_docente(usuario_id, profesion, asignaturas_int)

            mysql.connection.commit()
            flash("Usuario registrado exitosamente ✅", "success")
            return redirect(url_for('auth.login'))

        except Exception as e:
            import traceback
            print("Error en registro:", traceback.format_exc())
            mysql.connection.rollback()
            return manejar_error(f"Error al registrar: {str(e)}", roles, grados, asignaturas, request.form, request.form.getlist('asignatura_id'))

    return render_template('registro.html', roles=roles, grados=grados, asignaturas=asignaturas)
