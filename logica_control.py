from actuadores import *

def controlar_riego(humedad):
    if humedad < 40:
        activar_riego()
    elif humedad > 70:
        desactivar_riego()
    else:
        print("[INFO] 💧 Humedad dentro del rango óptimo.")

def controlar_ventilacion(temperatura):
    if temperatura > 30:
        activar_ventilacion()
    elif temperatura < 22:
        desactivar_ventilacion()
    else:
        print("[INFO] 🌡️ Temperatura dentro del rango óptimo.")

def controlar_luz(hora_actual):
    # Encender luz si es antes de las 6am o después de las 6pm
    if hora_actual < 6 or hora_actual >= 18:
        encender_luz()
    else:
        apagar_luz()

def evaluar_ph(ph):
    if ph < 5.8 or ph > 7.0:
        print(f"[ALERTA] ⚠️ pH fuera de rango: {ph}")
    else:
        print("[INFO] 🧪 pH dentro del rango óptimo.")
