from actuadores import *

def controlar_riego(humedad, parametros):
    min_humedad = float(parametros.get("humedad_min", 40))
    max_humedad = float(parametros.get("humedad_max", 70))
    if humedad < min_humedad:
        activar_riego()
    elif humedad > max_humedad:
        desactivar_riego()
    else:
        print("[INFO] 💧 Humedad dentro del rango óptimo.")

def controlar_ventilacion(temperatura, parametros):
    temp_min = float(parametros.get("temp_min", 22))
    temp_max = float(parametros.get("temp_max", 30))
    if temperatura > temp_max:
        activar_ventilacion()
    elif temperatura < temp_min:
        desactivar_ventilacion()
    else:
        print("[INFO] 🌡️ Temperatura dentro del rango óptimo.")

def controlar_luz(hora_actual, parametros):
    hora_inicio = int(parametros.get("hora_luz_inicio", 18))
    hora_fin = int(parametros.get("hora_luz_fin", 6))
    # Asumiendo que la luz se enciende si es fuera del rango hora_fin - hora_inicio
    if hora_actual >= hora_inicio or hora_actual < hora_fin:
        encender_luz()
    else:
        apagar_luz()

def evaluar_ph(ph, parametros):
    ph_min = float(parametros.get("ph_min", 5.8))
    ph_max = float(parametros.get("ph_max", 7.0))
    if ph < ph_min or ph > ph_max:
        print(f"[ALERTA] ⚠️ pH fuera de rango: {ph}")
    else:
        print("[INFO] 🧪 pH dentro del rango óptimo.")

