import sqlite3
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import subprocess

root = Tk()
root.geometry('1000x500')
root.iconbitmap("buscaminas.ico")

root.title("Comenzamiento")

contador_intentos = 0  # Contador global de intentos

#Para los estados de los dos jugadores, lo utilizo para poder habilitar el boton de "Empezar partida".

jugador1_listo = False
jugador2_listo = False


"""

----------------------------Funciones

"""
def bbdd():
    basededatos = sqlite3.connect("BasededatosM7.db")
    try:
        cursor = basededatos.cursor()
        cursor.execute("""CREATE TABLE jugadors(
            nick text,
            contrassenya text
            partides_jugades int
            partides_guanyades int
        );""")
        muestra = cursor.fetchall()
    except sqlite3.Error as er:
        print("La tabla ya esta creada.")

    return basededatos
def creacion_usuario():

    ventana_secundaria = Toplevel(root)
    ventana_secundaria.title("Creacion Usuarios")
    ventana_secundaria.geometry('600x600')

    etiqueta = Label(ventana_secundaria, text="Esta es la ventana para la creación de un usuario",
                        font=("Arial", 12))
    etiqueta.pack(pady=50, padx=10)  # Añade padding horizontal y vertical

    usuarionuevo_label = Label(ventana_secundaria, text="Usuario:")
    usuarionuevo_label.pack(pady=(0, 5))  # Añade espacio debajo de la etiqueta usuario

    usuarionuevo_entry = Entry(ventana_secundaria)
    usuarionuevo_entry.pack(pady=(0, 10))  # Añade espacio debajo de la entrada usuario

    contraseñanueva_label = Label(ventana_secundaria, text="Contraseña:")
    contraseñanueva_label.pack(pady=(10, 5))  # Añade espacio debajo de la etiqueta contraseña

    contraseñanueva_entry = Entry(ventana_secundaria, show="*")  # Para mostrar la contraseña como asteriscos
    contraseñanueva_entry.pack(pady=(0, 10))  # Añade espacio debajo de la entrada contraseña

    botonavanzar = Button(ventana_secundaria, text="Crear", command=lambda:insertardatos(usuarionuevo_entry, contraseñanueva_entry))
    botonavanzar.pack(pady=(0, 20))

#Estas dos funciones las utilizo para ir controlando que si la contraseña se falla 3 veces se cierre el programa.
def control_cierre_frame1():
    global contador_intentos
    contador_intentos += 1
    if contador_intentos == 3:
        framejug1.destroy()
        root.quit()
def control_cierre_frame2():
    global contador_intentos
    contador_intentos += 1
    if contador_intentos == 3:
        framejug2.destroy()
        root.quit()

#La dos siguientes funciones las utilizo para coger los datos de los usuarios y poder trabajar con ellos, tambien la enlazo con la funcion
#modificar perfil que utilizare para poder modificar los usuarios y contraseñas.
def obtener_datos_jugador1():
    global jugador1_listo
    usuario = usuario1_entry.get()
    contraseña = contraseña1_entry.get()
    print("Jugador 1 - Usuario:", usuario)
    print("Jugador 1 - Contraseña:", contraseña)

    conexion = sqlite3.connect('BasededatosM7.db')
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM jugadors WHERE nick = ? AND contrassenya = ?", (usuario, contraseña))
    resultado = cursor.fetchone()

    if resultado:
        print("Listo")
        framejug1.destroy()
        jugador1_listo = True
        actualizar_estado_boton_empezar()

        framejugadoriniciado1 = ttk.Frame(root, width=200, height=150)
        framejugadoriniciado1.place(x=150, y=150)

        titulo_jugador1 = ttk.Label(framejugadoriniciado1, text="Jugador 1", font=15)
        titulo_jugador1.grid(row=0, column=0, columnspan=2, padx=5, pady=10)

        nick_jugador1 = ttk.Label(framejugadoriniciado1, text=usuario, font=10)
        nick_jugador1.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        image = Image.open("persona.jpg")
        image = image.resize((100, 100))
        photo = ImageTk.PhotoImage(image)

        label = ttk.Label(framejugadoriniciado1, image=photo)
        label.image = photo
        label.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        porciento_jugador1 = ttk.Label(framejugadoriniciado1, text="%", font=10)
        porciento_jugador1.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        botonparamodoficar = ttk.Button(framejugadoriniciado1, text="Modificar perfil", command=lambda:modificarperfil(usuario,contraseña,image))
        botonparamodoficar.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    else:
        print("Credenciales incorrectas")
        control_cierre_frame1()

    conexion.close()
