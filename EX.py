import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="EDA y Dashboard Interactivo", layout="wide")

st.markdown(
    """
    <style>
        /* Fondo degradado para la página principal */
        body {
            background: rgb(5,172,153);
            background: linear-gradient(0deg, rgba(5,172,153,1) 0%, rgba(10,113,114,1) 100%);
            background-size: cover;
            color: white;
        }

        /* Fondo degradado para la barra lateral */
        [data-testid="stSidebar"] {
            background: rgb(5,172,153);
            background: linear-gradient(0deg, rgba(5,172,153,1) 0%, rgba(10,113,114,1) 100%);
            background-size: cover;
            color: white;
        }
        
    </style>
    """, unsafe_allow_html=True
)


st.title("Exploración de Datos y Dashboard Interactivo para Perfiles Financieros")

df = pd.read_excel("df/economia_financiera.xlsx")


colores = ['#29a19c', '#5af4ac', '#28cbb8', '#56f7a7', '#5ef286']


total_encuestados = df["ID"].nunique()
total_femenino = df[df["Genero"] == "Femenino"]["ID"].nunique()
total_masculino = df[df["Genero"] == "Masculino"]["ID"].nunique()

icono_total = "df/7.jpg"  
icono_femenino = "df/5.jpg"  
icono_masculino = "df/6.jpg"  


st.subheader("Análisis de Valores Faltantes en la base de datos")
missing_values = df.isnull().sum()
st.write(missing_values[missing_values > 0])



st.subheader("Estadísticas de Encuesta")

col1, col2, col3 = st.columns(3)

with col1:
    st.image(icono_total, width=50)  
    st.metric(label="Total Encuestados", value=total_encuestados)

with col2:
    st.image(icono_femenino, width=50)  
    st.metric(label="Total Sexo Femenino", value=total_femenino)

with col3:
    st.image(icono_masculino, width=50)  
    st.metric(label="Total Sexo Masculino", value=total_masculino)







with st.expander("Distribución de todas las variables "):
    st.subheader("Distribución de Variables")
    for column in df.select_dtypes(include=['object']).columns:
        st.write(f"Distribución de {column}")
        fig = px.histogram(df, x=column, color=column, color_discrete_sequence=colores)
        st.plotly_chart(fig, key=f"hist_{column}")
        
st.sidebar.image("df/image.gif", use_container_width=True)  


st.sidebar.header("Filtros")
genero = st.sidebar.multiselect("Seleccione Género", options=df["Genero"].unique())
rango_edad = st.sidebar.multiselect("Seleccione Rango de Edad", options=df["Rango_Edad"].unique())
nivel_educacion = st.sidebar.multiselect("Seleccione Nivel de Educación", options=df["Nivel_educacion"].unique())
nivel_socioeconomico = st.sidebar.multiselect("Seleccione Nivel Socioeconómico", options=df["nivel_socieconomico"].unique())
situacion_laboral = st.sidebar.multiselect("Seleccione Situación Laboral", options=df["Situacion_Laboral"].unique())
distrito = st.sidebar.multiselect("Seleccione Distrito", options=df["Distrito"].unique())

df_filtered = df.copy()
if genero:
    df_filtered = df_filtered[df_filtered["Genero"].isin(genero)]
if rango_edad:
    df_filtered = df_filtered[df_filtered["Rango_Edad"].isin(rango_edad)]
if nivel_educacion:
    df_filtered = df_filtered[df_filtered["Nivel_educacion"].isin(nivel_educacion)]
if nivel_socioeconomico:
    df_filtered = df_filtered[df_filtered["nivel_socieconomico"].isin(nivel_socioeconomico)]
if situacion_laboral:
    df_filtered = df_filtered[df_filtered["Situacion_Laboral"].isin(situacion_laboral)]
if distrito:
    df_filtered = df_filtered[df_filtered["Distrito"].isin(distrito)]


st.subheader("Distribución Jerárquica por Distrito y Variables Seleccionadas")
fig = px.treemap(
    df_filtered,
    path=["Distrito", "Nivel_educacion", "Situacion_Laboral", "nivel_socieconomico"],  
    values="ID", 
    title="Distribución Jerárquica por Distrito",
    color="nivel_socieconomico",  
    color_discrete_sequence=colores
)
st.plotly_chart(fig, use_container_width=True)


# Graficos
df_grouped = df_filtered.groupby(['Nivel_educacion', 'Situacion_Laboral']).size().reset_index(name='Count')

st.subheader("Distribución de Productos Financieros por Nivel de Educación y Situación Laboral")
fig_area = px.area(
    df_grouped,
    x="Nivel_educacion",     
    y="Count",               
    color="Situacion_Laboral", 
    title="Distribución de Productos Financieros por Nivel de Educación y Situación Laboral",
    labels={"Count": "Cantidad", "Nivel_educacion": "Nivel de Educación"},
    color_discrete_sequence=colores 
)
st.plotly_chart(fig_area, use_container_width=True)



st.subheader("Distribución por Género")
fig = px.bar(df_filtered, x="Genero", color="Genero", color_discrete_sequence=colores)
st.plotly_chart(fig, key="grafico_genero")


st.subheader("Distribución de Niveles Educativos")
fig = px.pie(df_filtered, names="Nivel_educacion", hole=0.3, color_discrete_sequence=colores)
st.plotly_chart(fig, key="grafico_niveles_educativos")


