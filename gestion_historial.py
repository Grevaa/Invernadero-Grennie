import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from manejo_csv import leer_csv_dict
import ui_estilos as ui

RUTA_HISTORIAL = "datos/historial.csv"

def crear_pestana_historial(parent):
    frame = tk.Frame(parent, bg=ui.COLOR_FRAME)

    tree = ttk.Treeview(frame, columns=("FechaHora", "Humedad", "Temperatura", "pH"), show="headings")
    for col in ("FechaHora", "Humedad", "Temperatura", "pH"):
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    datos = leer_csv_dict(RUTA_HISTORIAL)
    for fila in datos:
        tree.insert("", "end", values=(fila["FechaHora"], fila["Humedad"], fila["Temperatura"], fila["pH"]))

    btn_frame = ui.crear_frame(frame)
    btn_frame.pack(pady=10)

    graf_frame = ui.crear_frame(frame)
    graf_frame.pack(fill="both", expand=True, padx=10, pady=10)

    canvas = None

    def graficar(variable, titulo):
        nonlocal canvas
        for widget in graf_frame.winfo_children():
            widget.destroy()

        if not datos:
            messagebox.showinfo("Sin datos", "No hay datos para graficar.")
            return

        tiempos = [d["FechaHora"] for d in datos]
        valores = [float(d[variable]) for d in datos]

        fig, ax = plt.subplots(figsize=(8, 3), dpi=100)
        ax.plot(tiempos, valores, marker="o", linestyle="-")
        ax.set_title(titulo)
        ax.set_xlabel("Fecha y Hora")
        ax.set_ylabel(variable)
        ax.tick_params(axis='x', rotation=45)
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=graf_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    ui.crear_boton(btn_frame, "Graficar Humedad",
                   command=lambda: graficar("Humedad", "Historial de Humedad (%)")).pack(side="left", padx=5)
    ui.crear_boton(btn_frame, "Graficar Temperatura",
                   command=lambda: graficar("Temperatura", "Historial de Temperatura (°C)")).pack(side="left", padx=5)
    ui.crear_boton(btn_frame, "Graficar pH",
                   command=lambda: graficar("pH", "Historial de pH")).pack(side="left", padx=5)

    return frame


