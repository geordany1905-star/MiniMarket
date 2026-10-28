import tkinter as tk
from tkinter import ttk, messagebox
from database.database import obtener_conexion

def mostrar_productos():
    ventana_prod = tk.Toplevel()
    ventana_prod.title("Gestión de Productos - Mini Market")
    ventana_prod.geometry("850x600")
    ventana_prod.resizable(True, True)

    # 1. ENCABEZADO
    lbl_titulo = tk.Label(
        ventana_prod, 
        text="GESTIÓN DE PRODUCTOS E INVENTARIO", 
        font=("Arial", 16, "bold"),
        bg="#FF9800",
        fg="white",
        pady=10
    )
    lbl_titulo.pack(fill="x")

    # 2. FORMULARIO DE REGISTRO / EDICIÓN
    frame_form = tk.LabelFrame(ventana_prod, text=" Datos del Producto ", font=("Arial", 10, "bold"), padx=15, pady=10)
    frame_form.pack(fill="x", padx=20, pady=10)

    frame_form.grid_columnconfigure(1, weight=1)
    frame_form.grid_columnconfigure(3, weight=1)

    tk.Label(frame_form, text="Código:", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=5)
    txt_codigo = tk.Entry(frame_form, font=("Arial", 10))
    txt_codigo.grid(row=0, column=1, sticky="ew", padx=10, pady=5)

    tk.Label(frame_form, text="Producto:", font=("Arial", 10)).grid(row=0, column=2, sticky="w", pady=5)
    txt_nombre = tk.Entry(frame_form, font=("Arial", 10))
    txt_nombre.grid(row=0, column=3, sticky="ew", padx=10, pady=5)

    tk.Label(frame_form, text="Precio ($):", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=5)
    txt_precio = tk.Entry(frame_form, font=("Arial", 10))
    txt_precio.grid(row=1, column=1, sticky="ew", padx=10, pady=5)

    tk.Label(frame_form, text="Stock (Cantidad):", font=("Arial", 10)).grid(row=1, column=2, sticky="w", pady=5)
    txt_stock = tk.Entry(frame_form, font=("Arial", 10))
    txt_stock.grid(row=1, column=3, sticky="ew", padx=10, pady=5)

    # Variable para saber si editamos o creamos
    id_producto_sel = [None]

    # 3. FUNCIONES CRUD (SQL)
    def cargar_productos():
        for row in tabla.get_children():
            tabla.delete(row)

        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("SELECT id, codigo, nombre, precio, stock FROM productos ORDER BY id ASC")
            productos = cursor.fetchall()
            conn.close()

            for p in productos:
                estado = "✅ DISPONIBLE" if p[4] > 0 else "❌ AGOTADO"
                tabla.insert("", tk.END, values=(p[0], p[1], p[2], f"${p[3]:.2f}", p[4], estado))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los productos: {e}", parent=ventana_prod)

    def limpiar_campos():
        txt_codigo.delete(0, tk.END)
        txt_nombre.delete(0, tk.END)
        txt_precio.delete(0, tk.END)
        txt_stock.delete(0, tk.END)
        id_producto_sel[0] = None

    def agregar_nuevo_producto():
        cod = txt_codigo.get().strip()
        nom = txt_nombre.get().strip()
        prec_str = txt_precio.get().strip()
        stk_str = txt_stock.get().strip()

        if not cod or not nom or not prec_str or not stk_str:
            messagebox.showwarning("Atención", "Todos los campos son obligatorios.", parent=ventana_prod)
            return

        try:
            precio = float(prec_str)
            stock = int(stk_str)
        except ValueError:
            messagebox.showerror("Error", "Precio debe ser número y Stock debe ser un entero.", parent=ventana_prod)
            return

        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO productos (codigo, nombre, precio, stock)
                VALUES (?, ?, ?, ?)
            ''', (cod, nom, precio, stock))
            conn.commit()
            conn.close()

            messagebox.showinfo("¡Éxito!", f"Producto '{nom}' agregado correctamente al inventario SQL.", parent=ventana_prod)
            limpiar_campos()
            cargar_productos()
        except Exception as e:
            messagebox.showerror("Error SQL", f"El código de producto ya existe o hubo un error: {e}", parent=ventana_prod)

    def actualizar_producto_existente():
        if id_producto_sel[0] is None:
            messagebox.showwarning("Atención", "Seleccione un producto de la tabla abajo para actualizarlo.", parent=ventana_prod)
            return

        cod = txt_codigo.get().strip()
        nom = txt_nombre.get().strip()
        prec_str = txt_precio.get().strip()
        stk_str = txt_stock.get().strip()

        try:
            precio = float(prec_str)
            stock = int(stk_str)

            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE productos 
                SET codigo = ?, nombre = ?, precio = ?, stock = ?
                WHERE id = ?
            ''', (cod, nom, precio, stock, id_producto_sel[0]))
            conn.commit()
            conn.close()

            messagebox.showinfo("¡Éxito!", "Producto / Inventario actualizado en la Base de Datos.", parent=ventana_prod)
            limpiar_campos()
            cargar_productos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar: {e}", parent=ventana_prod)

    def eliminar_producto():
        if id_producto_sel[0] is None:
            messagebox.showwarning("Atención", "Seleccione un producto de la tabla para eliminarlo.", parent=ventana_prod)
            return

        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este producto?", parent=ventana_prod):
            try:
                conn = obtener_conexion()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto_sel[0],))
                conn.commit()
                conn.close()

                messagebox.showinfo("Éxito", "Producto eliminado correctamente.", parent=ventana_prod)
                limpiar_campos()
                cargar_productos()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar: {e}", parent=ventana_prod)

    def al_seleccionar_producto(event):
        item_sel = tabla.selection()
        if item_sel:
            valores = tabla.item(item_sel[0], "values")
            id_producto_sel[0] = valores[0]

            txt_codigo.delete(0, tk.END)
            txt_codigo.insert(0, valores[1])

            txt_nombre.delete(0, tk.END)
            txt_nombre.insert(0, valores[2])

            txt_precio.delete(0, tk.END)
            txt_precio.insert(0, valores[3].replace("$", ""))

            txt_stock.delete(0, tk.END)
            txt_stock.insert(0, valores[4])

    # 4. BOTONES DE ACCIÓN CLAROS
    frame_botones = tk.Frame(ventana_prod)
    frame_botones.pack(fill="x", padx=20, pady=5)

    btn_agregar = tk.Button(frame_botones, text="➕ Registrar Nuevo", font=("Arial", 10, "bold"), bg="#4CAF50", fg="white", padx=10, command=agregar_nuevo_producto)
    btn_agregar.pack(side="left", padx=5)

    btn_actualizar = tk.Button(frame_botones, text="✏️ Actualizar/Reabastecer", font=("Arial", 10, "bold"), bg="#2196F3", fg="white", padx=10, command=actualizar_producto_existente)
    btn_actualizar.pack(side="left", padx=5)

    btn_eliminar = tk.Button(frame_botones, text="🗑️ Eliminar", font=("Arial", 10, "bold"), bg="#F44336", fg="white", padx=10, command=eliminar_producto)
    btn_eliminar.pack(side="left", padx=5)

    btn_limpiar = tk.Button(frame_botones, text="🧹 Limpiar Campos", font=("Arial", 10), bg="#9E9E9E", fg="white", padx=10, command=limpiar_campos)
    btn_limpiar.pack(side="right", padx=5)

    # 5. TABLA DE INVENTARIO
    frame_tabla = tk.Frame(ventana_prod)
    frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)

    columnas = ("id", "codigo", "nombre", "precio", "stock", "estado")
    tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")

    tabla.heading("id", text="ID")
    tabla.heading("codigo", text="Código")
    tabla.heading("nombre", text="Nombre del Producto")
    tabla.heading("precio", text="Precio")
    tabla.heading("stock", text="Stock")
    tabla.heading("estado", text="Estado")

    tabla.column("id", width=50, anchor="center")
    tabla.column("codigo", width=100)
    tabla.column("nombre", width=300)
    tabla.column("precio", width=100, anchor="e")
    tabla.column("stock", width=80, anchor="center")
    tabla.column("estado", width=120, anchor="center")

    tabla.bind("<<TreeviewSelect>>", al_seleccionar_producto)
    tabla.pack(fill="both", expand=True)

    cargar_productos()