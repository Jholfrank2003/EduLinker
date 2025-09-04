# 🎓 EduLinker
**Sistema de Gestión de Citas Escolares**  
Proyecto de certificación – SENA  

EduLinker es una aplicación web desarrollada en **Flask + MySQL**, que permite gestionar la disponibilidad de los docentes y la solicitud de citas por parte de acudientes y estudiantes.  

---

## 🚀 Tecnologías utilizadas
- Python 3.x
- Flask
- MySQL
- Jinja2
- Bootstrap 5
- Flask-Login
- Werkzeug Security (hash de contraseñas)

---

## ⚙️ Instalación y configuración

### 1. Clonar el repositorio
```bash
git clone https://github.com/Jholfrank2003/EduLinker.git
cd EduLinker
```

### 2. Crear entorno virtual
```bash
python -m venv venv
```

### 3. Activar el entorno
- **Windows**
```bash
venv\Scripts\activate
```
- **Linux / macOS**
```bash
source venv/bin/activate
```

### 4. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 5. Configurar variables de entorno
Crea un archivo **`.env`** en la raíz del proyecto con tus credenciales locales:

```
FLASK_ENV=development
SECRET_KEY=una_clave_segura
MYSQL_USER=tu_usuario
MYSQL_PASSWORD=tu_contraseña
MYSQL_DB=edulinker
MYSQL_HOST=localhost
```

> ⚠️ Este archivo **no se sube a GitHub** por seguridad.

### 6. Configurar base de datos
1. Crear la base de datos en MySQL:
   ```sql
   CREATE DATABASE edulinker;
   ```
2. Importar el script SQL de las tablas (incluido en `/database/` si lo tienes preparado).

---

## ▶️ Ejecutar el proyecto
Con el entorno virtual activo:

```bash
flask run
```

La aplicación estará disponible en:  
👉 [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 📌 Funcionalidades principales
- Registro de usuarios dinámico (acudiente, estudiante, docente, admin).
- Login seguro con **Flask-Login** y contraseñas cifradas.
- Gestión de disponibilidad de docentes (bloques y slots).
- Solicitud de citas por acudientes/estudiantes.
- Aprobación/rechazo de citas por docentes.

---

## 👤 Autor
**Jholfrank Rojano**  
Técnico / Tecnólogo en ADSO – SENA  

---

## 📄 Licencia
Este proyecto se distribuye bajo la licencia **MIT**.  
Puedes usarlo y modificarlo libremente, siempre dando el crédito correspondiente.
