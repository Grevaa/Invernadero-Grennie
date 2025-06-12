import tkinter as tk
from tkinter import messagebox
import csv
import hashlib

from interfaz_datos import mostrar_ventana_datos
from interfaz_admin import mostrar_panel_admin

def encriptar_md5(texto):
    return hashlib.md5(texto.encode()).hexdigest()

def verificar_credenciales(usuario, clave):
    clave_encriptada = encriptar_md5(clave)
    try:
        with open("datos/usuarios.csv", newline="") as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                if fila["usuario"] == usuario and fila["clave"] == clave_encriptada:
                    return fila["tipo"]  # Retorna tipo: "admin" o "cliente"
    except FileNotFoundError:
        messagebox.showerror("Error", "Archivo de usuarios no encontrado.")
    return None


def iniciar_sesion():
    usuario = entrada_usuario.get()
    clave = entrada_clave.get()

    tipo = verificar_credenciales(usuario, clave)

    if tipo:
        ventana.destroy()
        if tipo == "cliente":
            mostrar_ventana_datos(usuario)
        elif tipo == "admin":
            mostrar_panel_admin(usuario)
    else:
        messagebox.showerror("Acceso denegado", "Usuario o contraseña incorrectos ❌")

# Interfaz de login
ventana = tk.Tk()
ventana.title("Inicio de Sesión")
ventana.geometry("300x200")

tk.Label(ventana, text="Usuario").pack(pady=5)
entrada_usuario = tk.Entry(ventana)
entrada_usuario.pack()

tk.Label(ventana, text="Contraseña").pack(pady=5)
entrada_clave = tk.Entry(ventana, show="*")
entrada_clave.pack()

tk.Button(ventana, text="Iniciar sesión", command=iniciar_sesion).pack(pady=15)

ventana.mainloop()
