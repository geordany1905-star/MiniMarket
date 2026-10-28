import tkinter as tk
from tkinter import ttk, messagebox
from database.database import obtener_conexion

def mostrar_reportes():
    ventana_reportes = tk.Toplevel()
    ventana_reportes.title("Consultas y Reportes - Mini Market")
    ventana_reportes.geometry("800x520")
    ventana_reportes.resizable(True, True)

    # 1. Título
    lbl_titulo = tk.Label(
        ventana_reportes, 
        text="📊 CONSULTAS Y REPORTES DE VENTAS", 
        font=("Arial", 16, "bold"),
        bg="#9C27B0",
        fg="white",
        pady=10
    )
    lbl_titulo.pack(fill="x")

    # 2. Resumen General (Tarjetas de Total)
    frame_resumen = tk.Frame(ventana_reportes, pady=10)
    frame_resumen.pack(fill="x", padx=20)

    lbl_total_ventas = tk.Label(
        frame_resumen, 
        text="Total Facturado: $0.00", 
        font=("Arial", 14, "bold"), 
        bg="#E1BEE7", 
        fg="#4A148C",
        padx=15, 
        pady=10
    )
    lbl_total_ventas.pack(side="left")

    btn_actualizar = tk.Button(
        frame_resumen, 
        text="🔄 Actualizar Reporte", 
        font=("Arial", 10, "bold"), 
        bg="#9C27B0", 
        fg="white",
        command=lambda: cargar_ventas()
    )
    btn_actualizar.pack(side="right")

    # 3. Tabla de Ventas
    frame_tabla = tk.Frame(ventana_reportes)
    frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)

    columnas = ("id", "cliente", "fecha", "total")
    tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=10)

    tabla.heading("id", text="N° Factura")
    tabla.heading("cliente", text="Cliente")
    tabla.heading("fecha", text="Fecha y Hora")
    tabla.heading("total", text="Total Facturado ($)")

    tabla.column("id", width=80, anchor="center")
    tabla.column("cliente", width=250)
    tabla.column("fecha", width=200, anchor="center")
    tabla.column("total", width=150, anchor="e")

    tabla.pack(fill="both", expand=True)

    # 4. Función para cargar datos
    def cargar_ventas():
        for row in tabla.get_children():
            tabla.delete(row)

        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            
            # Trae las ventas uniendo la información con el nombre del cliente
            cursor.execute('''
                SELECT v.id, c.nombre, v.fecha, v.total 
                FROM ventas v
                INNER JOIN clientes c ON v.cliente_id = c.id
                ORDER BY v.id DESC
            ''')
            filas = cursor.fetchall()

            grand_total = 0.0
            for f in filas:
                tabla.insert("", tk.END, values=(f[0], f[1], f[2], f"${f[3]:.2f}"))
                grand_total += f[3]

            lbl_total_ventas.config(text=f"Total Facturado: ${grand_total:.2f}")
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los reportes: {e}", parent=ventana_reportes)

    # Cargar datos al abrir
    cargar_ventas()