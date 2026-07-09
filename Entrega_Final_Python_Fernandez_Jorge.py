import sqlite3

conexion = sqlite3.connect("inventario.db")
cursor = conexion.cursor()
crear_tabla = """
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
    nombre = input("Ingresa el nombre del producto : ")
    descripcion = input("Ingresa a la descripción del producto : ")
    cantidad = int(input("Ingresar a la cantidad de productos : "))
    precio = float(input("Ingresa el precio del producto : "))
    categoria = input("Ingresa la categoría del producto : ")

    insertar = "INSERT INTO productos (nombre, descripcion,cantidad,precio,categoria) VALUES (?,?,?,?,?);"

    cursor.execute(insertar, (nombre, descripcion, cantidad, precio, categoria))

    conexion.commit()


def listar_productos():
    """Listado de productos"""
    print("Listado de productos")
    sql = "SELECT * FROM productos;"
    cursor.execute(sql)
    productos = cursor.fetchall()
    for prod in productos:
        print(
            f"ID : {prod[0]:<2} | NOMBRE : {prod[1]:<10} | DESCRIPCION : {prod[2]:<15} | CANTIDAD : {prod[3]:<2} | PRECIO : {prod[4]:<6} | CATEGORIA :{prod[5]}"
        )
    return productos


def actualizar_productos(id):
    """Actualiza producto por ID"""
    print("Actualización de producto")
    nuevo_precio = float(input("ingresa el nuevo precio : "))
    nueva_cantidad = int(input("ingresa la nueva cantidad : "))
    sql = """UPDATE productos SET cantidad=?, precio=? WHERE id=?"""
    cursor.execute(sql, (nueva_cantidad, nuevo_precio, id))
    conexion.commit()
    if cursor.rowcount==0:
        print("No se modifico ningun registro porque no existe")
    else:
        print("El producto fue modificado con exito")


def eliminar_producto(id):
    """Eliminacion de producto por id"""
    sql = """DELETE FROM productos WHERE id=?;"""
    respuesta = input("¿Está seguro que desea eliminar el producto si/no? : ")
    if respuesta == "si":
        cursor.execute(sql, (id,))
        cantidad_borrada = cursor.rowcount
        conexion.commit()
        if cantidad_borrada == 0:
            print("No se encontró ningún registro para borrar")
        else:
            print("El registro seleccionado fue borrado.")
    else:
        print("se canceló la eliminación del producto")


def buscar_producto(id):
    sql = """SELECT * FROM productos WHERE id = ?;"""
    cursor.execute(sql, (id,))
    resultado = cursor.fetchone()
    if resultado == None:
        print("no se encontró ningún registro")
    else:
        print("producto encontrado")
        print(
            f"ID : {resultado[0]:<2} | NOMBRE : {resultado[1]:<10} | DESCRIPCION : {resultado[2]:<15} | CANTIDAD : {resultado[3]:<2} | PRECIO : {resultado[4]:<6} | CATEGORIA :{resultado[5]}"
        )


def buscar_extendido(campo, valor):
    sql = f"""
    SELECT id, nombre,descripcion,cantidad, precio,categoria
        FROM productos 
        WHERE {campo} LIKE '%' || ? || '%' ;
    """

    cursor.execute(sql, (valor,))
    resultado = cursor.fetchall()
    if resultado == []:
        print("no se encontró ningún registro")
    else:
        print("producto encontrado")
        for fila in resultado:
            print(
                f"ID : {fila[0]:<2} | NOMBRE : {fila[1]:<10} | DESCRIPCION : {fila[2]:<15} | CANTIDAD : {fila[3]:<2} | PRECIO : {fila[4]:<6} | CATEGORIA :{fila[5]}"
            )

def reporte_stock_bajo(limite):
    sql="""SELECT * FROM productos WHERE cantidad <= ?"""
    cursor.execute(sql,(limite,))
    resultado = cursor.fetchall()
    if resultado == []:
        print("no se encontró ningún registro")
    else:
        print("producto encontrado")
        for fila in resultado:
            print(
                f"ID : {fila[0]:<2} | NOMBRE : {fila[1]:<10} | DESCRIPCION : {fila[2]:<15} | CANTIDAD : {fila[3]:<2} | PRECIO : {fila[4]:<6} | CATEGORIA :{fila[5]}"
            )

def menu():
    while True:
        print("Menú de opciones")
        print("1-Crear producto")
        print("2-Listar productos")
        print("3-Actualizar productos")
        print("4-Eliminar producto")
        print("5-Buscar producto")
        print("6-Buscar extendido")
        print("7-Revisar stock bajo")
        print("8-Salir")

        opcion=input("Ingrese una opcion valida entre 1-8 : ")
        if opcion =="1":
            crear_producto()            
        elif opcion =="2":
            listar_productos()
        elif opcion =="3":
            listar_productos()
            try:
                id=int(input("Ingresa el ID del producto que deseas actualizar : "))
                actualizar_productos(id)
            except ValueError:
                print("Error ")
        elif opcion =="4":
            listar_productos()
            try:
                id=int(input("Ingresa el ID del producto que deseas eliminar : "))
                eliminar_producto(id)
            except ValueError:
                print("Error ")
        elif opcion =="5":
            try:
                id=int(input("Ingresa el ID del producto que deseas buscar : "))
                buscar_producto(id)
            except ValueError:
                print("Error ")
        elif opcion =="6":
          
            campo=input("Ingresa el campo por el cual quieres buscar : ")
            valor=input("Ingresa el texto o numero a buscar : ")
            buscar_extendido(campo,valor)
           
        elif opcion =="7":
            try:
                limite=int(input("Ingresa el limite del stock que quieres buscar : "))
                reporte_stock_bajo(limite)
            except ValueError:
                print("Error")
        elif opcion =="8":
            print("Fin del programa ")
            conexion.close()
            break

        else:
            print("opcion no disponible")
menu()