from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
RAW, PROC, RES = ROOT/"data/raw", ROOT/"data/processed", ROOT/"results"
REGIONES = ["PIURA", "TUMBES", "LAMBAYEQUE"]
INICIO, FIN = "2010-05", "2021-12"      # igual que Mills et al.
FIN_DESARROLLO = "2017-12"              # prueba: 2018-01 a 2021-12
UMBRALES_DIR = (50, 150)                # brote: DIR mensual por 100 000 hab.
