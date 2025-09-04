from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from app.models.auth_model import User, get_user_by_email

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    if request.method == "POST":
        correo = request.form["correo"].strip().lower()
        contrasena = request.form["contrasena"]
        remember = "remember" in request.form  

        user = get_user_by_email(correo) 

        if user and check_password_hash(user.contrasena, contrasena):
            if hasattr(user, "estado") and user.estado != "activo":
                flash("Tu cuenta está inactiva. Contacta con soporte.", "warning")
                return redirect(url_for("auth.login"))

            login_user(user, remember=remember)
            flash("Inicio de sesión exitoso", "success")

            next_page = request.args.get("next")
            if next_page and next_page.startswith("/"):
                return redirect(next_page)
            return redirect(url_for("main.home"))

        else:
            flash("Correo o contraseña incorrectos", "danger")

    return render_template("login.html")



@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada correctamente", "info")
    return redirect(url_for("auth.login"))
