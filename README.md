# UADE - Calculadora de Tiempos de Llegada

Esta app web permite subir un archivo Excel con alumnos, sus coordenadas y sede asignada, y calcula el tiempo estimado de llegada a cada sede de UADE en distintos medios de transporte.

## ¿Cómo funciona?

1. Subís un archivo `.xlsx` con las columnas: `Latitud`, `Longitud`, `Sede más cercana`
2. El sistema consulta la API de Google Maps para calcular tiempos en auto, transporte público, bicicleta y caminando.
3. Devuelve:
   - Una tabla con los resultados
   - Descarga de Excel con toda la info
   - Detección de posibles llegadas tarde

## Cómo publicar esta app en la web

1. Subí estos archivos a un nuevo repositorio en GitHub
2. Entrá en https://streamlit.io/cloud
3. Hacé clic en 'New App'
4. Elegí tu repositorio y seleccioná `app.py` como archivo principal
5. ¡Listo! Tu app estará online.
