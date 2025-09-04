from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from app import mysql

registro_bp = Blueprint('registro', __name__)

@registro_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    cursor = mysql.connection.cursor()

    cursor.execute("SELECT id, nombre FROM grado")
    grados = cursor.fetchall()

    cursor.execute("SELECT id, nombre FROM asignatura")
    asignaturas = cursor.fetchall()

    if request.method == 'POST':
        try:
            nombre = request.form['nombre']
            apellido = request.form['apellido']
            correo = request.form['correo']
            telefono = request.form['telefono']
            contraseña = generate_password_hash(request.form['contraseña'])
            rol = request.form['rol']

            cursor.execute("""
                INSERT INTO usuarios (nombre, apellido, correo, telefono, contrasena, rol)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (nombre, apellido, correo, telefono, contraseña, rol))
            mysql.connection.commit()

            usuario_id = cursor.lastrowid

            if rol == 'estudiante':
                fecha_nacimiento = request.form['fecha_nacimiento']
                grado_id = request.form['grado_id']
                cursor.execute("""
                    INSERT INTO estudiante (usuario_id, fecha_nacimiento, grado_id)
                    VALUES (%s, %s, %s)
                """, (usuario_id, fecha_nacimiento, grado_id))

            elif rol == 'acudiente':
                ocupacion = request.form['ocupacion']
                cursor.execute("""
                    INSERT INTO acudiente (usuario_id, ocupacion)
                    VALUES (%s, %s)
                """, (usuario_id, ocupacion))

            elif rol == 'docente':
                profesion = request.form['profesion']
                asignatura_id = request.form.getlist('asignatura_id') 

                from app.models.usuario_model import registrar_docente
                registrar_docente(usuario_id, profesion, asignatura_id)


            mysql.connection.commit()
            flash("Usuario registrado exitosamente ✅", "success")
            return redirect(url_for('auth.login'))

        except Exception as e:
            import traceback
            print("Error en registro:", traceback.format_exc())
            flash(f"Error al registrar: {str(e)}", "danger")
            mysql.connection.rollback()

    return render_template('registro.html', grados=grados, asignaturas=asignaturas)
