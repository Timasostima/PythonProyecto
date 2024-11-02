import glob
import os
import unicodedata
import urllib
import tkinter as tk
from tkinter import ttk

import requests
from PIL import Image, ImageDraw, ImageFont, ImageTk
import textwrap
from dotenv import load_dotenv

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
        'User-Agent': env_vars['AGENT1'],
        "Authorization": env_vars['API_AUTH'],
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

        headers = {'User-Agent': env_vars['AGENT2']}
        request = urllib.request.Request(img_url, headers=headers)
        with urllib.request.urlopen(request) as response, open(f"{img_dir}/{name}{img_extension}", 'wb') as out_file:
            data = response.read()
            out_file.write(data)
        return f"{img_dir}/{name}{img_extension}"


def replace_special_characters(text):
    normalized_text = unicodedata.normalize('NFD', text)
    return ''.join(c for c in normalized_text if unicodedata.category(c) != 'Mn')


def render_text(text, font_size, fill="white"):
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


def reload_recipes(frame, recetas):
    for widget in frame.winfo_children():
        widget.destroy()
    for i in range(len(recetas)):
        row = i // 2
        column = i % 2
        create_recipe_card(frame, recetas[i], row, column)


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