st.subheader("Situación Laboral por Nivel Socioeconómico")
fig = px.bar(df_filtered, x="Situacion_Laboral", color="nivel_socieconomico", barmode="stack", color_discrete_sequence=colores)
st.plotly_chart(fig, key="grafico_situacion_laboral")


st.subheader("Distribución de Manejo de Productos Financieros por Rango de Edad")
fig = px.violin(
    df_filtered,
    x="Rango_Edad",
    y="manejo_productos_financieros",
    title="Distribución de Manejo de Productos Financieros por Rango de Edad",
    labels={"Rango_Edad": "Rango de Edad", "manejo_productos_financieros": "Manejo de Productos Financieros"},
    box=True, 
    points="all",  
    color_discrete_sequence=colores
)
st.plotly_chart(fig, use_container_width=True)


st.subheader("Uso de Productos Financieros por Nivel Socioeconómico")
fig = px.bar(df_filtered, x="nivel_socieconomico", y="manejo_productos_financieros", color="Situacion_Laboral", barmode="stack", color_discrete_sequence=colores)
st.plotly_chart(fig, key="grafico_uso_productos")


st.header("Preguntas de Análisis")
st.markdown("""1. **¿Cuál es la distribución de los niveles educativos entre los géneros?**""")
fig = px.histogram(df_filtered, x="Nivel_educacion", color="Genero", barmode="group", color_discrete_sequence=colores)
st.plotly_chart(fig, key="pregunta_nivel_educacion")

st.markdown("""2. **¿Quién es el principal responsable de las decisiones financieras en cada rango de edad?**""")
fig = px.histogram(df_filtered, x="Rango_Edad", y="manejo_productos_financieros", color="Genero", barmode="stack", color_discrete_sequence=colores)
st.plotly_chart(fig, key="pregunta_decisiones_financieras")

# Crear una tabla de frecuencia para Rango de Edad y Manejo de Productos Financieros
df_counts = df_filtered.groupby(['Rango_Edad', 'manejo_productos_financieros']).size().reset_index(name='Count')

# Gráfico de Mapa de Calor
st.subheader("Frecuencia de Combinaciones de Rango de Edad y Manejo de Productos Financieros")
fig = px.density_heatmap(
    df_counts, 
    x="Rango_Edad", 
    y="manejo_productos_financieros", 
    z="Count",
    color_continuous_scale="YlGnBu",
    title="Mapa de Calor de Frecuencia entre Rango de Edad y Manejo de Productos Financieros",
    labels={"Count": "Frecuencia"}
)
st.plotly_chart(fig, use_container_width=True)

# Gráfico de Barras Apiladas: Distribución de Manejo de Productos Financieros por Rango de Edad
st.subheader("Distribución de Manejo de Productos Financieros por Rango de Edad")
fig = px.bar(
    df_filtered,
    x="Rango_Edad",
    color="manejo_productos_financieros",
    title="Distribución de Manejo de Productos Financieros por Rango de Edad",
    labels={"manejo_productos_financieros": "Manejo de Productos Financieros", "Rango_Edad": "Rango de Edad"},
    color_discrete_sequence=colores,
    barmode="stack"
)
st.plotly_chart(fig, use_container_width=True)



st.subheader("Proporción de Manejo de Productos Financieros por Rango de Edad")
fig = px.sunburst(
    df_filtered,
    path=["Rango_Edad", "manejo_productos_financieros"],
    title="Proporción de Manejo de Productos Financieros por Rango de Edad",
    color="manejo_productos_financieros",
    color_discrete_sequence=colores
)
st.plotly_chart(fig, use_container_width=True)


st.markdown("""3. **¿Qué nivel socioeconómico predomina en la muestra?**""")
fig = px.histogram(df_filtered, x="nivel_socieconomico", color="nivel_socieconomico", color_discrete_sequence=colores)
st.plotly_chart(fig, key="pregunta_nivel_socioeconomico")

st.markdown("""5. **¿Qué productos financieros son más comunes en cada nivel socioeconómico?**""")


productos_financieros = ['tarjeta_debito', 'depositos_cuentas_ahorro', 'prestamos_personales', 'tarjeta_credito', 'compras_tarjeta_credito', 'ninguno']
df_productos = df.melt(id_vars=["nivel_socieconomico"], value_vars=productos_financieros, var_name="Producto_Financiero", value_name="Uso")
df_productos = df_productos[df_productos["Uso"] == "Si"].groupby(["nivel_socieconomico", "Producto_Financiero"]).size().reset_index(name="Count")




st.subheader("Productos Financieros más Comunes en Cada Nivel Socioeconómico")
fig = px.bar(
    df_productos,
    x="nivel_socieconomico",
    y="Count",
    color="Producto_Financiero",
    title="Distribución de Productos Financieros por Nivel Socioeconómico",
    labels={"nivel_socieconomico": "Nivel Socioeconómico", "Count": "Frecuencia de Uso"},
    color_discrete_sequence=colores, 
    barmode="stack"
)
st.plotly_chart(fig, use_container_width=True)


st.markdown("""6. **¿Cómo se relaciona la situación laboral con el nivel socioeconómico?**""")
fig = px.histogram(df_filtered, x="Situacion_Laboral", color="nivel_socieconomico", barmode="stack", color_discrete_sequence=colores)
st.plotly_chart(fig, key="pregunta_situacion_laboral")
