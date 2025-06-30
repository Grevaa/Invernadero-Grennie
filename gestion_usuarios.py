# === gestion_usuarios.py ===
import manejo_csv
from tkinter import messagebox
import hashlib

RUTA_USUARIOS = "datos/usuarios.csv"

def encriptar_md5(texto):
    return hashlib.md5(texto.encode()).hexdigest()

def cargar_usuarios():
    return manejo_csv.leer_csv_dict(RUTA_USUARIOS)

def cargar_usuarios_cliente():
    return [u['usuario'] for u in cargar_usuarios() if u['tipo'] == 'cliente']

def agregar_usuario(usuario, clave, tipo):
    usuarios = cargar_usuarios()
    for u in usuarios:
        if u['usuario'] == usuario:
            messagebox.showerror("Error", f"El usuario '{usuario}' ya existe.")
            return False
    clave_md5 = encriptar_md5(clave)
    manejo_csv.agregar_csv_dict(RUTA_USUARIOS, ["usuario", "clave", "tipo"], {
        "usuario": usuario,
        "clave": clave_md5,
        "tipo": tipo
    })
    return True

def editar_usuario(usuario, nueva_clave, nuevo_tipo):
    usuarios = cargar_usuarios()
    encontrado = False
    for u in usuarios:
        if u['usuario'] == usuario:
            u['tipo'] = nuevo_tipo
            if nueva_clave:
                u['clave'] = encriptar_md5(nueva_clave)
            encontrado = True
    if not encontrado:
        messagebox.showerror("Error", f"Usuario '{usuario}' no encontrado.")
        return False
    manejo_csv.escribir_csv_dict(RUTA_USUARIOS, ["usuario", "clave", "tipo"], usuarios)
    return True

def eliminar_usuario(usuario_a_eliminar):
    usuarios = cargar_usuarios()
    for u in usuarios:
        if u['usuario'] == usuario_a_eliminar and u['tipo'] == 'admin':
            messagebox.showwarning("Advertencia", "No se permite eliminar usuarios administradores.")
            return False
    usuarios_filtrados = [u for u in usuarios if u['usuario'] != usuario_a_eliminar]
    manejo_csv.escribir_csv_dict(RUTA_USUARIOS, ["usuario", "clave", "tipo"], usuarios_filtrados)
    return True
