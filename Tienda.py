import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFormLayout, QLineEdit, QStackedWidget, QMainWindow, QHBoxLayout,QTableWidget,QSizePolicy, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import Qt,QSize
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtGui import QIcon
from fpdf import FPDF
from datetime import datetime
import sqlite3

# Ventana para gestionar productos----

class VProductos(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel('Gestionar Productos')
        label.setAlignment(Qt.AlignCenter)  # esto es para  centrar el texto
        layout.addWidget(label)# esto es para agregar el label a la ventana

        # Formulario con campos de la ventana productos
        form_layout = QFormLayout()
        self.id_input = QLineEdit()
        self.id_input.setFixedSize(500, 40)
        form_layout.addRow('ID del Producto:', self.id_input)
        self.nombre_input = QLineEdit() # esto es para  crear un campo de texto
        self.nombre_input.setFixedSize(500, 40)# esto es para darle un tamaño a la caja de texto
        form_layout.addRow('Nombre del Producto:', self.nombre_input)# esto es para agragar el campo de texto al formulario
        self.precio_input = QLineEdit()
        self.precio_input.setFixedSize(500, 40)
        form_layout.addRow('Precio: $', self.precio_input)
        layout.addLayout(form_layout)# esto es para agregar el formulario a la ventana
        self.descripcion_input = QLineEdit()  # Campo para la descripción
        self.descripcion_input.setFixedSize(500, 40)
        form_layout.addRow('Descripción:', self.descripcion_input)

        self.cantidad_input = QLineEdit()  # Campo para la cantidad
        self.cantidad_input.setFixedSize(500, 40)
        form_layout.addRow('Cantidad:', self.cantidad_input)

        layout.addLayout(form_layout)

        # Layout para los botones
        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignCenter)# esto centra los botones

        self.btn_new_product = QPushButton('Nuevo')
        self.btn_new_product.setFixedSize(150, 40)
        self.btn_add_product = QPushButton('Agregar') # esto es para crear un boton
        self.btn_add_product.setFixedSize(150, 40)# esto es para darle un tamaño al boton
        self.btn_del_product = QPushButton('Eliminar')
        self.btn_del_product.setFixedSize(150, 40)

        btn_layout.addWidget(self.btn_new_product)
        btn_layout.addWidget(self.btn_add_product)# esto es para  agregar el boton a la ventana
        btn_layout.addWidget(self.btn_del_product)# 

        btn_layout.setContentsMargins(10, 10, 10, 10)
        btn_layout.setSpacing(60)#  esto es para darle un espacio entre los botones
        layout.addLayout(btn_layout)

        # Tabla para mostrar productos
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['ID', 'Nombre', 'Precio', 'Descripcion','Cantidad'])
        layout.addWidget(self.table)

        self.setLayout(layout)# 

        # Definir los estilos la ventana
        self.setStyleSheet("""
            QWidget {
                background-color:;
            }
            QLabel {
                color: white;
                font-size: 18px;
                font-weight: bold;
            }
            QLineEdit {
                padding: 10px;
                border-radius: 10px;
                border: 2px solid #918dd0 ;
                font-size: 16px;
            }               
            QPushButton {
                background-color: #918dd0;
                color: white;
                padding: 10px;
                border-radius: 10px;
                border: none;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #908af2;
            }
            QPushButton:pressed {
                background-color: #1a5276;
            }
        """)
        self.btn_new_product.clicked.connect(self.limpiar_campos)
        self.btn_add_product.clicked.connect(self.agregar_producto)
        self.btn_del_product.clicked.connect(self.eliminar_producto)
        self.table.cellClicked.connect(self.seleccionar_producto)

        self.cargar_productos()

    def cargar_productos(self):

        """Cargar productos desde la base de datos en la tabla."""

        conn = sqlite3.connect('Latiendita.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, nombre, precio, descripcion, cantidad FROM productos')
        productos = cursor.fetchall()
        conn.close()

        self.table.setRowCount(0)  # Limpiar la tabla
        for producto in productos:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            for column, data in enumerate(producto):
                self.table.setItem(row_position, column, QTableWidgetItem(str(data)))

