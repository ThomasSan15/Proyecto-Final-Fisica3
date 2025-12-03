🌀 Proyecto Final – Física III
Sistema Masa–Resorte–Amortiguador con Selección Automática de Aceite y Resorte

Este proyecto implementa un programa en Python capaz de leer dos bases de datos (resortes y aceites), seleccionar automáticamente los valores óptimos para alcanzar una frecuencia natural objetivo, mostrar los datos seleccionados y graficar la respuesta dinámica del sistema masa–resorte–amortiguador.

El programa también incluye herramientas adicionales para calcular fuerza, frecuencia, y otros parámetros mecánicos relevantes.

📂 Archivos incluidos

Resortes_resoil.xlsx → Base de datos con:

Constante elástica k (en lb/in)

Identificación/Nombre del resorte

Aceites_resoil.xlsx → Base de datos con:

Viscosidad cinemática a 40°C Visc_40 (mm²/s)

Identificación del aceite

⚙️ Funcionamiento del programa

El usuario ingresa:

Frecuencia natural objetivo (rad/s)

Masa del sistema (kg)

Amplitud inicial (m)

El programa:

Calcula el valor de k requerido para lograr la frecuencia natural objetivo.

Busca en el Excel el resorte cuya constante elástica sea más cercana.

Con la viscosidad de cada aceite calcula el coeficiente de amortiguamiento c.

Ajusta el valor de c comparando el factor de amortiguamiento ζ con uno esperado (≈ 0.2).

Selecciona el aceite más adecuado.

Muestra la información seleccionada (resorte + aceite).

Finalmente:

Calcula la respuesta dinámica:

x(t)=A0​e^−ζωn​t cos(ωd​t)

Grafica x(t) para mostrar el comportamiento oscilatorio amortiguado.

📈 Ejemplo de salida

La interfaz presenta:

Datos del resorte seleccionado

Datos del aceite óptimo

Valores calculados de:

$\zeta$

$\omega_d$

$k$ convertido a SI

Coeficiente de amortiguamiento c

Y una gráfica limpia de la función x(t).

🧠 Cálculos principales del programa
Conversión de unidades del resorte

$$
k_{SI} = k_{lb/in} \times 175.12677 \; [N/m]
$$

Frecuencia natural
$$
\omega_n = \sqrt{\frac{k}{m}}
$$
	​
Coeficiente de amortiguamiento
$$
c = \mu \cdot \alpha
$$

Factor de amortiguamiento

$$
\zeta = \frac{c}{2\sqrt{km}}
$$
	​

Frecuencia amortiguada
𝜔
𝑑
=
𝜔
𝑛
1
−
𝜁
2
ω
d
	​

=ω
n
	​

1−ζ
2
	​

🛠 Requisitos para ejecución

Debes tener instalados los siguientes módulos:

pip install pandas matplotlib openpyxl

▶️ Cómo ejecutar

Clona el repositorio con:

git clone <https://github.com/ThomasSan15/Proyecto-Final-Fisica3>


Abre el proyecto en VSCode o tu IDE preferido.

Ejecuta el script principal (resoil.py).

Ingresa los datos solicitados en las ventanas de diálogo.

🎯 Objetivo del proyecto

Este proyecto fue desarrollado como trabajo final de Física III, integrando conceptos reales de:

Oscilaciones mecánicas

Sistemas masa–resorte–amortiguador

Frecuencia natural y amortiguada

Amortiguamiento real de fluidos

Selección de materiales mediante análisis numérico

👨‍💻 Autores

Thomas Santiago Beltrán Arias

Juan José Gonzales Rios
