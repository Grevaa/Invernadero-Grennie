import tkinter as tk
from tkinter import messagebox
from manejo_csv import leer_csv_dict, escribir_csv_dict

RUTA_PARAMETROS = "datos/parametros.csv"
CAMPOS = ["usuario", "id_dispositivo", "parametro", "valor"]

# Parámetros por defecto para nuevos registros
PARAMETROS_POR_DEFECTO = {
    "humedad_min": "40",
    "humedad_max": "70",
    "temp_min": "22",
    "temp_max": "30",
    "ph_min": "5.8",
    "ph_max": "7.0",
    "hora_luz_inicio": "18",
    "hora_luz_fin": "6"
}

def cargar_parametros(usuario, id_disp):
    """Carga la lista de parámetros para el usuario y dispositivo especificados."""
    todos = leer_csv_dict(RUTA_PARAMETROS)
    # Filtrar solo los que coincidan usuario+dispositivo
    filtrados = [p for p in todos if p.get("usuario") == usuario and p.get("id_dispositivo") == id_disp]
    # Si no hay, crear con valores por defecto
    if not filtrados:
        filtrados = []
        for param, val in PARAMETROS_POR_DEFECTO.items():
            filtrados.append({"usuario": usuario, "id_dispositivo": id_disp, "parametro": param, "valor": val})
        # Guardar estos parámetros nuevos
        guardar_parametros(filtrados)
    return filtrados

def guardar_parametros(lista_parametros):
    """Guarda la lista completa de parámetros (para todos los usuarios y dispositivos)."""
    # Leer todos parámetros
    todos = leer_csv_dict(RUTA_PARAMETROS)
    # Para cada nuevo parámetro, eliminar el existente igual y agregar el nuevo
    for p in lista_parametros:
        todos = [x for x in todos if not (x.get("usuario") == p.get("usuario") and
                                          x.get("id_dispositivo") == p.get("id_dispositivo") and
                                          x.get("parametro") == p.get("parametro"))]
        todos.append(p)
    escribir_csv_dict(RUTA_PARAMETROS, CAMPOS, todos)

def mostrar_formulario_parametros(usuario, id_disp):
    """Muestra la ventana para que el usuario edite parámetros de su dispositivo."""
    parametros = cargar_parametros(usuario, id_disp)

    ventana = tk.Toplevel()
    ventana.title(f"Parámetros - Usuario: {usuario} - Dispositivo: {id_disp}")
    ventana.geometry("400x350")
    ventana.configure(bg="#34495e")

    campos_vars = {}

    tk.Label(ventana, text="Parámetros de Control", font=("Arial", 16, "bold"), bg="#34495e", fg="white").pack(pady=10)

    frm = tk.Frame(ventana, bg="#34495e")
    frm.pack(padx=20, pady=10, fill="both", expand=True)

    for idx, param in enumerate(parametros):
        tk.Label(frm, text=param["parametro"], font=("Arial", 12), bg="#34495e", fg="white").grid(row=idx, column=0, sticky="w", pady=5)
        var = tk.StringVar(value=param["valor"])
        entry = tk.Entry(frm, textvariable=var, font=("Arial", 12))
        entry.grid(row=idx, column=1, pady=5, sticky="ew")
        campos_vars[param["parametro"]] = var

    frm.columnconfigure(1, weight=1)

    def guardar():
        nuevos_parametros = []
        for param, var in campos_vars.items():
            valor = var.get().strip()
            if not valor:
                messagebox.showerror("Error", f"El valor para '{param}' no puede estar vacío.")
                return
            # Puedes agregar validaciones numéricas aquí si quieres
            nuevos_parametros.append({
                "usuario": usuario,
                "id_dispositivo": id_disp,
                "parametro": param,
                "valor": valor
            })
        guardar_parametros(nuevos_parametros)
        messagebox.showinfo("Guardado", "Parámetros guardados correctamente.")
        ventana.destroy()

    btn_guardar = tk.Button(ventana, text="Guardar", command=guardar, bg="#27ae60", fg="white", font=("Arial", 12, "bold"))
    btn_guardar.pack(pady=15, fill="x", padx=20)

    ventana.transient()
    ventana.grab_set()
    ventana.focus_force()
    ventana.wait_window()


