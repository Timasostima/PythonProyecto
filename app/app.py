import json
import os
from multiprocessing import Process
import time
import requests
import urllib.request
from PIL import Image
from dotenv import load_dotenv

from api.api import run
from api.api import api_port as port
from api.api import api_host as host

from Recipe_query import Recipe_query as Recipe

load_dotenv("variables.env")
env_vars = {
    "API_AUTH": os.getenv('API_AUTH'),
    "AGENT1": os.getenv('AGENT1'),
    "AGENT2": os.getenv('AGENT2')
}
print(env_vars)
url_base = f"http://{host}:{port}/recetas"
recipe = Recipe()


def fetch_image():
    img_headers = {
        'User-Agent': env_vars["AGENT1"],
        "Authorization": env_vars["API_AUTH"],
    }
    img_parameters = {"query": recipe.name, "orientation": "square", "per_page": "1"}
    img_response = requests.get(url="https://api.pexels.com/v1/search", headers=img_headers, params=img_parameters)
    print("Status code", img_response.status_code)
    if img_response.status_code == 200:
        img_url = img_response.json()['photos'][0]['src']['original']
        img_extension = os.path.splitext(img_url.split("?")[0])[1]

        headers = {'User-Agent': 'AGENT1'}
        request = urllib.request.Request(img_url, headers=headers)
        with urllib.request.urlopen(request) as response, open(f"img{img_extension}", 'wb') as out_file:
            data = response.read()
            out_file.write(data)

        img1 = Image.open(f"img{img_extension}")

        img1.show()


def find():
    global recipe
    print(recipe)
    if recipe.name is not None and recipe.name != "":
        print(f"by name {url_base}/{recipe.name}")
        response = requests.get(f"{url_base}/{recipe.name}").json()
        if isinstance(response, dict):
            fetch_image()

    elif recipe.__str__() == "":
        print(f"base {url_base}")
        response = requests.get(f"{url_base}").json()
    else:
        print(f"with params {url_base}?{recipe}")
        response = requests.get(f"{url_base}?{recipe}").json()

    if not isinstance(response, dict):
        response = json.dumps(response, indent=1)

    print(response)


def add_param():
    print("¿Qué parámetro quieres añadir?")
    while True:
        print("1) Nombre\n2) Tipo\n3) Maximo tiempo\n4) Maximo calorias\n5) Maxima dificultad\n6) Minima "
              "Dificultad\n7) Ingredientes\n8) Salir")
        opcion = input()
        if opcion.isnumeric() and int(opcion) in range(1, 9):
            return int(opcion)
        else:
            print("Error, no es la opcion válida")


def elige_tipo():
    global recipe
    print("¿Elige el tipo?")
    liss = ["Desayuno", "Primer plato", "Segundo Plato", "Postre"]
    while True:
        print("\n1) Desayuno\n2) Primer plato \n3) Segundo Plato \n4) Postre \n5)Salir")
        opcion = input()
        if opcion.isnumeric() and int(opcion) in range(1, 6):
            recipe.type = liss[int(opcion) - 1]
            break
        else:
            print("Error, no es la opcion válida")


def application():
    global recipe
    while True:
        opcion = add_param()
        match opcion:
            case 1:
                recipe.name = input("Introduce el nombre: ")
            case 2:
                elige_tipo()
            case 3:
                recipe.max_t = input("Introduce el tiempo máximo")
            case 4:
                recipe.max_cal = input("Introduce la cantidad máxima de calorías")
            case 7:
                find()
                recipe = Recipe()
            case 8:
                break


if __name__ == '__main__':
    flask_process = Process(target=run)
    flask_process.start()
    time.sleep(1)

    application()

    flask_process.kill()
