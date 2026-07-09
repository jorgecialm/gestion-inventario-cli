# Gestión de Inventario CLI

Sistema de gestión de inventario por línea de comandos (CLI), desarrollado en Python con persistencia en SQLite. Trabajo final del curso de Python de Talento Tech.

## Funcionalidades

- Registrar nuevos productos
- Listar todos los productos registrados
- Actualizar cantidad y precio de un producto por ID
- Eliminar un producto por ID (con confirmación)
- Buscar un producto por ID
- Buscar productos por nombre o categoría (coincidencia parcial)
- Generar un reporte de productos con stock bajo

## Requisitos

- Python 3.10 o superior
- [colorama](https://pypi.org/project/colorama/)

## Instalación

Cloná el repositorio:

```bash
git clone https://github.com/jorgecialm/gestion-inventario-cli.git
cd gestion-inventario-cli
```

Instalá las dependencias:

```bash
pip install colorama --break-system-packages
```

(el flag `--break-system-packages` es necesario en instalaciones de Python gestionadas por el sistema operativo, como en Linux Mint; si usás un entorno virtual, no hace falta)

## Uso

Ejecutá el programa:

```bash
python3 Entrega_Final_Python_Fernandez_Jorge.py
```

La primera vez que se ejecuta, se crea automáticamente el archivo `inventario.db` con la tabla `productos`.

Vas a ver un menú con las siguientes opciones:

```
1- Crear producto
2- Listar productos
3- Actualizar productos
4- Eliminar producto
5- Buscar producto
6- Buscar extendido
7- Revisar stock bajo
8- Salir
```

Elegí un número y seguí las instrucciones en pantalla.

## Estructura de la base de datos

La tabla `productos` tiene las siguientes columnas:

| Columna     | Tipo    | Restricción     |
|-------------|---------|------------------|
| id          | INTEGER | Clave primaria, autoincremental |
| nombre      | TEXT    | No nulo |
| descripcion | TEXT    | — |
| cantidad    | INTEGER | No nulo |
| precio      | REAL    | No nulo |
| categoria   | TEXT    | — |

## Autor

Jorge Fernández ([@jorgecialm](https://github.com/jorgecialm))