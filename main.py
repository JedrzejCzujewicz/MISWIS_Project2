import tkinter as tk
from tkinter import ttk
import serial
import time
import threading
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from queue import Queue
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

TEMP_MIN = 20
TEMP_MAX = 40
temp_zadana = 30

SERIAL_PORT = 'COM3'
BAUD_RATE = 9600
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)
queue = Queue()

def send_temp_zadana():
    if ser.is_open:
        ser.write(f"T{temp_zadana:.1f}\n".encode())


def read_from_serial():
    while True:
        if ser.is_open:
            try:
                line = ser.readline().decode().strip()
                if line:
                    queue.put(line)
            except:
                pass


def modify_temp(delta):
    global temp_zadana
    temp_zadana = max(TEMP_MIN, min(TEMP_MAX, temp_zadana + delta))
    send_temp_zadana()
    temp_label.config(text=f"Temperatura Zadana: {temp_zadana:.1f} °C")

threading.Thread(target=read_from_serial, daemon=True).start()

time_data = []
temp_zadana_data = []
temp_aktualna_data = []
syg_ster_data = []


def update_plot(frame):
    global time_data, temp_zadana_data, temp_aktualna_data, syg_ster_data
    while not queue.empty():
        line = queue.get()
        try:
            parts = line.split(',')
            if len(parts) == 3:
                t, temp_aktualna, syg_ster = map(float, parts)
                t_seconds = t / 10
                time_data.append(t_seconds)
                temp_zadana_data.append(temp_zadana)
                temp_aktualna_data.append(temp_aktualna)
                syg_ster_data.append((syg_ster/255*100))
                temp_actual_label.config(text=f"Temperatura Aktualna: {temp_aktualna:.2f} °C")
        except:
            pass

    ax1.clear()
    ax2.clear()
    ax1.plot(time_data, temp_zadana_data, label="Temperatura Zadana")
    ax1.plot(time_data, temp_aktualna_data, label="Temperatura Aktualna")
    ax1.set_title("Temperatura Aktualna i Zadana")
    ax1.set_xlabel("Czas [s]")
    ax1.set_ylabel("Temperatura [°C]")
    ax1.legend()
    ax1.grid()
    ax2.plot(time_data, syg_ster_data, label="Sygnał Sterujący")
    ax2.set_title("Sygnał Sterujący")
    ax2.set_xlabel("Czas [s]")
    ax2.set_ylabel("Sygnał Sterujący [%]")
    ax2.set_ylim(-10,110)
    ax2.grid()
    if time_data:
        ax1.set_xlim(0, time_data[-1])  # Oś X od 0 do ostatniej wartości czasu
        ax2.set_xlim(0, time_data[-1])

root = tk.Tk()
root.title("Arduino GUI")
frame = ttk.Frame(root)
frame.pack(padx=10, pady=10)
temp_actual_label = ttk.Label(frame, text="Temperatura Aktualna: -- °C")
temp_actual_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
temp_label = ttk.Label(frame, text=f"Temperatura Zadana: {temp_zadana:.1f} °C")
temp_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")

button_frame = ttk.Frame(frame)
button_frame.grid(row=1, column=0, columnspan=2)
ttk.Button(button_frame, text="-1", command=lambda: modify_temp(-1)).grid(row=0, column=0, padx=5)
ttk.Button(button_frame, text="-0.5", command=lambda: modify_temp(-0.5)).grid(row=0, column=1, padx=5)
ttk.Button(button_frame, text="+0.5", command=lambda: modify_temp(0.5)).grid(row=0, column=2, padx=5)
ttk.Button(button_frame, text="+1", command=lambda: modify_temp(1)).grid(row=0, column=3, padx=5)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
fig.subplots_adjust(hspace=0.5)
ani = FuncAnimation(fig, update_plot, interval=100, cache_frame_data=False)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

send_temp_zadana()
root.mainloop()