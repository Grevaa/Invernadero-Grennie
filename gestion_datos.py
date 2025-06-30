import tkinter as tk
from tkinter import ttk, messagebox
from manejo_csv import leer_csv_dict
from gestion_parametros import mostrar_formulario_parametros, cargar_parametros
from datetime import datetime
import ui_estilos as ui
import estado_actuadores

RUTA_HISTORIAL = "datos/historial.csv"
RUTA_DISPOSITIVOS = "datos/dispositivos.csv"

def crear_frame_estado(parent, usuario):
    frame = tk.Frame(parent, bg=ui.COLOR_FONDO)

    lbl_titulo = ui.crear_label(frame, "Estado del Invernadero", font_t=ui.FUENTE_TITULO)
    lbl_titulo.pack(pady=20)

    frm_datos = ui.crear_frame(frame, bd=2, relief="ridge")
    frm_datos.pack(padx=20, pady=10, fill="both", expand=True)

    lbl_fecha = ui.crear_label(frm_datos, "", font_t=ui.FUENTE_NORMAL)
    lbl_fecha.pack(pady=10)

    lbl_humedad = ui.crear_label(frm_datos, "", font_t=ui.FUENTE_VALOR, fg=ui.COLOR_HUMEDAD)
    lbl_humedad.pack(pady=10)

    lbl_temp = ui.crear_label(frm_datos, "", font_t=ui.FUENTE_VALOR, fg=ui.COLOR_TEMPERATURA)
    lbl_temp.pack(pady=10)

    lbl_ph = ui.crear_label(frm_datos, "", font_t=ui.FUENTE_VALOR, fg=ui.COLOR_PH)
    lbl_ph.pack(pady=10)

    lbl_estado = ui.crear_label(frame, "", font_t=ui.FUENTE_ESTADO, fg=ui.COLOR_ESTADO)
    lbl_estado.pack(pady=10)

    dispositivos = [d for d in leer_csv_dict(RUTA_DISPOSITIVOS) if d.get("usuario") == usuario]

    if not dispositivos:
        messagebox.showerror("Error", "No hay dispositivos asociados a este usuario.")
        return frame

    combo_disp = ttk.Combobox(frame, state="readonly", values=[d["id_dispositivo"] for d in dispositivos])
    combo_disp.current(0)
    combo_disp.pack(pady=5)

    frm_botones = ui.crear_frame(frame)
    frm_botones.pack(padx=20, pady=10, fill="x")

    btn_param = ui.crear_boton(frm_botones, "Configurar Parámetros",
                                command=lambda: mostrar_formulario_parametros(usuario, combo_disp.get()))
    btn_param.pack(fill="x")

    def actualizar_datos():
        id_disp = combo_disp.get()
        if not id_disp:
            return

        historial = leer_csv_dict(RUTA_HISTORIAL)
        if historial:
            ultima = historial[-1]
            fecha = ultima["FechaHora"]
            humedad = float(ultima["Humedad"])
            temperatura = float(ultima["Temperatura"])
            ph = float(ultima["pH"])

            lbl_fecha.config(text=f"Última lectura: {fecha}")
            lbl_humedad.config(text=f"Humedad: {humedad} %")
            lbl_temp.config(text=f"Temperatura: {temperatura} °C")
            lbl_ph.config(text=f"pH: {ph}")

            parametros_list = cargar_parametros(usuario, id_disp)
            parametros = {p["parametro"]: p["valor"] for p in parametros_list}

            estados = []

            # Estado basado en parámetros y lectura
            if humedad < float(parametros.get("humedad_min", 40)):
                estados.append("💧 Riego ACTIVADO")
            elif humedad > float(parametros.get("humedad_max", 70)):
                estados.append("💧 Riego DESACTIVADO")
            else:
                estados.append("💧 Humedad óptima")

            if temperatura > float(parametros.get("temp_max", 30)):
                estados.append("🌬️ Ventilación ACTIVADA")
            elif temperatura < float(parametros.get("temp_min", 22)):
                estados.append("🌬️ Ventilación DESACTIVADA")
            else:
                estados.append("🌬️ Temperatura óptima")

            ph_min = float(parametros.get("ph_min", 5.8))
            ph_max = float(parametros.get("ph_max", 7.0))
            if ph < ph_min or ph > ph_max:
                estados.append(f"⚠️ pH fuera de rango: {ph}")
            else:
                estados.append("🧪 pH óptimo")

            hora_actual = datetime.now().hour
            hora_luz_inicio = int(parametros.get("hora_luz_inicio", 18))
            hora_luz_fin = int(parametros.get("hora_luz_fin", 6))

            if hora_luz_inicio < hora_luz_fin:
                luz_activa = hora_luz_inicio <= hora_actual < hora_luz_fin
            else:
                luz_activa = hora_actual >= hora_luz_inicio or hora_actual < hora_luz_fin

            # Agregar estado de luz segun actuadores reales
            if estado_actuadores.estado_luz:
                estados.append("💡 Luz ACTIVADA")
            else:
                estados.append("💡 Luz DESACTIVADA")

            # Agregar estado de ventilacion segun actuadores reales
            if estado_actuadores.estado_ventilacion:
                estados.append("🌬️ Ventilación ACTIVADA (manual)")
            else:
                # Solo mostrar temperatura optima si no está activada manualmente
                if temperatura > float(parametros.get("temp_max", 30)) or temperatura < float(parametros.get("temp_min", 22)):
                    estados.append("🌬️ Ventilación AUTÓMATICA")
                else:
                    estados.append("🌬️ Temperatura óptima")

            # Agregar estado riego segun actuadores reales
            if estado_actuadores.estado_riego:
                estados.append("💧 Riego ACTIVADO (manual)")
            else:
                # Solo mostrar humedad optima si no está activado manualmente
                if humedad < float(parametros.get("humedad_min", 40)) or humedad > float(parametros.get("humedad_max", 70)):
                    estados.append("💧 Riego AUTÓMATICO")
                else:
                    estados.append("💧 Humedad óptima")

            # Estado techo (manual)
            if estado_actuadores.estado_techo:
                estados.append("🏠 Techo ABIERTO")
            else:
                estados.append("🏠 Techo CERRADO")

            lbl_estado.config(text="\n".join(estados))

        frame.after(10000, actualizar_datos)

    actualizar_datos()
    return frame