def obtener_datos_jugador2():
    global jugador2_listo
    usuario = usuario2_entry.get()
    contraseña = contraseña2_entry.get()
    print("Jugador 2 - Usuario:", usuario)
    print("Jugador 2 - Contraseña:", contraseña)

    conexion = sqlite3.connect('BasededatosM7.db')
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM jugadors WHERE nick = ? AND contrassenya = ?", (usuario, contraseña))
    resultado = cursor.fetchone()

    if resultado:
        print("Listo")
        framejug2.destroy()
        jugador2_listo = True
        actualizar_estado_boton_empezar()

        framejugadoriniciado2 = ttk.Frame(root, width=200, height=150)
        framejugadoriniciado2.place(x=700, y=150)

        titulo_jugador2 = ttk.Label(framejugadoriniciado2, text="Jugador 2", font=15)
        titulo_jugador2.grid(row=0, column=0, columnspan=2, padx=5, pady=10)

        nick_jugador2 = ttk.Label(framejugadoriniciado2, text=usuario, font=10)
        nick_jugador2.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        image = Image.open("persona.jpg")
        image = image.resize((100, 100))
        photo = ImageTk.PhotoImage(image)

        label = ttk.Label(framejugadoriniciado2, image=photo)
        label.image = photo
        label.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        porciento_jugador2 = ttk.Label(framejugadoriniciado2, text="%", font=10)
        porciento_jugador2.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

        botonparamodoficar = ttk.Button(framejugadoriniciado2, text="Modificar perfil", command=lambda:modificarperfil(usuario,contraseña))
        botonparamodoficar.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    else:
        print("Credenciales incorrectas")
        control_cierre_frame2()

    conexion.close()

#Esta funcion la utilizo para poder moficar el nombre de cada usuario, una vez cambiado se hace la conexion con la base de datos y se cambia tambien ahi.
def modificarnick(nick_actual):
    def aplicar_cambio():
        nuevo_nick = nuevo_nick_entry.get()
        conn = sqlite3.connect('BasededatosM7.db.')
        cursor = conn.cursor()

        # Para actualizar el nombre de usuario en la base de datos
        cursor.execute("UPDATE jugadors SET nick = ? WHERE nick = ?", (nuevo_nick_entry.get(), nick_actual))

        # Confirmar la transacción y cerrar la conexión.
        conn.commit()
        conn.close()

        # Cerrar la ventana secundaria después de aplicar el cambio
        ventana_nick.destroy()
        root.destroy()

        # Crear la ventana secundaria

    ventana_nick = Toplevel(root)
    ventana_nick.title("Modificar nombre de usuario")
    ventana_nick.geometry('500x300')

    etiqueta = Label(ventana_nick, text="Introduce el nuevo nombre de usuario", font=6)
    etiqueta.pack(pady=10)

    nuevo_nick_entry = Entry(ventana_nick, width=20)
    nuevo_nick_entry.pack(pady=10)

    boton_siguiente = Button(ventana_nick, text="Adelante", command=aplicar_cambio)
    boton_siguiente.pack(pady=10)

#Lo mismo pero para modificar la contraseña.

