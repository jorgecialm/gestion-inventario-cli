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


def crear_producto():
    """Registrar productos"""
    nombre=input("Ingresa el nombre del producto : ")
    descripcion= input("Ingresa a la descripción del producto : ")
    cantidad=int(input("Ingresar a la cantidad de productos : "))
    precio = float(input("Ingresa el precio del producto : "))
    categoria =input("Ingresa la categoría del producto : ")

    insertar="INSERT INTO productos (nombre, descripcion,cantidad,precio,categoria) VALUES (?,?,?,?,?);"

    cursor.execute(insertar,(nombre,descripcion,cantidad,precio,categoria))

    conexion.commit()
    

def listar_productos():
    """Listado de productos"""
    print("Listado de productos")
    sql="SELECT * FROM productos;"
    cursor.execute(sql)
    productos=cursor.fetchall()
    for prod in productos:
        print(f"ID : {prod[0]} | NOMBRE : {prod[1]} | DESCRIPCION : {prod[2]} | CANTIDAD : {prod[3]} | PRECIO : {prod[4]} | CATEGORIA :{prod[5]}")
    return productos


def actualizar_productos(id):
    """Actualiza producto por ID"""
    print("Actualización de producto")
    listar_productos()
    nuevo_precio=float(input("ingresa el nuevo precio : "))
    nueva_cantidad=int(input("ingresa la nueva cantidad : "))
    sql="""UPDATE productos SET cantidad=?, precio=? WHERE id=?"""
    cursor.execute(sql,(nueva_cantidad,nuevo_precio,id))
    conexion.commit()

