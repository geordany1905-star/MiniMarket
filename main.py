from database.database import crear_tablas
from vistas.login import mostrar_login
from vistas.menu import abrir_menu

def main():
    # Inicializa las tablas de la base de datos si no existen
    crear_tablas()


    # Inicia la aplicación mostrando primero el Login.
    # Si la contraseña es correcta, llamará automáticamente a 'abrir_menu'.
    mostrar_login(abrir_menu)

if __name__ == '__main__':
    main()