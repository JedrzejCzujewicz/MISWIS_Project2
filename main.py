import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def analyze_step_response(time, temperature, y0, y_final):
    """
    Analizuje odpowiedź skokową układu cieplnego.

    Parameters:
    time: tablica czasu [s]
    temperature: tablica temperatur [°C]
    y0: temperatura początkowa [°C]
    y_final: temperatura końcowa [°C]

    Returns:
    tau: stała czasowa [s]
    K: wzmocnienie statyczne [°C/jednostkę sterowania]
    T0: przybliżone opóźnienie transportowe [s]
    """
    # Normalizacja temperatury do zakresu 0-1
    temp_norm = (temperature - y0) / (y_final - y0)

    # Znalezienie stałej czasowej (czas do osiągnięcia 63.2% wartości końcowej)
    tau_index = np.argmin(np.abs(temp_norm - 0.632))
    tau = time[tau_index]

    # Wzmocnienie statyczne (zmiana wyjścia / zmiana wejścia)
    # Dla PWM 255, więc dzielimy przez 255
    K = (y_final - y0) / 255

    # Znalezienie opóźnienia transportowego
    # Szukamy momentu, gdy temperatura zacznie znacząco rosnąć (np. 1% zmiany)
    T0_index = np.argmin(np.abs(temp_norm - 0.01))
    T0 = time[T0_index]

    return tau, K, T0


# Wczytanie danych z pliku
temperature = np.loadtxt('file.txt')

# Generowanie wektora czasu (pomiary co 0.1s)
t = np.arange(len(temperature)) * 0.1

# Temperatura początkowa i końcowa
T0 = temperature[0]
Tf = temperature[-1]

# Analiza odpowiedzi skokowej
tau, K, T0_delay = analyze_step_response(t, temperature, T0, Tf)

# Wizualizacja
plt.figure(figsize=(12, 6))
plt.plot(t, temperature, 'b-', label='Temperatura zmierzona')
plt.axhline(y=T0 + 0.632 * (Tf - T0), color='r', linestyle='--',
            label='63.2% wartości końcowej')
plt.axvline(x=tau, color='g', linestyle='--', label=f'Stała czasowa (τ = {tau:.1f}s)')
plt.axvline(x=T0_delay, color='m', linestyle='--', label=f'Opóźnienie (T0 = {T0_delay:.1f}s)')
plt.grid(True)
plt.xlabel('Czas [s]')
plt.ylabel('Temperatura [°C]')
plt.title('Odpowiedź skokowa układu grzewczego - dane rzeczywiste')
plt.legend()
plt.show()

# Wyświetlenie parametrów
print(f"\nParametry układu:")
print(f"Temperatura początkowa: {T0:.2f}°C")
print(f"Temperatura końcowa: {Tf:.2f}°C")
print(f"Stała czasowa (τ): {tau:.1f} s")
print(f"Wzmocnienie statyczne (K): {K:.4f} °C/jednostkę PWM")
print(f"Opóźnienie transportowe (T0): {T0_delay:.1f} s")

# Obliczenie parametrów regulatora PID metodą Zieglera-Nicholsa
Kp = 1.2 * ((tau) / (K * T0_delay))
Ti = 2 * T0_delay
Td = 0.5 * T0_delay

# Przeliczenie na Ki i Kd
Ki = Kp / Ti
Kd = Kp * Td

print(f"\nZalecane parametry regulatora PID:")
print(f"Kp = {Kp:.2f}")
print(f"Ki = {Ki:.2f}")
print(f"Kd = {Kd:.2f}")