# manejo_servicio.py
import manejo_csv
from datetime import datetime
from tkinter import messagebox

RUTA_SERVICIOS = "datos/servicios.csv"
CAMPOS = ["id_servicio", "id_dispositivo", "usuario_cliente", "fecha_creacion", "descripcion",
          "estado", "tecnico_asignado", "fecha_cierre", "comentarios"]

def cargar_servicios():
    return manejo_csv.leer_csv_dict(RUTA_SERVICIOS)

def guardar_servicios(servicios):
    manejo_csv.escribir_csv_dict(RUTA_SERVICIOS, CAMPOS, servicios)

def generar_id_servicio(servicios):
    numeros = [int(s["id_servicio"][1:]) for s in servicios if s["id_servicio"].startswith("s") and s["id_servicio"][1:].isdigit()]
    nuevo_num = max(numeros, default=0) + 1
    return f"s{nuevo_num:03d}"

def agregar_servicio(id_dispositivo, usuario_cliente, descripcion):
    servicios = cargar_servicios()
    nuevo_id = generar_id_servicio(servicios)
    fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    nuevo_servicio = {
        "id_servicio": nuevo_id,
        "id_dispositivo": id_dispositivo,
        "usuario_cliente": usuario_cliente,
        "fecha_creacion": fecha_creacion,
        "descripcion": descripcion,
        "estado": "pendiente",
        "tecnico_asignado": "",
        "fecha_cierre": "",
        "comentarios": ""
    }
    servicios.append(nuevo_servicio)
    guardar_servicios(servicios)
    return nuevo_id

def editar_servicio(id_servicio, estado=None, tecnico_asignado=None, fecha_cierre=None, comentarios=None):
    servicios = cargar_servicios()
    encontrado = False
    for s in servicios:
        if s["id_servicio"] == id_servicio:
            if estado is not None:
                s["estado"] = estado
            if tecnico_asignado is not None:
                s["tecnico_asignado"] = tecnico_asignado
            if fecha_cierre is not None:
                s["fecha_cierre"] = fecha_cierre
            if comentarios is not None:
                s["comentarios"] = comentarios
            encontrado = True
            break
    if not encontrado:
        messagebox.showerror("Error", f"Servicio {id_servicio} no encontrado.")
        return False
    guardar_servicios(servicios)
    return True

def eliminar_servicio(id_servicio):
    servicios = cargar_servicios()
    servicios_filtrados = [s for s in servicios if s["id_servicio"] != id_servicio]
    if len(servicios) == len(servicios_filtrados):
        messagebox.showerror("Error", f"Servicio {id_servicio} no encontrado.")
        return False
    guardar_servicios(servicios_filtrados)
    return True

def filtrar_servicios(estado=None, tecnico=None, usuario_cliente=None):
    servicios = cargar_servicios()
    if estado:
        servicios = [s for s in servicios if s["estado"] == estado]
    if tecnico:
        servicios = [s for s in servicios if s["tecnico_asignado"] == tecnico]
    if usuario_cliente:
        servicios = [s for s in servicios if s["usuario_cliente"] == usuario_cliente]
    return servicios
