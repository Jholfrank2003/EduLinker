from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from app.models.perfil_model import (
    obtener_usuario,
    obtener_datos_docente,
    obtener_datos_estudiante,
    obtener_datos_acudiente,
    obtener_id_docente,
    actualizar_perfil,
    actualizar_docente,
    actualizar_estudiante,
    actualizar_acudiente,
    obtener_todas_asignaturas,
    actualizar_asignaturas_docente
)

perfil_bp = Blueprint('perfil', __name__, url_prefix="/perfil")

# ---------------- Ver perfil ----------------
@perfil_bp.route('/', methods=['GET'])
@login_required
def ver_perfil():
    usuario_id = current_user.id
    usuario = obtener_usuario(usuario_id)
    
    rol = usuario.get("rol", "").lower()
    if rol == "docente":
        usuario.update(obtener_datos_docente(usuario_id))
    elif rol == "estudiante":
        usuario.update(obtener_datos_estudiante(usuario_id))
    elif rol == "acudiente":
        usuario.update(obtener_datos_acudiente(usuario_id))

    return render_template("perfil/perfil.html", usuario=usuario)


# ---------------- Editar perfil ----------------
@perfil_bp.route('/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    usuario_id = current_user.id
    usuario = obtener_usuario(usuario_id)
    rol = usuario.get("rol", "").lower()

    todas_asignaturas = []

    if rol == "docente":
        datos_docente = obtener_datos_docente(usuario_id)
        usuario.update(datos_docente)
        todas_asignaturas = obtener_todas_asignaturas()
        if "asignaturas_list" not in usuario:
            usuario["asignaturas_list"] = []
    elif rol == "acudiente":
        datos_acudiente = obtener_datos_acudiente(usuario_id)
        usuario.update(datos_acudiente)
    elif rol == "estudiante":
        datos_estudiante = obtener_datos_estudiante(usuario_id)
        usuario.update(datos_estudiante)

    if request.method == "POST":
        form = request.form.to_dict()
        nombre = form.get('nombre')
        apellido = form.get('apellido')
        correo = form.get('correo')
        telefono = form.get('telefono')
        contrasena = form.get('contrasena')

        if not nombre or not apellido or not correo or not telefono:
            flash("Por favor complete todos los campos obligatorios.", "danger")
            usuario.update(form)
            return render_template("perfil/editar_perfil.html", usuario=usuario, todas_asignaturas=todas_asignaturas)

        actualizar_perfil(usuario_id, nombre, apellido, correo, telefono, contrasena)

        if rol == "docente":
            profesion = form.get('profesion')
            actualizar_docente(usuario_id, profesion)

            docente_id = obtener_id_docente(usuario_id)
            asignaturas_seleccionadas = [int(a) for a in request.form.getlist('asignaturas[]')]
            actualizar_asignaturas_docente(docente_id, asignaturas_seleccionadas)

        elif rol == "estudiante":
            fecha_nacimiento = form.get('fecha_nacimiento')
            actualizar_estudiante(usuario_id, None, fecha_nacimiento)

        elif rol == "acudiente":
            ocupacion = form.get('ocupacion')
            actualizar_acudiente(usuario_id, ocupacion)

        flash("Perfil actualizado correctamente ✅", "success")
        return redirect(url_for("perfil.ver_perfil"))

    return render_template("perfil/editar_perfil.html", usuario=usuario, todas_asignaturas=todas_asignaturas)
