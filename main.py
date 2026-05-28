#Importacion de la conexion creada en conexion.py para usarla
from conexion import conexion
#Permite trabajar con archivos json, crear carpetas, manejar fechas y horas
import json
#Permite trabajar con carpetas y archivos del sistema operativo
import os
#Permite trabajar con fechas y horas para generar logs
from datetime import datetime

#Para ejecutar consultas a la base de datos, se crea un cursor a partir de la conexion
cursor = conexion.cursor()

# =========================
# CREAR CARPETAS
# =========================
#Se crean las carpetas de Logs y Backups en caso de que no existan, se crean 
os.makedirs("logs", exist_ok=True)
os.makedirs("backups", exist_ok=True)

# =========================
# FUNCION LOG
# =========================

#Funcion para poder generar logs de las acciones realizadas en el sistema, se guarda con un mensaje y fecha y hora en un archivo de texto dentro de la carpeta logs
def generar_log(mensaje):

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # =========================
    # LOG TXT
    # =========================

    with open("logs/historial.log", "a", encoding="utf-8") as archivo:

        archivo.write(f"[{fecha}] {mensaje}\n")

    # =========================
    # HISTORIAL MYSQL
    # =========================

    query = """
    INSERT INTO t_historial_sistema(accion, fecha)
    VALUES(%s,%s)
    """

    valores = (mensaje, fecha)

    cursor.execute(query, valores)

    conexion.commit()

# =========================
# CREATE
# =========================
#Funcion para agregar a un nuevo usuario, pidiendo los datos por la terminal
def agregar_usuario():

    print("\n=== AGREGAR USUARIO ===")

    #Datos para insertar en la base de datos
    nombre = input("Nombre: ")
    correo = input("Correo: ")
    edad = input("Edad: ")
    telefono = input("Telefono: ")

    # =========================
    # VALIDACIONES
    # =========================

    if nombre.strip() == "":
        print("El nombre no puede estar vacio")
        return

    if "@" not in correo:
        print("Correo invalido")
        return

    if not edad.isdigit():
        print("La edad debe ser numerica")
        return

    if not telefono.isdigit():
        print("El telefono debe contener solo numeros")
        return

    #Inserccion de los datos del nuevo usuario a la base de datos
    query = """
    INSERT INTO t_usuarios(nombre, correo, edad, telefono)
    VALUES(%s,%s,%s,%s)
    """
    #tupla con los valores a insertar en la base de datos
    valores = (nombre, correo, edad, telefono)

    #Ejecuta la consulta con los valores y guarda los cambios en la base de datos
    cursor.execute(query, valores)
    conexion.commit()

    #Se genera un log con el mensaje del nuevo usuario agregfado
    generar_log(f"Usuario agregado: {nombre}")

    #Imprime el mensaje de que el usuario se agrego correctamente
    print("Usuario agregado correctamente")

# =========================
# READ
# =========================
#Funcion para leer los usuarios registrados en la base de datos
def mostrar_usuarios():

    print("\n=== LISTA DE USUARIOS ===")

    #Conuslta para obtener los usuario registrados en la base de datos
    query = "SELECT * FROM t_usuarios"

    #Ejecuta la consulta y obtiene los datos
    cursor.execute(query)

    #obtuiene los datos de la consulta y lo guarda
    datos = cursor.fetchall()

    #En caso de que no haya usuarios registrados, se muestra el mensaje de que no hay registro
    if len(datos) == 0:
        print("No hay usuarios")
        return

    #Recorre cada registro de usuario obtenido de la consulta
    for usuario in datos:

        print(f"""
            ID: {usuario[0]}
            Nombre: {usuario[1]}
            Correo: {usuario[2]}
            Edad: {usuario[3]}
            Telefono: {usuario[4]}
        """)

    #Genera el log de la consulta realizada para mostrar los usuarios registrados
    generar_log("Consulta de usuarios")

# =========================
# UPDATE
# =========================

