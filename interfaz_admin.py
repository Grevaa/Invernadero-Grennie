import tkinter as tk
from tkinter import ttk, messagebox
import csv
import hashlib
from datetime import datetime

RUTA_USUARIOS = "datos/usuarios.csv"
RUTA_DISPOSITIVOS = "datos/dispositivos.csv"

def encriptar_md5(texto):
    return hashlib.md5(texto.encode()).hexdigest()

# Leer usuarios
def cargar_usuarios(tree):
    tree.delete(*tree.get_children())  # Limpia la tabla
    with open(RUTA_USUARIOS, newline="") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            tree.insert("", "end", values=(fila["usuario"], fila["tipo"]))

# Cargar usuarios tipo cliente para el combo de dispositivos
def cargar_usuarios_cliente():
    usuarios = []
    with open(RUTA_USUARIOS, newline="") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            if fila["tipo"] == "cliente":
                usuarios.append(fila["usuario"])
    return usuarios

# Agregar nuevo usuario
def agregar_usuario(entry_usuario, entry_clave, combo_tipo, tree):
    usuario = entry_usuario.get().strip()
    clave = entry_clave.get().strip()
    tipo = combo_tipo.get().strip()

    if not usuario or not clave or not tipo:
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return

    clave_md5 = encriptar_md5(clave)

    with open(RUTA_USUARIOS, "a", newline="") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow([usuario, clave_md5, tipo])

    messagebox.showinfo("Éxito", f"Usuario '{usuario}' agregado correctamente.")
    cargar_usuarios(tree)

# --- Gestión de dispositivos ---

def cargar_dispositivos(tree_disp):
    tree_disp.delete(*tree_disp.get_children())
    try:
        with open(RUTA_DISPOSITIVOS, newline="") as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                tree_disp.insert("", "end", values=(
                    fila["id_dispositivo"],
                    fila["usuario"],
                    fila["ubicacion"],
                    fila["estado"],
                    fila["fecha_registro"]
                ))
    except FileNotFoundError:
        pass

