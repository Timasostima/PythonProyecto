import glob
import os
import tkinter as tk
import unicodedata
import urllib
from multiprocessing import Process
from tkinter import ttk
import time
import requests
from PIL import Image, ImageDraw, ImageFont, ImageTk
from RangeSlider import RangeSliderH
from dotenv import load_dotenv
import textwrap

from api.api import run

from Recipe import Recipe

recetas = []

load_dotenv("../variables.env")
env_vars = {
    "API_AUTH": os.getenv('API_AUTH'),
    "AGENT1": os.getenv('AGENT1'),
    "AGENT2": os.getenv('AGENT2')
}


def fetch_image(name, name_ing):
    img_dir = "../res/images"
    img_path_pattern = os.path.join(img_dir, f"{name}.*")
    existing_files = glob.glob(img_path_pattern)

    if existing_files:
        return existing_files[0]

    img_headers = {
        'User-Agent': env_vars["AGENT1"],
        "Authorization": env_vars["API_AUTH"],
    }
    img_parameters = {"query": name_ing, "orientation": "square", "per_page": "1"}
    img_response = requests.get(url="https://api.pexels.com/v1/search", headers=img_headers, params=img_parameters)

    print("Status code", img_response.status_code)
    if img_response.status_code == 200:
        try:
            img_url = img_response.json()['photos'][0]['src']['small']
        except IndexError:
            img_url = f"{img_dir}/default.png"
            return img_url
        img_extension = os.path.splitext(img_url.split("?")[0])[1]

        headers = {'User-Agent': 'AGENT1'}
        request = urllib.request.Request(img_url, headers=headers)
        with urllib.request.urlopen(request) as response, open(f"{img_dir}/{name}{img_extension}", 'wb') as out_file:
            data = response.read()
            out_file.write(data)
        return f"{img_dir}/{name}{img_extension}"


def replace_special_characters(text):
    normalized_text = unicodedata.normalize('NFD', text)
    return ''.join(c for c in normalized_text if unicodedata.category(c) != 'Mn')


