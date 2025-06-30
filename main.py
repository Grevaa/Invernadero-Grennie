import time
from datetime import datetime
from sensores import leer_humedad, leer_temperatura, leer_ph
from logica_control import controlar_riego, controlar_ventilacion, controlar_luz, evaluar_ph
import csv
import os
from manejo_csv import agregar_csv_dict

# Crear carpeta datos si no existe
if not os.path.exists("datos"):
    os.makedirs("datos")

# Archivo para guardar datos
ARCHIVO_DATOS = "datos/historial.csv"

# Escribir encabezados si archivo vacío
if not os.path.exists(ARCHIVO_DATOS) or os.path.getsize(ARCHIVO_DATOS) == 0:
    with open(ARCHIVO_DATOS, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["FechaHora", "Humedad", "Temperatura", "pH"])

def guardar_datos(humedad, temperatura, ph):
    agregar_csv_dict("datos/historial.csv",
                     ["FechaHora", "Humedad", "Temperatura", "pH"],
                     {"FechaHora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                      "Humedad": humedad,
                      "Temperatura": temperatura,
                      "pH": ph})

def main():
    print("=== Sistema de Invernadero Inteligente - Simulación ===")
    try:
        while True:
            humedad = leer_humedad()
            temperatura = leer_temperatura()
            ph = leer_ph()
            hora_actual = datetime.now().hour

            print(f"\nLectura sensores: Humedad={humedad}%, Temperatura={temperatura}°C, pH={ph}")

            controlar_riego(humedad)
            controlar_ventilacion(temperatura)
            controlar_luz(hora_actual)
            evaluar_ph(ph)

            guardar_datos(humedad, temperatura, ph)

            # Esperar 10 segundos antes de la siguiente lectura (puedes cambiarlo)
            time.sleep(10)

    except KeyboardInterrupt:
        print("\nSimulación finalizada por el usuario.")

if __name__ == "__main__":
    main()
