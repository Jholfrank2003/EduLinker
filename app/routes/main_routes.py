from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app import mysql

main_bp = Blueprint('main', __name__)

# Ruta raíz -> siempre redirige al login
@main_bp.route('/')
def index():
    return redirect(url_for("auth.login"))

# Ruta protegida -> solo accesible si está logueado
@main_bp.route('/home')
@login_required
def home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT DATABASE()")
    db_name = cur.fetchone()
    cur.close()

    return render_template("home.html", db=db_name["DATABASE()"])