def modificarcontra(nick_actual):
    def aplicar_cambio():
        nueva_contra = nueva_contra_entry.get()
        # Conectar a la base de datos.
        conn = sqlite3.connect('BasededatosM7.db')
        cursor = conn.cursor()

        # Para actualizar la contraseña en la base de datos
        cursor.execute("UPDATE jugadors SET contrassenya = ? WHERE nick = ?", (nueva_contra, nick_actual))

        # Confirmar la transacción y cerrar la conexión
        conn.commit()
        conn.close()

        # Cerrar la ventana secundaria después de aplicar el cambio
        ventana_contra.destroy()
        root.destroy()

    # Crear la ventana secundaria
    ventana_contra = Toplevel(root)
    ventana_contra.title("Modificar contraseña")
    ventana_contra.geometry('500x300')

    etiqueta = Label(ventana_contra, text="Introduce la nueva contraseña", font=6)
    etiqueta.pack(pady=10)

    nueva_contra_entry = Entry(ventana_contra, width=20, show="*")  # Show="*" para ocultar la contraseña
    nueva_contra_entry.pack(pady=10)

    boton_siguiente = Button(ventana_contra, text="Adelante", command=aplicar_cambio)
    boton_siguiente.pack(pady=10)

# Esta funcion crea la ventana para la modificacion de el usuario, la contraseña y la foto de perfil. Crea los botones y nos enlaza con las funciones.
def modificarperfil(nick, contra, image):

    ventana_mod = Toplevel(root)
    ventana_mod.title("Modificacion de perfiles")
    ventana_mod.geometry('600x600')

    etiqueta = Label(ventana_mod, text="Esta es la ventana para la modificacion de un usuario",font=("Arial", 12))
    etiqueta.pack(pady=50, padx=10)

    etiqueta2 = Label(ventana_mod, text="El usuario a modificar es: " + nick + " .", font=("Arial", 12))
    etiqueta2.pack(pady=50, padx=10)

    botoncambiarnick = Button(ventana_mod, text="Cambiar nombre de usuario", command=lambda:modificarnick(nick))
    botoncambiarnick.pack()

    botonnuevacontra = Button(ventana_mod, text="Cambiar contraseña de usuario", command=lambda:modificarcontra(contra))
    botonnuevacontra.pack()

    botonnuevoperfil = Button(ventana_mod, text="Cambiar foto de perfil de usuario")
    botonnuevoperfil.pack()

# Para insertar los datos de los usuarios en la base de datos.
def insertardatos(datou,datoc):

    conexion = bbdd()
    nick = datou.get()
    contrasenya = datoc.get()
    datos = ("INSERT INTO jugadors (nick,contrassenya) VALUES(?,?)")
    cursor = conexion.cursor()
    cursor.execute(datos,(nick,contrasenya))
    conexion.commit()

def select_from_db():
    # Conectar a la base de datos.
    conn = sqlite3.connect('BasededatosM7.db')
    cursor = conn.cursor()

    # Para la consulta SELECT en la tabla.
    cursor.execute("SELECT * FROM jugadors")
    rows = cursor.fetchall()  # Obtener los resultados de la consulta

    # Crear la ventana.
    ventana = Toplevel(root)
    ventana.title("Consulta a la base de datos")

    # Crear un Treeview para mostrar los datos.
    tree = ttk.Treeview(ventana)
    tree.pack()

    # Definir las columnas
    tree["columns"] = ("Usuario", "Contraseña")
    tree.column("#0", width=0, stretch=NO)  # Columna oculta para el índice

    # Encabezados de las columnas
    tree.heading("Usuario", text="Usuarios")
    tree.heading("Contraseña", text="Contraseñas")

    # Insertar los datos en el Treeview
    for row in rows:
        tree.insert("", END, values=row)

    # Cerrar la conexión a la base de datos
    conn.close()

#Esta funcion la utilizo para comprobar que los jugadores han iniciado sesion (con las variasbles globales que estan a "True" si el inicio de sesion se ha hecho
#correctamente). Al principio del codigo estan definidas en False y en la funcion obtener_datos_jugadorX la paso a True en el momento que se encuentra
#dicho usuario en la bbdd.
def actualizar_estado_boton_empezar():
    global jugador1_listo, jugador2_listo

    if jugador1_listo and jugador2_listo:
        boton_empezar.config(state=NORMAL)
    else:
        boton_empezar.config(state=DISABLED)

