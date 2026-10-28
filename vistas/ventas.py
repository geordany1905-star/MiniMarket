import tkinter as tk
from tkinter import ttk, messagebox
from database.database import obtener_conexion

def mostrar_ventas():
    ventana_ventas = tk.Toplevel()
    ventana_ventas.title("Punto de Venta - Mini Market")
    ventana_ventas.geometry("900x650") # Un poco más ancha de entrada
    ventana_ventas.resizable(True, True) # ¡Permite redimensionar y maximizar!

    # Variables
    lista_carrito = []
    diccionario_productos = {}
    diccionario_clientes = {}

    # 1. TÍTULO
    lbl_titulo = tk.Label(
        ventana_ventas, 
        text="🛒 PUNTO DE VENTA (FACTURACIÓN)", 
        font=("Arial", 16, "bold"),
        bg="#00bcd4",
        fg="white",
        pady=10
    )
    lbl_titulo.pack(fill="x")

    # 2. SECCIÓN CLIENTE
    frame_cliente = tk.LabelFrame(ventana_ventas, text=" Cliente ", font=("Arial", 10, "bold"), padx=15, pady=5)
    frame_cliente.pack(fill="x", padx=20, pady=5)

    tk.Label(frame_cliente, text="Seleccionar Cliente:", font=("Arial", 10)).pack(side="left", padx=5)
    
    cb_clientes = ttk.Combobox(frame_cliente, state="readonly", font=("Arial", 10))
    cb_clientes.pack(side="left", fill="x", expand=True, padx=5)

    # 3. SECCIÓN AGREGAR PRODUCTO (Formulario Adaptable con Grid)
    frame_producto = tk.LabelFrame(ventana_ventas, text=" Agregar Producto ", font=("Arial", 10, "bold"), padx=15, pady=10)
    frame_producto.pack(fill="x", padx=20, pady=5)

    # Hacemos que las columnas del formulario se estiren proporcionalmente
    frame_producto.grid_columnconfigure(1, weight=3) # Lista de productos se expande más
    frame_producto.grid_columnconfigure(3, weight=1) # Campo código

    # Fila 0: Campos y Desplegables
    tk.Label(frame_producto, text="Lista de Productos (A-Z):", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=5, padx=5)
    cb_productos = ttk.Combobox(frame_producto, state="readonly", font=("Arial", 10))
    cb_productos.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

    tk.Label(frame_producto, text="O Código:", font=("Arial", 10)).grid(row=0, column=2, sticky="w", pady=5, padx=5)
    txt_codigo = tk.Entry(frame_producto, font=("Arial", 10))
    txt_codigo.grid(row=0, column=3, sticky="ew", padx=5, pady=5)

    tk.Label(frame_producto, text="Cantidad:", font=("Arial", 10)).grid(row=0, column=4, sticky="w", pady=5, padx=5)
    txt_cantidad = tk.Entry(frame_producto, width=6, font=("Arial", 10))
    txt_cantidad.insert(0, "1")
    txt_cantidad.grid(row=0, column=5, padx=5, pady=5)

    # 4. CARGAR DATOS DE BASE DE DATOS
    def cargar_datos_iniciales():
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()

            # Cargar Clientes
            cursor.execute("SELECT id, nombre, cedula FROM clientes ORDER BY nombre ASC")
            clientes = cursor.fetchall()
            lista_cli_str = []
            for c in clientes:
                etiqueta = f"{c[1]} - ({c[2]})"
                diccionario_clientes[etiqueta] = c[0]
                lista_cli_str.append(etiqueta)
            cb_clientes['values'] = lista_cli_str

            # Cargar Productos en orden alfabético
            cursor.execute("SELECT id, codigo, nombre, precio, stock FROM productos ORDER BY nombre ASC")
            prods = cursor.fetchall()
            lista_prod_str = []
            for p in prods:
                etiqueta_p = f"{p[2]} | ${p[3]:.2f} (Stock: {p[4]})"
                diccionario_productos[etiqueta_p] = {
                    "id": p[0], "codigo": p[1], "nombre": p[2], "precio": p[3], "stock": p[4]
                }
                lista_prod_str.append(etiqueta_p)
            cb_productos['values'] = lista_prod_str

            conn.close()
        except Exception as e:
            print("Error al cargar datos en ventas:", e)

    def al_seleccionar_producto_combo(event):
        prod_sel = cb_productos.get()
        if prod_sel in diccionario_productos:
            txt_codigo.delete(0, tk.END)
            txt_codigo.insert(0, diccionario_productos[prod_sel]["codigo"])

    cb_productos.bind("<<ComboboxSelected>>", al_seleccionar_producto_combo)

    # 5. AGREGAR AL CARRITO
    def agregar_al_carrito():
        cod = txt_codigo.get().strip()
        cant_str = txt_cantidad.get().strip()

        if not cod:
            messagebox.showwarning("Atención", "Seleccione un producto de la lista o ingrese un código.", parent=ventana_ventas)
            return

        try:
            cant = int(cant_str)
            if cant <= 0:
                messagebox.showwarning("Atención", "La cantidad debe ser mayor a 0.", parent=ventana_ventas)
                return
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero.", parent=ventana_ventas)
            return

        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("SELECT id, codigo, nombre, precio, stock FROM productos WHERE codigo = ?", (cod,))
            prod = cursor.fetchone()
            conn.close()

            if not prod:
                messagebox.showerror("Error", "El código ingresado no existe.", parent=ventana_ventas)
                return

            p_id, p_cod, p_nom, p_precio, p_stock = prod

            if cant > p_stock:
                messagebox.showwarning("Stock Insuficiente", f"Solo quedan {p_stock} unidades de '{p_nom}'.", parent=ventana_ventas)
                return

            subtotal = p_precio * cant

            lista_carrito.append({
                "id": p_id, "codigo": p_cod, "nombre": p_nom, 
                "precio": p_precio, "cantidad": cant, "subtotal": subtotal
            })

            actualizar_tabla_carrito()
            txt_codigo.delete(0, tk.END)
            txt_cantidad.delete(0, tk.END)
            txt_cantidad.insert(0, "1")
            cb_productos.set("")

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}", parent=ventana_ventas)

    def actualizar_tabla_carrito():
        for row in tabla.get_children():
            tabla.delete(row)

        total = 0.0
        for item in lista_carrito:
            tabla.insert("", tk.END, values=(item["codigo"], item["nombre"], f"${item['precio']:.2f}", item["cantidad"], f"${item['subtotal']:.2f}"))
            total += item["subtotal"]

        lbl_total.config(text=f"Total: ${total:.2f}")

    btn_agregar = tk.Button(frame_producto, text="➕ Agregar", font=("Arial", 10, "bold"), bg="#4CAF50", fg="white", padx=10, command=agregar_al_carrito)
    btn_agregar.grid(row=0, column=6, padx=10, pady=5)

    # 6. TABLA DETALLE DE FACTURA (Resizable)
    frame_tabla = tk.Frame(ventana_ventas)
    frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)

    columnas = ("codigo", "producto", "precio", "cantidad", "subtotal")
    tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")

    tabla.heading("codigo", text="Código")
    tabla.heading("producto", text="Producto")
    tabla.heading("precio", text="Precio Unit.")
    tabla.heading("cantidad", text="Cant.")
    tabla.heading("subtotal", text="Subtotal")

    tabla.column("codigo", width=100)
    tabla.column("producto", width=350)
    tabla.column("precio", width=120, anchor="e")
    tabla.column("cantidad", width=80, anchor="center")
    tabla.column("subtotal", width=120, anchor="e")

    tabla.pack(fill="both", expand=True)

    # 7. PIE DE PÁGINA
    frame_pie = tk.Frame(ventana_ventas)
    frame_pie.pack(fill="x", padx=20, pady=10)

    lbl_total = tk.Label(frame_pie, text="Total: $0.00", font=("Arial", 14, "bold"), fg="#2196F3")
    lbl_total.pack(side="right", padx=10)

    def procesar_factura():
        if not lista_carrito:
            messagebox.showwarning("Carrito Vacío", "Agregue al menos un producto para procesar la venta.", parent=ventana_ventas)
            return

        cliente_str = cb_clientes.get()
        cliente_id = diccionario_clientes.get(cliente_str, None)
        total_venta = sum(item["subtotal"] for item in lista_carrito)

        try:
            conn = obtener_conexion()
            cursor = conn.cursor()

            cursor.execute("INSERT INTO ventas (cliente_id, total) VALUES (?, ?)", (cliente_id, total_venta))
            venta_id = cursor.lastrowid

            for item in lista_carrito:
                cursor.execute('''
                    INSERT INTO detalle_ventas (venta_id, producto_id, cantidad, precio_unitario, subtotal)
                    VALUES (?, ?, ?, ?, ?)
                ''', (venta_id, item["id"], item["cantidad"], item["precio"], item["subtotal"]))

                cursor.execute('''
                    UPDATE productos SET stock = stock - ? WHERE id = ?
                ''', (item["cantidad"], item["id"]))

            conn.commit()
            conn.close()

            messagebox.showinfo("¡Venta Exitosa!", f"¡Factura N° {venta_id} generada con éxito!", parent=ventana_ventas)
            lista_carrito.clear()
            actualizar_tabla_carrito()
            cargar_datos_iniciales()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo procesar la venta: {e}", parent=ventana_ventas)

    btn_procesar = tk.Button(frame_pie, text="💳 Procesar Factura", font=("Arial", 11, "bold"), bg="#2196F3", fg="white", padx=10, command=procesar_factura)
    btn_procesar.pack(side="left", padx=10)

    cargar_datos_iniciales()