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

## Fuentes de datos

| Fuente | Descripción | Enlace |
|--------|-------------|--------|
| MINCETUR - Estadísticas de Turismo | Arribo mensual de turistas internacionales por país de origen | [https://www.mincetur.gob.pe/turismo/estadisticas-generales/](https://www.mincetur.gob.pe/turismo/estadisticas-generales/) |
| DATATUR MINCETUR | Sistema de información estadística de turismo | [https://dataturismo.mincetur.gob.pe/](https://dataturismo.mincetur.gob.pe/) |
| PROMPERÚ - Perfil del Turista Extranjero | Características del turista extranjero que visita Perú | [https://www.promperu.gob.pe/TurismoIn/sitio/PerfTuristaExt](https://www.promperu.gob.pe/TurismoIn/sitio/PerfTuristaExt) |

## Visualizaciones

Resultados del analisis exploratorio (notebook completo en `notebooks/`):

![Arribos mensuales con impacto COVID](docs/images/grafico_01.png)

![Participacion de mercado por pais emisor](docs/images/grafico_02.png)

![Indice de estacionalidad mensual](docs/images/grafico_03.png)

## Licencia

MIT

---

# Tourism Pipeline - Peru

Did you know Peru received 4.4 million international tourists in 2019, but in 2020 that number plummeted to less than 900,000? Tourism represented 3.9% of GDP and generated over 1.3 million jobs. The pandemic didn't just cut visitor flow, it completely changed the composition of source markets.

I'm Gian Cruz. I built this pipeline to analyze tourist arrival data published by Peru's MINCETUR. It calculates seasonality indices, market share by country, measures the real COVID-19 impact, and generates a post-pandemic recovery index comparing each period against the 2019 baseline.

## Quick start

```bash
git clone https://github.com/giansocial/pipeline-turismo-peru.git
cd pipeline-turismo-peru
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python -m src.pipeline
```

## Data sources

| Source | Description | Link |
|--------|-------------|------|
| MINCETUR - Tourism Statistics | Monthly international tourist arrivals by country | [https://www.mincetur.gob.pe/turismo/estadisticas-generales/](https://www.mincetur.gob.pe/turismo/estadisticas-generales/) |
| DATATUR MINCETUR | Tourism statistical information system | [https://dataturismo.mincetur.gob.pe/](https://dataturismo.mincetur.gob.pe/) |

## License

MIT
