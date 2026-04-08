import streamlit as st

st.set_page_config(
    page_title="Pump 303 Dashboard",
    layout="wide"
)

st.title("🔧 Pump 303 - Las Bambas Monitoring Dashboard")

st.markdown("""
Bienvenido al dashboard de monitoreo de la bomba 303.

### Módulos disponibles:
- 📊 Calidad de datos
- ⚙️ Operación y carga
- 🌡️ Temperaturas y humedad
- 🚨 Anomalías / eventos

Utiliza el menú lateral para navegar.
""")
