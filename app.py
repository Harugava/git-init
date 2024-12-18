import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter  # Используем PillowWriter для GIF
import io
import base64
import os
from flask import Flask, render_template, request

app = Flask(__name__)

# Функция для генерации трохоиды
def generate_trochoid(R, h):
    t = np.linspace(0, 8 * np.pi, 100)  # Уменьшаем количество точек для ускорения
    x = R * t - h * np.sin(t)
    y = R - h * np.cos(t)
    return x, y

@app.route("/", methods=["GET", "POST"])
def index():
    graph_html = None
    if request.method == "POST":
        try:
            R = float(request.form["R"])
            h = float(request.form["h"])

            # Генерация трохоиды
            x, y = generate_trochoid(R, h)

            # Создание графика
            fig, ax = plt.subplots()
            ax.set_xlim(min(x) - 2 * R, max(x) + 2 * R)
            ax.set_ylim(min(y) - 4 * R, max(y) + 4 * R)
            ax.set_xlabel("x", fontsize=14)
            ax.set_ylabel("y", fontsize=14)
            ax.grid(True, linestyle='--', alpha=0.6)
            ax.axhline(0, color='black', linewidth=0.8, linestyle='--')
            ax.axvline(0, color='black', linewidth=0.8, linestyle='--')
            ax.tick_params(axis='both', which='major', labelsize=12)
            ax.set_aspect('equal')

            # Линия для анимации
            line, = ax.plot([], [], lw=3, color='blue')

            def init():
                line.set_data([], [])
                return line,

            def update(frame):
                line.set_data(x[:frame], y[:frame])
                return line,

            # Создаем анимацию
            ani = FuncAnimation(fig, update, frames=range(1, len(x)), init_func=init, blit=True, interval=30)

            gif_path = "trochoid_animation.gif"
            writer = PillowWriter(fps=120)
            ani.save(gif_path, writer=writer)

            # Чтение GIF и кодирование в base64
            with open(gif_path, "rb") as f:
                gif_data = f.read()
                graph_html = base64.b64encode(gif_data).decode('utf-8')

            # Удаляем временный файл GIF
            os.remove(gif_path)

        except ValueError:
            graph_html = "<p style='color: red;'>Пожалуйста, введите корректные значения!</p>"

    return render_template("index.html", graph_html=graph_html)

if __name__ == "__main__":
    app.run(debug=True)
