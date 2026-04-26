
import joblib
import pandas as pd
import os

# Ruta compatible con Render y con ejecución local
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "catboost_model_a.pkl")
model = joblib.load(MODEL_PATH)

def predict_popularity(duration_ms, danceability, energy, loudness,
                       speechiness, acousticness, instrumentalness,
                       liveness, valence, tempo, explicit, key,
                       mode, time_signature, artists, album_name,
                       track_name, track_genre):

    obs = pd.DataFrame([{
        "duration_ms":      float(duration_ms),
        "danceability":     float(danceability),
        "energy":           float(energy),
        "loudness":         float(loudness),
        "speechiness":      float(speechiness),
        "acousticness":     float(acousticness),
        "instrumentalness": float(instrumentalness),
        "liveness":         float(liveness),
        "valence":          float(valence),
        "tempo":            float(tempo),
        "explicit":         int(explicit),
        "key":              int(key),
        "mode":             int(mode),
        "time_signature":   int(time_signature),
        "artists":          str(artists),
        "album_name":       str(album_name),
        "track_name":       str(track_name),
        "track_genre":      str(track_genre)
    }])

    prediction = model.predict(obs)
    return round(float(prediction[0]), 2)
