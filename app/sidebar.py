"""
Autor: Tymur Kulivar Shymanskyi
Clase: Diseño de interfaces
"""

import tkinter as tk
from tkinter import ttk

import requests
from slider import Slider
from utils import render_text, fetch_image, reload_recipes
from Recipe import Recipe
from api.api import api_port

request_url = f"http://localhost:{api_port}/recetas"


class Sidebar(ttk.Frame):
    def __init__(self, frame, scrollable_frame):
        font_size = 15
        super().__init__(frame)

        # creado referencia al frame que contiene las recetas
        self.recipies_frame = scrollable_frame

        # Configuración del frame
        self.config(width=200, padding="10 10 10 10")
        self.pack(side=tk.LEFT, fill=tk.Y)

        max_calorias, max_duracion = self.api_values()

        # Título de la aplicación
        app_name_image = render_text("Busca Recetas", font_size + 8)
        app_name = tk.Label(self, image=app_name_image, bg="#333333")
        app_name.image = app_name_image
        app_name.pack(pady=(10, 40))

        # Campo de entrada para el nombre de la receta
        name_image = render_text("Nombre:", font_size)
        name = tk.Label(self, image=name_image, bg="#333333")
        name.image = name_image
        name.pack(padx=20, anchor=tk.W)
        self.name_entry = ttk.Entry(self, style='TEntry')
        self.name_entry.pack(pady=(5, 25), padx=20, fill=tk.X)

        # Slider para el tiempo de preparación
        minutes_image = render_text("Tiempo en minutos:", font_size)
        minutes = tk.Label(self, image=minutes_image, bg="#333333")
        minutes.image = minutes_image
        minutes.pack(padx=20, anchor=tk.W)
        self.time_slider = Slider(self, max_duracion)
        self.time_slider.pack(pady=(5, 25), padx=10, fill=tk.X)

        # Slider para la dificultad
        dif_image = render_text("Dificultad:", font_size)
        dif = tk.Label(self, image=dif_image, bg="#333333")
        dif.image = dif_image
        dif.pack(padx=20, anchor=tk.W)
        self.difficulty_slider = Slider(self, 10)
        self.difficulty_slider.pack(pady=(5, 25), padx=10, fill=tk.X)

        # Slider para las calorías
        calorias_image = render_text("Calorias:", font_size)
        calorias = tk.Label(self, image=calorias_image, bg="#333333")
        calorias.image = calorias_image
        calorias.pack(padx=20, anchor=tk.W)
        self.calories_slider = Slider(self, max_calorias)
        self.calories_slider.pack(pady=(5, 25), padx=10, fill=tk.X)

        # Combobox para el tipo de receta
        tipo_image = render_text("Tipo:", font_size)
        tipo_label = tk.Label(self, image=tipo_image, bg="#333333")
        tipo_label.image = tipo_image
        tipo_label.pack(anchor=tk.W, padx=20)
        combobox_values = ["", "Desayuno", "Primer plato", "Segundo plato", "Postre"]
        self.type_combobox = ttk.Combobox(self, values=combobox_values, state='readonly')
        self.type_combobox.pack(anchor=tk.W, padx=20, pady=(5, 25))

        # Espaciador para llenar el espacio restante
        spacer_frame = tk.Frame(self, bg="#333333")
        spacer_frame.pack(fill=tk.BOTH, expand=True)

        # Botón para realizar la consulta a la API
        query_button = tk.Button(self, text="Query", bg="lightblue", command=self.query_api)
        query_button.pack(side=tk.BOTTOM, fill=tk.X)

    def query_api(self):
        # Obtención de los valores de los campos de entrada y sliders
        name = self.name_entry.get()
        time_min, time_max = self.time_slider.get_value()
        difficulty_min, difficulty_max = self.difficulty_slider.get_value()
        calories_min, calories_max = self.calories_slider.get_value()
        type_ = self.type_combobox.get()

        # Creación del diccionario de parámetros para la consulta
        params = {
            "nombre": name,
            "min_t": time_min,
            "max_t": time_max,
            "min_diff": difficulty_min,
            "max_diff": difficulty_max,
            "min_cal": calories_min,
            "max_cal": calories_max,
            "tipo": type_
        }

        # Filtrado de parámetros vacíos
        params = {k: v for k, v in params.items() if v}
        # print(params)

        # Realización de la consulta a la API
        response = requests.get(request_url, params=params)

        if response.status_code == 200:
            recetas = []
            # Procesamiento de la respuesta de la API
            for jsonObj in response.json():
                receta = Recipe(
                    jsonObj['nombre'], jsonObj['descripcion'], jsonObj['tipo'], jsonObj['minutos'], jsonObj['calorias'],
                    jsonObj['dificultad'], jsonObj['ingredientes'],
                    fetch_image(jsonObj['nombre'], jsonObj['nombre_ing'])
                )
                recetas.append(receta)
                # print(receta.__str__())
            # Recarga de las recetas en el frame desplazable
            reload_recipes(self.recipies_frame, recetas)
        else:
            print("Error:", response.status_code, response.text)

    def api_values(self):
        # Realización de la consulta a la API
        response = requests.get(f"{request_url}/meta")

        if response.status_code == 200:
            max_calorias = response.json()['max_calorias']
            max_duracion = response.json()['max_duracion']
            return max_calorias, max_duracion
        else:
            print("Error:", response.status_code, response.text)
