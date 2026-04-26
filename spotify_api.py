
from flask import Flask
from flask_restx import Api, Resource, fields
from spotify_model import predict_popularity

app = Flask(__name__)

# Definición API Flask
api = Api(
    app,
    version="1.0",
    title="Spotify Popularity Prediction API",
    description="API para predecir la popularidad de canciones de Spotify")

ns = api.namespace("predict",
     description="Popularity Predictor")

# Definición de los parámetros de entrada
parser = ns.parser()
parser.add_argument("duration_ms",      type=float, required=True, help="Duración en milisegundos",              location="args")
parser.add_argument("danceability",     type=float, required=True, help="Bailabilidad (0.0 - 1.0)",              location="args")
parser.add_argument("energy",           type=float, required=True, help="Energía (0.0 - 1.0)",                   location="args")
parser.add_argument("loudness",         type=float, required=True, help="Sonoridad en dB",                       location="args")
parser.add_argument("speechiness",      type=float, required=True, help="Palabras habladas (0.0 - 1.0)",         location="args")
parser.add_argument("acousticness",     type=float, required=True, help="Acústica (0.0 - 1.0)",                  location="args")
parser.add_argument("instrumentalness", type=float, required=True, help="Instrumentalidad (0.0 - 1.0)",          location="args")
parser.add_argument("liveness",         type=float, required=True, help="Presencia de audiencia (0.0 - 1.0)",    location="args")
parser.add_argument("valence",          type=float, required=True, help="Positividad musical (0.0 - 1.0)",       location="args")
parser.add_argument("tempo",            type=float, required=True, help="Tempo en BPM",                          location="args")
parser.add_argument("explicit",         type=int,   required=True, help="Contenido explícito (0 o 1)",           location="args")
parser.add_argument("key",              type=int,   required=True, help="Tonalidad (0-11)",                      location="args")
parser.add_argument("mode",             type=int,   required=True, help="Modalidad (0=menor, 1=mayor)",          location="args")
parser.add_argument("time_signature",   type=int,   required=True, help="Firma de tiempo (3-7)",                 location="args")
parser.add_argument("artists",          type=str,   required=True, help="Nombre del artista",                    location="args")
parser.add_argument("album_name",       type=str,   required=True, help="Nombre del álbum",                      location="args")
parser.add_argument("track_name",       type=str,   required=True, help="Nombre de la canción",                  location="args")
parser.add_argument("track_genre",      type=str,   required=True, help="Género musical",                        location="args")

# Definición del formato de respuesta
resource_fields = api.model("Resource", {
    "popularity_prediction": fields.Float,
})

# Definición del endpoint
@ns.route("/")
class SpotifyApi(Resource):

    @ns.doc(parser=parser)
    @ns.marshal_with(resource_fields)
    def get(self):
        args = parser.parse_args()
        prediction = predict_popularity(
            duration_ms      = args["duration_ms"],
            danceability     = args["danceability"],
            energy           = args["energy"],
            loudness         = args["loudness"],
            speechiness      = args["speechiness"],
            acousticness     = args["acousticness"],
            instrumentalness = args["instrumentalness"],
            liveness         = args["liveness"],
            valence          = args["valence"],
            tempo            = args["tempo"],
            explicit         = args["explicit"],
            key              = args["key"],
            mode             = args["mode"],
            time_signature   = args["time_signature"],
            artists          = args["artists"],
            album_name       = args["album_name"],
            track_name       = args["track_name"],
            track_genre      = args["track_genre"]
        )
        return {"popularity_prediction": prediction}, 200

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, host="0.0.0.0", port=5000)
