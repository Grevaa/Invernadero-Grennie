import tkinter as tk
from tkinter import ttk
import ui_estilos as ui
from gestion_datos import crear_frame_estado
from gestion_historial import crear_pestana_historial
import gestion_actuadores

# Para el cliente
from gestion_servicio_cliente import crear_pestana_servicio_cliente


def mostrar_ventana_datos(usuario):
    ventana = tk.Tk()
    ui.aplicar_estilo_ventana(ventana, f"Invernadero - {usuario}", "800x600")

    notebook = ttk.Notebook(ventana)
    notebook.pack(fill="both", expand=True)

    # Estado Actual
    tab_estado = crear_frame_estado(notebook, usuario)
    notebook.add(tab_estado, text="Estado Actual")

    # Historial (con gráficos embebidos)
    tab_historial = crear_pestana_historial(notebook)
    notebook.add(tab_historial, text="Historial")

    # Actuadores
    tab_actuadores = gestion_actuadores.crear_pestana_actuadores(notebook)
    notebook.add(tab_actuadores, text="Actuadores")

    # Para el cliente
    notebook.add(crear_pestana_servicio_cliente(notebook, usuario), text="Soporte Técnico")

    ventana.mainloop()














