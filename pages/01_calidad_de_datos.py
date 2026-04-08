import streamlit as st
import pandas as pd

st.title("📊 Calidad de Datos")

df = pd.read_csv("data/processed/pump_303_clean_streamlit.csv", parse_dates=["timestamp"])

st.subheader("Cobertura de datos (%)")

coverage = df.notna().mean() * 100
st.dataframe(coverage.sort_values(ascending=False))

st.subheader("Valores faltantes por variable")

missing = df.isna().sum()
st.dataframe(missing.sort_values(ascending=False))

st.subheader("Registros con datos críticos faltantes")

st.metric(
    label="Registros con variables críticas faltantes",
    value=int(df["flag_any_critical_missing"].sum())
)

st.line_chart(df.set_index("timestamp")["flag_any_critical_missing"])
