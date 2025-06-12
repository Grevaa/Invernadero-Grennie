import random

def leer_humedad():
    # Simula un sensor de humedad en % (30-90)
    return random.randint(30, 90)

def leer_temperatura():
    # Simula un sensor de temperatura en °C (18.0 - 35.0)
    return round(random.uniform(18.0, 35.0), 1)

def leer_ph():
    # Simula un sensor de pH (acidez) (5.5 - 7.5)
    return round(random.uniform(5.5, 7.5), 2)
