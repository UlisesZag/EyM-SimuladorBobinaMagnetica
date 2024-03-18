#Matplotlib
import matplotlib as mpl
import matplotlib.pyplot as plt

#TKinter
import tkinter as tk
import tkinter.messagebox as tkmb

#Librerias normales
import math

class Bobina:
    def __init__(self, x, current, radius, n):
        self.x = x
        self.current = current
        self.radius = radiusç
        self.n = n

#Funcion que crea el grafico de matplotlib y lo muestra
def create_graphic(x_axis, y_axis, bobina1_x, bobina2_x):
    #Configura el grafico de MatPlotLib
    fig, ax = plt.subplots()  # Create a figure containing a single axes.

    nombre_lineas = ["Campo Magnetico", "Bobina 1", "Bobina 2"]

    ax.plot(x_axis, y_axis)  # Plot some data on the axes.
    ax.plot([bobina1_x, bobina1_x], [max(y_axis), min(y_axis)])

    ax.plot([bobina2_x, bobina2_x], [max(y_axis), min(y_axis)])

    #Titulo
    ax.set_title("Campo Magnetico")
    
    #Configura los ejes
    ax.set_xlabel("Posicion (cm)")
    ax.set_ylabel("Campo Magnetico (V)")

    ax.legend(nombre_lineas, bbox_to_anchor=(1, 1), bbox_transform=fig.transFigure)

    #Finalmente muestra el grafico
    plt.show()

#Calcula un punto de campo magnetico
def calc_mfield_point(x, bobina_x, current, radius, n):
    mfield_point = 0;
    cm = math.pow(10, -3)

    distance = x - bobina_x
    mu0 = (4 * math.pi * math.pow(10,-7))

    if distance == 0:
        mfield_point = (mu0 / 2) * ((n * current) / (radius * cm))
    else:
        nir2 = (n * current * math.pow(radius * cm, 2))
        r2z2 = math.pow(math.pow(radius * cm, 2) + math.pow(distance * cm, 2), 1.5)
        mfield_point = (mu0 / 2) * (nir2 / r2z2)
    
    return mfield_point

#Calcula los campos magneticos
def calc_mfields(bobina1_x, bobina2_x, current, radius, n, rango):
    mfields = []
    print("Rango: ", rango[0], " - ", rango[1])
    for i in range(rango[0], rango[1], 1):
        point = calc_mfield_point(i, bobina1_x, current, radius, n) + calc_mfield_point(i, bobina2_x, current, radius, n)
        mfields.append(point)
        #print("Campo magnetico en x=", i, ": ", point, ";")
    
    return mfields

def calcular_y_graficar(bobina1_x, bobina2_x, rango, n, current, radius):
    if radius <= 0:
        tkmb.showerror("Simulador Campos Magneticos", "ERROR: Por favor ingrese un radio mayor que cero.")
        return

    print("Graficando . . . ")

    #listas para hacer el plot
    x_axis = []
    y_axis = []
    for i in range(rango[0], rango[1], 1):
        x_axis.append(i) #Llena el eje X con los puntos a calcular

    #Calcula los valores
    y_axis = calc_mfields(bobina1_x, bobina2_x, current, radius, n, rango)

    create_graphic(x_axis, y_axis, bobina1_x, bobina2_x)

def makeMainWindow():
    print("Creando ventana . . . ")

    global window

    window.title("Simulador Campos Magneticos")
    window.geometry("540x335")
    window.resizable(False, False)

    tk.Label(master=window, text="Simulador Campos Magneticos", anchor="center", font=("Helvetica",20)).pack()

    #Separador
    tk.Frame(window, width=250, height=3, relief=tk.SUNKEN).pack()
    tk.Frame(window, width=250, height=10).pack()

    #Posicion de las bobinas
    tk.Label(master=window, text="Posicion de las bobinas:").pack()

    frame_posicion_bobinas = tk.Frame(master=window)
    frame_posicion_bobinas.pack()

    tk.Label(master=frame_posicion_bobinas, text="Bobina 1:").pack(side=tk.LEFT)
    entry_Bobina1 = tk.Entry(master=frame_posicion_bobinas)
    entry_Bobina1.pack(side=tk.LEFT)
    entry_Bobina1.insert(0, "-10") #default

    tk.Label(master=frame_posicion_bobinas, text="Bobina 2:").pack(side=tk.LEFT)
    entry_Bobina2 = tk.Entry(master=frame_posicion_bobinas)
    entry_Bobina2.pack(side=tk.LEFT)
    entry_Bobina2.insert(0, "10") #default

    #Separador
    tk.Frame(window, width=250, height=3, relief=tk.SUNKEN).pack()
    tk.Frame(window, width=250, height=10).pack()

    #Rango de distancia
    tk.Label(master=window, text="Rango de distancias:").pack()

    frame_rango = tk.Frame(master=window)
    frame_rango.pack()

    tk.Label(master=frame_rango, text="Inicio del rango:").pack(side=tk.LEFT)
    entry_RangoInicio = tk.Entry(master=frame_rango)
    entry_RangoInicio.pack(side=tk.LEFT)
    entry_RangoInicio.insert(0, "-30") #default

    tk.Label(master=frame_rango, text="Fin del rango:").pack(side=tk.LEFT)
    entry_RangoFin = tk.Entry(master=frame_rango)
    entry_RangoFin.pack(side=tk.LEFT)
    entry_RangoFin.insert(0, "30") #default

    #Separador
    tk.Frame(window, width=250, height=3, relief=tk.SUNKEN).pack()
    tk.Frame(window, width=250, height=10).pack()

    #Datos
    tk.Label(master=window, text="Radio de las bobinas:").pack()
    entry_Radius = tk.Entry(master=window)
    entry_Radius.pack()
    entry_Radius.insert(0, "10") #default

    tk.Label(master=window, text="N:").pack()
    entry_N = tk.Entry(master=window)
    entry_N.pack()
    entry_N.insert(0, "100") #default

    tk.Label(master=window, text="Corriente:").pack()
    entry_Current = tk.Entry(master=window)
    entry_Current.pack()
    entry_Current.insert(0, "0.85") #default

    #Separador
    tk.Frame(window, width=250, height=3, relief=tk.SUNKEN).pack()
    tk.Frame(window, width=250, height=10).pack()

    boton_calcular = tk.Button(master=window, text="Calcular", command = lambda:calcular_y_graficar(
        #Por alguna razon que no entiendo las posiciones de las bobinas estan invertidas
        #Aca invierte la posicion de las bobinas.
        int(entry_Bobina1.get()),
        int(entry_Bobina2.get()),
        (int(entry_RangoInicio.get()), int(entry_RangoFin.get())),
        int(entry_N.get()),
        float(entry_Current.get()), 
        int(entry_Radius.get()))
        )
    boton_calcular.pack()


#Programa Principal

window = tk.Tk()

makeMainWindow()

window.mainloop()