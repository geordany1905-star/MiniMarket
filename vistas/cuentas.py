import tkinter as tk
from tkinter import ttk, messagebox
from database.database import obtener_conexion

def mostrar_cuentas():
    ventana_cuentas = tk.Toplevel()
    ventana_cuentas.title("Cuentas por Cobrar - Mini Market")
    ventana_cuentas.geometry("750x500")
    ventana_cuentas.resizable(True, True)

    # 1. Título
    lbl_titulo = tk.Label(
        ventana_cuentas, 
        text="💳 GESTIÓN DE CUENTAS POR COBRAR", 
        font=("Arial", 16, "bold"),
        bg="#009688",
        fg="white",
        pady=10
    )
    lbl_titulo.pack(fill="x")

    # 2. Tabla
    frame_tabla = tk.Frame(ventana_cuentas)
    frame_tabla.pack(fill="both", expand=True, padx=20, pady=15)

    columnas = ("id", "cliente", "monto", "estado")
    tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=10)

    tabla.heading("id", text="N° Registro")
    tabla.heading("cliente", text="Cliente")
    tabla.heading("monto", text="Monto Pendiente ($)")
    tabla.heading("estado", text="Estado")

    tabla.column("id", width=80, anchor="center")
    tabla.column("cliente", width=250)
    tabla.column("monto", width=150, anchor="e")
    tabla.column("estado", width=120, anchor="center")

    tabla.pack(fill="both", expand=True)

    # 3. Función para cargar
    def cargar_cuentas():
        for row in tabla.get_children():
            tabla.delete(row)

        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT cpx.id, cl.nombre, cpx.monto_pendiente, cpx.estado
                FROM cuentas_por_cobrar cpx
                INNER JOIN clientes cl ON cpx.cliente_id = cl.id
            ''')
            filas = cursor.fetchall()
            for f in filas:
                tabla.insert("", tk.END, values=(f[0], f[1], f"${f[2]:.2f}", f[3]))
            conn.close()
        except Exception as e:
            print("Error al cargar cuentas:", e)

    cargar_cuentas()