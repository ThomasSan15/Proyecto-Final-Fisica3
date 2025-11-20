import math
from typing import Union

Number = Union[int, float]


# ==========================================================
#  CLASE: RESORTE
# ==========================================================
class Resorte:
    """
    Representa un resorte lineal (ley de Hooke) y sus propiedades físicas.

    Unidades (recomendación: usar SI en todo el programa):
      - k (constante elástica): N/m
      - long_libre (longitud libre): m
      - def_max (deformación máxima absoluta permitida): m
      - dm_in, dm_ex (diámetros interno/externo): m
      - deflexion (argumento de los métodos): m
      - masa (en métodos relacionados con frecuencia): kg

    Notas:
      - fuerza(deflexion) devuelve la fuerza en Newtons (N).
      - frec_natural(masa) devuelve la frecuencia natural en Hz.
      - omega_natural(masa) devuelve la frecuencia angular natural en rad/s.
    """

    def __init__(
        self,
        nombre: str,
        k: Number,
        long_libre: Number,
        def_max: Number,
        dm_in: Number,
        dm_ex: Number,
    ) -> None:
        # Validaciones de entrada
        if k <= 0:
            raise ValueError("k (N/m) debe ser positivo.")
        if long_libre <= 0:
            raise ValueError("long_libre (m) debe ser positivo.")
        if def_max < 0:
            raise ValueError("def_max (m) debe ser >= 0.")
        if dm_in < 0 or dm_ex < 0:
            raise ValueError("Diámetros (m) deben ser >= 0.")
        if dm_in > dm_ex:
            raise ValueError("dm_in no puede ser mayor que dm_ex.")

        self.nombre = nombre
        self.k = float(k)
        self.long_libre = float(long_libre)
        self.def_max = float(def_max)
        self.dm_in = float(dm_in)
        self.dm_ex = float(dm_ex)

    # ----------------------------------------------------------
    def fuerza(self, deflexion: Number) -> float:
        """
        Calcula la fuerza ejercida por el resorte según la ley de Hooke:
            F = k * x
        """
        return self.k * float(deflexion)

    # ----------------------------------------------------------
    def dentro_limites(self, deflexion: Number) -> bool:
        """
        Indica si una deflexión (m) está dentro de la deformación máxima permitida.
        """
        return abs(float(deflexion)) <= self.def_max

    # ----------------------------------------------------------
    def frec_natural(self, masa: Number) -> float:
        """
        Calcula la frecuencia natural en Hz del sistema masa-resorte:
            f = (1 / 2π) * sqrt(k / m)
        """
        m = float(masa)
        if m <= 0:
            raise ValueError("masa (kg) debe ser > 0.")
        return (1.0 / (2.0 * math.pi)) * math.sqrt(self.k / m)

    # ----------------------------------------------------------
    def omega_natural(self, masa: Number) -> float:
        """
        Calcula la frecuencia angular natural en rad/s:
            ω = sqrt(k / m)
        """
        m = float(masa)
        if m <= 0:
            raise ValueError("masa (kg) debe ser > 0.")
        return math.sqrt(self.k / m)


