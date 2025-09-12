from app import mysql
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from app.models.usuario_model import (
    crear_usuario, 
    registrar_estudiante,
    registrar_acudiente,
    registrar_docente, 
    obtener_roles, 
    obtener_nombre_rol, 
    validar_usuario, 
    validar_estudiante, 
    validar_acudiente, 
    validar_docente,
    manejar_error
)

registro_bp = Blueprint('registro', __name__)

@registro_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, nombre FROM grado")
    grados = cursor.fetchall()

    cursor.execute("SELECT id, nombre FROM asignatura")
    asignaturas = cursor.fetchall()

    roles = obtener_roles()

    if request.method == 'POST':
        try:
            nombre = request.form['nombre'].strip()
            apellido = request.form['apellido'].strip()
            correo = request.form['correo'].strip()
            telefono = request.form['telefono'].strip()
            contrasena = request.form['contraseña'].strip()
            rol_id = request.form['rol_id']

            valido, error_msg = validar_usuario(nombre, apellido, correo, telefono, contrasena)
            if not valido:
                return manejar_error(error_msg, roles, grados, asignaturas, request.form, request.form.getlist('asignatura_id'))

            contrasena_hash = generate_password_hash(contrasena)
            usuario_id = crear_usuario(nombre, apellido, correo, telefono, contrasena_hash, rol_id)
            rol_nombre = obtener_nombre_rol(rol_id)

            if rol_nombre == 'estudiante':
                fecha_nacimiento = request.form['fecha_nacimiento']
                grado_id = request.form['grado_id']
                valido, error_msg = validar_estudiante(grado_id, fecha_nacimiento)
                if not valido:
                    return manejar_error(error_msg, roles, grados, asignaturas, request.form)
                registrar_estudiante(usuario_id, grado_id, fecha_nacimiento)

            elif rol_nombre == 'acudiente':
                ocupacion = request.form['ocupacion']
                valido, error_msg = validar_acudiente(ocupacion)
                if not valido:
                    return manejar_error(error_msg, roles, grados, asignaturas, request.form)
                registrar_acudiente(usuario_id, ocupacion)

            elif rol_nombre == 'docente':
                profesion = request.form['profesion']
                asignatura_id = request.form.getlist('asignatura_id')
                valido, error_msg = validar_docente(profesion, asignatura_id)
                if not valido:
                    return manejar_error(error_msg, roles, grados, asignaturas, request.form, asignatura_id)
                registrar_docente(usuario_id, profesion, asignatura_id)

            mysql.connection.commit()
            flash("Usuario registrado exitosamente ✅", "success")
            return redirect(url_for('auth.login'))

        except Exception as e:
            import traceback
            print("Error en registro:", traceback.format_exc())
            mysql.connection.rollback()
            return manejar_error(f"Error al registrar: {str(e)}", roles, grados, asignaturas, request.form, request.form.getlist('asignatura_id'))

    return render_template('registro.html', roles=roles, grados=grados, asignaturas=asignaturas)
