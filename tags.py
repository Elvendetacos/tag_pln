from flask import Flask, request, jsonify
import spacy

app = Flask(__name__)

nlp = spacy.load('es_core_news_md')

tags_entretenimiento = [
    "videojuegos",
    "cine",
    "teatro",
    "música",
    "televisión",
    "videojugador",
    "juegos de Mesa",
    "ajedrez",
    "cartas",
    "juegos de rol",
    "puzzles",
    "juegos de estrategia",
    "juegos de preguntas",
    "juegos de habilidad",
    "juegos de aventura"
]
tags_deporte = [
        "fútbol",
        "correr",
        "baloncesto",
        "natación",
        "nadar",
        "tenis",
        "ciclismo",
        "voleibol",
        "béisbol",
        "gimnasia",
        "yoga",
        "entrenar",
        "atletismo",
        "boxeo",
        "karate",
        "gimnasio",
        "gym"
      ]
groserias = ["puto", "puta", "pendejo", "pendeja", "idiota", "imbecil", "estupido", "estupida",
             "mierda", "cabron", "cabrona", "verga", "vergota", "vergudo", "culero", "culera",
             "pendejada", "joto", "mampo", "mampa", "perra", "chinga", "maricon",
             "pendejote", "putazo", "mamon", "mamona"]
tags_bienestar = [
    "meditación",
    "ejercicio",
    "nutrición",
    "mindfulness",
    "masajes",
    "spa",
    "fitness",
    "pilates",
    "relajación",
    "acupuntura"
]
tags_ciencia = [
    "astronomía",
    "biología",
    "química",
    "física",
    "geología",
    "paleontología",
    "ecología",
    "genética",
    "antropología",
    "botánica"
]
tags_viajes = [
    "turismo aventura",
    "turismo cultural",
    "cruceros",
    "ecoturismo",
    "senderismo",
    "camping",
    "tours gastronómicos",
    "viajes en tren",
    "viajes en caravana",
    "turismo de salud"
]
tags_literatura = [
    "poesía",
    "novela",
    "cuento",
    "ensayo",
    "literatura clásica",
    "fantasía",
    "ciencia ficción",
    "teatro",
    "biografía",
    "misterio"
]
tags_cocina = [
    "repostería",
    "cocina internacional",
    "panadería",
    "cocina saludable",
    "cocina vegana",
    "parrilladas",
    "cocina molecular",
    "decoración de pasteles",
    "cocina mediterránea",
    "cocina cexicana"
]
tags_tecnologia = [
    "programación",
    "robótica",
    "desarrollo web",
    "inteligencia artificial",
    "ciberseguridad",
    "big data",
    "iot",
    "realidad virtual",
    "desarrollo de apps",
    "blockchain",
    "telefonos",
    "computadoras",
    "tablets",
    "smartwatches",
    "tecnología"
]
tags_arte = [
    "pintura",
    "escultura",
    "dibujo",
    "cerámica",
    "fotografía",
    "fotógrafo",
    "grabado",
    "diseño gráfico",
    "arquitectura",
    "ilustración",
    "tejido",
    "bordado",
    "origami",
    "arte urbano",
    "arte digital",
    "costura",
]
tags_musica = [
    "guitarra",
    "piano",
    "canto",
    "batería",
    "violín",
    "saxofón",
    "flauta",
    "bajo",
    "ukelele",
    "trompeta",
    "trombón",
    "arpa",
    "mandolina",
    "acorde",
    "percusión"
    "dj",
    "productor musical",
    "compositor",
    "director de orquesta",
    "cantautor",
]

tag_dict = {
    'entretenimiento': [nlp(tag) for tag in tags_entretenimiento],
    'deporte': [nlp(tag) for tag in tags_deporte],
    'bienestar': [nlp(tag) for tag in tags_bienestar],
    'ciencia': [nlp(tag) for tag in tags_ciencia],
    'viajes': [nlp(tag) for tag in tags_viajes],
    'literatura': [nlp(tag) for tag in tags_literatura],
    'cocina': [nlp(tag) for tag in tags_cocina],
    'tecnologia': [nlp(tag) for tag in tags_tecnologia],
    'arte': [nlp(tag) for tag in tags_arte],
    'musica': [nlp(tag) for tag in tags_musica]
}

@app.route('/tags', methods=['POST'])
def get_tags():
    descripcion = request.json.get('description', '').lower()
    if not descripcion:
        return jsonify({'error': 'No se proporcionó descripción'}), 400

    doc = nlp(descripcion)

    tags = []
    threshold = 0.7

    for token in doc:
        for tag, word_list in tag_dict.items():
            for word in word_list:
                if token.has_vector and word.has_vector:
                    similarity = token.similarity(word)
                    if similarity > threshold:
                        tags.append(tag)
        if token.text.lower() in groserias:
            return jsonify({'error': 'No se permiten groserias'}), 400

    tags = list(set(tags))

    return jsonify({'description': descripcion, 'tags': tags})

if __name__ == '__main__':
    app.run(debug=True)