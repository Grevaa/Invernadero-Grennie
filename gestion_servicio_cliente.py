# gestion_servicio_cliente.py
import tkinter as tk
from tkinter import ttk, messagebox
import manejo_servicios
import gestion_dispositivos
import ui_estilos as ui

def crear_pestana_servicio_cliente(parent, usuario_cliente):
    frame = ui.crear_frame(parent)

    lbl_titulo = ui.crear_label(frame, "Crear Llamada de Servicio", font_t=ui.FUENTE_TITULO)
    lbl_titulo.pack(pady=10)

    frm_form = ui.crear_frame(frame)
    frm_form.pack(fill="x", padx=20, pady=10)
    frm_form.columnconfigure(1, weight=1)

    ui.crear_label(frm_form, "Dispositivo:").grid(row=0, column=0, sticky="e", pady=5)
    dispositivos_cliente = [d["id_dispositivo"] for d in gestion_dispositivos.cargar_dispositivos()
                            if d["usuario"] == usuario_cliente]
    combo_disp = ttk.Combobox(frm_form, values=dispositivos_cliente, state="readonly")
    combo_disp.grid(row=0, column=1, sticky="ew", pady=5)

    ui.crear_label(frm_form, "Descripción:").grid(row=1, column=0, sticky="ne", pady=5)
    txt_descripcion = tk.Text(frm_form, height=4)
    txt_descripcion.grid(row=1, column=1, sticky="ew", pady=5)

    def enviar_llamada():
        dispositivo = combo_disp.get().strip()
        descripcion = txt_descripcion.get("1.0", "end").strip()

        if not dispositivo or not descripcion:
            messagebox.showerror("Error", "Debe seleccionar un dispositivo y escribir una descripción.")
            return

        nuevo_id = manejo_servicios.agregar_servicio(dispositivo, usuario_cliente, descripcion)
        messagebox.showinfo("Enviado", f"Llamado registrado con ID: {nuevo_id}")
        combo_disp.set("")
        txt_descripcion.delete("1.0", "end")

    btn_enviar = ui.crear_boton(frame, "Enviar Solicitud", enviar_llamada)
    btn_enviar.pack(pady=10, padx=20, fill="x")

    return frame
