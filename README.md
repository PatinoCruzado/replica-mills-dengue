# Réplica básica de Mills et al. (2025): pronóstico de dengue en Piura, Tumbes y Lambayeque

Réplica reducida de *Multi-model approach to understand and predict past and future dengue epidemic dynamics* (R. Soc. Open Sci. 12(11):241870, doi:10.1098/rsos.241870; preprint medRxiv 2024.10.18.24315690). Código original: https://github.com/cathalmills/peru_dengue_province

## Flujo
`datos crudos → preprocesamiento → modelos → evaluación`

| Paso | Script | Qué hace |
|---|---|---|
| 1 | `src/01_descarga.py` | Descarga ONI (NOAA) e ICEN (IGP) a `data/raw/` (opcional) |
| 2 | `src/02_preprocesamiento.py` | Casos semanales → mensuales por provincia, población, DIR, log(casos+1) |
| 3 | `src/03_modelos.py` | Baseline (random walk), SARIMA y SARIMAX con ONI (si existe) |
| 4 | `src/04_evaluacion.py` | R², RMSE, brote DIR ≥ 50/150; tabla vs Mills |

## Datos (`data/raw/`)
- `casos_dengue_2010_2021.csv`: lista de casos de dengue, CDC Perú (https://www.dge.gob.pe/salasituacional). Copia del archivo publicado en el repo de Mills.
- `poblacion_provincias.csv`: población por provincia, INEI.
- `oni.txt`, `icen.txt`: generados por el paso 1.

## Ejecutar
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cd src
python 01_descarga.py          # opcional (ONI/ICEN)
python 02_preprocesamiento.py
python 03_modelos.py
python 04_evaluacion.py
```
## Diseño
14 provincias, may-2010 a dic-2021. Desarrollo 2010–2017, prueba 2018–2021, pronóstico a 1 mes, reajuste mensual. Orden SARIMA elegido por AIC con datos de desarrollo.

## Limitaciones (no replicado)
Bayes-Climate (INLA), TCN, TimeGPT, ensambles, WorldClim/SPI-6, WIS/cuantiles. La sensibilidad/especificidad es por provincia-mes; Mills evalúa la detección del primer brote.

## Resultados
Ver `results/comparacion_con_mills.csv`.

## Clonar y ejecutar

```bash
git clone https://github.com/PatinoCruzado/replica-mills-dengue
cd replica-mills-dengue
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cd src
python 01_descarga.py          # opcional (ONI/ICEN)
python 02_preprocesamiento.py
python 03_modelos.py
python 04_evaluacion.py
```
