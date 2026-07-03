import sqlite3
conexion = sqlite3.connect("inventario.db")
cursor=conexion.cursor()
crear_tabla="""
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    descripcion TEXT ,
    cantidad INTEGER NOT NULL,
    precio REAL NOT NULL,
    categoria TEXT 
);
"""
cursor.execute(crear_tabla)
print("Tabla creada o ya existe")

conexion.commit()
conexion.close()
