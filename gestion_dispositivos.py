# === gestion_dispositivos.py ===
import manejo_csv
from tkinter import messagebox
from datetime import datetime

RUTA_DISPOSITIVOS = "datos/dispositivos.csv"

def cargar_dispositivos():
    return manejo_csv.leer_csv_dict(RUTA_DISPOSITIVOS)

def agregar_dispositivo(id_disp, usuario, ubicacion, estado):
    dispositivos = cargar_dispositivos()
    for d in dispositivos:
        if d['id_dispositivo'] == id_disp:
            messagebox.showerror("Error", f"El ID '{id_disp}' ya existe.")
            return False
        #if d['usuario'] == usuario:
        #    messagebox.showerror("Error", f"El usuario '{usuario}' ya tiene un dispositivo asociado.")
        #    return False
    fecha_registro = datetime.now().strftime("%Y-%m-%d")
    manejo_csv.agregar_csv_dict(RUTA_DISPOSITIVOS,
        ["id_dispositivo", "usuario", "ubicacion", "estado", "fecha_registro"],
        {"id_dispositivo": id_disp, "usuario": usuario, "ubicacion": ubicacion, "estado": estado, "fecha_registro": fecha_registro})
    return True

def editar_dispositivo(id_disp, usuario, ubicacion, estado):
    dispositivos = cargar_dispositivos()
    encontrado = False
    for d in dispositivos:
        if d['id_dispositivo'] == id_disp:
            for x in dispositivos:
                if x['usuario'] == usuario and x['id_dispositivo'] != id_disp:
                    messagebox.showerror("Error", f"El usuario '{usuario}' ya tiene otro dispositivo.")
                    return False
            d['usuario'] = usuario
            d['ubicacion'] = ubicacion
            d['estado'] = estado
            encontrado = True
    if not encontrado:
        messagebox.showerror("Error", f"No se encontró el dispositivo con ID '{id_disp}'.")
        return False
    manejo_csv.escribir_csv_dict(RUTA_DISPOSITIVOS,
        ["id_dispositivo", "usuario", "ubicacion", "estado", "fecha_registro"],
        dispositivos)
    return True

def eliminar_dispositivo(id_disp):
    dispositivos = cargar_dispositivos()
    dispositivos_filtrados = [d for d in dispositivos if d['id_dispositivo'] != id_disp]
    manejo_csv.escribir_csv_dict(RUTA_DISPOSITIVOS,
        ["id_dispositivo", "usuario", "ubicacion", "estado", "fecha_registro"],
        dispositivos_filtrados)
    return True
