from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3

def conectarBaseDatos():
    baseDatos = sqlite3.connect("empleados.db")
    cursor = baseDatos.cursor()

    try:
        cursor.execute("""CREATE TABLE empleados_informacion(ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                                             NOMBRE VARCHAR(50) NOT NULL,
                                                             CARGO VARCHAR(50) NOT NULL,
                                                             SALARIO REAL NOT NULL)""")
        
        messagebox.showinfo("CONEXION", "Base de datos creada exitosamente")
    
    except:
        messagebox.showinfo("CONEXION", "Conexion exitosa con la base de datos")

def eliminarBaseDatos():
    baseDatos = sqlite3.connect("empleados.db")
    cursor = baseDatos.cursor()
    if(messagebox.askyesno(message = "Los datos se perderan definitivamente, desea continuar?", title = "ADVERTENDIA") == True):
        cursor.execute("DROP TABLE empleados_informacion")
    else:
        pass

    limpiarCampos()
    mostrarRegistros()

def limpiarCampos():
    ID.set("")
    nombre.set("")
    cargo.set("")
    salario.set("")

def salirAplicacion():
    salir = messagebox.askquestion("SALIR", "Esta seguro que desea salir de la aplicacion?")
    if(salir == "yes"):
        ventana.destroy()
    else:
        pass

def informacionAplicacion():
    informacion = """
                      Aplicacion CRUD
                      Version 1.0
                      Tecnologia PYTHON con TKINTER
                  """

    messagebox.showinfo(title = "INFORMACION", message = informacion)

def crearRegistro():
    baseDatos = sqlite3.connect("empleados.db")
    cursor = baseDatos.cursor()

    try:
        datos = nombre.get(), cargo.get(), salario.get()

        cursor.execute("INSERT INTO empleados_informacion VALUES(NULL, ?, ?, ?)", (datos))
        baseDatos.commit()
    
    except:
        messagebox.showwarning("ADVERTENCIA", "Ocurrio un error al crear el registro, verifique conexion con la base de datos")
        pass

    limpiarCampos()
    mostrarRegistros()

def actualizarRegistro():
    baseDatos = sqlite3.connect("empleados.db")
    cursor = baseDatos.cursor()

    try:
        datos = nombre.get(), cargo.get(), salario.get()

        cursor.execute("UPDATE empleados_informacion SET NOMBRE = ?, CARGO = ?, SALARIO = ? WHERE ID =" + ID.get(), (datos))
        baseDatos.commit()
    
    except:
        messagebox.showwarning("ADVERTENCIA", "Ocurrio un error al actualizar el registro")
        pass

    limpiarCampos()
    mostrarRegistros()

def borrarRegistro():
    baseDatos = sqlite3.connect("empleados.db")
    cursor = baseDatos.cursor()

    try:
        if (messagebox.askyesno(message = "Desea realmente eliminar el registro?", title = "ADVERTENCIA")):
            cursor.execute("DELETE FROM empleados_informacion WHERE ID =" + ID.get())
            baseDatos.commit()
    except:
        messagebox.showwarning("ADVERTENCIA", "Ocurrio un error al eliminar el registro")
        pass

    limpiarCampos()
    mostrarRegistros()

def mostrarRegistros():
    baseDatos = sqlite3.connect("empleados.db")
    cursor = baseDatos.cursor()
    registros = arbol.get_children()
    
    for elemento in registros:
        arbol.delete(elemento)

    try:
        cursor.execute("SELECT * FROM empleados_informacion")
        for fila in cursor:
            arbol.insert("", 0, text = fila[0], values = (fila[1], fila[2], fila[3]))

    except:
        pass

def seleccionarUsandoClick(evento):
    objeto = arbol.identify("item", evento.x, evento.y)
    ID.set(arbol.item(objeto, "text"))
    nombre.set(arbol.item(objeto, "values")[0])
    cargo.set(arbol.item(objeto, "values")[1])
    salario.set(arbol.item(objeto, "values")[2])

ventana = Tk()
ventana.title("Aplicacion CRUD con base de datos")
ventana.geometry("600x350")

arbol = ttk.Treeview(height = 10, columns = ('#0', '#1', '#2'))
arbol.place(x = 0, y = 130)
arbol.column('#0', width = 100)
arbol.heading('#0', text = "ID", anchor = CENTER)
arbol.heading('#1', text = "Nombre del empleado", anchor = CENTER)
arbol.heading('#2', text = "Cargo", anchor = CENTER)
arbol.column('#3', width = 100)
arbol.heading('#3', text = "Salario", anchor = CENTER)

arbol.bind("<Double-1>", seleccionarUsandoClick)

menu = Menu(ventana)
menuBaseDatos = Menu(menu, tearoff = 0)
menuBaseDatos.add_command(label = "Crear/Conectar base de datos", command = conectarBaseDatos)
menuBaseDatos.add_command(label = "Eliminar base de datos", command = eliminarBaseDatos)
menuBaseDatos.add_command(label = "Salir", command = salirAplicacion)
menu.add_cascade(label = "Inicio", menu = menuBaseDatos)

menuAyuda = Menu(menuBaseDatos, tearoff = 0)
menuAyuda.add_command(label = "Resetear campos", command = limpiarCampos)
menuAyuda.add_command(label = "Informacion", command = informacionAplicacion)

menu.add_cascade(label = "Ayuda", menu = menuAyuda)
ventana.config(menu = menu)

ID = StringVar()
nombre = StringVar()
cargo = StringVar()
salario = StringVar()

entrada1 = Entry(ventana, textvariable = ID)

etiqueta2 = Label(ventana, text = "Nombre")
etiqueta2.place(x = 40, y = 10)
entrada2 = Entry(ventana, textvariable = nombre, width = 55)
entrada2.place(x = 100, y = 10)

etiqueta3 = Label(ventana, text = "Cargo")
etiqueta3.place(x = 50, y = 40)
entrada3 = Entry(ventana, textvariable = cargo)
entrada3.place(x = 100, y = 40)

etiqueta4 = Label(ventana, text = "Salario")
etiqueta4.place(x = 272, y = 40)
entrada4 = Entry(ventana, textvariable = salario, width = 13)
entrada4.place(x = 322, y = 40)

etiqueta5 = Label(ventana, text = "MXN")
etiqueta5.place(x = 404, y = 40)

boton1 = Button(ventana, text = "Crear registro", command = crearRegistro)
boton1.place(x = 50, y = 90)
boton2 = Button(ventana, text = "Modificar registro", command = actualizarRegistro)
boton2.place(x = 180, y = 90)
boton3 = Button(ventana, text = "Mostrar lista", command = mostrarRegistros)
boton3.place(x = 320, y = 90)
boton4 = Button(ventana, text = "Eliminar registro", command = borrarRegistro)
boton4.place(x = 450, y = 90)

ventana.mainloop()