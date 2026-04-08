import streamlit as st
import pandas as pd

st.title("🌡️ Temperaturas y Humedad")

df = pd.read_csv("data/processed/pump_303_clean_streamlit.csv", parse_dates=["timestamp"])

st.subheader("Rodamientos")

st.line_chart(df.set_index("timestamp")["bearing_temp_max_c"])

st.metric(
    "Máx temperatura rodamientos",
    round(df["bearing_temp_max_c"].max(), 2)
)

st.subheader("Motor")

st.line_chart(df.set_index("timestamp")["motor_temp_max_c"])

st.metric(
    "Máx temperatura motor",
    round(df["motor_temp_max_c"].max(), 2)
)

st.subheader("Humedad")

st.metric("Eventos alarma", int(df["flag_moisture_alarm"].sum()))
st.metric("Eventos trip", int(df["flag_moisture_trip"].sum()))

st.line_chart(df.set_index("timestamp")["flag_moisture_alarm"])
