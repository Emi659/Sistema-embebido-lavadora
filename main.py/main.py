import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time

class LavadoraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Lavadora")
        self.root.geometry("400x350")
        self.root.configure(bg="#e6f2ff")
        self.encendida = False
        self.lavando = False

        # Variables
        self.temp_var = tk.StringVar(value="Automática")
        self.nivel_var = tk.StringVar(value="Automático")
        self.estado_var = tk.StringVar(value="Lavadora apagada")

        # Crear UI
        self.crear_widgets()

    def crear_widgets(self):
        # Título
        titulo = tk.Label(self.root, text="Lavadora Automática", font=("Arial", 18, "bold"), bg="#e6f2ff")
        titulo.pack(pady=15)

        # Botón Prender / Apagar
        self.btn_power = tk.Button(self.root, text="Encender Lavadora", font=("Arial", 14), width=20,
                                   command=self.toggle_power)
        self.btn_power.pack(pady=10)

        # Frame para controles
        frame_controles = tk.LabelFrame(self.root, text="Configuración", font=("Arial", 12), bg="#cce6ff")
        frame_controles.pack(padx=20, pady=15, fill="x")

        # Temperatura
        tk.Label(frame_controles, text="Temperatura:", font=("Arial", 12), bg="#cce6ff").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        opciones_temp = ["Automática", "Caliente", "Fría"]
        self.combo_temp = ttk.Combobox(frame_controles, values=opciones_temp, state="readonly", textvariable=self.temp_var)
        self.combo_temp.grid(row=0, column=1, pady=5, padx=5)

        # Nivel de agua
        tk.Label(frame_controles, text="Nivel de agua:", font=("Arial", 12), bg="#cce6ff").grid(row=1, column=0, sticky="w", pady=5, padx=5)
        opciones_nivel = ["Automático", "Máximo", "Mínimo"]
        self.combo_nivel = ttk.Combobox(frame_controles, values=opciones_nivel, state="readonly", textvariable=self.nivel_var)
        self.combo_nivel.grid(row=1, column=1, pady=5, padx=5)

        # Botón iniciar lavado
        self.btn_iniciar = tk.Button(self.root, text="Iniciar Lavado", font=("Arial", 14), width=20,
                                    state="disabled", command=self.iniciar_lavado)
        self.btn_iniciar.pack(pady=15)

        # Label estado
        self.lbl_estado = tk.Label(self.root, textvariable=self.estado_var, font=("Arial", 12), bg="#e6f2ff")
        self.lbl_estado.pack(pady=10)

        # Barra de progreso
        self.progress = ttk.Progressbar(self.root, mode="determinate", length=300)
        self.progress.pack(pady=10)

    def toggle_power(self):
        if self.encendida:
            if self.lavando:
                messagebox.showwarning("Advertencia", "No puedes apagar mientras el ciclo está en progreso.")
                return
            self.encendida = False
            self.estado_var.set("Lavadora apagada")
            self.btn_power.config(text="Encender Lavadora")
            self.btn_iniciar.config(state="disabled")
            self.progress["value"] = 0
        else:
            self.encendida = True
            self.estado_var.set("Lavadora encendida")
            self.btn_power.config(text="Apagar Lavadora")
            self.btn_iniciar.config(state="normal")

    def iniciar_lavado(self):
        if not self.encendida:
            messagebox.showwarning("Advertencia", "Primero enciende la lavadora.")
            return
        if self.lavando:
            messagebox.showwarning("Advertencia", "Lavado en progreso.")
            return

        self.lavando = True
        self.btn_iniciar.config(state="disabled")
        self.estado_var.set(f"Lavando - Temp: {self.temp_var.get()}, Nivel: {self.nivel_var.get()}")
        self.progress["value"] = 0
        self.progress["maximum"] = 100

        # Ejecutar lavado en otro hilo para no congelar GUI
        threading.Thread(target=self.simular_lavado).start()

    def simular_lavado(self):
        duracion_segundos = 10  # Duración total simulada

        for i in range(duracion_segundos):
            time.sleep(1)
            progreso = ((i + 1) / duracion_segundos) * 100
            self.progress["value"] = progreso

        self.lavando = False
        self.estado_var.set("Lavado terminado. Lavadora encendida.")
        self.btn_iniciar.config(state="normal")
        messagebox.showinfo("Lavadora", "Ciclo de lavado terminado.")

if __name__ == "__main__":
    root = tk.Tk()
    app = LavadoraApp(root)
    root.mainloop()
