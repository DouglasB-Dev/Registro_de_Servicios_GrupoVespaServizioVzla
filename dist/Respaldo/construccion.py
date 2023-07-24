#primero llamamos a la libreria Tkinter para crear aplicaciones de escritorio, e importamos todos los widgets con "*"
import babel.numbers
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import *
from tkcalendar import DateEntry
import os
import shutil
import datetime
import time
from fpdf import FPDF
from PIL import Image, ImageTk
from tkinter.font import Font
import sqlite3

login = Tk()
login.title("Grupo Vespa Servizio Vzla 3110 C.A - Login")
login.geometry("800x600")
login.resizable(0, 0)
login.iconbitmap('Source/logo.ico')

top_login = Frame(login)
top_login.pack(expand=False, fill="x", side="top")
top_login.config(bg="#3b3b3b", height=100, width=100)

login_centro = Frame(login)
login_centro.pack(expand=True, fill="both", side="bottom")
login_centro.config(padx=120, pady=50)


# definir las etiquetas y campos de entrada para el nombre de usuario y la contraseña
username_label = Label(login_centro, text="Nombre de usuario:", font=64)
username_label.pack(pady=20)

username_entry = Entry(login_centro)
username_entry.pack(pady=20)

password_label = Label(login_centro, text="Contraseña:", font=64)
password_label.pack(pady=20)

password_entry = Entry(login_centro, show="*")
password_entry.pack(pady=20)

# Titulo de inicio de sesión
mi_fuente = Font(size=16, family="Arial")
titulo_login = Label(top_login, text="Iniciar Sesión", fg="white", bg="#3b3b3b", height=3, font=mi_fuente)
titulo_login.pack(pady=10, padx=10, ipady=10, ipadx=10, fill="both", expand=True, anchor=tk.CENTER)


def respaldo_automatico():
    # RESPALDO AUTOMATICO CADA 24 HORAS

    # nombre del archivo de la base de datos original
    source_file = "grupovespa.db"

    # ruta donde se guardarán las copias de la base de datos
    backup_folder = os.path.join(os.getcwd(), "Backup")

    # eliminar todos los backups antiguos para evitar llenar el disco
    for backup in os.listdir(backup_folder):
        backup_path = os.path.join(backup_folder, backup)
        os.remove(backup_path)

    # crear la carpeta de respaldo si no existe
    if not os.path.exists(backup_folder):
        os.mkdir(backup_folder)

    # generar una marca de tiempo para el nombre del backup
    timestamp = datetime.datetime.now().strftime('%Y_%m_%d')

    # crear la ruta de archivo para la copia de seguridad
    backup_path = os.path.join(backup_folder, f"{source_file.replace('.db', '')}_{timestamp}.db")

    # crear una copia de la base de datos original en la carpeta de respaldos
    shutil.copy(source_file, backup_path)

respaldo_automatico()

def logeo():
#creamos la conexion a la base de datos
    conexion = sqlite3.connect("grupovespa.db")
    cursor = conexion.cursor()

    usuario = username_entry.get()
    clave = password_entry.get()
    
    consulta = "SELECT * FROM usuarios WHERE nombre_usuario = ? AND clave_usuario = ?"
    valores = (usuario, clave)
    cursor.execute(consulta, valores)
    resultado = cursor.fetchone()
# cerrar la conexión a la base de datos
    conexion.close()

    if resultado:
        login.destroy()
        inicio()

    else:
        tk.messagebox.showerror("Error", "El usuario no existe"),

def salir():
    login.destroy()


# botón de inicio de sesión
login_button = Button(login_centro, text="Iniciar sesión", command=logeo, font=64, bg="#212F3D", fg="white")
login_button.pack(pady=20)
password_entry.bind('<Return>', lambda event: login_button.invoke())

salir_button = Button(login_centro, text="Salir", command=salir, font=64, width=8, bg="#212F3D", fg="white")
salir_button.pack(pady=20)

