import tkinter as tk
from tkinter import messagebox
import ui_estilos as ui
import estado_actuadores

def crear_pestana_actuadores(parent):
    frame = tk.Frame(parent, bg=ui.COLOR_FRAME)

    lbl_titulo = ui.crear_label(frame, "Control de Actuadores", font_t=ui.FUENTE_TITULO)
    lbl_titulo.pack(pady=20)

    btns_frame = tk.Frame(frame, bg=ui.COLOR_FRAME)
    btns_frame.pack(pady=10, fill="x", padx=20)

    # Luz
    luz_frame = tk.Frame(btns_frame, bg=ui.COLOR_FRAME)
    luz_frame.pack(pady=5, fill="x")
    ui.crear_label(luz_frame, "Luz:", font_t=ui.FUENTE_NORMAL).pack(side="left")
    ui.crear_boton(luz_frame, "Encender", encender_luz).pack(side="left", padx=5)
    ui.crear_boton(luz_frame, "Apagar", apagar_luz).pack(side="left", padx=5)

    # Ventilación
    vent_frame = tk.Frame(btns_frame, bg=ui.COLOR_FRAME)
    vent_frame.pack(pady=5, fill="x")
    ui.crear_label(vent_frame, "Ventilación:", font_t=ui.FUENTE_NORMAL).pack(side="left")
    ui.crear_boton(vent_frame, "Activar", activar_ventilacion).pack(side="left", padx=5)
    ui.crear_boton(vent_frame, "Desactivar", desactivar_ventilacion).pack(side="left", padx=5)

    # Riego
    riego_frame = tk.Frame(btns_frame, bg=ui.COLOR_FRAME)
    riego_frame.pack(pady=5, fill="x")
    ui.crear_label(riego_frame, "Riego:", font_t=ui.FUENTE_NORMAL).pack(side="left")
    ui.crear_boton(riego_frame, "Activar", activar_riego).pack(side="left", padx=5)
    ui.crear_boton(riego_frame, "Desactivar", desactivar_riego).pack(side="left", padx=5)

    # Techo
    techo_frame = tk.Frame(btns_frame, bg=ui.COLOR_FRAME)
    techo_frame.pack(pady=5, fill="x")
    ui.crear_label(techo_frame, "Techo:", font_t=ui.FUENTE_NORMAL).pack(side="left")
    ui.crear_boton(techo_frame, "Abrir", abrir_techo).pack(side="left", padx=5)
    ui.crear_boton(techo_frame, "Cerrar", cerrar_techo).pack(side="left", padx=5)

    return frame

def encender_luz():
    estado_actuadores.estado_luz = True
    messagebox.showinfo("Luz", "Luz encendida 💡")

def apagar_luz():
    estado_actuadores.estado_luz = False
    messagebox.showinfo("Luz", "Luz apagada 💡")

def activar_ventilacion():
    estado_actuadores.estado_ventilacion = True
    messagebox.showinfo("Ventilación", "Ventilación activada 🌬️")

def desactivar_ventilacion():
    estado_actuadores.estado_ventilacion = False
    messagebox.showinfo("Ventilación", "Ventilación desactivada 🌬️")

def activar_riego():
    estado_actuadores.estado_riego = True
    messagebox.showinfo("Riego", "Riego activado 💧")

def desactivar_riego():
    estado_actuadores.estado_riego = False
    messagebox.showinfo("Riego", "Riego desactivado 💧")

def abrir_techo():
    estado_actuadores.estado_techo = True
    messagebox.showinfo("Techo", "Techo abierto 🏠")

def cerrar_techo():
    estado_actuadores.estado_techo = False
    messagebox.showinfo("Techo", "Techo cerrado 🏠")






