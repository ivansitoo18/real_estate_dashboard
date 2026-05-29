import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Real Estate Dashboard RD",
    layout="wide"
)

st.title("🏠 Real Estate Intelligence Dashboard RD")

@st.cache_data
def load_data():
    return pd.read_csv("data/raw/properties.csv")

df = load_data()

st.sidebar.header("Filtros")

sectores = st.sidebar.multiselect(
    "Sector",
    options=df["sector"].unique(),
    default=df["sector"].unique()
)

habitaciones = st.sidebar.slider(
    "Habitaciones",
    min_value=int(df["habitaciones"].min()),
    max_value=int(df["habitaciones"].max()),
    value=(
        int(df["habitaciones"].min()),
        int(df["habitaciones"].max())
    )
)

filtered_df = df[
    (df["sector"].isin(sectores)) &
    (df["habitaciones"].between(
        habitaciones[0],
        habitaciones[1]
    ))
]

total_propiedades = len(filtered_df)
precio_promedio = round(filtered_df["precio_usd"].mean(), 2)
precio_maximo = round(filtered_df["precio_usd"].max(), 2)

col1, col2, col3 = st.columns(3)

col1.metric("Total Propiedades", total_propiedades)
col2.metric("Precio Promedio USD", f"${precio_promedio:,.0f}")
col3.metric("Precio Máximo USD", f"${precio_maximo:,.0f}")

st.divider()

grafico_sector = px.bar(
    filtered_df.groupby("sector")["precio_usd"]
    .mean()
    .reset_index(),
    x="sector",
    y="precio_usd",
    title="Precio promedio por sector"
)

st.plotly_chart(
    grafico_sector,
    use_container_width=True
)

grafico_scatter = px.scatter(
    filtered_df,
    x="metros",
    y="precio_usd",
    color="sector",
    size="habitaciones",
    hover_data=["tipo"],
    title="Relación entre metros y precio"
)

st.plotly_chart(
    grafico_scatter,
    use_container_width=True
)

st.subheader("Tabla de propiedades")

st.dataframe(filtered_df)

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "Descargar CSV",
    data=csv,
    file_name="propiedades_filtradas.csv",
    mime="text/csv"
)