"""Descarga índices climáticos a data/raw/. Requiere internet.
ONI (NOAA) es el que usa el modelo. ICEN (IGP) es opcional: si falla, se descarga a mano."""
import requests
from config import RAW

FUENTES = {
    "oni.txt": "https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt",  # NOAA (usado por el modelo)
}
OPCIONALES = {
    "icen.txt": "http://met.igp.gob.pe/datos/icen.txt",  # IGP: la URL cambió, puede dar 404
}

for nombre, url in {**FUENTES, **OPCIONALES}.items():
    try:
        r = requests.get(url, timeout=60); r.raise_for_status()
        (RAW / nombre).write_text(r.text); print("OK", nombre, len(r.text), "bytes")
    except requests.RequestException as e:
        if nombre in FUENTES: raise
        print(f"AVISO: {nombre} no se pudo descargar ({e}). No es necesario para el modelo básico.")