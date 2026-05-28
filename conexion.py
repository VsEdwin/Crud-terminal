#Conexion a la base de datos
#Importacion de la libreria mysql.connector para conectar python con mysql
import mysql.connector as db
from mysql.connector import pooling

#Configuracion de la conexion a la base de datos
config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'port': '3306',
    'database': 'crud_usuarios',
    'raise_on_warnings': True
}

#Try para conectar a la base de datos y manejar errores en caso de que la conexion falle
try:
    pool = pooling.MySQLConnectionPool(pool_name="mypool", pool_size=5, **config)
    conexion = pool.get_connection()
    # conexion = db.connect(**config)
    print("Conexion exitosa")
    
#Except para manejar errores de conexion y mostrar un mensaje de error en caso de que la conexion falle
except Exception as error:
    print(f"Error de conexion: {error}")