import sqlite3
import csv
import os

def crear_tablas():
    conexion = sqlite3.connect("minimarket.db")
    cursor = conexion.cursor()

    # 1. Tabla Clientes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cedula TEXT UNIQUE NOT NULL,
            nombre TEXT NOT NULL,
            telefono TEXT,
            direccion TEXT
        )
    ''')

    # 2. Tabla Productos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE NOT NULL,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    ''')

    # 3. Tabla Ventas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            fecha TEXT DEFAULT CURRENT_TIMESTAMP,
            total REAL NOT NULL,
            FOREIGN KEY (cliente_id) REFERENCES clientes (id)
        )
    ''')

    # 4. Tabla Detalle Ventas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS detalle_ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            venta_id INTEGER,
            producto_id INTEGER,
            cantidad INTEGER NOT NULL,
            precio_unitario REAL NOT NULL,
            subtotal REAL NOT NULL,
            FOREIGN KEY (venta_id) REFERENCES ventas (id),
            FOREIGN KEY (producto_id) REFERENCES productos (id)
        )
    ''')

    # 5. Tabla Cuentas por Cobrar
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cuentas_por_cobrar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            monto_pendiente REAL NOT NULL,
            estado TEXT DEFAULT 'Pendiente',
            FOREIGN KEY (cliente_id) REFERENCES clientes (id)
        )
    ''')

    conexion.commit()
    
    # IMPORTACIÓN MASIVA DESDE EL ARCHIVO CSV
    cursor.execute("SELECT COUNT(*) FROM productos")
    cantidad_actual = cursor.fetchone()[0]

    archivo_csv = "productos_minimarket.csv"
    if cantidad_actual == 0 and os.path.exists(archivo_csv):
        try:
            with open(archivo_csv, mode="r", encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader)  # Saltar encabezado

                for fila in reader:
                    if len(fila) == 4:
                        cod, nom, prec, stck = fila
                        cursor.execute('''
                            INSERT OR IGNORE INTO productos (codigo, nombre, precio, stock)
                            VALUES (?, ?, ?, ?)
                        ''', (cod, nom, float(prec), int(stck)))
            
            conexion.commit()
            print("¡Éxito! Se cargaron los 100 productos desde el CSV.")
        except Exception as e:
            print(f"Error al leer el CSV: {e}")

    conexion.close()

def obtener_conexion():
    return sqlite3.connect("minimarket.db")