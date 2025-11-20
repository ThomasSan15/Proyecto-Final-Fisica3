# tk_frontend.py
import tkinter as tk
from tkinter import filedialog, ttk, messagebox, simpledialog
import numpy as np
import main  
import io
import math
import pandas as pd
import matplotlib.pyplot as plt
# -----------------------------
# Clase principal
# -----------------------------
class Resoil:
    def __init__(self, root):
        self.root = root
        self.root.title("Resoil project")
        self.root.geometry("1100x700")

        self.img = None
        self.img2 = None
        self.result = None

        # Objetos físicos (inicialmente None)
        self.resorte = None
        self.amortiguador = None

        self._crear_menu()
        self._crear_panel_controles()
        self._crear_canvas()

    # ----------------------------
    # Secciones de UI
    # ----------------------------
    def _crear_menu(self):
        menubar = tk.Menu(self.root)
        archivo_menu = tk.Menu(menubar, tearoff=0)
        archivo_menu.add_command(label="Guardar resultado", command=self.guardar_resultado)
        archivo_menu.add_separator()
        archivo_menu.add_command(label="Salir", command=self.root.quit)
        menubar.add_cascade(label="Archivo", menu=archivo_menu)
        self.root.config(menu=menubar)

    def _crear_panel_controles(self):
        # Canvas para scroll
        panel_canvas = tk.Canvas(self.root, width=320)
        panel_canvas.pack(side=tk.LEFT, fill=tk.Y, expand=False)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=panel_canvas.yview)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        panel_canvas.configure(yscrollcommand=scrollbar.set)

        # Frame dentro del canvas
        frame = ttk.Frame(panel_canvas, padding=10)
        frame_id = panel_canvas.create_window((0,0), window=frame, anchor="nw")

        def on_frame_configure(event):
            panel_canvas.configure(scrollregion=panel_canvas.bbox("all"))
        frame.bind("<Configure>", on_frame_configure)

        # Habilitar scroll con la rueda del ratón
        def _on_mousewheel(event):
            panel_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        panel_canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # --- Controles para RESORTE ---
        ttk.Label(frame, text="=== RESORTE ===", font=("Arial", 10, "bold")).pack(pady=(5,8))
        
        ttk.Button(frame, text="Seleccionar resorte y aceite y graficar",
                   command=self.seleccionar_y_graficar).pack(fill=tk.X, pady=10)

        ttk.Label(frame, text="Nombre").pack()
        self.entry_r_nombre = ttk.Entry(frame, width=20)
        self.entry_r_nombre.insert(0, "Resorte A")
        self.entry_r_nombre.pack(pady=2)
        
        

        ttk.Label(frame, text="Constante elástica k (N/m)").pack()
        self.entry_r_k = ttk.Entry(frame, width=12)
        self.entry_r_k.insert(0, "200.0")
        self.entry_r_k.pack(pady=2)

        ttk.Label(frame, text="Longitud libre (m)").pack()
        self.entry_r_long = ttk.Entry(frame, width=12)
        self.entry_r_long.insert(0, "0.1")
        self.entry_r_long.pack(pady=2)

        ttk.Label(frame, text="Deformación máxima (m)").pack()
        self.entry_r_defmax = ttk.Entry(frame, width=12)
        self.entry_r_defmax.insert(0, "0.02")
        self.entry_r_defmax.pack(pady=2)

        ttk.Label(frame, text="Diámetro interno (m)").pack()
        self.entry_r_dmin = ttk.Entry(frame, width=12)
        self.entry_r_dmin.insert(0, "0.02")
        self.entry_r_dmin.pack(pady=2)

        ttk.Label(frame, text="Diámetro externo (m)").pack()
        self.entry_r_dmex = ttk.Entry(frame, width=12)
        self.entry_r_dmex.insert(0, "0.03")
        self.entry_r_dmex.pack(pady=2)

        # crear resorte
        ttk.Button(frame, text="Crear / actualizar resorte", command=self.crear_resorte).pack(fill=tk.X, pady=(6,4))

        # acciones sobre resorte
        ttk.Label(frame, text="Deflexión para fuerza (m)").pack()
        self.entry_r_deflex = ttk.Entry(frame, width=12)
        self.entry_r_deflex.insert(0, "0.01")
        self.entry_r_deflex.pack(pady=2)

        ttk.Button(frame, text="Calcular fuerza (F = k·x)", command=self.calcular_fuerza).pack(fill=tk.X, pady=2)

        ttk.Label(frame, text="Masa para frecuencia (kg)").pack()
        self.entry_r_masa = ttk.Entry(frame, width=12)
        self.entry_r_masa.insert(0, "1.0")
        self.entry_r_masa.pack(pady=2)

        ttk.Button(frame, text="Frecuencia natural (Hz)", command=self.calcular_frec_natural).pack(fill=tk.X, pady=2)
        ttk.Button(frame, text="Omega natural (rad/s)", command=self.calcular_omega_natural).pack(fill=tk.X, pady=2)

        # Label para mostrar resultados cortos
        self.label_resorte_result = ttk.Label(frame, text="", foreground="blue")
        self.label_resorte_result.pack(pady=(4,10))

        # --- Espacio separador ---
        ttk.Separator(frame, orient="horizontal").pack(fill=tk.X, pady=8)

        # --- Controles para AMORTIGUADOR ---
        ttk.Label(frame, text="=== AMORTIGUADOR ===", font=("Arial", 10, "bold")).pack(pady=(5,8))

        ttk.Label(frame, text="Nombre").pack()
        self.entry_a_nombre = ttk.Entry(frame, width=20)
        self.entry_a_nombre.insert(0, "Aceite 15W")
        self.entry_a_nombre.pack(pady=2)

        ttk.Label(frame, text="Densidad (g/cm³)").pack()
        self.entry_a_rho = ttk.Entry(frame, width=12)
        self.entry_a_rho.insert(0, "0.881")
        self.entry_a_rho.pack(pady=2)

        ttk.Label(frame, text="Visc. cinemática @40°C (cSt)").pack()
        self.entry_a_visc40 = ttk.Entry(frame, width=12)
        self.entry_a_visc40.insert(0, "72.6")
        self.entry_a_visc40.pack(pady=2)

        ttk.Label(frame, text="Visc. cinemática @100°C (cSt)").pack()
        self.entry_a_visc100 = ttk.Entry(frame, width=12)
        self.entry_a_visc100.insert(0, "11.6")
        self.entry_a_visc100.pack(pady=2)

        ttk.Button(frame, text="Crear / actualizar amortiguador", command=self.crear_amortiguador).pack(fill=tk.X, pady=(6,4))

        ttk.Label(frame, text="Temperatura para viscosidad (°C)").pack()
        self.entry_a_temp = ttk.Entry(frame, width=12)
        self.entry_a_temp.insert(0, "40")
        self.entry_a_temp.pack(pady=2)

        ttk.Button(frame, text="Viscosidad dinámica (Pa·s)", command=self.calcular_viscosidad).pack(fill=tk.X, pady=2)

        # c = factor * c_crit
        ttk.Label(frame, text="Masa para c (kg)").pack()
        self.entry_a_masa = ttk.Entry(frame, width=12)
        self.entry_a_masa.insert(0, "1.0")
        self.entry_a_masa.pack(pady=2)

        ttk.Label(frame, text="k para c (N/m)").pack()
        self.entry_a_k = ttk.Entry(frame, width=12)
        self.entry_a_k.insert(0, "200.0")
        self.entry_a_k.pack(pady=2)

        ttk.Label(frame, text="Factor para c (ej. 1.0 = crítico)").pack()
        self.entry_a_factor = ttk.Entry(frame, width=12)
        self.entry_a_factor.insert(0, "1.0")
        self.entry_a_factor.pack(pady=2)

        ttk.Button(frame, text="Coef. amortiguamiento c (N·s/m)", command=self.calcular_coef_amort).pack(fill=tk.X, pady=2)

        ttk.Label(frame, text="Valor de c (N·s/m) para ζ").pack()
        self.entry_a_c = ttk.Entry(frame, width=12)
        self.entry_a_c.insert(0, "10.0")
        self.entry_a_c.pack(pady=2)

        ttk.Button(frame, text="Relación amortiguamiento ζ", command=self.calcular_relacion_amort).pack(fill=tk.X, pady=2)

        self.label_amort_result = ttk.Label(frame, text="", foreground="blue")
        self.label_amort_result.pack(pady=(4,10))

        ttk.Separator(frame, orient="horizontal").pack(fill=tk.X, pady=8)

    def _crear_canvas(self):
        self.canvas = tk.Canvas(self.root, bg="gray")
        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # -----------------------------
    # Funciones de imagen
    # -----------------------------


    def guardar_resultado(self):
        if self.result is None:
            messagebox.showwarning("Aviso", "No hay imagen para guardar.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".png")
        if path:
            self.result.save(path)
            messagebox.showinfo("Guardado", f"Imagen guardada en {path}")

    # -----------------------------
    # Transformaciones de imagen (ejemplo que llamará a main si existen)
    # -----------------------------
    
    # -----------------------------
    # Funciones que conectan con main.Resorte
    # -----------------------------
    def crear_resorte(self):
        try:
            nombre = self.entry_r_nombre.get()
            k = float(self.entry_r_k.get())
            long_libre = float(self.entry_r_long.get())
            def_max = float(self.entry_r_defmax.get())
            dm_in = float(self.entry_r_dmin.get())
            dm_ex = float(self.entry_r_dmex.get())

            self.resorte = main.Resorte(nombre, k, long_libre, def_max, dm_in, dm_ex)
            msg = f"Resorte '{nombre}' creado. k={k} N/m, long={long_libre} m"
            self.label_resorte_result.config(text=msg)
            messagebox.showinfo("Resorte creado", msg)
        except Exception as e:
            messagebox.showerror("Error creando resorte", str(e))

    def calcular_fuerza(self):
        if self.resorte is None:
            messagebox.showwarning("Aviso", "Cree primero el resorte.")
            return
        try:
            deflex = float(self.entry_r_deflex.get())
            F = self.resorte.fuerza(deflex)
            texto = f"Fuerza = {F:.4f} N (k={self.resorte.k:.3f} N/m, x={deflex} m)"
            self.label_resorte_result.config(text=texto)
            messagebox.showinfo("Fuerza del resorte", texto)
        except Exception as e:
            messagebox.showerror("Error calculando fuerza", str(e))

    def calcular_frec_natural(self):
        if self.resorte is None:
            messagebox.showwarning("Aviso", "Cree primero el resorte.")
            return
        try:
            masa = float(self.entry_r_masa.get())
            f = self.resorte.frec_natural(masa)
            texto = f"Frecuencia natural = {f:.4f} Hz (masa={masa} kg)"
            self.label_resorte_result.config(text=texto)
            messagebox.showinfo("Frecuencia natural", texto)
        except Exception as e:
            messagebox.showerror("Error calculando frecuencia", str(e))

    def calcular_omega_natural(self):
        if self.resorte is None:
            messagebox.showwarning("Aviso", "Cree primero el resorte.")
            return
        try:
            masa = float(self.entry_r_masa.get())
            w = self.resorte.omega_natural(masa)
            texto = f"Omega natural = {w:.4f} rad/s (masa={masa} kg)"
            self.label_resorte_result.config(text=texto)
            messagebox.showinfo("Omega natural", texto)
        except Exception as e:
            messagebox.showerror("Error calculando omega", str(e))

    # -----------------------------
    # Funciones que conectan con main.Amortiguador
    # -----------------------------
    def crear_amortiguador(self):
        try:
            nombre = self.entry_a_nombre.get()
            densidad = float(self.entry_a_rho.get())
            visc40 = float(self.entry_a_visc40.get())
            visc100 = float(self.entry_a_visc100.get())

            self.amortiguador = main.Amortiguador(nombre, densidad, visc40, visc100)
            msg = f"Amortiguador '{nombre}' creado."
            self.label_amort_result.config(text=msg)
            messagebox.showinfo("Amortiguador creado", msg)
        except Exception as e:
            messagebox.showerror("Error creando amortiguador", str(e))

    def calcular_viscosidad(self):
        if self.amortiguador is None:
            messagebox.showwarning("Aviso", "Cree primero el amortiguador.")
            return
        try:
            temp = float(self.entry_a_temp.get())
            eta = self.amortiguador.viscosidad_dinamica(temp)
            texto = f"Viscosidad dinámica a {temp}°C = {eta:.6f} Pa·s"
            self.label_amort_result.config(text=texto)
            messagebox.showinfo("Viscosidad dinámica", texto)
        except Exception as e:
            messagebox.showerror("Error calculando viscosidad", str(e))

    def calcular_coef_amort(self):
        if self.amortiguador is None:
            messagebox.showwarning("Aviso", "Cree primero el amortiguador.")
            return
        try:
            masa = float(self.entry_a_masa.get())
            k = float(self.entry_a_k.get())
            factor = float(self.entry_a_factor.get())
            c = self.amortiguador.coef_amortiguamiento(masa, k, factor)
            texto = f"Coef. amortiguamiento c = {c:.4f} N·s/m (factor={factor})"
            self.label_amort_result.config(text=texto)
            messagebox.showinfo("Coef. amortiguamiento", texto)
        except Exception as e:
            messagebox.showerror("Error calculando c", str(e))

    def calcular_relacion_amort(self):
        if self.amortiguador is None:
            messagebox.showwarning("Aviso", "Cree primero el amortiguador.")
            return
        try:
            masa = float(self.entry_a_masa.get())
            k = float(self.entry_a_k.get())
            c = float(self.entry_a_c.get())
            zeta = self.amortiguador.relacion_amortiguamiento(masa, k, c)
            estado = "Subamortiguado" if zeta < 1 else ("Crítico" if abs(zeta-1) < 1e-3 else "Sobreamortiguado")
            texto = f"ζ = {zeta:.4f} → {estado}"
            self.label_amort_result.config(text=texto)
            messagebox.showinfo("Relación amortiguamiento", texto)
        except Exception as e:
            messagebox.showerror("Error calculando ζ", str(e))
       # ---------------------------------------------------------
    # FUNCIÓN: Buscar resorte, aceite y graficar x(t)
    # ---------------------------------------------------------
    def seleccionar_y_graficar(self):
        try:
            # Pedir datos al usuario
            w_n_obj = float(simpledialog.askstring("Frecuencia natural",
                                                   "Ingrese la frecuencia natural objetivo (rad/s):"))
            m = float(simpledialog.askstring("Masa",
                                             "Ingrese la masa (kg):"))
            A0 = float(simpledialog.askstring("Amplitud",
                                              "Ingrese la amplitud inicial (m):"))

            # --- Cargar Excel ---
            df_resortes = pd.read_excel("Resortes_resoil.xlsx")
            df_aceites = pd.read_excel("Aceites_resoil.xlsx")

            # Buscar columna de k
            col_k = "[Y] Constante elástica (lbs/in)"
            # k requerido
            k_req = m * w_n_obj**2
            
            
            # convertir la k del Excel
            df_resortes["k_Nm"] = df_resortes[col_k] * 175.1268


            df_resortes["error_k"] = abs(df_resortes["k_Nm"] - k_req)
            sel_resorte = df_resortes.loc[df_resortes["error_k"].idxmin()]
            k = sel_resorte["k_Nm"]

            # Buscar columna de viscosidad
            col_visc = "Visc_40 (mm²/s)"
            alpha = 5  # factor geométrico del amortiguador
            df_aceites["c_calc"] = df_aceites[col_visc] * alpha
            df_aceites["zeta"] = df_aceites["c_calc"] / (2 * np.sqrt(m*k))
            df_aceites["error_z"] = abs(df_aceites["zeta"] - 0.2)

            sel_aceite = df_aceites.loc[df_aceites["error_z"].idxmin()]
            c = sel_aceite["c_calc"]

            # Cálculos dinámicos
            zeta = c / (2 * np.sqrt(m*k))
            w_d = w_n_obj * np.sqrt(1 - zeta**2)

            # Generar señal
            t = np.linspace(0, 5, 2000)
            x = A0 * np.exp(-zeta * w_n_obj * t) * np.cos(w_d * t)

            # Mostrar info seleccionada
            info = (
                f"Resorte seleccionado:\n{sel_resorte}\n\n"
                f"Aceite seleccionado:\n{sel_aceite}\n\n"
                f"ζ = {zeta:.4f}\n"
                f"ω_d = {w_d:.4f} rad/s"
            )
            messagebox.showinfo("Selección automática", info)

            # Graficar
            plt.figure()
            plt.plot(t, x)
            plt.title("Respuesta x(t)")
            plt.xlabel("Tiempo (s)")
            plt.ylabel("Desplazamiento (m)")
            plt.grid(True)
            plt.show()

        except Exception as e:
            messagebox.showerror("Error", str(e))


# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = Resoil(root)
    root.mainloop()