def inicio():
    #creamos la ventana, asignamos un tamaño y un titulo
    ventana = Tk()
    ventana.title("Grupo Vespa Servizio Vzla 3110 C.A - RIF:J-412020943")
    ventana.geometry("800x600")
    ventana.resizable(0, 0)
    ventana.iconbitmap('Source/logo.ico')

    #creamos las funciones que utilizaresmos previamente

    def consultar():

        for widget in centro.winfo_children():
            widget.destroy()

        def validar_longitud_matricula(valor):
            if len(valor) <= 8:
                return True
            else:
                return False 

        def buscar_cliente():

            tree.delete(*tree.get_children())
            tree2.delete(*tree2.get_children())
            boton_servicio_nuevo.config(state="disabled")

            boton_buscar_presionado.insert(tk.END, "Presionado")

            conexion = sqlite3.connect("grupovespa.db")
            cursor = conexion.cursor()

        # Ejecutar consulta
            id_cliente = entry_id_cliente_busqueda.get()
            consulta = "SELECT vehiculos.matricula, vehiculos.tipo, vehiculos.modelo, vehiculos.color, estatus.nombre_estatus, vehiculos.id_cliente FROM vehiculos INNER JOIN estatus ON vehiculos.estatus = estatus.id_estatus WHERE vehiculos.id_cliente = ?"
            cursor.execute(consulta, (id_cliente,))
            resultados = cursor.fetchall()
            entry_id_cliente_busqueda.delete(0, tk.END)

        # Mostrar resultado en Treeview
            tree.delete(*tree.get_children())

            conexion.close()
            
            if resultados:
                for resultado in resultados:
                    tree.insert("", "end", values=resultado)
            else:

                if id_cliente.strip() == "":
                    tk.messagebox.showinfo("Error", "El campo de identificación se encuentra vacío.")
                else:
                    conexion = sqlite3.connect("grupovespa.db")
                    cursor = conexion.cursor()

                    cursor.execute('SELECT id_cliente FROM clientes WHERE clientes.id_cliente = ?', (id_cliente,))
                    existe_cliente = cursor.fetchone()

                    conexion.close()

                    if not existe_cliente:
                        respuesta_consulta = tk.messagebox.askyesno("Cliente no existe", f"No se encontró un cliente con la identificación: {id_cliente}  ¿desea agregarlo?")
                        if respuesta_consulta == True:
                            registro()
                        else:
                            pass
                    else:   
                        respuesta_consulta2 = tk.messagebox.askyesno("Vehiculo no encontrado", f"No se encontró ningun vehiculo asociado a la identificacion: {id_cliente}¿desea agregarlo?")
                        if respuesta_consulta2 == True:
                            registro()
                        else:
                            pass

        def filtrar_vehiculo(event):
            # Obtener el texto ingresado en el Entry
            id_cliente = event.widget.get()

            # Limpiar Treeview
            tree.delete(*tree.get_children())

            conexion = sqlite3.connect("grupovespa.db")
            cursor = conexion.cursor()
            # Realizar consulta SQL con filtro de texto en la columna 'id_cliente'
            cursor.execute(f"SELECT vehiculos.matricula, vehiculos.tipo, vehiculos.modelo, vehiculos.color, estatus.nombre_estatus, vehiculos.id_cliente FROM vehiculos INNER JOIN estatus ON vehiculos.estatus = estatus.id_estatus WHERE vehiculos.id_cliente LIKE '%{id_cliente}%'")
            datos_filtrados = cursor.fetchall()
            
            # Agregar los datos filtrados al Treeview
            for resultado in datos_filtrados:
                tree.insert("", "end", values=resultado)

        def vehiculo_seleccionado(event):
            tree2.delete(*tree2.get_children())
            boton_servicio_nuevo.config(state="normal")
            
            conexion = sqlite3.connect("grupovespa.db")
            cursor = conexion.cursor()    

            item1 = tree.selection()[0]
            matricula = tree.item(item1)["values"][0]

            cursor.execute("SELECT id_servicio, antecedente, reparacion, precio, fecha_entrada, fecha_salida, matricula, id_cliente FROM servicios WHERE servicios.matricula = ?", (matricula,))
            resultados = cursor.fetchall()    

        # Mostrar resultado en Treeview
            conexion.close()
            
            if resultados:
                for resultado in resultados:
                    tree2.insert("", "end", values=resultado)
            else:
                respuesta_servicio = tk.messagebox.askyesno("Cliente sin servicios", f"No se encontró ningún servicio de reparación asociado con la matricula: {matricula} ¿desea agregar un nuevo servicio?")
                if respuesta_servicio == True:
                        servicio_nuevo()
                else:
                    pass
                pass                 

        def mostrar_servicio(event):
            servicios = tk.Toplevel(ventana)
            servicios.title("Servicios")
            servicios.iconbitmap('Source/logo.ico')

            boton_servicio_nuevo.config(state="disabled")

            def guardar():
                guardar_antecedente = entry_antecedente.get("1.0", "end-1c")
                guardar_reparacion = entry_reparacion.get("1.0", "end-1c")
                guardar_precio = entry_precio.get()
                guardar_entrada = entry_entrada.get()
                guardar_salida = entry_salida.get()

                conexion = sqlite3.connect("grupovespa.db")
                cursor = conexion.cursor()

                if tree2.get_children():
                    item = tree2.selection()[0]
                    id_servicio = tree2.item(item)["values"][0]

                    cursor.execute("UPDATE servicios SET antecedente = ?, reparacion = ?, precio = ?, fecha_entrada = ?, fecha_salida = ? WHERE id_servicio = ?", (guardar_antecedente, guardar_reparacion, guardar_precio, guardar_entrada, guardar_salida, id_servicio))   
                    tk.messagebox.showinfo("Éxito", "Los datos del servicio han sido actualizados.")  

                else:
                    item1 = tree.selection()
                    datos = tree.item(item1)["values"]
                    
                    guardar_matricula = datos[0]
                    guardar_id_cliente = datos[5]

                    cursor.execute('INSERT INTO servicios (antecedente, reparacion, precio, fecha_entrada, fecha_salida, matricula, id_cliente) VALUES (?,?,?,?,?,?,?)', (guardar_antecedente, guardar_reparacion, guardar_precio, guardar_entrada, guardar_salida, guardar_matricula, guardar_id_cliente))
                    btn_guardar.config(state="disabled")
                    tk.messagebox.showinfo("Éxito", "Los datos del servicio han sido agregados.")

                conexion.commit()
                conexion.close()
                servicios.destroy()
                consultar()

            def salir_servicios():
                servicios.destroy()
                consultar() 

