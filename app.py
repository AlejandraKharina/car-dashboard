import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Verificar si el archivo existe
DATA_FILE = 'vehicles_us.csv'

if not os.path.exists(DATA_FILE):
    st.error(f"No se encontró el archivo '{DATA_FILE}'. Por favor, asegúrate de que el archivo está en el directorio raíz.")
else:
    # Cargar datos
    car_data = pd.read_csv(DATA_FILE)

    # Título de la aplicación
    st.title("Análisis de Anuncios de Venta de Coches")
    st.markdown(
        """
        Esta aplicación permite explorar datos de anuncios de venta de coches mediante visualizaciones interactivas.
        Selecciona las opciones a continuación para generar gráficos.
        """
    )

    # Menú desplegable para elegir el tipo de visualización
    visualization = st.selectbox(
        "Selecciona una visualización",
        ["Histograma", "Gráfico de Dispersión"]
    )

    # Opciones dinámicas según la visualización
    if visualization == "Histograma":
        column = st.selectbox("Selecciona la columna para el histograma", car_data.columns)
        st.write(f"Generando histograma para la columna: **{column}**")
        fig = px.histogram(car_data, x=column)
        st.plotly_chart(fig, use_container_width=True)

    elif visualization == "Gráfico de Dispersión":
        x_col = st.selectbox("Selecciona la columna para el eje X", car_data.columns)
        y_col = st.selectbox("Selecciona la columna para el eje Y", car_data.columns)
        st.write(f"Generando gráfico de dispersión: **{x_col}** vs **{y_col}**")
        fig = px.scatter(car_data, x=x_col, y=y_col)
        st.plotly_chart(fig, use_container_width=True)
