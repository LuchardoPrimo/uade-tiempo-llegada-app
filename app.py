# Requisitos: pip install streamlit pandas openpyxl requests
import streamlit as st
import pandas as pd
import requests
import time
from io import BytesIO

# API de Google
API_KEY = "AIzaSyCIwdFcOKCUwEFc51JnUwqIKhMYSTQ6EHI"

# Coordenadas sedes UADE
SEDES = {
    "Monserrat": "Lima 775, Buenos Aires, Argentina",
    "Recoleta": "Libertad 1340, Buenos Aires, Argentina",
    "Belgrano": "11 de Septiembre 1900, Buenos Aires, Argentina"
}

# Función principal
st.title("Calculadora de Tiempos de Llegada a UADE")
file = st.file_uploader("Subí el archivo Excel con los alumnos", type=["xlsx"])

if file:
    df = pd.read_excel(file)
    st.success("Archivo cargado correctamente")

    if 'Latitud' in df.columns and 'Longitud' in df.columns:
        tiempo_viaje = []
        umbral_tarde = 45

        with st.spinner("Calculando tiempos de viaje..."):
            for index, row in df.iterrows():
                origen = f"{row['Latitud']},{row['Longitud']}"
                fila = {
                    "Legajo": row.get("Legajo", index),
                    "Sede asignada": row.get("Sede más cercana", "No asignada")
                }
                posibles_tardanzas = []

                for sede, destino in SEDES.items():
                    for modo in ["driving", "transit", "walking", "bicycling"]:
                        url = (
                            f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origen}"
                            f"&destinations={destino}&mode={modo}&departure_time=now&key={API_KEY}"
                        )
                        r = requests.get(url)
                        data = r.json()
                        try:
                            duracion = data["rows"][0]["elements"][0]["duration"]["text"]
                            duracion_min = int(data["rows"][0]["elements"][0]["duration"]["value"]) // 60
                            fila[f"{modo}_{sede}"] = duracion
                            if duracion_min > umbral_tarde:
                                posibles_tardanzas.append(f"{modo}_{sede}: {duracion_min} min")
                        except:
                            fila[f"{modo}_{sede}"] = "Error"
                        time.sleep(1.1)

                fila["Posible llegada tarde"] = "; ".join(posibles_tardanzas) if posibles_tardanzas else "No"
                tiempo_viaje.append(fila)

        resultado = pd.DataFrame(tiempo_viaje)
        st.success("¡Listo!")
        st.dataframe(resultado)

        # Descargar Excel
        buffer = BytesIO()
        resultado.to_excel(buffer, index=False)
        buffer.seek(0)
        st.download_button("Descargar resultados en Excel", data=buffer, file_name="Resultados_UADE_Tiempos.xlsx")

    else:
        st.error("El archivo debe contener columnas 'Latitud', 'Longitud' y 'Sede más cercana'")
