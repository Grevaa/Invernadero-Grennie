import tkinter as tk
from tkinter import messagebox
import hashlib

from interfaz_datos import mostrar_ventana_datos
from interfaz_admin import mostrar_panel_admin
import gestion_usuarios  # módulo con funciones para usuarios
import ui_estilos as ui  # nuevo módulo de estilos

def encriptar_md5(texto):
    return hashlib.md5(texto.encode()).hexdigest()

def verificar_credenciales(usuario, clave):
    clave_encriptada = encriptar_md5(clave)
    usuarios = gestion_usuarios.cargar_usuarios()
    for fila in usuarios:
        if fila["usuario"] == usuario and fila["clave"] == clave_encriptada:
            return fila["tipo"]
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
ui.aplicar_estilo_ventana(ventana, "Inicio de Sesión", "360x640")

lbl_titulo = ui.crear_label(ventana, "Iniciar Sesión", font_t=ui.FUENTE_TITULO)
lbl_titulo.pack(pady=30)

frm_formulario = ui.crear_frame(ventana)
frm_formulario.pack(padx=20, pady=20, fill="both", expand=True)

ui.crear_label(frm_formulario, "Usuario").pack(pady=10)
entrada_usuario = ui.crear_entry(frm_formulario)
entrada_usuario.pack(pady=5, fill="x")

ui.crear_label(frm_formulario, "Contraseña").pack(pady=10)
entrada_clave = ui.crear_entry(frm_formulario, show="*")
entrada_clave.pack(pady=5, fill="x")

btn_iniciar = ui.crear_boton(ventana, "Iniciar sesión", iniciar_sesion)
btn_iniciar.pack(pady=20, fill="x", padx=40)

ventana.mainloop()