# ==========================================================
#  CLASE: AMORTIGUADOR
# ==========================================================
class Amortiguador:
    """
    Representa un amortiguador visto desde el punto de vista del fluido (propiedades del aceite).

    Campos esperados:
      - nombre: str
      - densidad: densidad del fluido en g/cm³ (como en catálogos)
      - visc_40: viscosidad cinemática a 40 °C (mm²/s o cSt)
      - visc_100: viscosidad cinemática a 100 °C (mm²/s o cSt)

    Métodos:
      - viscosidad_dinamica(temp): devuelve η (Pa·s) a la temperatura indicada (°C)
      - coef_amortiguamiento(masa, k, factor): devuelve c = factor * c_crit (kg/s)
      - relacion_amortiguamiento(masa, k, c): calcula ζ = c / c_crit (adimensional)
    """

    def __init__(
        self, nombre: str, densidad: Number, visc_40: Number, visc_100: Number
    ) -> None:
        if visc_40 <= 0 or visc_100 <= 0:
            raise ValueError("Viscosidades (mm²/s) deben ser > 0.")
        if densidad <= 0:
            raise ValueError("Densidad debe ser > 0 (g/cm³).")

        self.nombre = nombre
        self.densidad = float(densidad)
        self.visc_40 = float(visc_40)
        self.visc_100 = float(visc_100)

    # ----------------------------------------------------------
    def viscosidad_dinamica(self, temp: Number) -> float:
        """
        Calcula la viscosidad dinámica η (Pa·s) a una temperatura dada (°C).
        Usa interpolación lineal entre 40°C y 100°C si es necesario.
        """
        t = float(temp)
        rho = self.densidad * 1000.0  # g/cm³ → kg/m³

        # Selección/interpolación
        if t <= 40.0:
            nu = self.visc_40 * 1e-6
        elif t >= 100.0:
            nu = self.visc_100 * 1e-6
        else:
            nu_interp = self.visc_40 + (self.visc_100 - self.visc_40) * (
                t - 40.0
            ) / 60.0
            nu = nu_interp * 1e-6

        return nu * rho  # η = ν * ρ

    # ----------------------------------------------------------
    def coef_amortiguamiento(self, masa: Number, k: Number, factor: Number = 1.0) -> float:
        """
        Calcula el coeficiente de amortiguamiento c (kg/s) según:
            c = factor * c_crit
        donde:
            c_crit = 2 * sqrt(k * masa)
        """
        m = float(masa)
        kf = float(k)
        if m <= 0 or kf <= 0:
            raise ValueError("masa (kg) y k (N/m) deben ser > 0.")
        c_crit = 2.0 * math.sqrt(kf * m)
        return float(factor) * c_crit

    # ----------------------------------------------------------
    def relacion_amortiguamiento(self, masa: Number, k: Number, c: Number) -> float:
        """
        Calcula la razón de amortiguamiento ζ = c / c_crit (adimensional).

        Interpretación:
          ζ < 1 → subamortiguado
          ζ = 1 → críticamente amortiguado
          ζ > 1 → sobreamortiguado
        """
        c_crit = 2.0 * math.sqrt(float(k) * float(masa))
        return float(c) / c_crit

"""
# ==========================================================
#  PRUEBA DE FUNCIONAMIENTO (si se ejecuta directamente)
# ==========================================================
if __name__ == "__main__":
    # Ejemplo de resorte
    resorte = Resorte("Spring A", k=200.0, long_libre=0.1, def_max=0.02, dm_in=0.02, dm_ex=0.03)
    print(f"Frecuencia natural (1 kg): {resorte.frec_natural(1.0):.3f} Hz")

    # Ejemplo de amortiguador (aceite 15W)
    amort = Amortiguador("15W", densidad=0.881, visc_40=72.6, visc_100=11.6)
    print(f"Viscosidad dinámica a 40°C: {amort.viscosidad_dinamica(40):.3f} Pa·s")
    print(f"Viscosidad dinámica a 70°C: {amort.viscosidad_dinamica(70):.3f} Pa·s")
    print(f"Viscosidad dinámica a 100°C: {amort.viscosidad_dinamica(100):.3f} Pa·s")

    # Comparar tipos de amortiguamiento
    masa = 1.0  # kg
    k = 200.0   # N/m
    c_crit = amort.coef_amortiguamiento(masa, k)
    print(f"\nCoeficiente crítico: {c_crit:.2f} N·s/m")

    for factor in [0.5, 1.0, 2.0]:
        c = amort.coef_amortiguamiento(masa, k, factor)
        zeta = amort.relacion_amortiguamiento(masa, k, c)
        estado = (
            "Subamortiguado" if zeta < 1
            else "Crítico" if abs(zeta - 1) < 1e-3
            else "Sobreamortiguado"
        )
        print(f"Factor={factor:.1f} → c={c:.2f} N·s/m → ζ={zeta:.2f} → {estado}")
"""