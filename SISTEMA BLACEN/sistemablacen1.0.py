"""SISTEMA BLACEN"""
"""Documentación: se desarrolló un programa informático de consola utilizando Python, 
precedido por la planificación y lógica en el entorno PSeInt. 
La elección de estas herramientas responde a su facilidad de aprendizaje, flexibilidad 
y amplia aplicabilidad en proyectos educativos y reales. 
El sistema diseñado permite registrar ventas, generar facturas además de llevar el control
de productos en inventario, todo desde una interfaz sencilla."""

"""Creado por: 
Alexa Loaisiga, 
Chelsea Quintanilla, 
Fabiola Lanuza y
Luis Aguirre.
Grupo 3
"""
"""Versión 1.0"""

import json
import os

# Archivo donde se guardará el inventario
inventario_file = "inventario.json"


#Función para limpiar la consola
#Estética del programa
def limpiar():
    os.system('cls' if os.name == 'nt' else 'clear')



# Si existe archivo [inventario.json], lo cargamos; si no, inicializamos con los datos
def cargar_inventario():
    if os.path.exists(inventario_file):
        with open(inventario_file, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        # Inventario inicial
        return [
            {"nombre": "Aceite Castrol", "categoria": "Aceites y Lubricantes", "cantidad": 10, "precio": 400},
            {"nombre": "Aceite Axiom", "categoria": "Aceites y Lubricantes", "cantidad": 10, "precio": 450},
            {"nombre": "Neumático 3.25-17 GB Boy", "categoria": "Neumáticos y Llantas", "cantidad": 10, "precio": 700},
            {"nombre": "Neumático 4.00-17 GB Boy", "categoria": "Neumáticos y Llantas", "cantidad": 10, "precio": 800},
            {"nombre": "Neumático 3.00-17", "categoria": "Neumáticos y Llantas", "cantidad": 10, "precio": 900},
            {"nombre": "Cable clutch", "categoria": "Partes de transmisión y frenos", "cantidad": 10, "precio": 550},
            {"nombre": "Manigueta clutch", "categoria": "Partes de transmisión y frenos", "cantidad": 10, "precio": 600},
            {"nombre": "CDI CRF200", "categoria": "Eléctricos y electrónicos", "cantidad": 10, "precio": 450},
            {"nombre": "Bobina bajo 8M3 C6150-8", "categoria": "Eléctricos y electrónicos", "cantidad": 10, "precio": 350},
            {"nombre": "Chispero D8", "categoria": "Eléctricos y electrónicos", "cantidad": 10, "precio": 900},
            {"nombre": "Protector pedal cambio azul", "categoria": "Accesorios y varios", "cantidad": 10, "precio": 500},
            {"nombre": "Spray negro brillante", "categoria": "Accesorios y varios", "cantidad": 10, "precio": 250},
            {"nombre": "Boya shop has 8001", "categoria": "Accesorios y varios", "cantidad": 10, "precio": 600}
        ]

#Funcion para guardar el inventario
def guardar_inventario(productos):
    with open(inventario_file, "w") as f:
        json.dump(productos, f, indent=4)
        
#Funcion para cargar usuarios
def cargar_usuarios():
    usuarios={}
    if os.path.exists("users.txt"):
        with open("users.txt", "r") as archivo:
            for linea in archivo:
                usuario, contrasena=linea.strip().split(",")
                usuarios[usuario] = contrasena
    return usuarios
                
#IMPORTAMOS PWINPUT LUEGO DE INSTALARLA A TRAVÉS DE PIP, ESTA PERMITE OCULTAR LA CONTRASEÑA A TRAVÉS DE ASTERISCOS (*)
import pwinput

#Funcion para la validación del inicio de sesión, máximo 3 intentos
#AL INGRESAR AL SISTEMA ES ESTA LA VENTANA QUE NOS RECIBE
def login():
    
    print("====== INICIO DE SESIÓN SISTEMA BLACEN =====")
    usuarios= cargar_usuarios()
    
    intentos = 3
    while intentos > 0:
        usuario = input("Usuario: ")
        contrasena_ingresada = pwinput.pwinput("Contraseña: ", mask='*')
    
        if usuario in usuarios and usuarios[usuario] == contrasena_ingresada:
            print("¡Acceso concedido!\n")
            return True
        else:
            print("Credenciales incorrectas.")
            intentos -= 1
    print("Demasiados intentos fallidos.")
    return False

#Opcion 3 del menu principal
#Definición de la función para mostrar el inventario
def mostrar_inventario(productos):
    print("\n-------------------------------------------- INVENTARIO ACTUAL ---------------------------------------------------")
    print(f"{'No.':<7}{'Producto':<40}{'Categoría':<50}{'Cant':<6}{'Precio (C$)':<10}")
    print("-" * 115)
    for i, p in enumerate(productos, 1):
        print(f"{i:<7}{p['nombre']:<40}{p['categoria']:<50}{p['cantidad']:<6}{p['precio']:<10.2f}")
    print()



#Opción 2 del menu principal:
#Definición para agregar productos, si encuentra en inventario el producto que estamos agregando, pregunta si deseas agregar
# más cantidad, así mismo pregunta si deseas actualizar precio.
def agregar_producto(productos):
    nombre_ingresado = input("Nombre del producto: ").strip()
    categoria_ingresada = input("Categoría: ").strip()

    def normalizar(texto):
        return ' '.join(texto.lower().split())

    nombre_norm = normalizar(nombre_ingresado)
    categoria_norm = normalizar(categoria_ingresada)

    for producto in productos:
        nombre_existente = normalizar(producto["nombre"])
        categoria_existente = normalizar(producto["categoria"])

        if nombre_existente == nombre_norm and categoria_existente == categoria_norm:
            print(f"\nEl producto '{producto['nombre']}' ya existe en la categoría '{producto['categoria']}'.")
            opcion = input("¿Desea añadir más cantidad a este producto? (si/no): ").lower()
            if opcion == "si":
                try:
                    cantidad_extra = int(input("¿Cuántas unidades desea añadir?: "))
                    if cantidad_extra > 0:
                        producto["cantidad"] += cantidad_extra

                        nuevo_precio_str = input(f"Precio actual: C${producto['precio']:.2f}. Ingrese nuevo precio o presione Enter para mantenerlo: ").strip()
                        if nuevo_precio_str:
                            nuevo_precio = float(nuevo_precio_str)
                            if nuevo_precio != producto["precio"]:
                                confirmar = input(f"¿Confirmar cambio de precio de C${producto['precio']:.2f} a C${nuevo_precio:.2f}? (si/no): ").lower()
                                if confirmar == "si":
                                    producto["precio"] = nuevo_precio
                                    print("Precio actualizado.")
                                else:
                                    print("Precio no modificado.")
                        guardar_inventario(productos)
                        print("Cantidad actualizada correctamente.\n")
                    else:
                        print("La cantidad debe ser mayor que cero.\n")
                except:
                    print("Entrada inválida. No se actualizó la cantidad ni el precio.\n")
            else:
                print("No se modificó el producto existente.\n")
            return

    # Si no existe, agregar como nuevo producto
    try:
        cantidad = int(input("Cantidad: "))
        precio = float(input("Precio: "))
        productos.append({
            "nombre": nombre_ingresado,
            "categoria": categoria_ingresada,
            "cantidad": cantidad,
            "precio": precio
        })
        guardar_inventario(productos)
        print("Producto agregado correctamente.\n")
    except:
        print("Datos inválidos. No se agregó el producto.\n")

#Función para eliminar productos del inventario
def eliminar_producto(productos):
    if not productos:
        print("El inventario está vacío. No hay productos para eliminar.\n")
        return
    
    mostrar_inventario(productos)
    
    try:
        indice = int(input("Ingrese el número del producto que desea eliminar: ")) - 1
        if 0 <= indice < len(productos):
            producto_eliminado = productos.pop(indice)
            guardar_inventario(productos)
            print(f"Producto '{producto_eliminado['nombre']}' eliminado correctamente.\n")
        else:
            print("Número inválido. No se eliminó ningún producto.\n")
    except ValueError:
        print("Entrada inválida. Por favor ingrese un número válido.\n")


#Función para agregar clientes a nuestros archivos especiales para ello: clientes_frecuentes.txt

def guardar_cliente(nombre, ruc):
    nombre = nombre.strip().lower()
    ruc = ruc.strip().lower()
    
    clientes_existentes = set()

    if os.path.exists("clientes_frecuentes.txt"):
        with open("clientes_frecuentes.txt", "r") as archivo:
            for linea in archivo:
                partes = linea.strip().split("-")
                if len(partes) >= 2:
                    cliente_guardado = partes[0].strip().lower()
                    ruc_guardado = partes[1].replace("RUC:", "").strip().lower()
                    clientes_existentes.add((cliente_guardado, ruc_guardado))

    if (nombre, ruc) not in clientes_existentes:
        with open("clientes_frecuentes.txt", "a") as archivo:
            archivo.write(f"{nombre.title()} - RUC: {ruc.upper()}\n")
    else:
        print(f"\nAviso: El cliente '{nombre.title()}' con RUC '{ruc.upper()}' ya está registrado como frecuente.\n")


#Función para ver clientes frecuentes, busca el archivo especial para mostrarlo en consola.

def ver_clientes_frecuentes():
    print("\n========== CLIENTES FRECUENTES ==========")
    if os.path.exists("clientes_frecuentes.txt"):
        with open("clientes_frecuentes.txt", "r") as archivo:
            lineas = archivo.readlines()
            if not lineas:
                print("No hay clientes frecuentes registrados.")
            else:
                for i, linea in enumerate(lineas, 1):
                    print(f"{i}. {linea.strip()}")
    else:
        print("No hay clientes frecuentes registrados.")
    print("==========================================\n")

#Función que permite guardar facturas en el archivo "facturas.txt"
def guardar_factura(cliente, ruc, fecha, items, subtotal, iva, descuento, total):
    with open("factura.txt", "a") as f:
        f.write("========== FACTURA ==========\n")
        f.write(f"Cliente: {cliente}\n")
        if ruc != "":
            f.write(f"RUC: {ruc}\n")
        f.write(f"Fecha: {fecha}\n")
        f.write("Producto\tCant\tPrecio\tTotal\n")
        for item in items:
            f.write(f"{item['nombre']}\t{item['cantidad']}\tC${item['precio']}\tC${item['total']}\n")
        f.write(f"\nSubtotal: C${subtotal:.2f}\n")
        f.write(f"IVA (15%): C${iva:.2f}\n")
        f.write(f"Descuento: C${descuento:.2f}\n")
        f.write(f"TOTAL A PAGAR: C${total:.2f}\n")
        f.write("=============================\n\n") 
        
#Función que permite realizar una venta cuando el usuario selecciona la opción 1 del menu principal       
def realizar_venta(productos):
    cliente = input("Nombre del cliente: ")
    ruc = input("RUC (opcional): ")
    fecha = input("Fecha: ")
    items = []
    subtotal = 0

    # Ciclo para agregar varios productos
    while True:
        mostrar_inventario(productos)
        try:
            indice = int(input("Ingrese número del producto a vender: ")) - 1
            if 0 <= indice < len(productos):
                prod = productos[indice]
                cantidad = int(input(f"Ingrese cantidad a vender (Disponible: {prod['cantidad']}): "))
                if 0 < cantidad <= prod["cantidad"]:
                    total_item = cantidad * prod["precio"]
                    items.append({
                        "nombre": prod["nombre"],
                        "cantidad": cantidad,
                        "precio": prod["precio"],
                        "total": total_item
                    })
                    subtotal += total_item
                    productos[indice]["cantidad"] -= cantidad
                    guardar_inventario(productos)
                else:
                    print("Cantidad inválida.")
            else:
                print("Producto no encontrado.")
        except:
            print("Entrada inválida.")

        otro = input("¿Agregar otro producto? (si/no): ").lower()
        if otro != "si":
            break
    
    # Cálculo de impuestos y descuento
    iva = subtotal * 0.15
    descuento = 0
    aplicar_desc = input("¿Aplicar descuento por temporada? (si/no): ").lower()
    if aplicar_desc == "si":
        try:
            porcentaje = float(input("Porcentaje de descuento (%): "))
            descuento = subtotal * (porcentaje / 100)
        except:
            print("Porcentaje inválido. No se aplicó descuento.")
    total = subtotal + iva - descuento

    # Muestra factura en pantalla
    print("\n========= FACTURA =========")
    print(f"Cliente: {cliente}")
    print(f"Fecha: {fecha}")
    print("Producto\tCant\tPrecio\tTotal")
    for item in items:
        print(f"{item['nombre']}\t{item['cantidad']}\tC${item['precio']}\tC${item['total']}")
    print(f"\nSubtotal: C${subtotal:.2f}")
    print(f"IVA (15%): C${iva:.2f}")
    print(f"Descuento: C${descuento:.2f}")
    print(f"TOTAL A PAGAR: C${total:.2f}")
    print("============================\n")

    guardar_factura(cliente, ruc, fecha, items, subtotal, iva, descuento, total)
    guardar_cliente(cliente, ruc)


# ------------ PROGRAMA PRINCIPAL ------------

if login(): # Si el login es exitoso, entra al menú
    productos = cargar_inventario()
    while True:
        limpiar()
        print("===== MENÚ BLACEN =====")
        print("1. Realizar venta")
        print("2. Agregar producto nuevo")
        print("3. Ver inventario")
        print("4. Ver clientes frecuentes")
        print("5. Eliminar producto")
        print("6. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            realizar_venta(productos)
        elif opcion == "2":
            agregar_producto(productos)
        elif opcion == "3":
            mostrar_inventario(productos)
        elif opcion == "4":
            ver_clientes_frecuentes()
        elif opcion == "5":
            eliminar_producto(productos)
        elif opcion == "6":
            print("Gracias por usar el sistema BLACEN.")
            break
        else:
            print("Opción inválida.\n")
            
        input("Presione Enter para continuar...")

