from flask import Flask, render_template, request ,jsonify
from main import Main
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['POST'])
def inicio():  # put application's code here
    sentence=request.json['sentencia']
    print(sentence)

    # Iniciar el controlador logico
    main=Main(sentence)

    # main retorna una lista de resultados de los 3 analisis
    results=main.get_results()
    banderas=main.get_bands()
    sugerencia=main.get_suggerence()
    print(results[0],banderas[0])
    print(results[1],banderas[1])
    print(results[2],banderas[2])
    print(results[3],banderas[3])

    # Crear diccionarios para crear el JSON
    tokens_dict = {
        "correctTokens": banderas[0],
        "responseTokens": results[0]
    }

    sintaxis = {
        "correctSintaxis": banderas[1],
        "responseSintaxis": results[1]
    }

    semantica = {
        "correctSemantica": banderas[2],
        "responseSemantica": results[2]
    }

    traduccion = {
        "correctTraduccion": banderas[3],
        "responseTraduccion": results[3]
    }

    # Uniendo todos los diccionarios
    diccionario_final = {
        "tokens": tokens_dict,
        "sintaxis": sintaxis,
        "semantica": semantica,
        "traduccion": traduccion,
        "sugerencia":sugerencia
    }

    sugerencia = {
        "response": sugerencia
    }

    # Convertir el diccionario a formato JSON
    json_string = json.dumps(diccionario_final)

    # Imprimir el resultado
    print(json_string)



    # Convertir la lista a JSON
    # var_json = json.dumps(results)
    # var_json = jsonify(results)

    # Retornar el JSON
    return json_string


if __name__ == '__main__':
    app.run()
