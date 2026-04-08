# Pump 303 Monitoring Dashboard - Las Bambas

Streamlit dashboard and ETL pipeline for operational monitoring, anomaly detection, and failure analysis of HNS pump 303.

## Features

- Data quality assessment
- Operational performance monitoring
- Temperature and humidity tracking
- Anomaly and event detection

## Data Processing

The dataset is cleaned and normalized using a custom ETL pipeline:
- Invalid values removed (Bad Input, No Data, etc.)
- Sensor normalization
- Feature engineering (load, temperature aggregation, flags)

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
