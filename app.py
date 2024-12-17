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
        Utiliza filtros y gráficos para analizar las tendencias.
        """
    )

    # Filtros Interactivos en la Barra Lateral
    st.sidebar.header("Filtros de Datos")
    min_price, max_price = st.sidebar.slider("Rango de Precio", 0, int(car_data["price"].max()), (0, 20000))
    min_odometer, max_odometer = st.sidebar.slider("Rango de Kilometraje", 0, int(car_data["odometer"].max()), (0, 100000))

    # Aplicar filtros
    filtered_data = car_data[
        (car_data["price"] >= min_price) & (car_data["price"] <= max_price) &
        (car_data["odometer"] >= min_odometer) & (car_data["odometer"] <= max_odometer)
    ]

    st.write("### Datos Filtrados")
    st.write(filtered_data)

    # Indicadores Clave (KPIs)
    st.write("### Indicadores Clave")
    total_cars = len(filtered_data)
    avg_price = filtered_data["price"].mean()
    avg_odometer = filtered_data["odometer"].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Vehículos", total_cars)
    col2.metric("Precio Promedio", f"${avg_price:,.2f}")
    col3.metric("Kilometraje Promedio", f"{avg_odometer:,.0f} km")

    # Menú desplegable para elegir el tipo de visualización
    visualization = st.selectbox(
        "Selecciona una visualización",
        ["Histograma", "Gráfico de Dispersión", "Tendencia de Precios"]
    )

    # Opciones dinámicas según la visualización
    if visualization == "Histograma":
        column = st.selectbox("Selecciona la columna para el histograma", filtered_data.columns)
        st.write(f"Generando histograma para la columna: **{column}**")
        fig = px.histogram(filtered_data, x=column)
        st.plotly_chart(fig, use_container_width=True)

        # Interpretación basada en la columna seleccionada
        st.write("### Interpretación:")
        if column == "price":
            st.info("Este histograma muestra la distribución de precios. Observa si hay una concentración de vehículos baratos o costosos.")
        elif column == "odometer":
            st.info("Este histograma muestra el kilometraje de los coches. Analiza si la mayoría tiene recorridos largos o cortos.")
        else:
            st.info(f"Estás viendo la distribución de **{column}**. Utiliza esto para entender cómo varían los valores en esta columna.")

    elif visualization == "Gráfico de Dispersión":
        x_col = st.selectbox("Selecciona la columna para el eje X", filtered_data.columns)
        y_col = st.selectbox("Selecciona la columna para el eje Y", filtered_data.columns)
        st.write(f"Generando gráfico de dispersión: **{x_col}** vs **{y_col}**")
        fig = px.scatter(filtered_data, x=x_col, y=y_col)
        st.plotly_chart(fig, use_container_width=True)

        # Interpretación basada en las columnas seleccionadas
        st.write("### Interpretación:")
        if x_col == "odometer" and y_col == "price":
            st.info("Este gráfico muestra la relación entre el kilometraje y el precio. Generalmente, los coches con mayor kilometraje tienen precios más bajos.")
        elif x_col == "model_year" and y_col == "price":
            st.info("Este gráfico muestra la relación entre el año del modelo y el precio. Es probable que los coches más nuevos tengan precios más altos.")
        else:
            st.info(f"Este gráfico muestra la relación entre **{x_col}** y **{y_col}**. Observa si existe alguna tendencia o patrón interesante.")

    elif visualization == "Tendencia de Precios":
        if "model_year" in filtered_data.columns:
            st.write("### Tendencia de Precios a lo Largo del Tiempo")
            avg_price_per_year = filtered_data.groupby("model_year")["price"].mean().reset_index()
            fig_line = px.line(avg_price_per_year, x="model_year", y="price", title="Precio Promedio por Año del Modelo")
            st.plotly_chart(fig_line)
        else:
            st.warning("No se encontró la columna 'model_year' en los datos. No se puede generar la tendencia de precios.")

    # Resumen Estadístico
    st.write("### Resumen Estadístico")
    st.write(filtered_data.describe())

    # Descargar Datos Filtrados
    st.write("### Descargar Datos Filtrados")
    csv = filtered_data.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Descargar CSV",
        data=csv,
        file_name="filtered_vehicles_data.csv",
        mime="text/csv"
    )
