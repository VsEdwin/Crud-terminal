import mysql.connector as db

config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'port': '3306',
    'database': 'crud_usuarios',
    'raise_on_warnings': True
}

try:
    conexion = db.connect(**config)
    print("Conexion exitosa")

except Exception as error:
    print(f"Error de conexion: {error}")