# Creacion de los widgets de Servicios

            antecedente = Label(servicios, text="Antecedentes: ")
            entry_antecedente = Text(servicios, height=5, width=30)
            reparacion = Label(servicios, text="Reparación: ")
            entry_reparacion = Text(servicios, height=5, width=30)
            precio = Label(servicios, text="Precio: ")
            entry_precio = Entry(servicios, width=9)
            entrada = Label(servicios, text="Entrada: ")
            entry_entrada = DateEntry(servicios, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
            salida = Label(servicios, text="Salida: ")
            entry_salida = DateEntry(servicios, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')

            btn_guardar = Button(servicios, text="Guardar", command=guardar, bg="#212F3D", fg="white")
            btn_salir = Button(servicios, text="Salir", command=salir_servicios, bg="#212F3D", fg="white")
        
# Posicionamiento para los widgets de Servicios

            antecedente.grid        (row=0, column=0, padx=10, pady=5)
            entry_antecedente.grid  (row=1, column=0, padx=10, pady=10)
            reparacion.grid         (row=0, column=1, padx=10, pady=5)
            entry_reparacion.grid   (row=1, column=1, padx=25, pady=10)
            precio.grid             (row=0, column=2, padx=10, pady=0)
            entry_precio.grid       (row=1, column=2, padx=10, pady=0)
            entrada.grid            (row=3, column=0, padx=10, pady=10)
            entry_entrada.grid      (row=4, column=0, padx=10, pady=10)
            salida.grid             (row=3, column=1, padx=10, pady=10)
            entry_salida.grid       (row=4, column=1, padx=10, pady=10)

            btn_guardar.grid        (row=4, column=2)
            btn_salir.grid          (row=3, column=2)

            conexion = sqlite3.connect("grupovespa.db")
            cursor = conexion.cursor()

            if tree2.get_children():

                item = tree2.selection()[0]
                id_servicio = tree2.item(item)["values"][0]

                cursor.execute('SELECT * FROM servicios WHERE id_servicio = ?', (id_servicio,))
                existe_servicio = cursor.fetchone()

                if existe_servicio:
                    entry_antecedente.delete("1.0", tk.END)
                    entry_reparacion.delete("1.0", tk.END)
                    entry_precio.delete(0, tk.END)
                    entry_entrada.delete(0, tk.END)
                    entry_salida.delete(0, tk.END)

                    entry_antecedente.config(state="normal")
                    
                    entry_antecedente.insert('insert', existe_servicio[1])
                    entry_reparacion.insert('insert', existe_servicio[2])
                    entry_precio.insert(0, existe_servicio[3])
                    entry_entrada.insert(0, existe_servicio[4])
                    entry_salida.insert(0, existe_servicio[5])

                    entry_antecedente.config(state="disabled")
                else:
                    entry_antecedente.delete("1.0", tk.END)
                    entry_reparacion.delete("1.0", tk.END)
                    entry_precio.delete(0, tk.END)
                    entry_entrada.delete(0, tk.END)
                    entry_salida.delete(0, tk.END)                                     
            else:
                entry_antecedente.delete("1.0", tk.END)
                entry_reparacion.delete("1.0", tk.END)
                entry_precio.delete(0, tk.END)
                entry_entrada.delete(0, tk.END)
                entry_salida.delete(0, tk.END)    

            conexion.close()           
        
        def servicio_nuevo():
            servicios = tk.Toplevel(ventana)
            servicios.title("Servicios")

            def guardar():
                guardar_antecedente = entry_antecedente.get("1.0", "end-1c")
                guardar_reparacion = entry_reparacion.get("1.0", "end-1c")
                guardar_precio = entry_precio.get()
                guardar_entrada = entry_entrada.get()
                guardar_salida = entry_salida.get()

                item1 = tree.selection()
                datos = tree.item(item1)["values"]
                
                guardar_matricula = datos[0]
                guardar_id_cliente = datos[5]

                conexion = sqlite3.connect("grupovespa.db")
                cursor = conexion.cursor()

                cursor.execute('INSERT INTO servicios (antecedente, reparacion, precio, fecha_entrada, fecha_salida, matricula, id_cliente) VALUES (?,?,?,?,?,?,?)', (guardar_antecedente, guardar_reparacion, guardar_precio, guardar_entrada, guardar_salida, guardar_matricula, guardar_id_cliente))
                btn_guardar.config(state="disabled")
                tk.messagebox.showinfo("Éxito", "Los datos del servicio han sido agregados.")

                conexion.commit()
                conexion.close()
                servicios.destroy()
                consultar()

            def salir_servicios():
                servicios.destroy()
                consultar() 

            # Creacion de los widgets de Servicios

            antecedente = Label(servicios, text="Antecedentes: ")
            entry_antecedente = Text(servicios, height=5, width=30)
            reparacion = Label(servicios, text="Reparación: ")
            entry_reparacion = Text(servicios, height=5, width=30)
            precio = Label(servicios, text="Precio: ")
            entry_precio = Entry(servicios, width=9)
            entrada = Label(servicios, text="Entrada: ")
            entry_entrada = DateEntry(servicios, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
            salida = Label(servicios, text="Salida: ")
            entry_salida = DateEntry(servicios, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')

            btn_guardar = Button(servicios, text="Guardar", command=guardar, bg="#212F3D", fg="white")
            btn_salir = Button(servicios, text="Salir", command=salir_servicios, bg="#212F3D", fg="white")

            entry_antecedente.delete("1.0", tk.END)
            entry_reparacion.delete("1.0", tk.END)
            entry_precio.delete(0, tk.END)
            entry_entrada.delete(0, tk.END)
            entry_salida.delete(0, tk.END) 
        
# Posicionamiento para los widgets de Servicios

            antecedente.grid        (row=0, column=0, padx=10, pady=5)
            entry_antecedente.grid  (row=1, column=0, padx=10, pady=10)
            reparacion.grid         (row=0, column=1, padx=10, pady=5)
            entry_reparacion.grid   (row=1, column=1, padx=25, pady=10)
            precio.grid             (row=0, column=2, padx=10, pady=0)
            entry_precio.grid       (row=1, column=2, padx=10, pady=0)
            entrada.grid            (row=3, column=0, padx=10, pady=10)
            entry_entrada.grid      (row=4, column=0, padx=10, pady=10)
            salida.grid             (row=3, column=1, padx=10, pady=10)
            entry_salida.grid       (row=4, column=1, padx=10, pady=10)

            btn_guardar.grid        (row=4, column=2)
            btn_salir.grid          (row=3, column=2)

# Entry de control
        boton_buscar_presionado = Entry(centro)

# Creacion de widgets para Consultar
        frame_superior = ttk.Frame(centro, padding=(10,10))
        frame_inferior = Frame(centro)
        frame_consulta = Frame(centro)

        label_id_cliente = Label(frame_superior, text="Ingresar identificación del cliente:")
        entry_id_cliente_busqueda = Entry(frame_superior, width=10, validate="key")
        entry_id_cliente_busqueda.configure(validatecommand=(centro.register(validar_longitud_matricula), '%P'))
        entry_id_cliente_busqueda.bind("<KeyRelease>", filtrar_vehiculo)

        boton_buscar = Button(frame_superior, text="Buscar", command=buscar_cliente, bg="#212F3D", fg="white")
        boton_servicio_nuevo = Button(frame_superior, text="Servicio Nuevo", command=servicio_nuevo, state="disabled", bg="#212F3D", fg="white")

        entry_id_cliente_busqueda.bind('<Return>', lambda event: boton_buscar.invoke())


# Treeview 1: Muestra la información del vehiculo del cliente
        columns = ("matricula", "tipo", "modelo", "color", "estatus", "cliente")
        tree = ttk.Treeview(frame_inferior, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col.capitalize())
            tree.column(col, width=100)

        scrollbar = ttk.Scrollbar(frame_inferior, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.bind("<Double-1>", lambda event: vehiculo_seleccionado(event))
        

# Treeview 2: Muestra la información del vehiculo del cliente
        columns2 = ("Nº", "antecedente", "reparacion", "precio", "entrada", "salida")
        widths = [5, 160, 217, 10, 40, 40]    # Lista de anchos de columna

        tree2 = ttk.Treeview(frame_consulta, columns=columns2, show="headings")
        for i, col in enumerate(columns2):
            tree2.heading(col, text=col.capitalize())
            tree2.column(col, width=widths[i], stretch=tk.YES)    # Aplicar el ancho correspondiente a la columna

            scrollbar2 = ttk.Scrollbar(frame_consulta, orient="vertical", command=tree2.yview)
            tree2.configure(yscrollcommand=scrollbar.set)
        
        #tree2.bind('<<TreeviewSelect>>', mostrar_servicio)
        tree2.bind("<Double-1>", lambda event: mostrar_servicio(event))

    # Porsicionamiento de widgets para Consultar

        frame_superior.pack(fill="both")
        frame_inferior.pack(fill="both")
        frame_consulta.pack(side="bottom", fill="both")

        label_id_cliente.pack(side="left")
        entry_id_cliente_busqueda.pack(side="left", padx=(5, 0))

        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        tree2.pack(side="left", fill="both", expand=True, pady=20)
        scrollbar2.pack(side="right", fill="y")

        boton_buscar.pack(side="left", padx=(5, 0))
        boton_servicio_nuevo.pack(side="left", padx=(200, 0))

        
        if boton_buscar_presionado.get() == "Presionado":
            boton_buscar_presionado.delete()            
        else:
            # Muestreo de datos de vehiculos
            # Limpiar Treeview
            tree.delete(*tree.get_children())

            conexion = sqlite3.connect("grupovespa.db")
            cursor = conexion.cursor()
            # Realizar consulta SQL sin filtro
            cursor.execute("SELECT vehiculos.matricula, vehiculos.tipo, vehiculos.modelo, vehiculos.color, estatus.nombre_estatus, vehiculos.id_cliente FROM vehiculos INNER JOIN estatus ON vehiculos.estatus = estatus.id_estatus")
            datos_vehiculos = cursor.fetchall()
            conexion.close()

            # Agregar los datos filtrados al Treeview
            for row in datos_vehiculos:
                tree.insert("", "end", values=row)  


    def registro():
        
        for widget in centro.winfo_children():
            widget.destroy()

        #Creamos algunas validaciones
        
        def validar_longitud_razon_social(valor):
            if len(valor) <= 45:
                return True
            else:
                return False
            
        def validar_longitud_direccion(valor):
            if len(valor) <= 150:
                return True
            else:
                return False  
            
        def validar_cedula(valor):
            if valor.isdigit() or valor == "":
                if len(entry_id_cliente.get()) < 10:
                    return True
                else:
                    return False
            else:
                return False
            
        def validar_telefono(valor):
            if valor.isdigit() or valor == "":
                if len(entry_telefono.get()) < 7:
                    return True
                else:
                    return False
            else:
                return False
            
        def validar_matricula(valor):
            if len(valor) <= 7 and valor.isupper():
                return True
            else:
                return False

            
        def validar_modelo_color(valor):
            if len(valor) <= 40:
                return True
            else:
                return False


        def buscar_cliente():

            conexion = sqlite3.connect("grupovespa.db")
            cursor = conexion.cursor()

            cursor.execute('SELECT nombre_estado FROM estados')
            datos_estados = cursor.fetchall()
            cursor.execute('SELECT cod_area FROM cod_area_telefono')
            datos_cod_area = cursor.fetchall()
            cursor.execute('SELECT denominacion_tipo_documento FROM tipo_documento')
            datos_tipo_documento = cursor.fetchall()

            id_cliente = entry_id_cliente.get()
            cursor.execute("SELECT tipo_documento.denominacion_tipo_documento, clientes.id_cliente, clientes.razon_social, estados.nombre_estado, clientes.direccion, cod_area_telefono.cod_area, clientes.telefono FROM clientes INNER JOIN tipo_documento ON clientes.tipo_documento = tipo_documento.id_tipo_documento INNER JOIN estados ON clientes.estado = estados.id_estado INNER JOIN cod_area_telefono ON clientes.cod_area = cod_area_telefono.id_cod_area WHERE clientes.id_cliente = ?", (id_cliente,))
            datos = cursor.fetchone()

            conexion.close()
            if datos:

                entry_id_cliente.config(state="disabled")
                combo_tipo_documento.config(state="normal")
                entry_razon_social.config(state="normal")
                combo_estado.config(state="normal")
                entry_direccion.config(state="normal")
                combo_cod_area.config(state="normal")
                entry_telefono.config(state="normal")

                btn_guardar_cliente.config(state="normal")
                btn_buscar_cliente.config(state="disabled")

                combo_tipo_documento ['values'] = [row[0] for row in datos_tipo_documento]
                combo_estado ['values'] = [row[0] for row in datos_estados]
                combo_cod_area ['values'] = [row[0] for row in datos_cod_area]

                combo_tipo_documento.delete(0, tk.END)
                combo_tipo_documento.insert(0, datos[0])
                entry_id_cliente.delete(0, tk.END)
                entry_id_cliente.insert(0, datos[1])
                entry_razon_social.delete(0, tk.END)
                entry_razon_social.insert(0, datos[2])
                combo_estado.delete(0, tk.END)
                combo_estado.insert(0, datos[3])
                entry_direccion.delete(0, tk.END)
                entry_direccion.insert(0, datos[4])
                combo_cod_area.delete(0, tk.END)
                combo_cod_area.insert(0, datos[5])
                entry_telefono.delete(0, tk.END)
                entry_telefono.insert(0, datos[6])

            else:
                respuesta_buscar = tk.messagebox.askyesno("Confirmar", "El cliente no existe, ¿desea agregarlo?")
                if respuesta_buscar == True:
                    agregar_cliente()
                else:
                    pass

        def agregar_cliente():
            conexion = sqlite3.connect("grupovespa.db")
            cursor = conexion.cursor()

            cursor.execute('SELECT nombre_estado FROM estados')
            datos_estados = cursor.fetchall()
            cursor.execute('SELECT cod_area FROM cod_area_telefono')
            datos_cod_area = cursor.fetchall()
            cursor.execute('SELECT denominacion_tipo_documento FROM tipo_documento')
            datos_tipo_documento = cursor.fetchall()

            conexion.close()

            combo_tipo_documento ['values'] = [row[0] for row in datos_tipo_documento]
            combo_estado ['values'] = [row[0] for row in datos_estados]
            combo_cod_area ['values'] = [row[0] for row in datos_cod_area]

            entry_id_cliente.config(state="disabled")
            combo_tipo_documento.config(state="normal")
            entry_razon_social.config(state="normal")
            combo_estado.config(state="normal")
            entry_direccion.config(state="normal")
            combo_cod_area.config(state="normal")
            entry_telefono.config(state="normal")

            btn_guardar_cliente.config(state="normal")
            btn_buscar_cliente.config(state="disabled")


        def guardar_cliente():

            entry_id_cliente.config(state="normal")
            tipo_documento = combo_tipo_documento.get()
            id_cliente = entry_id_cliente.get()
            razon_social = entry_razon_social.get()
            estado = combo_estado.get()
            direccion = entry_direccion.get()
            cod_area = combo_cod_area.get()
            telefono = entry_telefono.get()

            conexion = sqlite3.connect("grupovespa.db")
            cursor = conexion.cursor()

            cursor.execute("SELECT id_tipo_documento FROM tipo_documento WHERE denominacion_tipo_documento = ?", (tipo_documento,))
            dato_tipo_documento = cursor.fetchone()[0]

            cursor.execute("SELECT id_estado FROM estados WHERE nombre_estado = ?", (estado,))
            dato_estado = cursor.fetchone()[0]

            cursor.execute("SELECT id_cod_area FROM cod_area_telefono WHERE cod_area = ?", (cod_area,))
            dato_cod_area = cursor.fetchone()[0]
            
            cursor.execute('SELECT id_cliente FROM clientes WHERE clientes.id_cliente = ?', (id_cliente,))
            existe = cursor.fetchone()

            if existe:

                cursor.execute("UPDATE clientes SET tipo_documento = ?, razon_social = ?, estado = ?, direccion = ?, cod_area = ?, telefono = ? WHERE id_cliente = ?", (dato_tipo_documento, razon_social, dato_estado, direccion, dato_cod_area, telefono, id_cliente))

                combo_tipo_documento.delete(0, 'end')
                entry_id_cliente.delete(0,'end')
                entry_razon_social.delete(0,'end')
                combo_estado.delete(0, 'end')
                entry_direccion.delete(0, 'end')
                combo_cod_area.delete(0, 'end')
                entry_telefono.delete(0,'end')

                tk.messagebox.showinfo("Éxito", "Los datos del cliente han sido actualizados.")
                registro()

            else:

                cursor.execute("INSERT INTO clientes (tipo_documento, id_cliente, razon_social, estado, direccion, cod_area, telefono) VALUES (?,?,?,?,?,?,?)", (dato_tipo_documento, id_cliente, razon_social, dato_estado, direccion, dato_cod_area, telefono))

                combo_tipo_documento.delete(0, 'end')
                entry_id_cliente.delete(0,'end')
                entry_razon_social.delete(0,'end')
                combo_estado.delete(0, 'end')
                entry_direccion.delete(0, 'end')
                combo_cod_area.delete(0, 'end')
                entry_telefono.delete(0,'end')

                tk.messagebox.showinfo("Éxito", "Los datos del cliente han sido registrados.")
                registro()

            conexion.commit()
            conexion.close()

        def buscar_vehiculo():

            conexion = sqlite3.connect("grupovespa.db")
            cursor = conexion.cursor()

            cursor.execute('SELECT nombre_estatus FROM estatus')
            datos_estatus = cursor.fetchall()

            cursor.execute('SELECT matricula FROM vehiculos WHERE vehiculos.id_cliente = ?', (entry_id_cliente_vehiculo.get(),))
            datos_matricula = cursor.fetchall()

            if datos_matricula:

                def seleccionar_item(event):
                    seleccion = combo_matricula.get()
                    if seleccion:
                        conexion = sqlite3.connect("grupovespa.db")
                        cursor = conexion.cursor()

                        cursor.execute('SELECT vehiculos.tipo, vehiculos.modelo, vehiculos.color, vehiculos.estatus, estatus.nombre_estatus FROM vehiculos INNER JOIN estatus ON vehiculos.estatus = estatus.id_estatus WHERE matricula = ?',(seleccion,))
                        datos_vehiculo = cursor.fetchall()

                        if datos_vehiculo:
                            combo_tipo.config(state="normal")
                            entry_modelo.config(state="normal")
                            entry_color.config(state="normal")
                            combo_estatus.config(state="normal")

                            btn_buscar_vehiculo.config(state="disabled")
                            btn_guardar_vehiculo.config(state="normal")

                            combo_estatus ['values'] = [row[0] for row in datos_estatus]                        

                            combo_tipo.delete(0, tk.END)
                            combo_tipo.insert(0, datos_vehiculo[0][0])
                            entry_modelo.delete(0, tk.END)
                            entry_modelo.insert(0, datos_vehiculo[0][1])
                            entry_color.delete(0, tk.END)
                            entry_color.insert(0, datos_vehiculo[0][2])
                            combo_estatus.delete(0, tk.END)
                            combo_estatus.insert(0, datos_vehiculo[0][4])      
                        else:
                            pass
                    else:
                        pass

                entry_id_cliente_vehiculo.config(state="disabled")
                combo_matricula.config(state="normal")
                combo_matricula ['values'] = [row[0] for row in datos_matricula]
                btn_buscar_vehiculo.config(state="disabled")

                btn_añadir_matricula.place(x= 190 , y= 55)

                combo_matricula.bind("<<ComboboxSelected>>", seleccionar_item)

            else:

                cursor.execute('SELECT id_cliente FROM clientes WHERE clientes.id_cliente = ?',(entry_id_cliente_vehiculo.get(),))
                existe_cliente = cursor.fetchone()
                if not existe_cliente:
                    sin_cliente = tk.messagebox.askyesno("Cliente no registrado", "El cliente no está registrado, ¿desea agregarlo?")
                    if sin_cliente == True:
                        entry_id_cliente.insert(0, entry_id_cliente_vehiculo.get())
                        entry_id_cliente_vehiculo.delete(0, tk.END)
                        agregar_cliente()
                    else:
                        pass
                else:
                    respuesta_buscar = tk.messagebox.askyesno("Cliente sin vehiculo asignado", "El cliente no posee ningún vehículo asignado, ¿desea agregar uno?")
                    if respuesta_buscar == True:
                        vehiculo_nuevo()
                    else:
                        pass
                    pass                
            conexion.close()

        def vehiculo_nuevo():
            conexion = sqlite3.connect("grupovespa.db")
            cursor = conexion.cursor()

            cursor.execute('SELECT nombre_estatus FROM estatus')
            datos_estatus = cursor.fetchall()

            combo_matricula.destroy()
            entry_id_cliente_vehiculo.config(state="disabled")
            combo_tipo.config(state="normal")
            entry_modelo.config(state="normal")
            entry_color.config(state="normal")
            combo_estatus.config(state="normal")

            combo_tipo.delete(0, tk.END)
            entry_modelo.delete(0, tk.END)
            entry_color.delete(0, tk.END)
            combo_estatus.delete(0, tk.END)

            combo_estatus ['values'] = [row[0] for row in datos_estatus] 

            entry_matricula.place(x=100, y=60)

            btn_buscar_vehiculo.config(state="disabled")
            btn_guardar_vehiculo.config(state="normal")

            conexion.close()
            btn_añadir_matricula.config(state="disabled")

        def guardar_vehiculo():

            conexion = sqlite3.connect("grupovespa.db")
            cursor = conexion.cursor()
        
            matricula_nueva = entry_matricula.get()
            tipo = combo_tipo.get()
            modelo = entry_modelo.get()
            color = entry_color.get()
            estatus = combo_estatus.get()
            id_cliente = entry_id_cliente_vehiculo.get()

            cursor.execute("SELECT id_estatus FROM estatus WHERE nombre_estatus = ?", (estatus,))
            dato_estatus = cursor.fetchone()[0]

            def agregar_vehiculo():

                cursor.execute('SELECT matricula FROM vehiculos WHERE vehiculos.matricula = ?', (matricula_nueva,))
                existe = cursor.fetchone()

                if existe:
                    tk.messagebox.showinfo("Error", "La matricula ya esta registrada")
                    entry_matricula.delete(0, tk.END)
                    registro()
                else:
                    pass

                entry_id_cliente_vehiculo.config(state="normal")

                cursor.execute("INSERT INTO vehiculos (matricula, tipo, modelo, color, estatus, id_cliente) VALUES (?,?,?,?,?,?)", (matricula_nueva, tipo, modelo, color, dato_estatus, id_cliente))

                entry_id_cliente_vehiculo.delete(0, 'end')
                entry_matricula.delete(0,'end')
                combo_tipo.delete(0,'end')
                entry_modelo.delete(0, 'end')
                entry_color.delete(0, 'end')
                combo_estatus.delete(0, 'end')

                tk.messagebox.showinfo("Éxito", "Se ha añadido un nuevo vehiculo al cliente")
                registro()

            def actualizar_vehiculo():

                buscar_matricula = combo_matricula.get()

                cursor.execute("UPDATE vehiculos SET tipo = ?, modelo = ?, color = ?, estatus = ? WHERE matricula = ?", (tipo, modelo, color, dato_estatus, buscar_matricula))
                
                combo_matricula.delete(0, 'end')
                combo_tipo.delete(0,'end')
                entry_modelo.delete(0,'end')
                entry_color.delete(0, 'end')
                combo_estatus.delete(0, 'end')

                tk.messagebox.showinfo("Éxito", "Los datos del vehiculo han sido actualizados.")
                registro()

            if matricula_nueva:
                agregar_vehiculo()
            else:
                actualizar_vehiculo()

            conexion.commit()
            conexion.close()

        izquierdo = LabelFrame(centro, text="  Cliente  ", font=("Calibri", 14))
        derecho = LabelFrame (centro, text="  Vehiculo  ", font=("Calibri", 14))
        abajo = LabelFrame(centro, text="  Opciones  ", font=("Calibri", 14))

        izquierdo.place(x=30, y=20, width=280, height=400)
        derecho.place(x=365, y=20, width=280, height=400)
        abajo.place(x=62, y=440, width=550, height=60)

        #Creación de widgets cliente

        id_cliente = Label(izquierdo, text="Identificación: ")
        combo_tipo_documento = tk.ttk.Combobox(izquierdo, width=2, state="disabled")
        entry_id_cliente = Entry (izquierdo, validate='key')
        entry_id_cliente.configure(validatecommand=(centro.register(validar_cedula), '%P'))
        razon_social = Label(izquierdo, text="Razon Social: ")
        entry_razon_social = Entry(izquierdo, validate='key', state="disabled")
        entry_razon_social.configure(validatecommand=(centro.register(validar_longitud_razon_social), '%P'))
        direccion = Label(izquierdo, text="Dirección: ")
        combo_estado = tk.ttk.Combobox(izquierdo, width=15, state="disabled")
        entry_direccion = Entry(izquierdo, width=35, validate='key', state="disabled")
        entry_direccion.configure(validatecommand=(centro.register(validar_longitud_direccion), '%P'))
        telefono = Label(izquierdo, text="Telefono: ")
        combo_cod_area = tk.ttk.Combobox(izquierdo, width=4, state="disabled")
        entry_telefono = Entry(izquierdo, width=11, validate='key', state="disabled")
        entry_telefono.configure(validatecommand=(centro.register(validar_telefono), '%P'))

        btn_buscar_cliente = Button(izquierdo, text="Buscar", command=buscar_cliente, bg="#212F3D", fg="white")
        btn_guardar_cliente = Button(izquierdo, text="Guardar", command=guardar_cliente, state="disabled", bg="#212F3D", fg="white")

        entry_id_cliente.bind('<Return>', lambda event: btn_buscar_cliente.invoke())
        entry_telefono.bind('<Return>', lambda event: btn_guardar_cliente.invoke())

        #Posicionamiento de widgets cliente

        id_cliente.place(x=10, y=20)
        combo_tipo_documento.place(x=100, y=20)
        entry_id_cliente.place(x=140, y=20)
        razon_social.place(x=10, y=60)
        entry_razon_social.place(x= 100, y=60)
        direccion.place(x=10, y=110)
        combo_estado.place(x=100, y=110)
        entry_direccion.place(x=10, y=150)
        telefono.place(x=10, y=200)
        combo_cod_area.place(x=80, y=200)
        entry_telefono.place(x=150, y=200)

        btn_buscar_cliente.place(x=60, y=320)
        btn_guardar_cliente.place(x=140, y=320)

        #Creación de widgets vehiculos

        id_cliente_vehiculo = Label(derecho, text="Identificación: ")
        entry_id_cliente_vehiculo = Entry (derecho)
        matricula = Label(derecho, text="Matricula: ")
        combo_matricula = tk.ttk.Combobox(derecho, width=10, state="disabled")
        entry_matricula = Entry(derecho, width=10, validate='key')
        entry_matricula.configure(validatecommand=(centro.register(validar_matricula), '%P'))
        btn_añadir_matricula = Button(derecho, text="Añadir", command=vehiculo_nuevo, bg="#212F3D", fg="white")
        tipo_vehiculo = Label(derecho, text="Tipo: ")
        tipo_opcion = tk.StringVar()
        combo_tipo = ttk.Combobox(derecho, textvariable=tipo_opcion, values=["Moto", "Carro"], width=10, state="disabled")
        combo_tipo.current(0)
        modelo = Label(derecho, text="Modelo: ")
        entry_modelo = Entry(derecho, state="disabled", validate='key')
        entry_modelo.configure(validatecommand=(centro.register(validar_modelo_color), '%P'))
        color = Label(derecho, text="Color: ")
        entry_color = Entry(derecho, state="disabled", validate='key')
        entry_color.configure(validatecommand=(centro.register(validar_modelo_color), '%P'))
        estatus = Label(derecho, text="Estatus: ")
        combo_estatus = tk.ttk.Combobox(derecho, width=15, state="disabled")

        btn_buscar_vehiculo = Button(derecho, text="Buscar", command=buscar_vehiculo, bg="#212F3D", fg="white")
        btn_guardar_vehiculo = Button(derecho, text="Guardar", command=guardar_vehiculo, state="disabled", bg="#212F3D", fg="white")

        entry_id_cliente_vehiculo.bind('<Return>', lambda event: btn_buscar_vehiculo.invoke())
        combo_estatus.bind('<Return>', lambda event: btn_guardar_vehiculo.invoke())


        #Posicionamiento de widgets vehiculos

        id_cliente_vehiculo.place(x=10, y=20)
        entry_id_cliente_vehiculo.place(x=100, y=20)
        matricula.place(x=10, y=60)
        combo_matricula.place(x=100, y=60)
        tipo_vehiculo.place(x= 10, y=110)
        combo_tipo.place(x=100, y=110)
        modelo.place(x=10, y= 150)
        entry_modelo.place(x=100, y=150)
        color.place(x=10, y=200)
        entry_color.place(x=100, y=200)
        estatus.place(x= 10, y=250)
        combo_estatus.place(x=100, y=250)


        #Creación y posicionamiento de widgets Opciones

        btn_limpiar = Button(abajo, text="Limpiar", command=registro, bg="#212F3D", fg="white")
        btn_limpiar.pack()

        btn_buscar_vehiculo.place(x=60, y=320)
        btn_guardar_vehiculo.place(x=140, y=320)
            

    def reporte():

        for widget in centro.winfo_children():
            widget.destroy()

        def generar_reporte():

            # Obtener los datos desde la base de datos
            conexion = sqlite3.connect('grupovespa.db')
            cursor = conexion.cursor()
            cursor.execute('SELECT * FROM categoria')
            datos = cursor.fetchall()

            # Crear el archivo PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font('Arial', 'B', 16)
            pdf.cell(40, 10, 'Tabla Categoria')

            # Agregar una línea vacía
            pdf.ln(10)

            # Encabezados de la tabla
            pdf.cell(40, 10, 'ID', border=1)
            pdf.cell(50, 10, 'Nombre', border=1)

            # Agregar una línea vacía
            pdf.ln()

            # Cuerpo de la tabla
            for dato in datos:
                pdf.cell(40, 10, str(dato[0]), border=1)
                pdf.cell(50, 10, str(dato[1]), border=1)
                pdf.ln()

            # Guardar el archivo PDF
            pdf.output('Reportes/tabla_categoria.pdf', 'F')

            # Cerrar la conexión con la base de datos
            conexion.close()


        def buscar_cliente():
            conexion = sqlite3.connect("grupovespa.db")
            cursor = conexion.cursor()

            cursor.execute('SELECT matricula FROM vehiculos WHERE vehiculos.id_cliente = ?', (entry_id_cliente.get(),))
            datos_matricula = cursor.fetchall()
            combo_matricula ['values'] = [row[0] for row in datos_matricula]

        # Creación de Widgets

        id_cliente = Label(centro, text="Identificación: ")
        entry_id_cliente = Entry(centro, width=10)

        matricula = Label(centro, text="Matricula: ")
        combo_matricula = tk.ttk.Combobox(centro, width=10, state="disabled")

        btn_buscar_cliente = Button(centro, text="Buscar", command=buscar_cliente, bg="#212F3D", fg="white")
        btn_generar_reporte = Button(centro, text="Generar Reporte", command=generar_reporte, bg="#212F3D", fg="white")

        #Posicionamiento de Widgets

        id_cliente.place            (x=60, y=10)
        entry_id_cliente.place      (x=60, y=50)
        matricula.place             (x=170, y=10)
        combo_matricula.place       (x=170, y=50)

        btn_buscar_cliente.place    (x=60, y= 180)
        btn_generar_reporte.place   (x=180, y=180)


    def salir():
        respaldo_automatico()
        ventana.destroy()

    #creamos unos Frames para separar los espacios disponibles en ventana que nos permitan modificar su contenido con mayor facilidad

    barra_vertical = Frame(ventana, bg="#3b3b3b")
    barra_vertical.place(x=0, y=0, relheight=1.00, width=100)

    barra_superior = Frame(ventana, bg="#2f2f2f")
    barra_superior.place(x=100, y=0, height=50, relwidth=1.00)

    centro = Frame(ventana)
    centro.place(x=110, y=50, height=530, width=680)

    #añadimos contenido a los frames

    titulo = Label(barra_superior, text="Grupo Vespa Servizio Vzla 3110 C.A - RIF:J-412020943", fg="white", font="Helvetica", bg="#2f2f2f")
    titulo.place(x=10, y=5, height=40)

    imagen_original = Image.open("Source\logo_70x72.png")
    imagen = ImageTk.PhotoImage(imagen_original)
    label_logo = Label(barra_vertical, image=imagen)
    label_logo.place(x= 12, y= 15)

    #se crean botones para mostrar las operaciones del sistema

    btn_consulta = Button(ventana, text="Busqueda", command=consultar, bg="#212F3D", fg="white")
    btn_consulta.place(x= 10, y= 105, height=30, width=80)

    btn_registrar = Button(ventana, text="Registro", command=registro, bg="#212F3D", fg="white")
    btn_registrar.place(x= 10, y= 165, height=30, width=80)

    btn_eliminar = Button(ventana, text="Reporte", command=reporte, bg="#212F3D", fg="white")
    btn_eliminar.place(x= 10, y= 285, height=30, width=80)

    btn_salir = Button(ventana, text="Salir", command=salir, bg="#212F3D", fg="white")
    btn_salir.place(x= 10, y= 385, height=30, width=80)

#por ultimo creamos el bucle principal de la aplicacion, esto nos permite interactuar con el programa
    ventana.mainloop()

#por ultimo creamos el bucle principal de la aplicacion, esto nos permite interactuar con el programa
login.mainloop()