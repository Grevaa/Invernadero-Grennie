# gestion_servicio_admin.py
import tkinter as tk
from tkinter import ttk, messagebox
import manejo_servicios
import ui_estilos as ui
from datetime import datetime

def crear_pestana_servicios_admin(parent):
    frame = ui.crear_frame(parent)

    lbl_titulo = ui.crear_label(frame, "Llamadas de Servicio", font_t=ui.FUENTE_TITULO)
    lbl_titulo.pack(pady=10)

    tree = ttk.Treeview(frame, columns=("ID", "Dispositivo", "Cliente", "Fecha", "Estado", "Técnico", "Cierre", "Comentarios"), show="headings")
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")
    tree.pack(padx=10, pady=10, fill="both", expand=True)

    def refrescar():
        tree.delete(*tree.get_children())
        for s in manejo_servicios.cargar_servicios():
            tree.insert("", "end", values=(s["id_servicio"], s["id_dispositivo"], s["usuario_cliente"],
                                           s["fecha_creacion"], s["estado"], s["tecnico_asignado"],
                                           s["fecha_cierre"], s["comentarios"]))

    frm = ui.crear_frame(frame)
    frm.pack(fill="x", padx=10, pady=10)
    frm.columnconfigure(1, weight=1)

    lbl_id = ui.crear_label(frm, "ID:")
    lbl_id.grid(row=0, column=0, sticky="e")
    entry_id = tk.Entry(frm)
    entry_id.grid(row=0, column=1, sticky="ew")

    lbl_estado = ui.crear_label(frm, "Estado:")
    lbl_estado.grid(row=1, column=0, sticky="e")
    combo_estado = ttk.Combobox(frm, values=["pendiente", "en proceso", "completado"], state="readonly")
    combo_estado.grid(row=1, column=1, sticky="ew")

    lbl_tecnico = ui.crear_label(frm, "Técnico:")
    lbl_tecnico.grid(row=2, column=0, sticky="e")
    entry_tecnico = tk.Entry(frm)
    entry_tecnico.grid(row=2, column=1, sticky="ew")

    lbl_coment = ui.crear_label(frm, "Comentarios:")
    lbl_coment.grid(row=3, column=0, sticky="ne")
    entry_coment = tk.Text(frm, height=3)
    entry_coment.grid(row=3, column=1, sticky="ew")

    def actualizar_servicio():
        id_serv = entry_id.get().strip()
        estado = combo_estado.get().strip()
        tecnico = entry_tecnico.get().strip()
        comentarios = entry_coment.get("1.0", "end").strip()
        fecha_cierre = datetime.now().strftime("%Y-%m-%d %H:%M:%S") if estado == "completado" else ""

        if not id_serv:
            messagebox.showerror("Error", "Debe ingresar el ID del servicio.")
            return

        ok = manejo_servicios.editar_servicio(id_serv, estado=estado, tecnico_asignado=tecnico,
                                             fecha_cierre=fecha_cierre, comentarios=comentarios)
        if ok:
            messagebox.showinfo("Actualizado", "Servicio actualizado correctamente.")
            refrescar()

    btn_actualizar = ui.crear_boton(frm, "Actualizar", actualizar_servicio)
    btn_actualizar.grid(row=4, column=0, columnspan=2, pady=10, sticky="ew")

    refrescar()
    return frame
