import tkinter as tk
from tkinter import ttk
import csv

def cargar_datos(treeview):
    with open("datos/historial.csv", newline="") as archivo:
        lector = csv.reader(archivo)
        encabezados = next(lector)  # Leer encabezados
        treeview["columns"] = encabezados
        treeview["show"] = "headings"

        for col in encabezados:
            treeview.heading(col, text=col)
            treeview.column(col, width=100)

        for fila in lector:
            treeview.insert("", "end", values=fila)

def mostrar_ventana_datos(usuario):
    ventana = tk.Tk()
    ventana.title(f"Historial de Datos - Usuario: {usuario}")
    ventana.geometry("500x400")

    label = tk.Label(ventana, text="Datos del Invernadero", font=("Arial", 14))
    label.pack(pady=10)

    tabla = ttk.Treeview(ventana)
    tabla.pack(expand=True, fill="both", padx=10, pady=10)

    cargar_datos(tabla)

    ventana.mainloop()