#Funcion para poder actualizar los datos de un usuario seleccionado por el ID
def actualizar_usuario():

    #Muestra el mensaje de que se va a actualizar el usuario
    print("\n=== ACTUALIZAR USUARIO ===")

    #Pide el ID del usuario que se desea actualizar
    id_usuario = input("ID del usuario: ")

    #Datos nuevos para actualizar el usuario seleccionado
    nombre = input("Nuevo nombre: ")
    correo = input("Nuevo correo: ")
    edad = input("Nueva edad: ")
    telefono = input("Nuevo telefono: ")
    
    # =========================
    # VALIDACIONES
    # =========================

    if nombre.strip() == "":
        print("El nombre no puede estar vacio")
        return

    if "@" not in correo:
        print("Correo invalido")
        return

    if not edad.isdigit():
        print("La edad debe ser numerica")
        return

    if not telefono.isdigit():
        print("El telefono debe contener solo numeros")
        return

    #Modifica el registro del usuario seleccionado por el ID, Where indica que solo el usario con el Id se va a actulizar
    query = """
    UPDATE t_usuarios
    SET nombre=%s, correo=%s, edad=%s, telefono=%s
    WHERE id=%s
    """

    #tupla con los nuevos datos actualizados
    valores = (nombre, correo, edad, telefono, id_usuario)

    #
    cursor.execute(query, valores)

    #Guarda los cambios realizados
    conexion.commit()

    #Genera el log con el mensaje del usuairo actuazlizado
    generar_log(f"Usuario actualizado ID: {id_usuario}")

    print("Usuario actualizado")

# =========================
# DELETE
# =========================

#Funcion para eliminar un usuario seleccionado por el ID
def eliminar_usuario():

    #Muestra el mensaje de que se va a eliminar el usuario
    print("\n=== ELIMINAR USUARIO ===")

    #Pide el ID del usuario que se desea eliminar
    id_usuario = input("ID del usuario: ")

    #Elimina el registro del usuario seleccionado por el ID
    query = "DELETE FROM t_usuarios WHERE id=%s"

    #tupla con el id del usuario a eliminar
    valores = (id_usuario,)

    #Realiza la eliminacion del usuario seleccionado por el ID
    cursor.execute(query, valores)

    #Guarda los cambios realizados
    conexion.commit()

    #Genera el log cin el mensaje del usuario eliminado
    generar_log(f"Usuario eliminado ID: {id_usuario}")

    print("Usuario eliminado")

# =========================
# VER HISTORIAL
# =========================

#Funcion para mostrar el historial de acciones realizadas en el sistema, se lee el archivo de texto donde se guardan los logs y se muestra su contenido
def ver_historial():

    print("\n=== HISTORIAL ===")

    #Se intenta abrir el archivo de texto donde se guardan los logs, si el archivo no existe o hay un error al abrirlo, se muestra un mensaje de error
    try:

        #Abre el archivo de texto en modo lectura y con codificacion utf-8 para mostrar los logs guardados
        archivo = open("logs/historial.log", "r", encoding="utf-8")

        #Lee el contenido del archivo y lo guarda en la variable contenido
        contenido = archivo.read()

        #Muestra el contenido del archivo de texto con los logs guardados
        print(contenido)

    #En caso de que haya un error al abrir el archivo o leerlo, se muestra un mensaje de error con el contenido del error
    except Exception as error:

        print(f"Error: {error}")

    #En caso de que el archivo se abra correctamente, se cierra el archivo para liberar recursos del sistema
    finally:

        archivo.close()

# =========================
# RESPALDO JSON
# =========================

#Funcion para generar un respaldo de los usuarios registrados en la base de datos, se obtiene la informacion de los usuarios y se guarda en un archivo json dentro de la carpeta backups
def generar_respaldo():

    print("\n=== GENERANDO RESPALDO ===")

    #Consulta para obtener los usuarios registrados en la base de datos
    query = "SELECT * FROM t_usuarios"

    cursor.execute(query)

    #Obtiene los datos de la consulta y lo guarda en la variable datos
    datos = cursor.fetchall()

    #En caso de que no haya usuarios registrados, se muestra el mensaje de que no hay registro y no se genera el respaldo
    usuarios = []

    #Recorre cada registro de usuario obtenido de la consulta y lo guarda en una lista de diccionarios con los campos id, nombre, correo, edad y telefono
    for usuario in datos:

        usuarios.append({
            "id": usuario[0],
            "nombre": usuario[1],
            "correo": usuario[2],
            "edad": usuario[3],
            "telefono": usuario[4]
        })

    #Respalda la lista de usuarios en un archivo json dentro de la carpeta backups, se guarda con una identacion de 4 espacios y con codificacion utf-8 para que se muestren los caracteres especiales correctamente
    with open("backups/respaldo.json", "w", encoding="utf-8") as archivo:

        #EL metodo dump de la libreria json se encarga de convertir la lista de usuarios en formato json y guardarlo en el archivo especificado
        json.dump(usuarios, archivo, indent=4, ensure_ascii=False)

    #Genera el log con el mensaje de que se genero el respaldo json
    generar_log("Respaldo JSON generado")

    print("Respaldo creado correctamente")

