import tkinter as tk
from tkinter import messagebox
def validar_login(ventana_login, abrir_menu_callback):
    usuario = txt_usuario.get().strip()
    contrasena = txt_contrasena.get().strip()
    
    # 2. Comprobamos si dejó alguna caja vacía
    if usuario == "" or contrasena == "":
        messagebox.showwarning(" Atención", "Por favor, ingrese usuario y contraseña.")
        return
    # 3. Comprobamos si los datos son correctos (datos de prueba)
    if usuario == "admin" and contrasena == "1234":
        messagebox.showinfo("Éxito", "¡Bienvenido al Sistema Mini Market!")
        ventana_login.destroy() # Esta instrucción CIERRA la ventanita de login
        abrir_menu_callback() # Esta instrucción ABRE el menú principal
        
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
#CREACION DE LAS VENTANAS    
def mostrar_login(abrir_menu_callback):
    # Hacemos que estas dos variables se puedan usar dentro de la función de validar
    global txt_usuario, txt_contrasena

    # 1. Creación y configuración de la ventana
    ventana = tk.Tk()
    ventana.title("Mini Market - Inicio de Sesión")  
    ventana.geometry("400x350")
    ventana.resizable(True, True )
    
    # 2. Título principal en la ventana
    titulo = tk.Label(
        ventana,
        text="MINI MARKET",
        font=("Arial", 18, "bold")
    )
    titulo.pack(pady=20)
    
    # 3. Etiqueta y Caja de texto para el Usuario
    lbl_usuario = tk.Label(ventana, text="Usuario:", font=("Arial", 11))
    lbl_usuario.pack (anchor="w", padx=50)
    
    txt_usuario = tk.Entry(ventana, width=30, font=("Arial", 11))
    txt_usuario.pack(pady=5)
    
    # 4. Etiqueta y Caja de texto para la Contraseña
    lbl_contrasena = tk.Label(ventana, text="Contraseña:", font=("Arial", 11))
    lbl_contrasena.pack(anchor="w", padx=50)
    
    txt_contrasena = tk.Entry(ventana, width=30, font=("Arial", 11), show="*")
    txt_contrasena.pack(pady=5)
    
    # 5. Botón de Iniciar Sesión
    btn_ingresar = tk.Button(
        ventana, 
        text= "Iniciar Sesión",
        font=("Arial", 11, "bold"),
        bg="#4CAF50",
        fg="white",
        width= 18,
        command= lambda: validar_login(ventana, abrir_menu_callback)
        
    ) 
    btn_ingresar.pack(pady=25)   
    # 6. Mantiene la ventana abierta esperando que el usuario haga clic
    ventana.mainloop()                      
     
    