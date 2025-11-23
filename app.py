import os

import pandas as pd
import plotly.express as px
import snowflake.connector
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Tendencias Mercado Libre",
    layout="wide"
)

st.title("Dashboard Mercado Libre ")
st.caption("Tendencias Avanzadas de Ingeniería de Software – Snowflake + Python")


@st.cache_resource
def get_connection():
    return snowflake.connector.connect(
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        user=os.environ["SNOWFLAKE_USER"],
        password=os.environ["SNOWFLAKE_PASSWORD"],
        warehouse=os.environ.get("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH"),
        database=os.environ["SNOWFLAKE_DATABASE"],
        schema=os.environ["SNOWFLAKE_SCHEMA"],
    )


@st.cache_data
def run_query(sql: str) -> pd.DataFrame:
    conn = get_connection()
    df = pd.read_sql(sql, conn)
    df.columns = [c.lower() for c in df.columns]
    return df


# ======================================
# PREGUNTA 1  -> Q1
# ======================================
st.subheader("1. ¿Cuál es la marca de ventiladores más vendidos en Colombia?")

df_q1 = run_query("""
    SELECT brand, COUNT(*) AS total
    FROM Q1
    GROUP BY brand
    ORDER BY total DESC
""")

if df_q1.empty:
    st.warning("La tabla Q1 está vacía o no existen datos.")
