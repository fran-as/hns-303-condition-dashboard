import streamlit as st
import pandas as pd

st.title("🚨 Anomalías y Eventos")

df = pd.read_csv("data/processed/pump_303_clean_streamlit.csv", parse_dates=["timestamp"])

events = df[
    (df["flag_bearing_alarm"] == 1) |
    (df["flag_motor_alarm"] == 1) |
    (df["flag_moisture_alarm"] == 1) |
    (df["flag_current_high"] == 1)
]

st.subheader("Eventos detectados")

st.dataframe(events.head(100))

st.subheader("Cantidad de eventos")

st.metric("Total eventos", len(events))

st.subheader("Timeline eventos")

st.line_chart(events.set_index("timestamp").count(axis=1))