# =========================
# RESTAURAR RESPALDO
# =========================

#Funcion para restaurar el respaldo de los usuarios registrados en la base de datos, se lee el archivo json donde se guardo el respaldo y se insertan los datos en la base de datos, antes de insertar los datos se borra la tabla para evitar duplicados
def restaurar_respaldo():

    print("\n=== RESTAURAR RESPALDO ===")

    #Se intenta abrir el archivo json donde se guardo el respaldo, si el archivo no existe o hay un error al abrirlo, se muestra un mensaje de error
    try:

        #Abre el archivo json en modo lectura y con codificacion utf-8 para leer el respaldo guardado
        with open("backups/respaldo.json", "r", encoding="utf-8") as archivo:

            usuarios = json.load(archivo)

        # borrar tabla
        cursor.execute("DELETE FROM t_usuarios")

        #Recorre cada usuario obtenido del archivo json y lo inserta en la base de datos, se utiliza una consulta de inserccion con los campos id, nombre, correo, edad y telefono para insertar los datos de cada usuario en la tabla usuarios
        for usuario in usuarios:

            query = """
            INSERT INTO t_usuarios(id,nombre,correo,edad,telefono)
            VALUES(%s,%s,%s,%s,%s)
            """

            #tupla con los valores a insertar en la base de datos, se obtiene el id, nombre, correo, edad y telefono de cada usuario del archivo json para insertarlo en la tabla usuarios
            valores = (
                usuario["id"],
                usuario["nombre"],
                usuario["correo"],
                usuario["edad"],
                usuario["telefono"]
            )

            #Ejecuta la consulta con los valores y guarda los cambios en la base de datos para cada usuario del archivo json
            cursor.execute(query, valores)

        conexion.commit()

        #Genera el log con el mensaje de que se restauro el respaldo json
        generar_log("Base de datos restaurada")

        print("Respaldo restaurado correctamente")
        
    #En caso de que haya un error al abrir el archivo o leerlo, se muestra un mensaje de error con el contenido del error
    except Exception as error:

        print(f"Error: {error}")

# =========================
# TRUNCAR TABLA
# =========================

#Funcion para vaciar completamente la tabla usuarios
def truncar_tabla():

    print("\n=== TRUNCAR TABLA USUARIOS ===")

    confirmacion = input("¿Seguro que deseas eliminar TODOS los registros? (si/no): ")

    if confirmacion.lower() == "si":

        query = "TRUNCATE TABLE t_usuarios"

        cursor.execute(query)

        conexion.commit()

        generar_log("Tabla usuarios truncada")

        print("Tabla vaciada correctamente")

    else:

        print("Operacion cancelada")
# =========================
# MENU
# =========================

#Funcion para mostrar el menu de opciones del sistema, se muestra un menu con las opciones disponibles para realizar las operaciones CRUD, ver el historial, generar un respaldo json, restaurar un respaldo json o salir del sistema, se utiliza un ciclo while para mostrar el menu de forma continua hasta que el usuario seleccione la opcion de salir
def menu():

    #Ciclo while para mostrar el menu de forma continua hasta que el usuario seleccione la opcion de salir
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
8. Truncar tabla usuarios
9. Salir

===============================
""")

        #Pide al usuario que seleccione una opcion del menu para realizar la operacion correspondiente, se guarda la opcion seleccionada en la variable opcion
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

            truncar_tabla()

        elif opcion == "9":

            generar_log("Salida del sistema")
            print("Adios")
            break

        else:
            print("Opcion invalida")

# =========================
# INICIO
# =========================
#se genera un log con el mensaje de que se inicio el sistema
#Se inicia el menu para mostrar las opciones disponibles para realizar las operaciones CRUD, ver el historial, generar un respaldo json, restaurar un respaldo json o salir del sistema
menu()