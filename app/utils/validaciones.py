import re

# ---------------- Expresiones Regulares ----------------
solo_letras = re.compile(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$')
solo_numeros = re.compile(r'^\d{7,15}$')
solo_correo = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')

# ---------------- Validar Usuario General ----------------
def validar_usuario(nombre, apellido, correo, telefono, contrasena):
    if not nombre or not solo_letras.match(nombre):
        return False, "El nombre solo puede contener letras."
    if not apellido or not solo_letras.match(apellido):
        return False, "El apellido solo puede contener letras."
    if not correo or not solo_correo.match(correo):
        return False, "Ingrese un correo válido."
    if not telefono or not solo_numeros.match(telefono):
        return False, "El teléfono debe tener entre 7 y 15 dígitos numéricos."
    if not contrasena or len(contrasena) < 6:
        return False, "La contraseña debe tener mínimo 6 caracteres."
    return True, None

# ---------------- Validar Estudiante ----------------
def validar_estudiante(grado_id, fecha_nacimiento):
    if not grado_id:
        return False, "Debe seleccionar un grado."
    if not fecha_nacimiento:
        return False, "Debe ingresar la fecha de nacimiento."
    return True, None

# ---------------- Validar Acudiente ----------------
def validar_acudiente(ocupacion):
    if not ocupacion or not solo_letras.match(ocupacion):
        return False, "La ocupación solo puede contener letras."
    return True, None

# ---------------- Validar Docente ----------------
def validar_docente(profesion, asignaturas):
    if not profesion or not solo_letras.match(profesion):
        return False, "La profesión solo puede contener letras."
    if not asignaturas or not any(asignaturas):
        return False, "Debe seleccionar al menos una asignatura."
    return True, None

# ---------------- Validar Administrador ----------------
def validar_admin_form(nombre, apellido, correo, telefono, password=None):
    if not nombre or not solo_letras.match(nombre):
        return False, "El nombre solo puede contener letras."
    if not apellido or not solo_letras.match(apellido):
        return False, "El apellido solo puede contener letras."
    if not correo or not solo_correo.match(correo):
        return False, "Ingrese un correo válido."
    if not telefono or not solo_numeros.match(telefono):
        return False, "El teléfono debe tener entre 7 y 15 dígitos numéricos."
    if password and len(password) < 6:
        return False, "La contraseña debe tener mínimo 6 caracteres."
    return True, None

def validar_estudiante(nombre, apellido, correo, telefono, grado_id, fecha_nacimiento, contrasena=None):
    if not nombre or not solo_letras.match(nombre):
        return False, "El nombre solo puede contener letras."
    if not apellido or not solo_letras.match(apellido):
        return False, "El apellido solo puede contener letras."
    if not correo or not solo_correo.match(correo):
        return False, "Ingrese un correo válido."
    if not telefono or not solo_numeros.match(telefono):
        return False, "El teléfono debe tener entre 7 y 15 dígitos numéricos."
    if not grado_id:
        return False, "Debe seleccionar un grado."
    if not fecha_nacimiento:
        return False, "Debe ingresar la fecha de nacimiento."
    if contrasena and len(contrasena) < 6:
        return False, "La contraseña debe tener mínimo 6 caracteres."
    return True, None

def validar_acudiente(nombre, apellido, correo, telefono, ocupacion, contrasena=None):
    if not nombre or not solo_letras.match(nombre):
        return False, "El nombre solo puede contener letras."
    if not apellido or not solo_letras.match(apellido):
        return False, "El apellido solo puede contener letras."
    if not correo or not solo_correo.match(correo):
        return False, "Ingrese un correo válido."
    if not telefono or not solo_numeros.match(telefono):
        return False, "El teléfono debe tener entre 7 y 15 dígitos numéricos."
    if not ocupacion or not solo_letras.match(ocupacion):
        return False, "La ocupación solo puede contener letras."
    if contrasena and len(contrasena) < 6:
        return False, "La contraseña debe tener mínimo 6 caracteres."
    return True, None

def validar_docente(nombre, apellido, correo, telefono, profesion, asignaturas, contrasena=None):
    if not nombre or not solo_letras.match(nombre):
        return False, "El nombre solo puede contener letras."
    if not apellido or not solo_letras.match(apellido):
        return False, "El apellido solo puede contener letras."
    if not correo or not solo_correo.match(correo):
        return False, "Ingrese un correo válido."
    if not telefono or not solo_numeros.match(telefono):
        return False, "El teléfono debe tener entre 7 y 15 dígitos numéricos."
    if not profesion or not solo_letras.match(profesion):
        return False, "La profesión solo puede contener letras."
    if not asignaturas or not any(asignaturas):
        return False, "Debe seleccionar al menos una asignatura."
    if contrasena and len(contrasena) < 6:
        return False, "La contraseña debe tener mínimo 6 caracteres."
    return True, None

def validar_rol(nombre, descripcion=None):
    if not nombre or not solo_letras.match(nombre):
        return False, "El nombre del rol solo puede contener letras."
    if not descripcion:
        return False, "La descripción es obligatoria."
    if not re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9\s.,;:()¡!¿?'-]*$", descripcion):
        return False, "La descripción contiene caracteres no permitidos."
    return True, None

def validar_asignatura(nombre):
    if not nombre or not solo_letras.match(nombre):
        return False, "El nombre de la asignatura solo puede contener letras."
    return True, None



