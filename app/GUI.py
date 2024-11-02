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

from api.api import run

from Recipe import Recipe

recetas = []

load_dotenv("../variables.env")
env_vars = {
    "API_AUTH": os.getenv('API_AUTH'),
    "AGENT1": os.getenv('AGENT1'),
    "AGENT2": os.getenv('AGENT2')
}


def fetch_image(name):
    img_dir = "../imgs"
    name2 = replace_special_characters(name)
    print(name2)
    img_path_pattern = os.path.join(img_dir, f"{name}.*")
    existing_files = glob.glob(img_path_pattern)

    # Verificar si la imagen ya existe
    if existing_files:
        return existing_files[0]

    img_headers = {
        'User-Agent': env_vars["AGENT1"],
        "Authorization": env_vars["API_AUTH"],
    }
    img_parameters = {"query": name2, "orientation": "square", "per_page": "1"}
    img_response = requests.get(url="https://api.pexels.com/v1/search", headers=img_headers, params=img_parameters)

    print("Status code", img_response.status_code)
    if img_response.status_code == 200:
        try:
            img_url = img_response.json()['photos'][0]['src']['small']
        except IndexError:
            img_url = "../imgs/default.png"
            return img_url
        img_extension = os.path.splitext(img_url.split("?")[0])[1]

        headers = {'User-Agent': 'AGENT1'}
        request = urllib.request.Request(img_url, headers=headers)
        with urllib.request.urlopen(request) as response, open(f"../imgs/{name2}{img_extension}", 'wb') as out_file:
            data = response.read()
            out_file.write(data)
        return f"{img_dir}/{name2}{img_extension}"


def replace_special_characters(text):
    normalized_text = unicodedata.normalize('NFD', text)
    return ''.join(c for c in normalized_text if unicodedata.category(c) != 'Mn')


