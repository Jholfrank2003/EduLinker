# from app import mysql

# def crear_disponibilidades_iniciales(docente_id):
#     dias = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes']
#     cur = mysql.connection.cursor()
#     for dia in dias:
#         cur.execute("""
#             INSERT INTO disponibilidad (docente_id, dia, hora_inicio, hora_fin, estado)
#             VALUES (%s, %s, %s, %s, %s)
#         """, (docente_id, dia, "07:00:00", "09:00:00", 'disponible'))
#     mysql.connection.commit()
#     cur.close()


# def obtener_disponibilidad_por_docente(docente_id):
#     """
#     Devuelve todas las disponibilidades de un docente (para mostrarlas en FullCalendar).
#     """
#     cur = mysql.connection.cursor()
#     cur.execute("""
#         SELECT id, dia, hora_inicio, hora_fin, estado
#         FROM disponibilidad
#         WHERE docente_id = %s
#     """, (docente_id,))
#     disponibilidades = cur.fetchall()
#     cur.close()
#     return disponibilidades


# def actualizar_disponibilidad(disponibilidad_id, dia, hora_inicio, hora_fin, estado):
#     """
#     Permite al docente actualizar un bloque de disponibilidad.
#     """
#     cur = mysql.connection.cursor()
#     cur.execute("""
#         UPDATE disponibilidad
#         SET dia = %s, hora_inicio = %s, hora_fin = %s, estado = %s
#         WHERE id = %s
#     """, (dia, hora_inicio, hora_fin, estado, disponibilidad_id))
#     mysql.connection.commit()
#     cur.close()
