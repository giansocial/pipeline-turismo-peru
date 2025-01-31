# Pipeline Turismo - Perú

¿Sabías que Perú recibió 4.4 millones de turistas internacionales en 2019, pero en 2020 esa cifra se desplomó a menos de 900 mil? El turismo representaba el 3.9% del PBI y generaba más de 1.3 millones de empleos. La pandemia no solo cortó el flujo de visitantes, cambió por completo la composición de mercados emisores.

Soy Gian Cruz. Construí este pipeline para analizar los datos de arribo de turistas publicados por el MINCETUR. Calcula estacionalidad, participación de mercado por país, mide el impacto real del COVID-19 y genera un índice de recuperación post-pandemia comparando cada período contra la línea base de 2019.

## Qué hace

- Carga datos de arribo de turistas desde CSVs (exportaciones MINCETUR)
- Limpieza: normaliza países, parsea números con comas, elimina duplicados
- Calcula crecimiento interanual (YoY) por país
- Genera índice de estacionalidad mensual
- Calcula participación de mercado por país/año
- Mide impacto COVID: caída 2020 vs promedio 2018-2019
- Genera índice de recuperación post-COVID (base 2019)
- Carga a warehouse SQLite con esquema estrella

## Instalación

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

| Fuente | Descripción | Enlace |
|--------|-------------|--------|
| MINCETUR - Estadísticas de Turismo | Arribo mensual de turistas internacionales por país de origen | [https://www.mincetur.gob.pe/turismo/estadisticas-generales/](https://www.mincetur.gob.pe/turismo/estadisticas-generales/) |
| DATATUR MINCETUR | Sistema de información estadística de turismo | [https://dataturismo.mincetur.gob.pe/](https://dataturismo.mincetur.gob.pe/) |
| PROMPERÚ - Perfil del Turista Extranjero | Características del turista extranjero que visita Perú | [https://www.promperu.gob.pe/TurismoIn/sitio/PerfTuristaExt](https://www.promperu.gob.pe/TurismoIn/sitio/PerfTuristaExt) |
