"""Pronóstico a 1 mes con reajuste mensual: baseline (random walk), SARIMA y, si hay ONI, SARIMAX."""
import warnings, numpy as np, pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
from config import *
warnings.filterwarnings("ignore")
df = pd.read_csv(PROC/"serie_mensual_provincias.csv")
usa_oni = "oni_lag2" in df.columns and df.oni_lag2.notna().all()
ORDENES = [((1,0,0),(1,0,0,12)), ((1,0,1),(1,0,0,12)), ((2,0,0),(0,0,0,0)), ((1,0,1),(0,0,0,0)), ((1,1,1),(0,0,0,0))]
salida = []
for prov, g in df.groupby("provincia"):
    g = g.reset_index(drop=True); y = g.log_casos.values
    ex = g[["oni_lag2"]].values if usa_oni else None
    t0 = int((g.mes > FIN_DESARROLLO).values.argmax())
    mejor, aic = None, np.inf          # orden por AIC solo con datos de desarrollo
    for o, so in ORDENES:
        try:
            m = SARIMAX(y[:t0], order=o, seasonal_order=so).fit(disp=False)
            if m.aic < aic: mejor, aic = (o, so), m.aic
        except Exception: pass
    for t in range(t0, len(g)):
        fila = dict(provincia=prov, mes=g.mes[t], obs=y[t], poblacion=g.poblacion[t], dir_obs=g.dir_100k[t], baseline=y[t-1])
        try: fila["sarima"] = max(SARIMAX(y[:t], order=mejor[0], seasonal_order=mejor[1]).fit(disp=False).forecast(1)[0], 0)
        except Exception: fila["sarima"] = y[t-1]
        if usa_oni:
            try: fila["sarimax_oni"] = max(SARIMAX(y[:t], exog=ex[:t], order=mejor[0], seasonal_order=mejor[1]).fit(disp=False).forecast(1, exog=ex[t:t+1])[0], 0)
            except Exception: fila["sarimax_oni"] = y[t-1]
        salida.append(fila)
pd.DataFrame(salida).to_csv(RES/"predicciones.csv", index=False); print("predicciones:", len(salida))