else:
    fig = px.bar(
        df_q1,
        x="brand",
        y="total",
        title="Ventas por marca de ventiladores",
        text="total",
        color_discrete_sequence=["#084063"],
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(xaxis_title="Marca", yaxis_title="Cantidad de productos")
    st.plotly_chart(fig, use_container_width=True)

    marca_top = df_q1.iloc[0]["brand"]
    st.success(f"La marca de ventiladores más vendida en Colombia es **{marca_top}**.")

st.divider()
# ======================================
# PREGUNTA 2  -> Q2
# ======================================
st.subheader("2. ¿Cuál es el top de modelos más vendidos de Air Fryer?")

df_q2 = run_query("""
    SELECT name
    FROM Q2
""")

if df_q2.empty:
    st.warning("La tabla Q2 está vacía o no existen datos de Air Fryer.")
else:
    
    df_q2 = df_q2[df_q2["name"].notna()]
    df_q2 = df_q2[df_q2["name"].str.strip().str.lower() != "name"]

    df_q2 = df_q2.reset_index(drop=True)
    df_q2["ranking"] = range(1, len(df_q2) + 1)

    df_display = df_q2[["ranking", "name"]].rename(
        columns={
            "ranking": "Ranking", 
            "name": "Nombre completo",
        }
    )

    def highlight_top(row):
        rank = row["Ranking"]
        if rank == 1:
            color = "background-color: #fec749"
        elif rank == 2:
            color = "background-color: #8abe50"
        elif rank == 3:
            color = "background-color: #00b0bc"
        else:
            color = ""
        return [color] * len(row)

    st.write(
        "La siguiente tabla muestra el **ranking de modelos de Air Fryer**, "
        "manteniendo el orden original de la consulta. "
        "Los tres primeros lugares se resaltan con colores."
    )

    st.dataframe(
        df_display.style.apply(highlight_top, axis=1),
        use_container_width=True,
    )

    top1 = df_q2.iloc[0]["name"]
    st.success(f"El modelo de Air Fryer más vendido es **{top1}**.")


# ======================================
# Cargamos Q3567 una sola vez (P3, P5, P6, P7)
# ======================================
df_q3567 = run_query("""
    SELECT name, highlight_score, sale_fee_amount, valor_relativo
    FROM Q3567
""")

# ======================================
# PREGUNTA 3  -> Q3567
# ======================================
st.subheader("3. ¿Cuáles son los “niveles” con mayor peso relativo? (Q3567)")

if df_q3567.empty:
    st.warning("La tabla Q3567 está vacía o no existen datos.")
else:
    df3 = df_q3567.copy()
    df3 = df3[df3["valor_relativo"].notna() & (df3["valor_relativo"] > 0)]

    
    df3 = df3.sort_values("valor_relativo", ascending=False)

    
    ordered_colors = [
        "#3e873c",     
        "#fec749",     
        "#ec6825",      
        "#d0228e","#97439e",
        "#00b0bc", "#0087bc",
    ]

    unique_levels = df3["name"].unique() 
    color_map = {}
    for i, level in enumerate(unique_levels):
        if i < len(ordered_colors):
            color_map[level] = ordered_colors[i]
        else:
            color_map[level] = ordered_colors[-1]

    fig = px.pie(
        df3,
        names="name",
        values="valor_relativo",
        title="Distribución por nivel (usando valor_relativo)",
        color="name",
        color_discrete_map=color_map,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(fig, use_container_width=True)

st.divider()


# ======================================
# PREGUNTA 4  -> Q4
# ======================================
st.subheader("4. ¿Cuál es la marca predilecta en el conjunto de electrodomésticos analizados? (Q4)")

df_q4 = run_query("""
    SELECT brand
    FROM Q4
""")

if df_q4.empty:
    st.warning("La tabla Q4 está vacía o no existen datos.")
else:
    df4 = (
        df_q4.groupby("brand")
        .size()
        .reset_index(name="total")
        .sort_values("total", ascending=False)
    )

    fig = px.bar(
        df4,
        x="brand",
        y="total",
        title="Preferencia de marcas en los electrodomésticos de Q4",
        text="total",
        color_discrete_sequence=["#084063"],
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(xaxis_title="Marca", yaxis_title="Cantidad de productos")
    st.plotly_chart(fig, use_container_width=True)

    marca_top_q4 = df4.iloc[0]["brand"]
    st.success(
        f"La marca con mayor presencia en el conjunto específico de electrodomésticos "
        f"analizados (Q4) es **{marca_top_q4}**."
    )

st.divider()

# ======================================
# PREGUNTA 5  -> Q3567
# ======================================
st.subheader("5. ¿Qué tipo de exposición brinda la mejor relación entre visibilidad y costo? (Q3567)")

if df_q3567.empty:
    st.warning("La tabla Q3567 está vacía o no existen datos de exposiciones.")
else:
    df5 = df_q3567.copy()
    df5 = df5[df5["sale_fee_amount"] > 0]
    df5["relacion"] = df5["highlight_score"] / df5["sale_fee_amount"]

    mejor = df5.loc[df5["relacion"].idxmax()]

    fig = px.scatter(
        df5,
        x="sale_fee_amount",
        y="highlight_score",
        color="name",
        title="Relación visibilidad (highlight_score) vs costo (sale_fee_amount)",
        hover_data=["valor_relativo", "relacion"],
        color_discrete_sequence=["#00b0bc", "#0087bc", "#005d8e", "#084063"],
    )
    fig.update_layout(
        xaxis_title="Costo (sale_fee_amount)",
        yaxis_title="Visibilidad (highlight_score)",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.success(
        f"La mejor relación visibilidad/costo la ofrece el tipo de exposición "
        f"**{mejor['name']}**."
    )

st.divider()

# ======================================
# PREGUNTA 6  -> Q3567
# ======================================
st.subheader("6. ¿Qué tipo de publicación requiere mayor inversión para obtener una exposición alta? (Q3567)")

if df_q3567.empty:
    st.warning("La tabla Q3567 está vacía o no existen datos de exposiciones.")
else:
    df6 = df_q3567.copy()
    umbral = df6["highlight_score"].mean()
    df_altas = df6[df6["highlight_score"] >= umbral]

    if df_altas.empty:
        st.info("No hay registros con exposición considerada alta.")
    else:
        mas_caro = df_altas.loc[df_altas["sale_fee_amount"].idxmax()]

        fig = px.scatter(
            df6,
            x="sale_fee_amount",
            y="highlight_score",
            color="name",
            title="Inversión vs exposición por tipo de publicación",
            color_discrete_sequence=["#00b0bc", "#0087bc", "#005d8e", "#084063"],
        )
        fig.add_annotation(
            x=mas_caro["sale_fee_amount"],
            y=mas_caro["highlight_score"],
            text=f"Mayor inversión (alta exposición): {mas_caro['name']}",
            showarrow=True,
        )
        fig.update_layout(xaxis_title="Costo", yaxis_title="Visibilidad")
        st.plotly_chart(fig, use_container_width=True)

        st.warning(
            f"El tipo de publicación que requiere **mayor inversión** para lograr "
            f"una exposición alta es **{mas_caro['name']}**."
        )

st.divider()

# ======================================
# PREGUNTA 7  -> Q3567
# ======================================
st.subheader("7. ¿Qué tipo de publicación ofrece la mayor visibilidad general dentro de Mercado Libre? (Q3567)")

if df_q3567.empty:
    st.warning("La tabla Q3567 está vacía o no existen datos de exposiciones.")
else:
    df7 = df_q3567.copy()
    df_g = df7.groupby("name", as_index=False)["highlight_score"].mean()
    df_g = df_g.sort_values("highlight_score", ascending=False)

    fig = px.bar(
        df_g,
        x="name",
        y="highlight_score",
        title="Visibilidad promedio por tipo de publicación",
        text="highlight_score",
        color_discrete_sequence=["#084063"],
    )
    fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")
    fig.update_layout(
        xaxis_title="Tipo de publicación",
        yaxis_title="Visibilidad promedio",
    )
    st.plotly_chart(fig, use_container_width=True)

    mejor = df_g.iloc[0]
    st.success(
        f"El tipo de publicación con **mayor visibilidad general** es "
        f"**{mejor['name']}** (score promedio {mejor['highlight_score']:.2f})."
    )

st.divider()
# ======================================
# PREGUNTA 8  -> Q8
# ======================================
st.subheader(
    "8. ¿Cuáles son los 3 productos que más se suelen comprar "
    "relacionados al producto más vendido de electrodomésticos? (Q8)"
)

df_q8 = run_query("""
    SELECT ranking, name, brand, model
    FROM Q8
    ORDER BY ranking ASC
    LIMIT 3
""")

if df_q8.empty:
    st.warning("La tabla Q8 está vacía o no existen datos.")
else:
    
    df_q8["label"] = df_q8.apply(
        lambda row: f"{row['brand']} {row['model']}"
        if pd.notnull(row["model"]) and str(row["model"]).strip() != ""
        else row["brand"],
        axis=1,
    )

    max_rank = df_q8["ranking"].max()
    df_q8["peso"] = max_rank + 1 - df_q8["ranking"]

    ordered_colors = [
        "#3e873c",                
        "#fec749",
        "#d0228e", "#97439e",    
    ]

    df8_sorted = df_q8.sort_values("peso", ascending=False)
    labels_order = df8_sorted["label"].tolist()

    color_map = {}
    for i, lab in enumerate(labels_order):
        if i < len(ordered_colors):
            color_map[lab] = ordered_colors[i]
        else:
            color_map[lab] = ordered_colors[-1]

    fig = px.pie(
        df_q8,
        names="label",
        values="peso",
        title="Top 3 productos relacionados (ponderados por ranking)",
        color="label",
        color_discrete_map=color_map,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(fig, use_container_width=True)

    st.table(df_q8[["ranking", "label", "name", "brand", "model"]].set_index("ranking"))