import numpy as np
import matplotlib.pyplot as plt

def analyze_step_response(time, temperature, y0, y_final):
    temp_norm = (temperature - y0) / (y_final - y0)
    tau_index = np.argmin(np.abs(temp_norm - 0.632))
    tau = time[tau_index]
    K = (y_final - y0) / 255
    T0_index = np.argmin(np.abs(temp_norm - 0.01))
    T0 = time[T0_index]
    return tau, K, T0

temperature = np.loadtxt('file.txt')
t = np.arange(len(temperature)) * 0.1
T0 = temperature[0]
Tf = temperature[-1]
tau, K, T0_delay = analyze_step_response(t, temperature, T0, Tf)

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

print(f"\nParametry układu:")
print(f"Temperatura początkowa: {T0:.2f}°C")
print(f"Temperatura końcowa: {Tf:.2f}°C")
print(f"Stała czasowa (τ): {tau:.1f} s")
print(f"Wzmocnienie statyczne (K): {K:.4f} °C/jednostkę PWM")
print(f"Opóźnienie transportowe (T0): {T0_delay:.1f} s")

Kp = 1.2 * ((tau) / (K * T0_delay))
Ti = 2 * T0_delay
Td = 0.5 * T0_delay
Ki = Kp / Ti
Kd = Kp * Td

print(f"\nWyznaczone parametry regulatora PID:")
print(f"Kp = {Kp:.2f}")
print(f"Ki = {Ki:.2f}")
print(f"Kd = {Kd:.2f}")
