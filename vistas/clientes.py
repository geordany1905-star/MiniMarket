import tkinter as tk
from tkinter import ttk, messagebox
from database.database import obtener_conexion

def mostrar_clientes():
    ventana_clientes = tk.Toplevel()
    ventana_clientes.title("Gestión de Clientes - Mini Market")
    ventana_clientes.geometry("750x540")
    ventana_clientes.resizable(True, True)

    # Variable global para saber si estamos editando un cliente existente
    id_cliente_seleccionado = tk.StringVar()

    # 1. TÍTULO
    lbl_titulo = tk.Label(
        ventana_clientes, 
        text="GESTIÓN DE CLIENTES", 
        font=("Arial", 16, "bold"),
        bg="#4CAF50",
        fg="white",
        pady=10
    )
    lbl_titulo.pack(fill="x")

    # 2. FORMULARIO
    frame_form = tk.LabelFrame(ventana_clientes, text=" Datos del Cliente ", font=("Arial", 10, "bold"), padx=15, pady=10)
    frame_form.pack(fill="x", padx=20, pady=10)

    tk.Label(frame_form, text="Cédula/RNC:", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=5)
    txt_cedula = tk.Entry(frame_form, width=20, font=("Arial", 10))
    txt_cedula.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_form, text="Nombre Completo:", font=("Arial", 10)).grid(row=0, column=2, sticky="w", pady=5)
    txt_nombre = tk.Entry(frame_form, width=30, font=("Arial", 10))
    txt_nombre.grid(row=0, column=3, padx=5, pady=5)

    tk.Label(frame_form, text="Teléfono:", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=5)
    txt_telefono = tk.Entry(frame_form, width=20, font=("Arial", 10))
    txt_telefono.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(frame_form, text="Dirección:", font=("Arial", 10)).grid(row=1, column=2, sticky="w", pady=5)
    txt_direccion = tk.Entry(frame_form, width=30, font=("Arial", 10))
    txt_direccion.grid(row=1, column=3, padx=5, pady=5)

    # 3. LÓGICA DEL BACKEND (Lógica de la base de datos)

    def limpiar_campos():
        # Explicación: Borra el texto de los inputs y reinicia la variable de ID
        txt_cedula.delete(0, tk.END)
        txt_nombre.delete(0, tk.END)
        txt_telefono.delete(0, tk.END)
        txt_direccion.delete(0, tk.END)
        id_cliente_seleccionado.set("")

    def cargar_clientes():
        # Explicación: Limpia la tabla visual y trae todos los registros con SELECT
        for item in tabla.get_children():
            tabla.delete(item)
            
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clientes")
            filas = cursor.fetchall() # fetchall() trae todas las filas devueltas
            for fila in filas:
                tabla.insert("", tk.END, values=fila)
            conn.close()
        except Exception as e:
            print("Error al cargar clientes:", e)

    def guardar_cliente():
        # Explicación: Guarda o Actualiza dependiendo de si seleccionamos alguien
        cedula = txt_cedula.get().strip()
        nombre = txt_nombre.get().strip()
        telefono = txt_telefono.get().strip()
        direccion = txt_direccion.get().strip()

        if not cedula or not nombre:
            messagebox.showwarning("Atención", "Cédula y Nombre son obligatorios.", parent=ventana_clientes)
            return

        try:
            conn = obtener_conexion()
            cursor = conn.cursor()

            # SI id_cliente_seleccionado TIENE VALOR -> HACEMOS UPDATE
            if id_cliente_seleccionado.get():
                cursor.execute('''
                    UPDATE clientes 
                    SET cedula=?, nombre=?, telefono=?, direccion=? 
                    WHERE id=?
                ''', (cedula, nombre, telefono, direccion, id_cliente_seleccionado.get()))
                messagebox.showinfo("Éxito", "¡Cliente actualizado correctamente!", parent=ventana_clientes)
            
            # SI NO TIENE VALOR -> HACEMOS INSERT (Guardar nuevo)
            else:
                cursor.execute('''
                    INSERT INTO clientes (cedula, nombre, telefono, direccion) 
                    VALUES (?, ?, ?, ?)
                ''', (cedula, nombre, telefono, direccion))
                messagebox.showinfo("Éxito", "¡Cliente registrado correctamente!", parent=ventana_clientes)

            conn.commit() # commit() guarda permanentemente los cambios
            conn.close()

            limpiar_campos()
            cargar_clientes()
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}", parent=ventana_clientes)
    def seleccionar_cliente_de_tabla(event):
        # 1. Obtenemos la fila seleccionada con el clic
        item_seleccionado = tabla.focus()
        if not item_seleccionado:
            return

        valores = tabla.item(item_seleccionado, 'values')
        if not valores:
            return

        # 2. PRIMERO limpiamos los campos de texto
        txt_cedula.delete(0, tk.END)
        txt_nombre.delete(0, tk.END)
        txt_telefono.delete(0, tk.END)
        txt_direccion.delete(0, tk.END)

        # 3. DESPUÉS guardamos el ID y rellenamos los datos en pantalla
        id_cliente_seleccionado.set(valores[0]) # ID
        txt_cedula.insert(0, valores[1])        # Cédula
        txt_nombre.insert(0, valores[2])        # Nombre
        txt_telefono.insert(0, valores[3])        # Teléfono
        txt_direccion.insert(0, valores[4])        # Dirección

    def eliminar_cliente():
        id_actual = id_cliente_seleccionado.get()

        # Si por alguna razón la variable id_actual está vacía, la buscamos directamente de la fila seleccionada
        if not id_actual:
            item_seleccionado = tabla.focus()
            if item_seleccionado:
                valores = tabla.item(item_seleccionado, 'values')
                if valores:
                    id_actual = valores[0]

        # Si sigue sin haber nada seleccionado, avisamos al usuario
        if not id_actual:
            messagebox.showwarning("Atención", "Seleccione un cliente de la tabla para eliminar.", parent=ventana_clientes)
            return

        # Confirmación de seguridad antes de borrar de la Base de Datos
        confirmar = messagebox.askyesno("Confirmar Eliminación", "¿Está seguro de eliminar este cliente permanentemente?", parent=ventana_clientes)
        if confirmar:
            try:
                conn = obtener_conexion()
                cursor = conn.cursor()
                
                # Ejecutamos la consulta SQL DELETE
                cursor.execute("DELETE FROM clientes WHERE id = ?", (id_actual,))
                conn.commit() # Confirmamos el cambio en la base de datos
                conn.close()

                messagebox.showinfo("Éxito", "Cliente eliminado correctamente.", parent=ventana_clientes)
                limpiar_campos()
                cargar_clientes() # Recargamos la tabla para ver que ya no está
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar de la base de datos: {e}", parent=ventana_clientes)

    # 4. BOTONES
    frame_acciones = tk.Frame(ventana_clientes)
    frame_acciones.pack(pady=5)

    btn_guardar = tk.Button(frame_acciones, text="💾 Guardar", font=("Arial", 10, "bold"), bg="#2196F3", fg="white", width=12, command=guardar_cliente)
    btn_guardar.pack(side="left", padx=5)

    btn_eliminar = tk.Button(frame_acciones, text="🗑️ Eliminar", font=("Arial", 10, "bold"), bg="#f44336", fg="white", width=12, command=eliminar_cliente)
    btn_eliminar.pack(side="left", padx=5)

    btn_limpiar = tk.Button(frame_acciones, text="🧹 Limpiar", font=("Arial", 10), width=12, command=limpiar_campos)
    btn_limpiar.pack(side="left", padx=5)

    # 5. TABLA
    frame_tabla = tk.Frame(ventana_clientes)
    frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)

    columnas = ("id", "cedula", "nombre", "telefono", "direccion")
    tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=8)

    tabla.heading("id", text="ID")
    tabla.heading("cedula", text="Cédula/RNC")
    tabla.heading("nombre", text="Nombre")
    tabla.heading("telefono", text="Teléfono")
    tabla.heading("direccion", text="Dirección")

    tabla.column("id", width=40, anchor="center")
    tabla.column("cedula", width=110)
    tabla.column("nombre", width=200)
    tabla.column("telefono", width=110)
    tabla.column("direccion", width=220)

    # Escuchador de eventos: Cuando el usuario hace clic en una fila, ejecuta seleccionar_cliente_de_tabla
    tabla.bind("<ButtonRelease-1>", seleccionar_cliente_de_tabla)

    tabla.pack(fill="both", expand=True)

    cargar_clientes()