def mostrar_panel_admin(usuario):
    ventana = tk.Tk()
    ventana.title(f"Panel de Administración - {usuario}")
    ventana.geometry("900x600")

    notebook = ttk.Notebook(ventana)
    tab_usuarios = ttk.Frame(notebook)
    notebook.add(tab_usuarios, text="Gestión de Usuarios")

    tab_dispositivos = ttk.Frame(notebook)
    notebook.add(tab_dispositivos, text="Gestión de Dispositivos")

    notebook.pack(expand=True, fill="both")

    # --- Gestión de Usuarios ---

    # Tabla usuarios
    tree = ttk.Treeview(tab_usuarios, columns=("Usuario", "Tipo"), show="headings", selectmode="browse")
    tree.heading("Usuario", text="Usuario")
    tree.heading("Tipo", text="Tipo")
    tree.pack(pady=10, fill="both", expand=True)
    cargar_usuarios(tree)

    # Formulario usuarios
    frm = ttk.Frame(tab_usuarios)
    frm.pack(pady=10)

    ttk.Label(frm, text="Usuario:").grid(row=0, column=0, padx=5, sticky="e")
    entrada_usuario = ttk.Entry(frm)
    entrada_usuario.grid(row=0, column=1)

    ttk.Label(frm, text="Contraseña:").grid(row=1, column=0, padx=5, sticky="e")
    entrada_clave = ttk.Entry(frm, show="*")
    entrada_clave.grid(row=1, column=1)

    ttk.Label(frm, text="Tipo:").grid(row=2, column=0, padx=5, sticky="e")
    combo_tipo = ttk.Combobox(frm, values=["admin", "cliente"], state="readonly")
    combo_tipo.grid(row=2, column=1)

    def cargar_usuario_en_formulario(event):
        seleccionado = tree.selection()
        if seleccionado:
            valores = tree.item(seleccionado, "values")
            entrada_usuario.delete(0, tk.END)
            entrada_usuario.insert(0, valores[0])
            combo_tipo.set(valores[1])
            entrada_clave.delete(0, tk.END)

    tree.bind("<<TreeviewSelect>>", cargar_usuario_en_formulario)

    def agregar_usuario_btn():
        agregar_usuario(entrada_usuario, entrada_clave, combo_tipo, tree)

    def editar_usuario():
        usuario = entrada_usuario.get().strip()
        nueva_clave = entrada_clave.get().strip()
        nuevo_tipo = combo_tipo.get().strip()

        if not usuario or not nuevo_tipo:
            messagebox.showerror("Error", "Selecciona un usuario y completa los campos.")
            return

        usuarios_actualizados = []
        encontrado = False
        with open(RUTA_USUARIOS, newline="") as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                if fila["usuario"] == usuario:
                    encontrado = True
                    fila["tipo"] = nuevo_tipo
                    if nueva_clave:
                        fila["clave"] = encriptar_md5(nueva_clave)
                usuarios_actualizados.append(fila)

        if not encontrado:
            messagebox.showerror("Error", "Usuario no encontrado.")
            return

        with open(RUTA_USUARIOS, "w", newline="") as archivo:
            campos = ["usuario", "clave", "tipo"]
            escritor = csv.DictWriter(archivo, fieldnames=campos)
            escritor.writeheader()
            escritor.writerows(usuarios_actualizados)

        messagebox.showinfo("Éxito", f"Usuario '{usuario}' editado correctamente.")
        cargar_usuarios(tree)

    def eliminar_usuario():
        seleccionado = tree.selection()
        if not seleccionado:
            messagebox.showerror("Error", "Selecciona un usuario para eliminar.")
            return

        valores = tree.item(seleccionado, "values")
        usuario_a_eliminar = valores[0]
        tipo_usuario = valores[1]

        if tipo_usuario == "admin":
            messagebox.showwarning("Advertencia", "No se permite eliminar usuarios administradores.")
            return

        if messagebox.askyesno("Confirmar", f"¿Eliminar usuario '{usuario_a_eliminar}'?"):
            usuarios_restantes = []
            with open(RUTA_USUARIOS, newline="") as archivo:
                lector = csv.DictReader(archivo)
                for fila in lector:
                    if fila["usuario"] != usuario_a_eliminar:
                        usuarios_restantes.append(fila)

            with open(RUTA_USUARIOS, "w", newline="") as archivo:
                campos = ["usuario", "clave", "tipo"]
                escritor = csv.DictWriter(archivo, fieldnames=campos)
                escritor.writeheader()
                escritor.writerows(usuarios_restantes)

            messagebox.showinfo("Éxito", f"Usuario '{usuario_a_eliminar}' eliminado.")
            cargar_usuarios(tree)
            entrada_usuario.delete(0, tk.END)
            entrada_clave.delete(0, tk.END)
            combo_tipo.set("")

    ttk.Button(frm, text="Agregar", command=agregar_usuario_btn).grid(row=3, column=0, pady=10)
    ttk.Button(frm, text="Editar", command=editar_usuario).grid(row=3, column=1, pady=10)
    ttk.Button(frm, text="Eliminar", command=eliminar_usuario).grid(row=3, column=2, padx=10)

    # --- Gestión de Dispositivos ---

    # Tabla dispositivos
    tree_disp = ttk.Treeview(tab_dispositivos,
                             columns=("ID", "Usuario", "Ubicación", "Estado", "Fecha Registro"),
                             show="headings", selectmode="browse"
                             )
    for col, ancho in zip(tree_disp["columns"], [80, 100, 150, 100, 100]):
        tree_disp.heading(col, text=col)
        tree_disp.column(col, width=ancho, anchor="center")
    tree_disp.pack(pady=10, fill="both", expand=True)
    cargar_dispositivos(tree_disp)

    # Formulario dispositivos
    frm_disp = ttk.Frame(tab_dispositivos)
    frm_disp.pack(pady=10, padx=10, fill="x")

    ttk.Label(frm_disp, text="ID Dispositivo:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entrada_id_disp = ttk.Entry(frm_disp)
    entrada_id_disp.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frm_disp, text="Usuario asociado:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    combo_usuario_disp = ttk.Combobox(frm_disp, state="readonly")
    combo_usuario_disp['values'] = cargar_usuarios_cliente()
    combo_usuario_disp.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(frm_disp, text="Ubicación:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    entrada_ubicacion_disp = ttk.Entry(frm_disp)
    entrada_ubicacion_disp.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(frm_disp, text="Estado:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
    combo_estado_disp = ttk.Combobox(frm_disp, values=["activo", "mantenimiento", "inactivo"], state="readonly")
    combo_estado_disp.grid(row=3, column=1, padx=5, pady=5)
    combo_estado_disp.set("activo")

    def limpiar_formulario_dispositivo():
        entrada_id_disp.delete(0, tk.END)
        combo_usuario_disp.set("")
        entrada_ubicacion_disp.delete(0, tk.END)
        combo_estado_disp.set("activo")

    def agregar_dispositivo():
        id_disp = entrada_id_disp.get().strip()
        usuario_asoc = combo_usuario_disp.get().strip()
        ubicacion = entrada_ubicacion_disp.get().strip()
        estado = combo_estado_disp.get().strip()

        if not id_disp or not usuario_asoc or not ubicacion or not estado:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        dispositivos = []
        try:
            with open(RUTA_DISPOSITIVOS, newline="") as archivo:
                lector = csv.DictReader(archivo)
                for fila in lector:
                    dispositivos.append(fila)
        except FileNotFoundError:
            pass

        # Validar que el id no esté repetido
        for d in dispositivos:
            if d["id_dispositivo"] == id_disp:
                messagebox.showerror("Error", f"El ID '{id_disp}' ya existe.")
                return
            if d["usuario"] == usuario_asoc:
                messagebox.showerror("Error", f"El usuario '{usuario_asoc}' ya tiene un dispositivo asociado.")
                return

        fecha_registro = datetime.now().strftime("%Y-%m-%d")

        nuevo_disp = {
            "id_dispositivo": id_disp,
            "usuario": usuario_asoc,
            "ubicacion": ubicacion,
            "estado": estado,
            "fecha_registro": fecha_registro
        }
        dispositivos.append(nuevo_disp)

        with open(RUTA_DISPOSITIVOS, "w", newline="") as archivo:
            campos = ["id_dispositivo", "usuario", "ubicacion", "estado", "fecha_registro"]
            escritor = csv.DictWriter(archivo, fieldnames=campos)
            escritor.writeheader()
            escritor.writerows(dispositivos)

        messagebox.showinfo("Éxito", f"Dispositivo '{id_disp}' agregado correctamente.")
        cargar_dispositivos(tree_disp)
        limpiar_formulario_dispositivo()

    def cargar_dispositivo_en_formulario(event):
        seleccionado = tree_disp.selection()
        if seleccionado:
            valores = tree_disp.item(seleccionado, "values")
            entrada_id_disp.delete(0, tk.END)
            entrada_id_disp.insert(0, valores[0])
            combo_usuario_disp.set(valores[1])
            entrada_ubicacion_disp.delete(0, tk.END)
            entrada_ubicacion_disp.insert(0, valores[2])
            combo_estado_disp.set(valores[3])

    tree_disp.bind("<<TreeviewSelect>>", cargar_dispositivo_en_formulario)

    def editar_dispositivo():
        id_disp = entrada_id_disp.get().strip()
        usuario_asoc = combo_usuario_disp.get().strip()
        ubicacion = entrada_ubicacion_disp.get().strip()
        estado = combo_estado_disp.get().strip()

        if not id_disp or not usuario_asoc or not ubicacion or not estado:
            messagebox.showerror("Error", "Todos los campos son obligatorios para editar.")
            return

        dispositivos = []
        encontrado = False
        try:
            with open(RUTA_DISPOSITIVOS, newline="") as archivo:
                lector = csv.DictReader(archivo)
                for fila in lector:
                    if fila["id_dispositivo"] == id_disp:
                        encontrado = True
                        # Validar que no haya otro dispositivo con mismo usuario, excepto este mismo id_disp
                        for d in dispositivos:
                            if d["usuario"] == usuario_asoc and d["id_dispositivo"] != id_disp:
                                messagebox.showerror("Error",
                                                     f"El usuario '{usuario_asoc}' ya tiene otro dispositivo asociado.")
                                return
                        # Actualizamos el registro
                        fila["usuario"] = usuario_asoc
                        fila["ubicacion"] = ubicacion
                        # No cambiamos fecha_registro
                        fila["estado"] = estado
                    dispositivos.append(fila)
        except FileNotFoundError:
            messagebox.showerror("Error", "Archivo de dispositivos no encontrado.")
            return

        if not encontrado:
            messagebox.showerror("Error", f"No se encontró el dispositivo con ID '{id_disp}'.")
            return

        # Validar unicidad usuario en la lista actualizada
        usuarios_asociados = {}
        for d in dispositivos:
            if d["usuario"] in usuarios_asociados and d["id_dispositivo"] != id_disp:
                messagebox.showerror("Error", f"El usuario '{d['usuario']}' está asociado a más de un dispositivo.")
                return
            usuarios_asociados[d["usuario"]] = d["id_dispositivo"]

        with open(RUTA_DISPOSITIVOS, "w", newline="") as archivo:
            campos = ["id_dispositivo", "usuario", "ubicacion", "estado", "fecha_registro"]
            escritor = csv.DictWriter(archivo, fieldnames=campos)
            escritor.writeheader()
            escritor.writerows(dispositivos)

        messagebox.showinfo("Éxito", f"Dispositivo con ID '{id_disp}' editado correctamente.")
        cargar_dispositivos(tree_disp)
        limpiar_formulario_dispositivo()

    def eliminar_dispositivo():
        seleccionado = tree_disp.selection()
        if not seleccionado:
            messagebox.showerror("Error", "Selecciona un dispositivo para eliminar.")
            return

        valores = tree_disp.item(seleccionado, "values")
        id_disp = valores[0]

        if messagebox.askyesno("Confirmar", f"¿Eliminar dispositivo con ID '{id_disp}'?"):
            dispositivos_restantes = []
            try:
                with open(RUTA_DISPOSITIVOS, newline="") as archivo:
                    lector = csv.DictReader(archivo)
                    for fila in lector:
                        if fila["id_dispositivo"] != id_disp:
                            dispositivos_restantes.append(fila)
            except FileNotFoundError:
                messagebox.showerror("Error", "Archivo de dispositivos no encontrado.")
                return

            with open(RUTA_DISPOSITIVOS, "w", newline="") as archivo:
                campos = ["id_dispositivo", "usuario", "ubicacion", "estado", "fecha_registro"]
                escritor = csv.DictWriter(archivo, fieldnames=campos)
                escritor.writeheader()
                escritor.writerows(dispositivos_restantes)

            messagebox.showinfo("Éxito", f"Dispositivo con ID '{id_disp}' eliminado.")
            cargar_dispositivos(tree_disp)
            limpiar_formulario_dispositivo()

    btn_agregar_disp = ttk.Button(frm_disp, text="Agregar", command=agregar_dispositivo)
    btn_agregar_disp.grid(row=4, column=0, pady=10)

    btn_editar_disp = ttk.Button(frm_disp, text="Editar", command=editar_dispositivo)
    btn_editar_disp.grid(row=4, column=1, pady=10)

    btn_eliminar_disp = ttk.Button(frm_disp, text="Eliminar", command=eliminar_dispositivo)
    btn_eliminar_disp.grid(row=4, column=2, pady=10)

    ventana.mainloop()