#funcion para seleccionar los campos
    def seleccionar_producto(self, row, column):
        """Seleccionar producto de la tabla y llenar los campos de entrada."""
        self.id_input.setText(self.table.item(row, 0).text())
        self.nombre_input.setText(self.table.item(row, 1).text())
        self.precio_input.setText(self.table.item(row, 2).text())
        self.descripcion_input.setText(self.table.item(row, 3).text())
        self.cantidad_input.setText(self.table.item(row, 4).text())


    def mostrar_mensaje(self, mensaje):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(mensaje)
        msg.setWindowTitle("Notificación")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


  #funcion para agregar productos  

    def agregar_producto(self):
        id = self.id_input.text()
        nombre = self.nombre_input.text()
        precio = self.precio_input.text()
        descripcion = self.descripcion_input.text()
        cantidad = self.cantidad_input.text()

        if nombre and precio and  descripcion and cantidad:
            try:
                precio = float(precio)  # Convertir a float
                cantidad = int(cantidad)  # Convertir a int
                conn = sqlite3.connect('Latiendita.db')
                cursor = conn.cursor()
                cursor.execute('INSERT INTO productos (nombre, precio, descripcion, cantidad) VALUES (?, ?, ?, ?)', (nombre, precio, descripcion, cantidad))
                conn.commit()
                conn.close()
                self.limpiar_campos()
                self.mostrar_mensaje("Producto agregado")               
                self.cargar_productos()

            except Exception as e:
                print("Error al agregar producto:", e)
                self.mostrar_mensaje(f"Error al agregar producto: {e}")
        else:
            self.mostrar_mensaje("Por favor, complete todos los campos.")

#funcion para limpiar los campos
    def limpiar_campos(self):
        self.nombre_input.clear()
        self.precio_input.clear()
        self.descripcion_input.clear()
        self.cantidad_input.clear()

#funcion para mostrar la notificacion
    def mostrar_mensaje(self, mensaje):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText(mensaje)
            msg.setWindowTitle("Notificacion")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

#funcion para eliminar productos de la base de datos
    def eliminar_producto(self):
            id_producto = self.id_input.text()


            if id_producto:
                try:
                    conn = sqlite3.connect('Latiendita.db')
                    cursor = conn.cursor()
                    cursor.execute('DELETE FROM productos WHERE id = ?', (id_producto,))
                    conn.commit()
                    conn.close()
                    self.mostrar_mensaje("Producto eliminado correctamente.")
                    self.cargar_productos()
                    self.id_input.clear()
                except Exception as e:
                    print("Error al eliminar producto:", e)
                    self.mostrar_mensaje("Error al eliminar el producto.")
            else:
                self.mostrar_mensaje("Por favor, ingrese el ID del producto a eliminar.")


