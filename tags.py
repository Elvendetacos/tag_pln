from flask import Flask, request, jsonify
import spacy

app = Flask(__name__)

nlp = spacy.load('es_core_news_md')

groserias = ["pendejo", "pendeja", "pendejos", "pendejas",
             "cabron", "cabrona", "cabrones", "cabronas",
             "pinche", "pinches",
             "culero", "culera", "culeros", "culeras",
             "hijo de puta", "hija de puta", "hijos de puta", "hijas de puta",
             "chingón", "chingona", "chingones", "chingonas",
             "perro", "perra", "perros", "perras",
             "baboso", "babosa", "babosos", "babosas",
             "maldito", "maldita", "malditos", "malditas",
             "cabronazo", "cabronaza", "cabronazos", "cabronazas",
             "mierda", "mierdas",
             "puto", "puta", "putos", "putas",
             "pinche cabrón", "pinche cabrona", "pinches cabrones", "pinches cabronas",
             "mamón", "mamona", "mamones", "mamonas",
             "chingada", "chingadas",
             "estúpido", "estúpida", "estúpidos", "estúpidas",
             "pito", "pitos",
             "naco", "naca", "nacos", "nacas",
             "culerito", "culerita", "culeritos", "culeritas",
             "pinche pendejo", "pinche pendeja", "pinches pendejos", "pinches pendejas",
             "cabrón de mierda", "cabrona de mierda", "cabrones de mierda", "cabronas de mierda",
             "pendejo de mierda", "pendeja de mierda", "pendejos de mierda", "pendejas de mierda",
             "maricón", "maricona", "maricones", "mariconas",
             "cojudo", "cojuda", "cojudos", "cojudas",
             "chingadazo", "chingadaza", "chingadazos", "chingadazas",
             "mampo", "mampa", "mampos", "mampas",
             ]


@app.route('/tags', methods=['POST'])
def get_tags():
    descripcion = request.json.get('description', '').lower()
    if not descripcion:
        return jsonify({'error': 'No se proporcionó descripción'}), 400

    doc = nlp(descripcion)

    for token in doc:
        if token.text.lower() in groserias:
            return jsonify({'error': 'No se permiten groserias'}), 400

    return jsonify({'success': 'No se encontraron groserias'}), 200


if __name__ == '__main__':
    app.run(debug=True)
