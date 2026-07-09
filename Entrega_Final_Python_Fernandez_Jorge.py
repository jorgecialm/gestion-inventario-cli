"""
Sistema de Gestión de Inventario

Trabajo Final - Curso de Python Talento Tech

Permite:
- Registrar productos.
- Listar productos.
- Actualizar información.
- Eliminar productos.
- Buscar por ID.
- Buscar por nombre o categoría.
- Generar un reporte de stock bajo.

Base de datos: SQLite
"""
# ==========================
# IMPORTACIÓN DE LIBRERÍAS
# ==========================

# Importación de librerías necesarias para el sistema,
# manejo de archivos, base de datos y colores en consola.
import os
import sqlite3
from colorama import Fore , init
init(autoreset=True)
# ==========================
# CONEXIÓN A LA BASE DE DATOS
# ========================

# Conexión con la base de datos SQLite y creación del cursor.
conexion = sqlite3.connect("inventario.db")
cursor = conexion.cursor()

# Crear la tabla de productos si todavía no existe.
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
print(f"{Fore.GREEN}Tabla creada o ya existe.\n")

conexion.commit()

# ==========================
# FUNCIONES DEL SISTEMA
# ==========================

# Limpia la consola para mantener una interfaz ordenada.
def limpiar_pantalla():
    """
    Limpia la consola según el sistema operativo utilizado.
    """
    if os.name == "nt":      # Windows
        os.system("cls")
    else:                    # Linux y macOS
        os.system("clear")

# Espera que el usuario presione Enter antes de volver al menú.
def pausar():
    """
    Pausa la ejecución hasta que el usuario presione Enter
    y luego limpia la pantalla.
    """
    input(f"{Fore.YELLOW}\nPresione Enter para continuar...")
    limpiar_pantalla()

def crear_producto():
    """
    Solicita los datos de un producto y lo registra
    en la base de datos.
    """
    nombre = input(f"{Fore.BLUE}Ingresa el nombre del producto : ")
    descripcion = input(f"{Fore.BLUE}Ingresa la descripción del producto : ")
    try:
        cantidad = int(input(f"{Fore.BLUE}Ingresar la cantidad de productos : "))
    except ValueError:
        print(f"{Fore.RED}Error : Debe ingresar un valor válido.")
        return 

    try:
        precio = float(input(f"{Fore.BLUE}Ingresa el precio del producto : "))
    except ValueError:
        print(f"{Fore.RED}Error : Debe ingresar un valor válido.")
        return

    categoria = input(f"{Fore.BLUE}Ingresa la categoría del producto : ")

    insertar = "INSERT INTO productos (nombre, descripcion,cantidad,precio,categoria) VALUES (?,?,?,?,?);"

    cursor.execute(insertar, (nombre, descripcion, cantidad, precio, categoria))

    conexion.commit()
    print(f"{Fore.GREEN}Producto registrado correctamente en el inventario.")

def listar_productos():
    """
    Obtiene y muestra todos los productos registrados
    en la base de datos.
    """
    print(f"{Fore.BLUE}\nListado de productos\n")
    sql = "SELECT * FROM productos;"
    cursor.execute(sql)
    productos = cursor.fetchall()
    for prod in productos:
        print(
            f"ID: {prod[0]:<2} | "
            f"NOMBRE: {prod[1]:<15} | "
            f"DESCRIPCIÓN: {prod[2]:<20} | "
            f"CANTIDAD: {prod[3]:<3} | "
            f"PRECIO: ${prod[4]:<10.2f} | "
            f"CATEGORÍA: {prod[5]}"
        )
    return productos


def actualizar_productos(id):
    """
    Actualiza el precio y la cantidad de un producto
    utilizando su ID.
    """
    print(f"{Fore.BLUE}Actualización de producto")
    nuevo_precio = float(input(f"{Fore.BLUE}Ingresa el nuevo precio : "))
    nueva_cantidad = int(input(f"{Fore.BLUE}Ingresa la nueva cantidad : "))
    sql = """UPDATE productos SET cantidad=?, precio=? WHERE id=?"""
    cursor.execute(sql, (nueva_cantidad, nuevo_precio, id))
    conexion.commit()
    if cursor.rowcount==0:
        print(f"{Fore.RED}No se modifico ningun registro porque no existe.")
    else:
        print(f"{Fore.GREEN}El producto fue modificado con éxito.")


def eliminar_producto(id):
    """
    Elimina un producto de la base de datos
    a partir de su ID.
    """
    sql = """DELETE FROM productos WHERE id=?;"""
    respuesta = input(f"{Fore.BLUE}¿Está seguro que desea eliminar el producto? (si/no) : ")
    if respuesta == "si":
        cursor.execute(sql, (id,))
        cantidad_borrada = cursor.rowcount
        conexion.commit()
        if cantidad_borrada == 0:
            print(f"{Fore.RED}No se encontró ningún registro para borrar.")
        else:
            print(f"{Fore.GREEN}El registro seleccionado fue borrado.")
    else:
        print(f"{Fore.YELLOW}Se canceló la eliminación del producto.")


def buscar_producto(id):
    """
    Busca un producto por su ID y muestra
    su información en pantalla.
    """
    sql = """SELECT * FROM productos WHERE id = ?;"""
    cursor.execute(sql, (id,))
    resultado = cursor.fetchone()
    if resultado == None:
        print(f"{Fore.RED}No se encontró ningún registro.")
    else:
        print(f"{Fore.GREEN}Producto encontrado.")
        print(
            f"ID: {resultado[0]:<2} | "
            f"NOMBRE: {resultado[1]:<15} | "
            f"DESCRIPCIÓN: {resultado[2]:<20} | "
            f"CANTIDAD: {resultado[3]:<3} | "
            f"PRECIO: ${resultado[4]:<10.2f} | "
            f"CATEGORÍA: {resultado[5]}"
        )


