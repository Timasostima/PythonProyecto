import os
from pathlib import Path

from flask import Flask, jsonify, request, redirect, url_for
import json

app = Flask(__name__)
jsonn = Path(__file__).resolve().parent / "recetas.json"
api_host = '0.0.0.0'
api_port = 5000


@app.route('/recetas/<nombre>', methods=['GET'])
def info_receta(nombre):
    with open(jsonn, 'r') as file:
        js = json.load(file)
    for obj in js:
        if obj['nombre'].lower() == nombre.lower():
            return obj
    else:
        return redirect(f"/recetas?nombre={nombre}")


@app.route('/')
def hello():
    return redirect(f"{api_host}:{api_port}/recetas", code=200)


@app.route('/recetas', methods=["GET"])
def obtener_lista2():
    with open(jsonn, 'r') as file:
        js = json.load(file)

    nombre = request.args.get('nombre', type=str)
    tipo = request.args.get('tipo', type=str)
    max_cal = request.args.get('max_cal', type=int)
    max_t = request.args.get('max_t', type=int)
    max_diff = request.args.get('max_diff', type=int)
    min_diff = request.args.get('min_diff', type=int)
    ingr = request.args.get('ingr', type=str)

    if nombre:
        js = [receta_js for receta_js in js if nombre.lower() in receta_js['nombre'].lower()]
    if tipo:
        js = [receta_js for receta_js in js if receta_js['tipo'].count(tipo) != 0]
    if max_cal:
        js = [receta_js for receta_js in js if int(receta_js['calorias']) <= max_cal]
    if max_t:
        js = [receta_js for receta_js in js if int(receta_js['minutos']) <= max_t]
    if max_diff:
        js = [receta_js for receta_js in js if int(receta_js['dificultad']) <= max_diff]
    if min_diff:
        js = [receta_js for receta_js in js if int(receta_js['dificultad']) >= min_diff]
    if ingr:
        lis = []
        for receta in js:
            matches = set()
            query_list = ingr.split(',')
            for ing_query in query_list:
                for ing_receta in receta['ingredientes']:
                    if ing_query.lower() in ing_receta.lower():
                        matches.add(ing_query)
            hay_todos = len(matches) == len(query_list)
            if hay_todos:
                lis.append(receta)
        return jsonify(lis)

    return jsonify(js)


@app.route('/recetas', methods=["POST"])
def add_receta():
    if request.is_json:
        new_data = request.get_json()[0]

        with open(jsonn, 'r') as file:
            js = json.load(file)

        for receta in js:
            if receta['nombre'] == new_data['nombre']:
                return jsonify("Error, already exists")
        js.append(new_data)

        with open(jsonn, 'w') as file:
            json.dump(js, file)

        return jsonify(new_data)
    else:
        return jsonify("error, no body"), 400


def run():
    app.run(debug=True, host=api_host, port=api_port, use_reloader=False)


if __name__ == "__main__":
    app.run(debug=True, host=api_host, port=api_port)