class VVentas(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QWidget {
                background-color: #ceb2f9;  
            }
            QLabel {
                color: white;
                font-size: 18px;
                font-weight: bold;
            }
            QLineEdit {
                padding: 10px;
                border-radius: 10px;
                border: 2px solid #918dd0;
                font-size: 16px;
            }               
            QPushButton {
                background-color: #918dd0;
                color: white;
                padding: 10px;
                border-radius: 10px;
                border: none;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #908af2;
            }
            QPushButton:pressed {
                background-color: #1a5276;
            }
            QTableWidget {
                background-color: #ceb2f9;  
                color: white;  
                font-size: 16px;
            }
            QHeaderView::section {
                background-color: #918dd0;  
                color: white;  
                font-size: 16px;
                font-weight: bold;
            }
        """)

        l_principal = QHBoxLayout(self)

        # Sección de búsqueda y tabla de productos
        seccion_productos = QVBoxLayout()
        
        titulo = QLabel("Punto de Venta")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 18px; font-weight: bold;")
        seccion_productos.addWidget(titulo)

        self.b_busqueda = QLineEdit()
        self.b_busqueda.setPlaceholderText("Buscar producto...")
        self.b_busqueda.setFixedHeight(40)
        self.b_busqueda.textChanged.connect(self.filtrar_tabla)
        seccion_productos.addWidget(self.b_busqueda)

        self.tab_productos = QTableWidget(0, 4)
        self.tab_productos.setHorizontalHeaderLabels(["Id", "Nombre", "Precio", "Descripción"])
        seccion_productos.addWidget(self.tab_productos)

        # Botón para agregar productos
        self.btn_agr_producto = QPushButton("Agregar Producto")
        self.btn_agr_producto.clicked.connect(self.agregar_producto)
        seccion_productos.addWidget(self.btn_agr_producto)

        l_principal.addLayout(seccion_productos)

        # Sección de productos seleccionados
        seccion_seleccionados = QVBoxLayout()

        titulo_seleccionados = QLabel("Productos Seleccionados")
        titulo_seleccionados.setAlignment(Qt.AlignCenter)
        titulo_seleccionados.setStyleSheet("font-size: 18px; font-weight: bold;")
        seccion_seleccionados.addWidget(titulo_seleccionados)

        self.tab_seleccionados = QTableWidget(0, 4)
        self.tab_seleccionados.setHorizontalHeaderLabels(["Id", "Nombre", "Cantidad", "Precio"])
        seccion_seleccionados.addWidget(self.tab_seleccionados)

        # Botón para generar factura
        self.btn_g_factura = QPushButton("Generar Factura")
        self.btn_g_factura.clicked.connect(self.generar_factura)
        seccion_seleccionados.addWidget(self.btn_g_factura)

        l_principal.addLayout(seccion_seleccionados)

        # Cargar productos
        self.cargar_productos()

    def cargar_productos(self):
        try:
            conn = sqlite3.connect('Latiendita.db')
            cursor = conn.cursor()
            cursor.execute('SELECT id, nombre, precio, descripcion FROM productos')
            productos = cursor.fetchall()
            self.tab_productos.setRowCount(len(productos))
            
            for row_index, row_data in enumerate(productos):
                for column_index, item in enumerate(row_data):
                    self.tab_productos.setItem(row_index, column_index, QTableWidgetItem(str(item)))
            
            conn.close()
        except Exception as e:
            self.mostrar_mensaje(f"Error al cargar productos: {e}")

#filtrar productos para la barra de busqueda

    def filtrar_tabla(self):
        texto_busqueda = self.b_busqueda.text().lower()
        for row in range(self.tab_productos.rowCount()):
            item = self.tab_productos.item(row, 1)  # Columna "Nombre"
            self.tab_productos.setRowHidden(row, texto_busqueda not in item.text().lower())

#funcion para agregar productos
    def agregar_producto(self):
        fila = self.tab_productos.currentRow()
        if fila == -1:
            self.mostrar_mensaje("Por favor, selecciona un producto.")
            return

        id_producto = self.tab_productos.item(fila, 0).text()
        nombre = self.tab_productos.item(fila, 1).text()
        precio = float(self.tab_productos.item(fila, 2).text())

        # Verificar si el producto ya está en la tabla de seleccionados
        for row in range(self.tab_seleccionados.rowCount()):
            if self.tab_seleccionados.item(row, 0).text() == id_producto:
                cantidad_actual = int(self.tab_seleccionados.item(row, 2).text())
                self.tab_seleccionados.setItem(row, 2, QTableWidgetItem(str(cantidad_actual + 1)))
                return

        # Agregar nuevo producto a la tabla de seleccionados
        row_count = self.tab_seleccionados.rowCount()
        self.tab_seleccionados.insertRow(row_count)
        self.tab_seleccionados.setItem(row_count, 0, QTableWidgetItem(id_producto))
        self.tab_seleccionados.setItem(row_count, 1, QTableWidgetItem(nombre))
        self.tab_seleccionados.setItem(row_count, 2, QTableWidgetItem("1"))  # Cantidad inicial
        self.tab_seleccionados.setItem(row_count, 3, QTableWidgetItem(f"{precio:.2f}"))

#funcin para generar la factura
    def generar_factura(self):
        if self.tab_seleccionados.rowCount() == 0:
            self.mostrar_mensaje("No hay productos seleccionados para generar una factura.")
            return

        try:
            # Crear el objeto PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            pdf.image("c:/Users/lenovo/Downloads/SVG/gift-shop.png", x=10, y=8, w=30)
            pdf.ln(10)
            # Título

            pdf.set_font("Arial", style="B", size=16)
            pdf.cell(200, 10, txt="La Tiendita", ln=True, align="C")
            pdf.ln(10)  # Espacio en blanco

            pdf.set_font("Arial", style="B", size=16)
            pdf.cell(200, 10, txt="Factura", ln=True, align="C")
            pdf.ln(10)  

            # Fecha 
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"Fecha de Emision: {fecha}", ln=True, align="L")
            pdf.cell(200, 10, txt="Tipo de Documento: Factura", ln=True, align="L")
            pdf.ln(10)

            pdf.set_font("Arial", style="B", size=12)
            pdf.cell(40, 10, "RECEPTOR", ln=True, align="L")
            pdf.ln(5)

            pdf.set_font("Arial", size=10)
            pdf.cell(50, 10, "Nombre:", 1)
            pdf.cell(140, 10, "No registrado", 1)
            pdf.ln()
            
            pdf.cell(50, 10, "DUI:", 1)
            pdf.cell(140, 10, "0000000-0", 1)
            pdf.ln()
            pdf.cell(50, 10, "Dirección:", 1)
            pdf.cell(140, 10, "Colonia no registrada, calle 123 ", 1)
            pdf.ln(10)


            # Tabla de productos
            pdf.set_font("Arial", style="B", size=12)
            pdf.cell(40, 10, "ID", 1)
            pdf.cell(80, 10, "Descripción", 1)
            pdf.cell(30, 10, "Cantidad", 1)
            pdf.cell(40, 10, "Precio", 1)
            pdf.ln()

            total = 0
            for row in range(self.tab_seleccionados.rowCount()):
                try:
                    id_producto = self.tab_seleccionados.item(row, 0).text()
                    nombre = self.tab_seleccionados.item(row, 1).text()
                    cantidad = self.tab_seleccionados.item(row, 2).text()
                    precio = self.tab_seleccionados.item(row, 3).text()
 
                    if not (id_producto and nombre and cantidad and precio):
                        raise ValueError("Faltan datos en una de las filas.")

                    pdf.set_font("Arial", size=12)
                    pdf.cell(40, 10, id_producto, 1)
                    pdf.cell(80, 10, nombre, 1)
                    pdf.cell(30, 10, cantidad, 1)
                    pdf.cell(40, 10, precio, 1)
                    pdf.ln()

                    total += float(precio) * int(cantidad)
                except Exception as e:
                    self.mostrar_mensaje(f"Error al procesar la fila {row + 1}: {e}")
                    continue

            # Total
            pdf.set_font("Arial", style="B", size=12)
            pdf.cell(150, 10, "Total:", 1, align="R")
            pdf.cell(40, 10, f"${total:.2f}", 1, align="R")

            # Guardar el archivo
            nombre_archivo = f"Factura_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            pdf.output(nombre_archivo)
            self.mostrar_mensaje(f"Factura generada exitosamente: {nombre_archivo}")

        except Exception as e:
            self.mostrar_mensaje(f"Error general al generar la factura: {e}")

    def mostrar_mensaje(self, mensaje):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText(mensaje)
        msg_box.setWindowTitle("Información")
        msg_box.exec_()

    # inicio----
class Inicio(QWidget):
        def __init__(self):
            super().__init__()
            layout = QVBoxLayout()

            label = QLabel('Bienvenido a la Administración de la Tienda')
            label.setAlignment(Qt.AlignCenter)  
            layout.addWidget(label)
            self.setLayout(layout)
            layout.addStretch()

            
        
'''
        def _crear_botones_inicio(self):
            # Layout para los botones
            botones_layout = QHBoxLayout()

            # Botón de "Usuario"
            self.btn_usuario = QPushButton()
            self.btn_usuario.setIcon(QIcon('ruta/a/imagen_usuario.png'))  # Cambia esta ruta por la de tu imagen
            self.btn_usuario.setIconSize(QSize(100, 100))  # Tamaño de la imagen
            self.btn_usuario.setFixedSize(120, 120)  # Tamaño cuadrado del botón
            self.btn_usuario.setStyleSheet("background-color: transparent; border: none;")  # Botón sin borde ni fondo

            # Botón de "Productos"
            self.btn_productos = QPushButton()
            self.btn_productos.setIcon(QIcon('ruta/a/imagen_productos.png'))  # Cambia esta ruta por la de tu imagen
            self.btn_productos.setIconSize(QSize(100, 100))  # Tamaño de la imagen
            self.btn_productos.setFixedSize(120, 120)  # Tamaño cuadrado del botón
            self.btn_productos.setStyleSheet("background-color: transparent; border: none;")  # Botón sin borde ni fondo

            # Botón de "Ventas"
            self.btn_ventas = QPushButton()
            self.btn_ventas.setIcon(QIcon('ruta/a/imagen_ventas.png'))  # Cambia esta ruta por la de tu imagen
            self.btn_ventas.setIconSize(QSize(100, 100))  # Tamaño de la imagen
            self.btn_ventas.setFixedSize(120, 120)  # Tamaño cuadrado del botón
            self.btn_ventas.setStyleSheet("background-color: transparent; border: none;")  # Botón sin borde ni fondo

            # Añadir los botones al layout horizontal
            botones_layout.addStretch(1)  # Añadir espacio antes de los botones
            botones_layout.addWidget(self.btn_usuario)
            botones_layout.addWidget(self.btn_productos)
            botones_layout.addWidget(self.btn_ventas)
            botones_layout.addStretch(1)  # Añadir espacio después de los botones

'''


 # factura
class FacturaPDF(FPDF):
    def __init__(self, vendedor, cliente, productos):
        super().__init__()
        self.vendedor = vendedor
        self.cliente = cliente
        self.productos = productos
        self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.numero_factura = self.generar_numero_factura()

    def generar_numero_factura(self):
        return str(int(datetime.now().timestamp()))  # Número de factura basado en el tiempo actual

    def calcular_totales(self):
        subtotal = sum(prod['precio'] * prod['cantidad'] for prod in self.productos)
        impuestos = subtotal * 0.16  # 16% de IVA
        total = subtotal + impuestos
        return subtotal, impuestos, total

    def generar_factura_pdf(self):
        subtotal, impuestos, total = self.calcular_totales()
        self.add_page()
        
        
        # Información del vendedor
        self.set_font("Arial", 'B', 12)
        self.cell(0, 10, 'Factura', 0, 1, 'C')
        self.set_font("Arial", '', 12)
        self.cell(0, 10, f'Factura No: {self.numero_factura}', 0, 1)
        self.cell(0, 10, f'Fecha: {self.fecha}', 0, 1)
        self.cell(0, 10, f'Vendedor: {self.vendedor["nombre"]}', 0, 1)
        self.cell(0, 10, f'Dirección: {self.vendedor["direccion"]}', 0, 1)
        self.cell(0, 10, f'Teléfono: {self.vendedor["telefono"]}', 0, 1)
        self.cell(0, 10, f'Correo: {self.vendedor["correo"]}', 0, 1)
        self.cell(0, 10, '', 0, 1)  # Espacio en blanco
        
        # Información del cliente
        self.cell(0, 10, f'Cliente: {self.cliente["nombre"]}', 0, 1)
        self.cell(0, 10, f'Dirección: {self.cliente["direccion"]}', 0, 1)
        self.cell(0, 10, f'Teléfono: {self.cliente["telefono"]}', 0, 1)
        self.cell(0, 10, '', 0, 1)  # Espacio en blanco

        # Detalles de productos
        self.cell(0, 10, 'Productos:', 0, 1)
        self.set_font("Arial", '', 10)
        for prod in self.productos:
            self.cell(0, 10, f"{prod['nombre']} - Cantidad: {prod['cantidad']} - Precio: ${prod['precio']:.2f} - Total: ${prod['precio'] * prod['cantidad']:.2f}", 0, 1)

        self.cell(0, 10, '', 0, 1)  # Espacio en blanco

        # Totales
        self.cell(0, 10, f'Subtotal: ${subtotal:.2f}', 0, 1)
        self.cell(0, 10, f'Impuestos: ${impuestos:.2f}', 0, 1)
        self.cell(0, 10, f'Total: ${total:.2f}', 0, 1)

        # Guardar el archivo
        self.output(f'factura_{self.numero_factura}.pdf')


class VPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('La Tiendita')
        self.setGeometry(100, 100, 800, 400)  # tamaño de la ventana

      

        self.setWindowIcon(QIcon("c:/Users/lenovo/Downloads/SVG/store.png"))  # Ruta al ícono

        # Inicializar la base de datos
        self.inicializar_bd_()

        layout = QVBoxLayout()    
        self.st_widget = QStackedWidget()
      
        #vistas
        self.v_inicio = Inicio()
        self.v_productos = VProductos()
        self.v_ventas = VVentas()

        
        self.st_widget.addWidget(self.v_inicio)
        self.st_widget.addWidget(self.v_productos)
        self.st_widget.addWidget(self.v_ventas)

        # layout para los botones
        botones_layout = QHBoxLayout()
        botones_layout.setContentsMargins(10, 10, 10, 10)  # margenes internos del layout (izquierda, arriba, derecha, abajo)
        botones_layout.setSpacing(90)  #

        #Agregar estilo
        self.setStyleSheet("background-color:  #dfddff;")
        self.btn_inicio = QPushButton('Inicio')
        self.btn_inicio.setFixedSize(150, 40)
        self.btn_inicio.setStyleSheet ("""
            QPushButton {
                background-color: #a39ef0 ;
                color: white;
                border: 2px solid #918dd0 ;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #908af2 ;
            }
            QPushButton:pressed {
                background-color: #7f78f0;
            }
        """)
        self.btn_inicio.clicked.connect(self.vista_inicio)        
        self.btn_productos = QPushButton('Productos')
        self.btn_productos.setFixedSize(150, 40)
        self.btn_productos.setStyleSheet ("""
            QPushButton {
                background-color: #a39ef0 ;
                color: white;
                border: 2px solid #918dd0 ;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #908af2 ;
            }
            QPushButton:pressed {
                background-color: #7f78f0;
            }
        """)
        self.btn_productos.clicked.connect(self.vista_productos)
        self.btn_ventas = QPushButton('Ventas')
        self.btn_ventas.setFixedSize(150, 40)
        self.btn_ventas.setStyleSheet ("""
            QPushButton {
                background-color: #a39ef0 ;
                color: white;
                border: 2px solid #918dd0 ;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #908af2 ;
            }
            QPushButton:pressed {
                background-color: #7f78f0;
            }
        """)
        self.btn_ventas.clicked.connect(self.vista_ventas)

        # añadir los botones al layout
        botones_layout.addStretch(1)
        botones_layout.addWidget(self.btn_inicio)
        botones_layout.addWidget(self.btn_productos)
        botones_layout.addWidget(self.btn_ventas)
        botones_layout.addStretch(1)

        # añadir el stacked_widget y el layout de botones al layout principal
        layout.addWidget(self.st_widget)
        layout.addLayout(botones_layout)

        # crear un widget central para la ventana principal
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # muetrar la pantalla de inicio por defecto
        self.vista_inicio()

    def inicializar_bd_(self):
        self.conn = sqlite3.connect('Latiendita.db')
        self.cursor = self.conn.cursor()

        # Crear tabla de productos 
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                precio FLOAT NOT NULL,
                cantidad INTEGER NOT NULL
            )
        ''')
        self.conn.commit()



    # funciones para mostrar las vistas
    def vista_inicio(self):
        self.st_widget.setCurrentIndex(0)

    def vista_productos(self):
        self.st_widget.setCurrentIndex(1)

    def vista_ventas(self):
        self.v_ventas.cargar_productos() 
        self.st_widget.setCurrentIndex(2)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # se crea y se muestra la ventana principal
    ventana = VPrincipal()
    ventana.show()

    sys.exit(app.exec_())
