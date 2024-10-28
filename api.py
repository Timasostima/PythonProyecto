from flask import Flask, jsonify, request
import json

app = Flask(__name__)


@app.route('/recetas/<nombre>', methods=['GET'])
def info_receta(nombre):
    with open('recetas.json', 'r') as file:
        js = json.load(file)
    for obj in js:
        if obj['nombre'].lower() == nombre.lower():
            print(obj)
            return obj
    return "no hay"


@app.route('/recetas', methods=["GET"])
def obtener_lista2():
    with open('recetas.json', 'r') as file:
        js = json.load(file)

    tipo = request.args.get('tipo', type=str)
    max_cal = request.args.get('max_cal', type=int)
    max_t = request.args.get('max_t', type=int)
    max_diff = request.args.get('max_diff', type=int)
    min_diff = request.args.get('min_diff', type=int)
    ingr = request.args.get('ingr', type=str)

    if tipo:
        js = [item for item in js if item['tipo'].count(tipo) != 0]
    if max_cal:
        js = [item for item in js if int(item['calorias']) <= max_cal]
    if max_t:
        js = [item for item in js if int(item['minutos']) <= max_t]
    if max_diff:
        js = [item for item in js if int(item['dificultad']) <= max_diff]
    if min_diff:
        js = [item for item in js if int(item['dificultad']) >= min_diff]
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

        with open('recetas.json', 'r') as file:
            js = json.load(file)

        for receta in js:
            if receta['nombre'] == new_data['nombre']:
                return jsonify("Error, already exists")
        js.append(new_data)

        with open('recetas.json', 'w') as file:
            json.dump(js, file)

        return jsonify(new_data)
    else:
        return jsonify("error, no body"), 400


if __name__ == "__main__":
    app.run(debug=True)