def render_text(text, font_path, font_size):
    font = ImageFont.truetype(font_path, font_size)
    dummy_image = Image.new('RGBA', (1, 1))
    draw = ImageDraw.Draw(dummy_image)
    bbox = draw.textbbox((0, 0), text, font=font)
    padding = 1.5
    size = (int(bbox[2] - bbox[0] + padding * 2), int(bbox[3] - bbox[1] + padding * 2))
    image = Image.new('RGBA', size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    draw.text((padding, padding), text, font=font, fill="black")
    return ImageTk.PhotoImage(image)


def create_recipe_card(frame, recipe, row, column):
    font_size = 10

    card_frame = ttk.Frame(frame, padding="10 10 10 10", style='Card.TFrame')
    card_frame.grid(row=row, column=column, padx=10, pady=10, sticky=tk.NSEW)

    card_frame.config(borderwidth=2, relief="groove", style='Card.TFrame')
    style = ttk.Style()
    style.configure('Card.TFrame', background='#ffffff')

    image = Image.open(recipe.image_path)
    image = image.resize((150, 150), Image.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    image_label = ttk.Label(card_frame, image=photo, style='Card.TLabel')
    image_label.image = photo
    image_label.grid(row=0, column=0, rowspan=3, padx=10, pady=10)

    name_label = ttk.Label(card_frame, text=recipe.name, font=("Arial", 16, "bold"), style='Card.TLabel')
    name_label.grid(row=0, column=1, sticky=tk.W, padx=10)

    description_label = ttk.Label(card_frame, text=recipe.descripcion, font=("Arial", font_size),
                                  style='Card.TLabel', wraplength=400)
    description_label.grid(row=1, column=1, sticky=tk.W, padx=10)

    types_label = ttk.Label(card_frame, text=f"Tipo: {recipe.tipo}", font=("Arial", font_size),
                            style='Card.TLabel', width=38, wraplength=400)
    types_label.grid(row=2, column=1, sticky=tk.W, padx=10)

    ingredients_label = ttk.Label(card_frame, text=f"Ingredientes: {recipe.ingredients}", font=("Arial", font_size),
                                  style='Card.TLabel', width=38, wraplength=400)
    ingredients_label.grid(row=3, column=1, sticky=tk.W, padx=10)

    calories_label = ttk.Label(card_frame, text=f"{recipe.calorias}cal", font=("Arial", font_size),
                               style='Card.TLabel')
    calories_label.grid(row=0, column=2, sticky=tk.W, padx=10, pady=(10, 0))

    time_label = ttk.Label(card_frame, text=f"{recipe.minutos} minutes", font=("Arial", font_size),
                           style='Card.TLabel')
    time_label.grid(row=4, column=1, sticky=tk.W, padx=10, pady=(10, 0))

    complexity_label = ttk.Label(card_frame, text=f"Dif:{recipe.dificultad}", font=("Arial", font_size),
                                 style='Card.TLabel')
    complexity_label.grid(row=4, column=2, sticky=tk.W, padx=10, pady=(10, 0))


def reload_recipes(frame):
    for i in range(len(recetas)):
        row = i // 2
        column = i % 2
        create_recipe_card(frame, recetas[i], row, column)


class Slider:
    def __init__(self, frame, max_val):
        self.left = tk.DoubleVar()
        self.right = tk.DoubleVar(value=max_val)
        rs1 = RangeSliderH(frame, [self.left, self.right], Width=350, Height=39, padX=11, min_val=0, max_val=max_val,
                           show_value=True, font_size=7, line_color="yellow", bgColor="#f0f0f0", step_size=1)
        rs1.pack(pady=5, padx=10, fill=tk.X)

        def change(var, idx, mode):
            pass

        self.left.trace_add("write", change)
        self.right.trace_add("write", change)

    def get_value(self):
        left_value = self.left.get()
        right_value = self.right.get()

        if left_value and right_value:
            return int(left_value), int(right_value)
        elif left_value:
            return int(left_value)
        elif right_value:
            return int(right_value)
        else:
            return None


class Sidebar(ttk.Frame):
    def __init__(self, frame):
        super().__init__()
        self.parent = frame

        sidebar_frame = ttk.Frame(frame, width=200, padding="10 10 10 10")
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Update this path to a valid font file on your system
        name_image = render_text("Nombre:", font_path, 12)
        name = tk.Label(sidebar_frame, image=name_image, bg="#f0f0f0")
        name.image = name_image
        name.pack(pady=5, padx=10, anchor=tk.W)
        self.name_entry = ttk.Entry(sidebar_frame)
        self.name_entry.pack(pady=5, padx=10, fill=tk.X)

        minutes_image = render_text("Tiempo en minutos:", font_path, 12)
        minutes = tk.Label(sidebar_frame, image=minutes_image, bg="#f0f0f0")
        minutes.image = minutes_image
        minutes.pack(pady=5, padx=10, anchor=tk.W)
        self.time_slider = Slider(sidebar_frame, 100)

        dif_image = render_text("Dificultad:", font_path, 12)
        dif = tk.Label(sidebar_frame, image=dif_image, bg="#f0f0f0")
        dif.image = dif_image
        dif.pack(pady=5, padx=10, anchor=tk.W)
        self.difficulty_slider = Slider(sidebar_frame, 10)

        calorias_image = render_text("Calorias:", font_path, 12)
        calorias = tk.Label(sidebar_frame, image=calorias_image, bg="#f0f0f0")
        calorias.image = calorias_image
        calorias.pack(pady=5, padx=10, anchor=tk.W)
        self.calories_slider = Slider(sidebar_frame, 1000)

        tipo_image = render_text("Tipo:", font_path, 12)
        tipo_label = tk.Label(sidebar_frame, image=tipo_image, bg="#f0f0f0")
        tipo_label.image = tipo_image
        tipo_label.pack(anchor=tk.W, padx=20, pady=5)
        self.type_combobox = ttk.Combobox(sidebar_frame, values=["Desayuno", "Primer plato", "Segundo Plato", "Postre"])
        self.type_combobox.pack(anchor=tk.W, padx=20, pady=5)

        query_button = ttk.Button(sidebar_frame, text="Query", style='TButton', command=self.query_api)
        query_button.pack(fill=tk.X, expand=True, pady=10)

    def query_api(self):
        global recetas
        recetas = []

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
            for jsonObj in response.json():
                receta = Recipe(
                    jsonObj['nombre'], jsonObj['descripcion'], jsonObj['tipo'], jsonObj['minutos'], jsonObj['calorias'],
                    jsonObj['dificultad'], jsonObj['ingredientes'], fetch_image(jsonObj['nombre'])
                )
                recetas.append(receta)
                print(receta.__str__())
            reload_recipes(self.parent)
        else:
            print("Error:", response.status_code, response.text)


class SimpleGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Busca Recetas")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}")
        self.configure(bg="#f0f0f0")

        style = ttk.Style(self)
        style.theme_use('clam')

        # Define custom styles
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0')
        style.configure('TButton', background='#4CAF50', foreground='white', font=("Arial", 12, "bold"))
        style.map('TButton', background=[('active', '#45a049')])

        # Create the main frame
        main_frame = ttk.Frame(self, padding="10 10 10 10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Create the left sidebar frame
        Sidebar(main_frame)

        # Create a canvas and a scrollbar for the right content frame
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        reload_recipes()


if __name__ == "__main__":
    flask_process = Process(target=run)
    flask_process.start()
    time.sleep(1)

    app = SimpleGUI()
    app.mainloop()

    flask_process.kill()
