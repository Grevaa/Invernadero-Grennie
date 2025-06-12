import tkinter as tk
from tkinter import ttk
import csv
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

def cargar_datos():
    """Carga los datos del CSV y devuelve listas separadas por columna."""
    fechas, humedades, temperaturas, phs = [], [], [], []
    try:
        with open("datos/historial.csv", newline="") as archivo:
            lector = csv.reader(archivo)
            next(lector)  # Saltar encabezados
            for fila in lector:
                fechas.append(fila[0])
                humedades.append(float(fila[1]))
                temperaturas.append(float(fila[2]))
                phs.append(float(fila[3]))
        return fechas, humedades, temperaturas, phs
    except FileNotFoundError:
        return [], [], [], []

def mostrar_grafico(tipo):
    """Muestra un gráfico según el tipo solicitado (humedad/temperatura/ph)."""
    fechas, humedades, temperaturas, phs = cargar_datos()
    if not fechas:
        tk.messagebox.showerror("Error", "No hay datos para graficar.")
        return

    fig = Figure(figsize=(5, 3), dpi=100)
    ax = fig.add_subplot(111)

    if tipo == "humedad":
        ax.plot(fechas, humedades, 'b-', label="Humedad (%)")
        ax.set_title("Variación de Humedad")
        ax.set_ylabel("Humedad (%)")
    elif tipo == "temperatura":
        ax.plot(fechas, temperaturas, 'r-', label="Temperatura (°C)")
        ax.set_title("Variación de Temperatura")
        ax.set_ylabel("Temperatura (°C)")
    elif tipo == "ph":
        ax.plot(fechas, phs, 'g-', label="pH")
        ax.set_title("Variación de pH")
        ax.set_ylabel("pH")

    ax.set_xlabel("Fecha/Hora")
    ax.legend()
    ax.grid(True)

    # Rotar fechas para mejor visualización
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

    # Mostrar gráfico en una nueva ventana
    ventana_grafico = tk.Toplevel()
    ventana_grafico.title(f"Gráfico de {tipo}")
    canvas = FigureCanvasTkAgg(fig, master=ventana_grafico)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

def mostrar_ventana_datos(usuario):
    ventana = tk.Tk()
    ventana.title(f"Datos del Invernadero - Usuario: {usuario}")
    ventana.geometry("800x600")

    # Frame para los botones de gráficos
    frame_botones = ttk.Frame(ventana)
    frame_botones.pack(pady=10)

    btn_humedad = ttk.Button(frame_botones, text="Gráfico Humedad",
                            command=lambda: mostrar_grafico("humedad"))
    btn_humedad.pack(side=tk.LEFT, padx=5)

    btn_temp = ttk.Button(frame_botones, text="Gráfico Temperatura",
                         command=lambda: mostrar_grafico("temperatura"))
    btn_temp.pack(side=tk.LEFT, padx=5)

    btn_ph = ttk.Button(frame_botones, text="Gráfico pH",
                       command=lambda: mostrar_grafico("ph"))
    btn_ph.pack(side=tk.LEFT, padx=5)

    # Tabla de datos
    tree = ttk.Treeview(ventana)
    tree["columns"] = ("Fecha", "Humedad", "Temperatura", "pH")
    tree.column("#0", width=0, stretch=tk.NO)  # Columna fantasma
    for col in tree["columns"]:
        tree.column(col, width=100, anchor="center")
        tree.heading(col, text=col)

    # Scrollbar
    scroll = ttk.Scrollbar(ventana, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scroll.set)
    scroll.pack(side=tk.RIGHT, fill=tk.Y)
    tree.pack(expand=True, fill="both", padx=10, pady=10)

    # Cargar datos en la tabla
    try:
        with open("datos/historial.csv", newline="") as archivo:
            lector = csv.reader(archivo)
            next(lector)  # Saltar encabezados
            for fila in lector:
                tree.insert("", "end", values=fila)
    except FileNotFoundError:
        tk.messagebox.showerror("Error", "No se encontró el archivo de datos.")

    ventana.mainloop()