def render_text(text, font_size, fill="white"):
    # font_path = "../res/Bluebird-Regular.otf"
    font_path = "../res/Gilroy-Bold.ttf"
    font = ImageFont.truetype(font_path, font_size)
    dummy_image = Image.new('RGBA', (1, 1))
    draw = ImageDraw.Draw(dummy_image)
    bbox = draw.textbbox((0, 0), text, font=font)
    padding = 6
    size = (int(bbox[2] - bbox[0] + padding * 2), int(bbox[3] - bbox[1] + padding * 2))
    image = Image.new('RGBA', size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    draw.text((padding, padding), text, font=font, fill=fill)
    return ImageTk.PhotoImage(image)


def create_recipe_card(frame, recipe, row, column):
    font_size = 16
    wrap_width = 50

    card_frame = ttk.Frame(frame, padding="5 5 5 5", style='Card.TFrame')
    card_frame.grid(row=row, column=column, padx=5, pady=5, sticky=tk.NSEW)

    card_frame.config(borderwidth=1, relief="groove", style='Card.TFrame')
    style = ttk.Style()
    style.configure('Card.TFrame', background='#333333')

    # Configure rows and columns to expand equally
    for i in range(5):
        card_frame.grid_rowconfigure(i, weight=1)

    card_frame.grid_columnconfigure(1, weight=1)
    card_frame.grid_columnconfigure(2, weight=1)

    image = Image.open(recipe.image_path)
    image = image.resize((195, 195), Image.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    image_label = ttk.Label(card_frame, image=photo, style='Card.TLabel')
    image_label.image = photo
    image_label.grid(row=0, column=0, rowspan=5, padx=5, pady=5, sticky=tk.NS)

    name_image = render_text(recipe.name, font_size + 10, fill="white")
    name_label = ttk.Label(card_frame, image=name_image, style='Card.TLabel')
    name_label.image = name_image
    name_label.grid(row=0, column=1, sticky=tk.W, padx=5)

    description_text = textwrap.fill(recipe.descripcion, wrap_width)
    description_image = render_text(description_text, font_size, fill="white")
    description_label = ttk.Label(card_frame, image=description_image, style='Card.TLabel')
    description_label.image = description_image
    description_label.grid(row=1, column=1, sticky=tk.W, padx=5)

    types_text = textwrap.fill(f"Tipo: {recipe.tipo}", wrap_width)
    types_image = render_text(types_text, font_size, fill="white")
    types_label = ttk.Label(card_frame, image=types_image, style='Card.TLabel')
    types_label.image = types_image
    types_label.grid(row=2, column=1, sticky=tk.W, padx=5)

    ingredients_text = textwrap.fill(f"Ingredientes: {recipe.ingredients}", wrap_width)
    ingredients_image = render_text(ingredients_text, font_size, fill="white")
    ingredients_label = ttk.Label(card_frame, image=ingredients_image, style='Card.TLabel')
    ingredients_label.image = ingredients_image
    ingredients_label.grid(row=3, column=1, sticky=tk.W, padx=5)

    calories_image = render_text(f"{recipe.calorias}cal", font_size, fill="white")
    calories_label = ttk.Label(card_frame, image=calories_image, style='Card.TLabel')
    calories_label.image = calories_image
    calories_label.grid(row=0, column=2, sticky=tk.E, padx=5, pady=(5, 0))

    time_image = render_text(f"{recipe.minutos} minutos", font_size, fill="white")
    time_label = ttk.Label(card_frame, image=time_image, style='Card.TLabel')
    time_label.image = time_image
    time_label.grid(row=4, column=1, sticky=tk.W, padx=5, pady=(5, 0))

    complexity_image = render_text(f"Dif:{recipe.dificultad}", font_size, fill="white")
    complexity_label = ttk.Label(card_frame, image=complexity_image, style='Card.TLabel')
    complexity_label.image = complexity_image
    complexity_label.grid(row=4, column=2, sticky=tk.E, padx=5, pady=(5, 0))


def reload_recipes(frame):
    for widget in frame.winfo_children():
        widget.destroy()
    for i in range(len(recetas)):
        row = i // 2
        column = i % 2
        create_recipe_card(frame, recetas[i], row, column)


class Slider(RangeSliderH):
    def __init__(self, frame, max_val):
        self.left = tk.DoubleVar()
        self.right = tk.DoubleVar(value=max_val)
        super().__init__(
            frame,
            [self.left, self.right],
            Width=350,
            Height=39,
            padX=11,
            min_val=0,
            max_val=max_val,
            show_value=True,
            font_size=7,
            line_color="white",
            line_s_color="lightblue",
            bgColor="#333333",
            step_size=1,
            font_color="white",
            bar_color_inner="#555555",
            bar_color_outer="#777777",
        )

    def get_value(self):
        left_value = self.left.get()
        right_value = self.right.get()

        return (
            (int(left_value) if left_value else None),
            (int(right_value) if right_value else None)
        )


class Sidebar(ttk.Frame):
    def __init__(self, frame, scrollable_frame):
        font_size = 15
        super().__init__(frame)
        self.recipies_frame = scrollable_frame
        self.config(width=200, padding="10 10 10 10")
        self.pack(side=tk.LEFT, fill=tk.Y)

        app_name_image = render_text("Busca Recetas", font_size+8)
        app_name = tk.Label(self, image=app_name_image, bg="#333333")
        app_name.image = app_name_image
        app_name.pack(pady=(10, 40))

        name_image = render_text("Nombre:", font_size)
        name = tk.Label(self, image=name_image, bg="#333333")
        name.image = name_image
        name.pack(padx=20, anchor=tk.W)
        self.name_entry = ttk.Entry(self, style='TEntry')
        self.name_entry.pack(pady=(5, 25), padx=20, fill=tk.X)

        minutes_image = render_text("Tiempo en minutos:", font_size)
        minutes = tk.Label(self, image=minutes_image, bg="#333333")
        minutes.image = minutes_image
        minutes.pack(padx=20, anchor=tk.W)
        self.time_slider = Slider(self, 100)
        self.time_slider.pack(pady=(5, 25), padx=10, fill=tk.X)

        dif_image = render_text("Dificultad:", font_size)
        dif = tk.Label(self, image=dif_image, bg="#333333")
        dif.image = dif_image
        dif.pack(padx=20, anchor=tk.W)
        self.difficulty_slider = Slider(self, 10)
        self.difficulty_slider.pack(pady=(5, 25), padx=10, fill=tk.X)

        calorias_image = render_text("Calorias:", font_size)
        calorias = tk.Label(self, image=calorias_image, bg="#333333")
        calorias.image = calorias_image
        calorias.pack(padx=20, anchor=tk.W)
        self.calories_slider = Slider(self, 1000)
        self.calories_slider.pack(pady=(5, 25), padx=10, fill=tk.X)

        tipo_image = render_text("Tipo:", font_size)
        tipo_label = tk.Label(self, image=tipo_image, bg="#333333")
        tipo_label.image = tipo_image
        tipo_label.pack(anchor=tk.W, padx=20)
        combobox_values = ["", "Desayuno", "Primer plato", "Segundo plato", "Postre"]
        self.type_combobox = ttk.Combobox(self, values=combobox_values, state='readonly')
        self.type_combobox.pack(anchor=tk.W, padx=20, pady=(5, 25))

        spacer_frame = tk.Frame(self, bg="#333333")
        spacer_frame.pack(fill=tk.BOTH, expand=True)

        query_button = tk.Button(self, text="Query", bg="lightblue", command=self.query_api)
        query_button.pack(side=tk.BOTTOM, fill=tk.X)

    def query_api(self):
        name = self.name_entry.get()
        time_min, time_max = self.time_slider.get_value()
        difficulty_min, difficulty_max = self.difficulty_slider.get_value()
        calories_min, calories_max = self.calories_slider.get_value()
        type_ = self.type_combobox.get()

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

        params = {k: v for k, v in params.items() if v}
        print(params)
        response = requests.get("http://localhost:5000/recetas", params=params)

        if response.status_code == 200:
            global recetas
            recetas = []
            for jsonObj in response.json():
                receta = Recipe(
                    jsonObj['nombre'], jsonObj['descripcion'], jsonObj['tipo'], jsonObj['minutos'], jsonObj['calorias'],
                    jsonObj['dificultad'], jsonObj['ingredientes'], fetch_image(jsonObj['nombre'], jsonObj['nombre_ing'])
                )
                recetas.append(receta)
                print(receta.__str__())
            reload_recipes(self.recipies_frame)
        else:
            print("Error:", response.status_code, response.text)


class GUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Busca Recetas")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}")
        self.configure(bg="#333333")

        style = ttk.Style(self)
        style.theme_use('clam')

        style.configure('TFrame', background='#333333')
        style.configure('TLabel', background='#333333', foreground='white')
        style.configure('TButton', background='#4CAF50', foreground='white', font=("Arial", 12, "bold"))
        style.map('TButton', background=[('active', '#45a049')])
        style.configure('TCombobox', background='#333333', foreground='white', fieldbackground='#333333',
                        selectbackground='#555555', selectforeground='white', font=("Arial", 12, "bold"))
        style.map('TCombobox', fieldbackground=[('readonly', '#333333')], selectbackground=[('readonly', '#555555')],
                  selectforeground=[('readonly', 'white')])
        style.configure('TEntry', background='#333333', foreground='white', fieldbackground='#333333')
        style.configure('TScrollbar', background='#333333', troughcolor='#333333', arrowcolor='white')
        style.map('TScrollbar', background=[('active', '#555555'), ('pressed', '#777777')],
                  troughcolor=[('active', '#444444'), ('pressed', '#666666')],
                  arrowcolor=[('active', 'white'), ('pressed', 'white')])

        main_frame = ttk.Frame(self, padding="10 10 10 10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(main_frame, bg="#333333")
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview, style='TScrollbar')
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set, scrollregion=(0, 0, 0, 1))

        Sidebar(main_frame, self.scrollable_frame)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        reload_recipes(self.scrollable_frame)


if __name__ == "__main__":
    flask_process = Process(target=run)
    flask_process.start()
    time.sleep(1)

    app = GUI()
    app.mainloop()

    flask_process.kill()
