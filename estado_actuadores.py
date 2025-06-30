# estado_actuadores.py

# Variables globales de estado de actuadores (valores booleanos)
estado_luz = False
estado_ventilacion = False
estado_riego = False
estado_techo = False

def set_estado_luz(valor: bool):
    global estado_luz
    estado_luz = valor

def get_estado_luz() -> bool:
    return estado_luz

def set_estado_ventilacion(valor: bool):
    global estado_ventilacion
    estado_ventilacion = valor

def get_estado_ventilacion() -> bool:
    return estado_ventilacion

def set_estado_riego(valor: bool):
    global estado_riego
    estado_riego = valor

def get_estado_riego() -> bool:
    return estado_riego

def set_estado_techo(valor: bool):
    global estado_techo
    estado_techo = valor

def get_estado_techo() -> bool:
    return estado_techo