def abrir_ventana_juego():
    # Llama a juego.py usando subprocess
    subprocess.run(["python", "juego.py"])


"""

----------------------- Botones

"""

#Creo los botones y los titulos principales.

titulo1= ttk.Label(text="Bienvenido", font=25)
titulo1.place(x=470, y=80)

titulo2 = ttk.Label(text="Buscaminas", foreground="red", font=30)
titulo2.place(x=470, y=120)

botoncrearusuario = ttk.Button(text="Crear usuario", command=creacion_usuario)
botoncrearusuario.place(x=470, y=350)

boton_empezar = ttk.Button(text="Empezar partida", state=DISABLED, command=abrir_ventana_juego)
boton_empezar.place(x=470, y=300)

boton_mostrar = Button(root, text="Mostrar Datos", command=select_from_db)
boton_mostrar.place(x=470, y=400)


""""

Hasta aqui el frame principal, ahora paso a los frame de los dos jugadores.

"""

#Creo los Frames para cada jugador, con sus Labels, Entrys y Botones correspondientes.

# Frame para el jugador 1

framejug1 = ttk.Frame(root, width=200, height=150)
framejug1.place(x=150, y=250)

# Título "Jugador 1"
titulo_jugador1 = ttk.Label(framejug1, text="Jugador 1", font=15)
titulo_jugador1.grid(row=0, column=0, columnspan=2, padx=5, pady=35)

# Entry para el usuario
usuario1_label = ttk.Label(framejug1, text="Usuario:")
usuario1_label.grid(row=1, column=0, padx=5, pady=5)

usuario1_entry = ttk.Entry(framejug1)
usuario1_entry.grid(row=1, column=1, padx=5, pady=5)

# Entry para la contraseña
contraseña1_label = ttk.Label(framejug1, text="Contraseña:")
contraseña1_label.grid(row=2, column=0, padx=5, pady=5)

contraseña1_entry = ttk.Entry(framejug1, show="*")  # Para que la contraseña se muestra como asteriscos
contraseña1_entry.grid(row=2, column=1, padx=5, pady=5)

# Botón para obtener los datos del Jugador 1
obtener_datos_button1 = ttk.Button(framejug1, text="Adelante", command=obtener_datos_jugador1)
obtener_datos_button1.grid(row=3, column=0, columnspan=2, padx=5, pady=10)


"""
------------------------------------------------------
"""

# Frame para el jugador 2
# Esta parte no la comento, basicamente porque es lo mismo que el jugador1 pero dedicado para el jugador2

framejug2 = ttk.Frame(root, width=200, height=150)
framejug2.place(x=700, y=250)

# Título "Jugador 2"
titulo_jugador2 = ttk.Label(framejug2, text="Jugador 2", font=15)
titulo_jugador2.grid(row=0, column=0, columnspan=2, padx=5, pady=35)

# Entry para el usuario
usuario2_label = ttk.Label(framejug2, text="Usuario:")
usuario2_label.grid(row=1, column=0, padx=5, pady=5)

usuario2_entry = ttk.Entry(framejug2)
usuario2_entry.grid(row=1, column=1, padx=5, pady=5)

# Entry para la contraseña
contraseña2_label = ttk.Label(framejug2, text="Contraseña:")
contraseña2_label.grid(row=2, column=0, padx=5, pady=5)

contraseña2_entry = ttk.Entry(framejug2, show="*")
contraseña2_entry.grid(row=2, column=1, padx=5, pady=5)

# Botón para obtener los datos del Jugador 2
obtener_datos_button2 = ttk.Button(framejug2, text="Adelante", command=obtener_datos_jugador2)
obtener_datos_button2.grid(row=3, column=0, columnspan=2, padx=5, pady=10)


root.mainloop()