"""Lista de casos -> serie mensual por provincia (casos, población, DIR, log) + ONI si existe."""
import numpy as np, pandas as pd
from config import *
d = pd.read_csv(RAW/"casos_dengue_2010_2021.csv", encoding="utf-8-sig")
d = d[d["Departamnento"].isin(REGIONES) & d["Provincia"].notna() & d["Semana"].between(1, 52)]
# mes = lunes de la semana ISO (criterio del repo original)
d["fecha"] = pd.to_datetime(d["Ano"].astype(str) + "-W" + d["Semana"].astype(int).astype(str).str.zfill(2) + "-1", format="%G-W%V-%u")
d["mes"] = d["fecha"].dt.to_period("M")
d["provincia"] = d["Departamnento"] + "|" + d["Provincia"]
casos = d.groupby(["provincia", "mes"]).size().unstack(0)
casos = casos.reindex(pd.period_range(INICIO, FIN, freq="M")).fillna(0)

# población: interpolación lineal entre 1993, 2007, 2017 y 2022
p = pd.read_csv(RAW/"poblacion_provincias.csv", encoding="utf-8")
p.columns = ["nombre", "tipo", "c1993", "c2007", "c2017", "c2022"]
quitar = str.maketrans("ÑÁÉÍÓÚ", "NAEIOU")
reg, pob_ref = None, {}
for _, r in p.iterrows():
    if r.tipo == "Region": reg = r.nombre.upper()
    elif r.tipo == "Province" and reg in REGIONES:
        pob_ref[f"{reg}|{r.nombre.upper()}".translate(quitar)] = [float(str(r[c]).replace(",", "")) for c in ["c1993","c2007","c2017","c2022"]]
casos.columns = [c.translate(quitar) for c in casos.columns]
fechas_ref = pd.to_datetime(["1993-07-11", "2007-10-21", "2017-10-22", "2022-06-30"]).astype("int64")
t = casos.index.to_timestamp().astype("int64")
pob = pd.DataFrame({c: np.interp(t, fechas_ref, pob_ref[c]) for c in casos.columns}, index=casos.index)

largo = (casos.stack().rename("casos").to_frame().join(pob.stack().rename("poblacion")).reset_index())
largo.columns = ["mes", "provincia", "casos", "poblacion"]
largo["dir_100k"] = largo.casos / largo.poblacion * 1e5
largo["log_casos"] = np.log1p(largo.casos)

# covariable opcional: ONI (si se ejecutó 01_descarga.py), rezago de 2 meses
oni_f = RAW/"oni.txt"
if oni_f.exists():
    o = pd.read_csv(oni_f, sep=r"\s+")           # columnas: SEAS YR TOTAL ANOM
    o["mes"] = pd.PeriodIndex(pd.to_datetime(dict(year=o.YR, month=o.groupby("YR").cumcount() + 1, day=1)), freq="M")
    o = o.set_index("mes")["ANOM"].rename("oni")
    largo = largo.merge(o.shift(2).rename("oni_lag2"), left_on="mes", right_index=True, how="left")
largo["mes"] = largo["mes"].astype(str)
largo.to_csv(PROC/"serie_mensual_provincias.csv", index=False)
print(largo.provincia.nunique(), "provincias |", largo.mes.nunique(), "meses |", len(largo), "filas")
