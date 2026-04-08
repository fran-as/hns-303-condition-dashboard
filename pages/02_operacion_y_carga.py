import streamlit as st
import pandas as pd

st.title("⚙️ Operación y Carga")

df = pd.read_csv("data/processed/pump_303_clean_streamlit.csv", parse_dates=["timestamp"])

st.subheader("Corriente vs Nominal")

st.line_chart(df.set_index("timestamp")["pump_303_current_a"])

st.metric(
    "Corriente máxima (A)",
    round(df["pump_303_current_a"].max(), 2)
)

st.metric(
    "% Corriente nominal máxima",
    round(df["current_pct_nominal"].max(), 2)
)

st.subheader("Velocidad")

st.line_chart(df.set_index("timestamp")["pump_303_speed_rpm"])

st.subheader("Operación")

st.metric(
    "Tiempo en operación (%)",
    round(df["pump_running_flag"].mean() * 100, 2)
)