def buscar_extendido(campo, valor):
    """
    Busca productos por nombre o categoría
    utilizando una búsqueda parcial.
    """
    sql = f"""
    SELECT id, nombre,descripcion,cantidad, precio,categoria
        FROM productos 
        WHERE {campo} LIKE '%' || ? || '%' ;
    """

    cursor.execute(sql, (valor,))
    resultado = cursor.fetchall()

    if resultado == []:
        print(f"{Fore.RED}No se encontró ningún registro.")
    else:
        print(f"{Fore.GREEN}Producto encontrado.")
        for fila in resultado:
            print(
                f"ID: {fila[0]:<2} | "
                f"NOMBRE: {fila[1]:<15} | "
                f"DESCRIPCIÓN: {fila[2]:<20} | "
                f"CANTIDAD: {fila[3]:<3} | "
                f"PRECIO: ${fila[4]:<10.2f} | "
                f"CATEGORÍA: {fila[5]}"
            )

def reporte_stock_bajo(limite):
    """
    Muestra todos los productos cuyo stock
    sea menor o igual al límite indicado.
    """
    sql="""SELECT * FROM productos WHERE cantidad <= ?"""
    cursor.execute(sql,(limite,))
    resultado = cursor.fetchall()
    if resultado == []:
        print(f"{Fore.RED}No se encontró ningún registro.")
    else:
        print(f"{Fore.GREEN}Productos encontrados.")
        for fila in resultado:
            print(
            f"ID: {fila[0]:<2} | "
            f"NOMBRE: {fila[1]:<15} | "
            f"DESCRIPCIÓN: {fila[2]:<20} | "
            f"CANTIDAD: {fila[3]:<3} | "
            f"PRECIO: ${fila[4]:<10.2f} | "
            f"CATEGORÍA: {fila[5]}"
        )
# ==========================
# MENÚ PRINCIPAL
# ==========================
def menu():
    """
    Muestra el menú principal y permite al usuario
    interactuar con el sistema hasta seleccionar
    la opción de salida.
    """
    while True:
        limpiar_pantalla()
        print(f"{Fore.BLUE}\nMenú de opciones \n")
        print(f"{Fore.YELLOW}1- Crear producto")
        print(f"{Fore.YELLOW}2- Listar productos")
        print(f"{Fore.YELLOW}3- Actualizar productos")
        print(f"{Fore.YELLOW}4- Eliminar producto")
        print(f"{Fore.YELLOW}5- Buscar producto")
        print(f"{Fore.YELLOW}6- Buscar extendido")
        print(f"{Fore.YELLOW}7- Revisar stock bajo")
        print(f"{Fore.YELLOW}8- Salir\n")

        opcion=input(f"{Fore.BLUE}Ingrese una opcion válida entre 1-8 : ")
        if opcion =="1":
            limpiar_pantalla()
            crear_producto() 
            pausar()           
        elif opcion =="2":
            limpiar_pantalla()
            listar_productos()
            pausar()
        elif opcion =="3":
            limpiar_pantalla()
            listar_productos()
            try:
                id=int(input(f"{Fore.BLUE}\nIngresa el ID del producto que deseas actualizar : "))
                actualizar_productos(id)
            except ValueError:
                print(f"{Fore.RED}Error : Debe ingresar un valor válido.")
            pausar()
        elif opcion =="4":
            limpiar_pantalla()
            listar_productos()
            try:
                id=int(input(f"{Fore.BLUE}\nIngresa el ID del producto que deseas eliminar : "))
                eliminar_producto(id)
            except ValueError:
                print(f"{Fore.RED}Error : Debe ingresar un  valor válido.")
            pausar()
        elif opcion =="5":
            limpiar_pantalla()
            try:
                id=int(input(f"{Fore.BLUE}Ingresa el ID del producto que deseas buscar : "))
                buscar_producto(id)
            except ValueError:
                print(f"{Fore.RED}Error : Debe ingresar un  valor válido.")
            pausar()
        elif opcion =="6":
            campo = input(f"{Fore.BLUE}Ingresa el campo por el cual quieres buscar (nombre/categoría) : ").strip().lower()
            valor = input(f"{Fore.BLUE}Ingresa el nombre o la categoría que queres buscar: ")
            if campo not in ["nombre", "categoria"]:
                print(f"{Fore.RED}Error: El campo debe ser 'nombre' o 'categoría'.")
            elif valor.strip() == "":
                print(f"{Fore.RED}Error: No puede contener datos vacíos.")
            else:
                buscar_extendido(campo, valor)  
            pausar()
        elif opcion =="7":
            try:
                limite=int(input(f"{Fore.BLUE}Ingresa el limite del stock que quieres buscar : "))
                reporte_stock_bajo(limite)
                
            except ValueError:
                print(f"{Fore.RED}Error : Debe ingresar un valor válido.")

            pausar()

        elif opcion =="8":
            print(f"{Fore.YELLOW}Fin del programa.")
            conexion.close()
            break

        else:
            print(f"{Fore.RED}Opcion no disponible.")
            pausar()
# ==========================================
# PUNTO DE ENTRADA DEL PROGRAMA
# ==========================================            

# Inicia la ejecución del sistema de inventario.
menu()