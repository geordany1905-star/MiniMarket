import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk  # Requiere: pip install pillow
import os
import shutil

def abrir_menu():
    ventana_menu = tk.Tk()
    ventana_menu.title("Sistema de Gestión - Mini Market")
    ventana_menu.geometry("900x620")
    ventana_menu.resizable(True, True)  # Permitir maximizar
    ventana_menu.configure(bg="#f5f5f5")

    # Ruta de la imagen del logo
    carpeta_imagenes = "imagenes"
    ruta_logo = os.path.join(carpeta_imagenes, "logo.png")

    if not os.path.exists(carpeta_imagenes):
        os.makedirs(carpeta_imagenes)

    # 1. ENCABEZADO
    header = tk.Frame(ventana_menu, bg="#00bcd4", pady=15)
    header.pack(fill="x")

    lbl_titulo = tk.Label(
        header, 
        text="🏪 SISTEMA DE GESTIÓN MINI MARKET", 
        font=("Arial", 18, "bold"), 
        bg="#00bcd4", 
        fg="white"
    )
    lbl_titulo.pack()

    # 2. CONTENEDOR PRINCIPAL
    body = tk.Frame(ventana_menu, bg="#f5f5f5", padx=20, pady=15)
    body.pack(fill="both", expand=True)

    body.grid_columnconfigure(0, weight=1)
    body.grid_columnconfigure(1, weight=1)
    body.grid_rowconfigure(0, weight=1)

    # --- COLUMNA IZQUIERDA: LOGO Y BOTÓN DE CARGA ---
    frame_izq = tk.Frame(body, bg="white", bd=2, relief="groove", padx=10, pady=10)
    frame_izq.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    lbl_bienvenida = tk.Label(
        frame_izq, 
        text="¡Bienvenido al Sistema!", 
        font=("Arial", 14, "bold"), 
        bg="white", 
        fg="#333"
    )
    lbl_bienvenida.pack(side="top", pady=5)

    # Botón fijado abajo
    btn_cargar_foto = tk.Button(
        frame_izq, 
        text="📷 Cambiar Logo del Negocio", 
        font=("Arial", 10, "bold"), 
        bg="#607D8B", 
        fg="white", 
        cursor="hand2",
        command=lambda: seleccionar_y_guardar_imagen()
    )
    btn_cargar_foto.pack(side="bottom", fill="x", pady=5)

    # Label para la imagen ocupando TODO el centro sobrante
    lbl_img = tk.Label(frame_izq, bg="white")
    lbl_img.pack(side="top", fill="both", expand=True, pady=5)

    # Función para ajustar y escalar la imagen dinámicamente al tamaño del cuadro
    def redimensionar_y_mostrar(event=None):
        if os.path.exists(ruta_logo):
            try:
                # Obtener el ancho y alto disponible en tiempo real
                ancho = lbl_img.winfo_width()
                alto = lbl_img.winfo_height()

                if ancho < 50 or alto < 50:
                    ancho, alto = 380, 380

                img_original = Image.open(ruta_logo)
                img_resized = img_original.resize((ancho, alto), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img_resized)

                lbl_img.config(image=photo, text="")
                lbl_img.image = photo
            except Exception as e:
                lbl_img.config(text=f"Error al cargar imagen:\n{e}", image="", fg="red")
        else:
            lbl_img.config(
                text="🛒\n\n[Sin Logo Seleccionado]\nHaz clic en 'Cambiar Logo'\npara subir uno desde tu PC.", 
                font=("Arial", 10), 
                fg="#888",
                image=""
            )

    # Evento para reescalar la imagen automáticamente al cambiar el tamaño de la ventana
    lbl_img.bind("<Configure>", redimensionar_y_mostrar)

    def seleccionar_y_guardar_imagen():
        tipos_archivo = [("Archivos de Imagen", "*.png *.jpg *.jpeg *.bmp *.gif")]
        archivo_seleccionado = filedialog.askopenfilename(
            title="Seleccionar Logo del Mini Market",
            filetypes=tipos_archivo
        )

        if archivo_seleccionado:
            try:
                shutil.copy(archivo_seleccionado, ruta_logo)
                redimensionar_y_mostrar()
                messagebox.showinfo("¡Éxito!", "El logo del negocio se actualizó correctamente.", parent=ventana_menu)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar la imagen: {e}", parent=ventana_menu)

    # --- COLUMNA DERECHA: BOTONES DE NAVEGACIÓN ---
    frame_der = tk.Frame(body, bg="#f5f5f5")
    frame_der.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    def ir_a_clientes():
        from vistas.clientes import mostrar_clientes
        mostrar_clientes()

    def ir_a_productos():
        from vistas.productos import mostrar_productos
        mostrar_productos()

    def ir_a_ventas():
        from vistas.ventas import mostrar_ventas
        mostrar_ventas()

    def ir_a_cuentas():
        from vistas.cuentas import mostrar_cuentas
        mostrar_cuentas()

    def ir_a_reportes():
        from vistas.reportes import mostrar_reportes
        mostrar_reportes()

    opciones = [
        ("👥  Gestión de Clientes", ir_a_clientes, "#4CAF50"),
        ("📦  Gestión de Productos", ir_a_productos, "#FF9800"),
        ("🛒  Punto de Venta (Facturación)", ir_a_ventas, "#00BCD4"),
        ("💳  Cuentas por Cobrar", ir_a_cuentas, "#E91E63"),
        ("📊  Consultas y Reportes", ir_a_reportes, "#9C27B0")
    ]

    for texto, comando, color in opciones:
        btn = tk.Button(
            frame_der, 
            text=texto, 
            font=("Arial", 11, "bold"), 
            bg=color, 
            fg="white", 
            activebackground="#333", 
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=comando
        )
        btn.pack(fill="x", pady=8, ipady=8)

    # 3. PIE DE PÁGINA
    footer = tk.Frame(ventana_menu, bg="#e0e0e0", pady=5)
    footer.pack(fill="x", side="bottom")

    lbl_footer = tk.Label(
        footer, 
        text="Mini Market System v2.0 - Universidad UFHEC", 
        font=("Arial", 8), 
        bg="#e0e0e0", 
        fg="#666"
    )
    lbl_footer.pack()

    ventana_menu.mainloop()