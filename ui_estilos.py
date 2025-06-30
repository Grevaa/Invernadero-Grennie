import tkinter as tk
from tkinter import ttk, font

# Colores generales
COLOR_FONDO = "#2c3e50"        # Fondo principal de ventanas
COLOR_FRAME = "#34495e"         # Fondo de frames secundarios
COLOR_BOTON = "#2980b9"         # Fondo de botones
COLOR_TEXTO = "white"           # Color de texto general

# Colores específicos para valores de sensores y estados
COLOR_HUMEDAD = "#85c1e9"       # Azul claro para humedad
COLOR_TEMPERATURA = "#f39c12"   # Naranja para temperatura
COLOR_PH = "#27ae60"             # Verde para pH
COLOR_ESTADO = "yellow"          # Amarillo para estado general

# Fuentes
FUENTE_TITULO = ("Arial", 18, "bold")
FUENTE_SUBTITULO = ("Arial", 14, "bold")
FUENTE_NORMAL = ("Arial", 12)
FUENTE_VALOR = ("Arial", 16, "bold")
FUENTE_ESTADO = ("Arial", 14, "bold")
FUENTE_BOTON = ("Arial", 12, "bold")

def aplicar_estilo_ventana(win, title, size="320x400"):
    win.title(title)
    win.geometry(size)
    win.configure(bg=COLOR_FONDO)

def crear_boton(master, text, command, **kwargs):
    return tk.Button(master, text=text, command=command,
                     bg=COLOR_BOTON, fg=COLOR_TEXTO,
                     font=FUENTE_BOTON, relief="flat", **kwargs)

def crear_label(master, text, font_t=FUENTE_NORMAL, **kwargs):
    if "fg" not in kwargs:
        kwargs["fg"] = COLOR_TEXTO
    if "bg" not in kwargs:
        kwargs["bg"] = COLOR_FONDO
    return tk.Label(master, text=text, font=font_t, **kwargs)

def crear_entry(master, **kwargs):
    return tk.Entry(master, font=FUENTE_NORMAL, **kwargs)

def crear_frame(master, bg=COLOR_FRAME, **kwargs):
    return tk.Frame(master, bg=bg, **kwargs)


