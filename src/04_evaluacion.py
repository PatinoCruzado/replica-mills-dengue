"""R², RMSE (log(casos+1)) y clasificación de brotes (DIR>=50/150) + tabla comparativa con Mills."""
import json, numpy as np, pandas as pd
from sklearn.metrics import r2_score, mean_squared_error, roc_auc_score
from config import *
r = pd.read_csv(RES/"predicciones.csv")
modelos = [m for m in ["baseline", "sarima", "sarimax_oni"] if m in r.columns]
out = {}
for m in modelos:
    r[f"dir_{m}"] = np.expm1(r[m]) / r.poblacion * 1e5
    o = {"R2": r2_score(r.obs, r[m]), "RMSE": float(np.sqrt(mean_squared_error(r.obs, r[m])))}
    for u in UMBRALES_DIR:
        yt, yp = r.dir_obs >= u, r[f"dir_{m}"] >= u
        o[f"sens_{u}"] = float((yt & yp).sum() / yt.sum()); o[f"spec_{u}"] = float((~yt & ~yp).sum() / (~yt).sum())
        o[f"AUC_{u}"] = float(roc_auc_score(yt, r[f"dir_{m}"])); o[f"n_brotes_{u}"] = int(yt.sum())
    out[m] = o
json.dump(out, open(RES/"metricas.json", "w"), indent=1)
t = pd.DataFrame(out).T.round(3)
t.loc["Mills baseline (preprint)", ["R2", "sens_50", "spec_50", "AUC_50"]] = [0.74, 0.909, 0.450, 0.68]
t.loc["Mills SARIMA (preprint)", ["R2", "sens_50", "spec_50", "AUC_50"]] = [0.73, 0.636, 0.961, 0.80]
t.to_csv(RES/"comparacion_con_mills.csv"); print(t.to_string())
