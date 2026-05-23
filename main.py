from conexion import conexion
import json
import os
from datetime import datetime

cursor = conexion.cursor()

# =========================
# CREAR CARPETAS
# =========================

os.makedirs("logs", exist_ok=True)
os.makedirs("backups", exist_ok=True)

# =========================
# FUNCION LOG
# =========================

def generar_log(mensaje):

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("logs/historial.log", "a", encoding="utf-8") as archivo:
        archivo.write(f"[{fecha}] {mensaje}\n")

# =========================
# CREATE
# =========================

def agregar_usuario():

    print("\n=== AGREGAR USUARIO ===")

    nombre = input("Nombre: ")
    correo = input("Correo: ")
    edad = input("Edad: ")
    telefono = input("Telefono: ")

    query = """
    INSERT INTO usuarios(nombre, correo, edad, telefono)
    VALUES(%s,%s,%s,%s)
    """

    valores = (nombre, correo, edad, telefono)

    cursor.execute(query, valores)
    conexion.commit()

    generar_log(f"Usuario agregado: {nombre}")

    print("Usuario agregado correctamente")

# =========================
# READ
# =========================

def mostrar_usuarios():

    print("\n=== LISTA DE USUARIOS ===")

    query = "SELECT * FROM usuarios"

    cursor.execute(query)

    datos = cursor.fetchall()

    if len(datos) == 0:
        print("No hay usuarios")
        return

    for usuario in datos:

        print(f"""
ID: {usuario[0]}
Nombre: {usuario[1]}
Correo: {usuario[2]}
Edad: {usuario[3]}
Telefono: {usuario[4]}
        """)

    generar_log("Consulta de usuarios")

# =========================
# UPDATE
# =========================

def actualizar_usuario():

    print("\n=== ACTUALIZAR USUARIO ===")

    id_usuario = input("ID del usuario: ")

    nombre = input("Nuevo nombre: ")
    correo = input("Nuevo correo: ")
    edad = input("Nueva edad: ")
    telefono = input("Nuevo telefono: ")

    query = """
    UPDATE usuarios
    SET nombre=%s, correo=%s, edad=%s, telefono=%s
    WHERE id=%s
    """

    valores = (nombre, correo, edad, telefono, id_usuario)

    cursor.execute(query, valores)

    conexion.commit()

    generar_log(f"Usuario actualizado ID: {id_usuario}")

    print("Usuario actualizado")

# =========================
# DELETE
# =========================

def eliminar_usuario():

    print("\n=== ELIMINAR USUARIO ===")

    id_usuario = input("ID del usuario: ")

    query = "DELETE FROM usuarios WHERE id=%s"

    valores = (id_usuario,)

    cursor.execute(query, valores)

    conexion.commit()

    generar_log(f"Usuario eliminado ID: {id_usuario}")

    print("Usuario eliminado")

# =========================
# VER HISTORIAL
# =========================

def ver_historial():

    print("\n=== HISTORIAL ===")

    try:

        archivo = open("logs/historial.log", "r", encoding="utf-8")

        contenido = archivo.read()

        print(contenido)

    except Exception as error:

        print(f"Error: {error}")

    finally:

        archivo.close()

# =========================
# RESPALDO JSON
# =========================

def generar_respaldo():

    print("\n=== GENERANDO RESPALDO ===")

    query = "SELECT * FROM usuarios"

    cursor.execute(query)

    datos = cursor.fetchall()

    usuarios = []

    for usuario in datos:

        usuarios.append({
            "id": usuario[0],
            "nombre": usuario[1],
            "correo": usuario[2],
            "edad": usuario[3],
            "telefono": usuario[4]
        })

    with open("backups/respaldo.json", "w", encoding="utf-8") as archivo:

        json.dump(usuarios, archivo, indent=4, ensure_ascii=False)

    generar_log("Respaldo JSON generado")

    print("Respaldo creado correctamente")

# =========================
# RESTAURAR RESPALDO
# =========================

def restaurar_respaldo():

    print("\n=== RESTAURAR RESPALDO ===")

    try:

        with open("backups/respaldo.json", "r", encoding="utf-8") as archivo:

            usuarios = json.load(archivo)

        # borrar tabla
        cursor.execute("DELETE FROM usuarios")

        for usuario in usuarios:

            query = """
            INSERT INTO usuarios(id,nombre,correo,edad,telefono)
            VALUES(%s,%s,%s,%s,%s)
            """

            valores = (
                usuario["id"],
                usuario["nombre"],
                usuario["correo"],
                usuario["edad"],
                usuario["telefono"]
            )

            cursor.execute(query, valores)

        conexion.commit()

        generar_log("Base de datos restaurada")

        print("Respaldo restaurado correctamente")

    except Exception as error:

        print(f"Error: {error}")

# =========================
# MENU
# =========================

def menu():

    while True:

        print("""
======== CRUD USUARIOS ========

1. Agregar usuario
2. Mostrar usuarios
3. Actualizar usuario
4. Eliminar usuario
5. Ver historial
6. Generar respaldo JSON
7. Restaurar respaldo JSON
8. Salir

===============================
        """)

        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            agregar_usuario()

        elif opcion == "2":
            mostrar_usuarios()

        elif opcion == "3":
            actualizar_usuario()

        elif opcion == "4":
            eliminar_usuario()

        elif opcion == "5":
            ver_historial()

        elif opcion == "6":
            generar_respaldo()

        elif opcion == "7":
            restaurar_respaldo()

        elif opcion == "8":

            generar_log("Sistema cerrado")

            print("Adios")
            break

        else:
            print("Opcion invalida")

# =========================
# INICIO
# =========================

menu()