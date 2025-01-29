# Pipeline Turismo - Peru

Soy Gian Cruz.

Pipeline de datos que analiza el flujo de turistas internacionales al Peru. Procesa estadisticas de arribo por pais de origen, calcula estacionalidad, participacion de mercado y mide el impacto del COVID-19 en el sector. Los datos provienen del portal estadistico del MINCETUR.

Peru recibio 4.4 millones de turistas internacionales en 2019. En 2020 ese numero cayo a menos de 900 mil. Este proyecto mide la caida, la recuperacion y los cambios en la composicion de mercados emisores.

## Que hace

- Carga datos de arribo de turistas desde CSVs (exportaciones MINCETUR)
- Limpieza: normaliza paises, parsea numeros con comas, elimina duplicados
- Calcula crecimiento interanual (YoY) por pais
- Genera indice de estacionalidad mensual
- Calcula participacion de mercado por pais/anio
- Mide impacto COVID: caida 2020 vs promedio 2018-2019
- Genera indice de recuperacion post-COVID (base 2019)
- Carga a warehouse SQLite con esquema estrella

## Instalacion

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Uso

```bash
# Colocar CSVs de arribo en data/raw/
python -m src.pipeline

# Filtrar por paises
python -m src.pipeline --countries Chile "Estados Unidos"
```

## Tests

```bash
pytest tests/ -v
```

## Stack

- Python 3.10+
- pandas + numpy
- SQLite
- pytest

## Estructura

```
pipeline-turismo-peru/
├── src/
│   ├── config/settings.py
│   ├── extract/data_loader.py
│   ├── transform/
│   │   ├── cleaner.py
│   │   └── enricher.py
│   ├── quality/validators.py
│   ├── load/exporter.py
│   ├── utils/logger.py
│   └── pipeline.py
├── tests/
│   ├── fixtures/arribos_sample.csv
│   ├── test_loader.py
│   ├── test_cleaner.py
│   ├── test_enricher.py
│   ├── test_validators.py
│   └── test_exporter.py
└── requirements.txt
```

---

## What it does

Data pipeline analyzing international tourist arrivals to Peru. Processes arrival statistics by country of origin, calculates seasonality, market share, and measures COVID-19 impact on tourism. Data comes from MINCETUR statistical portal.

Peru received 4.4 million international tourists in 2019. In 2020 that number dropped to less than 900k. This project measures the decline, recovery, and changes in source market composition.

---

## Fuentes de datos

| Fuente | Descripcion | Enlace |
|--------|-------------|--------|
| MINCETUR - Estadisticas de Turismo | Arribo mensual de turistas internacionales por pais de origen | [https://www.mincetur.gob.pe/turismo/estadisticas-generales/](https://www.mincetur.gob.pe/turismo/estadisticas-generales/) |
| DATATUR MINCETUR | Sistema de informacion estadistica de turismo | [https://dataturismo.mincetur.gob.pe/](https://dataturismo.mincetur.gob.pe/) |
| PROMPERU - Perfil del Turista Extranjero | Caracteristicas del turista extranjero que visita Peru | [https://www.promperu.gob.pe/TurismoIn/sitio/PerfTuristaExt](https://www.promperu.gob.pe/TurismoIn/sitio/PerfTuristaExt) |
