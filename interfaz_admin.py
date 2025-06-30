import tkinter as tk
from tkinter import ttk, messagebox
import gestion_usuarios
import gestion_dispositivos
import gestion_servicio_admin
import ui_estilos as ui

def mostrar_panel_admin(usuario_admin):
    ventana = tk.Tk()
    ui.aplicar_estilo_ventana(ventana, f"Panel de Administración - {usuario_admin}", "1000x600")

    notebook = ttk.Notebook(ventana)
    notebook.pack(fill="both", expand=True)

    # --- Pestaña Usuarios ---
    tab_usuarios = ui.crear_frame(notebook)
    notebook.add(tab_usuarios, text="Gestión de Usuarios")

    tree_users = ttk.Treeview(tab_usuarios, columns=("Usuario", "Tipo"), show="headings")
    tree_users.heading("Usuario", text="Usuario")
    tree_users.heading("Tipo", text="Tipo")
    tree_users.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=20, pady=10)
    tab_usuarios.rowconfigure(0, weight=1)
    tab_usuarios.columnconfigure(0, weight=1)

    def refrescar_usuarios():
        tree_users.delete(*tree_users.get_children())
        for u in gestion_usuarios.cargar_usuarios():
            tree_users.insert("", "end", values=(u["usuario"], u["tipo"]))

    frm = ui.crear_frame(tab_usuarios)
    frm.grid(row=1, column=0, sticky="ew", pady=15, padx=20)
    frm.columnconfigure(1, weight=1)

    ui.crear_label(frm, "Usuario:", font_t=ui.FUENTE_NORMAL).grid(row=0, column=0, padx=5, sticky="e")
    entrada_usuario = tk.Entry(frm, font=ui.FUENTE_NORMAL)
    entrada_usuario.grid(row=0, column=1, sticky="ew")

    ui.crear_label(frm, "Contraseña:", font_t=ui.FUENTE_NORMAL).grid(row=1, column=0, padx=5, sticky="e")
    entrada_clave = tk.Entry(frm, show="*", font=ui.FUENTE_NORMAL)
    entrada_clave.grid(row=1, column=1, sticky="ew")

    ui.crear_label(frm, "Tipo:", font_t=ui.FUENTE_NORMAL).grid(row=2, column=0, padx=5, sticky="e")
    combo_tipo = ttk.Combobox(frm, values=["admin", "cliente"], state="readonly", font=ui.FUENTE_NORMAL)
    combo_tipo.grid(row=2, column=1, sticky="ew")

    def agregar_usuario():
        if gestion_usuarios.agregar_usuario(entrada_usuario.get(), entrada_clave.get(), combo_tipo.get()):
            refrescar_usuarios()

    def editar_usuario():
        if gestion_usuarios.editar_usuario(entrada_usuario.get(), entrada_clave.get(), combo_tipo.get()):
            refrescar_usuarios()

    def eliminar_usuario():
        seleccionado = tree_users.selection()
        if seleccionado:
            usuario = tree_users.item(seleccionado, "values")[0]
            if gestion_usuarios.eliminar_usuario(usuario):
                refrescar_usuarios()

    ui.crear_boton(frm, "Agregar", agregar_usuario).grid(row=3, column=0, pady=10, sticky="ew")
    ui.crear_boton(frm, "Editar", editar_usuario).grid(row=3, column=1, pady=10, sticky="ew")
    ui.crear_boton(frm, "Eliminar", eliminar_usuario).grid(row=3, column=2, pady=10, sticky="ew")

    refrescar_usuarios()

    # --- Pestaña Dispositivos ---
    tab_dispositivos = ui.crear_frame(notebook)
    notebook.add(tab_dispositivos, text="Gestión de Dispositivos")

    tree_disp = ttk.Treeview(tab_dispositivos, columns=("ID", "Usuario", "Ubicacion", "Estado", "Fecha"), show="headings")
    for col in ("ID", "Usuario", "Ubicacion", "Estado", "Fecha"):
        tree_disp.heading(col, text=col)
    tree_disp.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=20, pady=10)
    tab_dispositivos.rowconfigure(0, weight=1)
    tab_dispositivos.columnconfigure(0, weight=1)

    def refrescar_dispositivos():
        tree_disp.delete(*tree_disp.get_children())
        for d in gestion_dispositivos.cargar_dispositivos():
            tree_disp.insert("", "end", values=(d["id_dispositivo"], d["usuario"], d["ubicacion"], d["estado"], d["fecha_registro"]))

    frm_disp = ui.crear_frame(tab_dispositivos)
    frm_disp.grid(row=1, column=0, sticky="ew", pady=15, padx=20)
    frm_disp.columnconfigure(1, weight=1)

    ui.crear_label(frm_disp, "ID:", font_t=ui.FUENTE_NORMAL).grid(row=0, column=0, padx=5, sticky="e")
    entrada_id = tk.Entry(frm_disp, font=ui.FUENTE_NORMAL)
    entrada_id.grid(row=0, column=1, sticky="ew")

    ui.crear_label(frm_disp, "Usuario:", font_t=ui.FUENTE_NORMAL).grid(row=1, column=0, padx=5, sticky="e")
    combo_usuario = ttk.Combobox(frm_disp, values=gestion_usuarios.cargar_usuarios_cliente(), state="readonly", font=ui.FUENTE_NORMAL)
    combo_usuario.grid(row=1, column=1, sticky="ew")

    ui.crear_label(frm_disp, "Ubicacion:", font_t=ui.FUENTE_NORMAL).grid(row=2, column=0, padx=5, sticky="e")
    entrada_ubicacion = tk.Entry(frm_disp, font=ui.FUENTE_NORMAL)
    entrada_ubicacion.grid(row=2, column=1, sticky="ew")

    ui.crear_label(frm_disp, "Estado:", font_t=ui.FUENTE_NORMAL).grid(row=3, column=0, padx=5, sticky="e")
    combo_estado = ttk.Combobox(frm_disp, values=["activo", "mantenimiento", "inactivo"], state="readonly", font=ui.FUENTE_NORMAL)
    combo_estado.set("activo")
    combo_estado.grid(row=3, column=1, sticky="ew")

    def agregar_disp():
        if gestion_dispositivos.agregar_dispositivo(entrada_id.get(), combo_usuario.get(), entrada_ubicacion.get(), combo_estado.get()):
            refrescar_dispositivos()

    def editar_disp():
        if gestion_dispositivos.editar_dispositivo(entrada_id.get(), combo_usuario.get(), entrada_ubicacion.get(), combo_estado.get()):
            refrescar_dispositivos()

    def eliminar_disp():
        seleccionado = tree_disp.selection()
        if seleccionado:
            id_disp = tree_disp.item(seleccionado, "values")[0]
            if gestion_dispositivos.eliminar_dispositivo(id_disp):
                refrescar_dispositivos()

    ui.crear_boton(frm_disp, "Agregar", agregar_disp).grid(row=4, column=0, pady=10, sticky="ew")
    ui.crear_boton(frm_disp, "Editar", editar_disp).grid(row=4, column=1, pady=10, sticky="ew")
    ui.crear_boton(frm_disp, "Eliminar", eliminar_disp).grid(row=4, column=2, pady=10, sticky="ew")

    refrescar_dispositivos()

    # --- Pestaña Servicios ---
    tab_servicios = gestion_servicio_admin.crear_pestana_servicios_admin(notebook)
    notebook.add(tab_servicios, text="Gestión de Servicios")

    ventana.mainloop()











