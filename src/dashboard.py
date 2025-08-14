import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Data Reading

df = pd.read_excel("../data/edited_dataset.xlsx")

stores = sorted(df.id_loja.unique().tolist())
vehicles = sorted(df.categoria_veiculo.unique().tolist())
minimum_date = df["data_inicio_locacao"].min().date()
maximum_date = df["data_inicio_locacao"].max().date()

# Menu

st.sidebar.title("Filtros")

selec_stores = st.sidebar.multiselect(
    "Selecione as lojas:",
    options=stores,
    placeholder="Escolha uma (ou mais) opção",
)
selec_vehicles = st.sidebar.multiselect(
    "Selecione a categoria do veículo:",
    options=vehicles,
    placeholder="Escolha uma (ou mais) opção",
)
selec_date = st.sidebar.date_input(
    "Selecione o intervalo de datas:",
    value=(minimum_date, maximum_date),
    min_value=minimum_date,
    max_value=maximum_date,
    help="Essa é a data do início da locação.",
)

if not selec_stores:
    selec_stores = stores
if not selec_vehicles:
    selec_vehicles = vehicles

# Data and Filters

df_filtered = df.copy()

df_filtered = df_filtered[df_filtered["id_loja"].isin(selec_stores)]
df_filtered = df_filtered[df_filtered["categoria_veiculo"].isin(selec_vehicles)]

if len(selec_date) == 2:
    start_date, end_date = selec_date
    df_filtered = df_filtered[
        (df_filtered["data_inicio_locacao"].dt.date >= start_date)
        & (df_filtered["data_inicio_locacao"].dt.date <= end_date)
    ]

# Exhibition

st.title(f"Análise Exploratória de Locações")

### Plot 1
st.subheader("Estatísticas das Lojas")

df_filtered.rename(columns={"id_loja": "Lojas"}, inplace=True)

statistics_stores = df_filtered.groupby("Lojas").agg(
    id_contrato_count=("id_contrato", "count"),
    diaria_media=("diaria_media", "mean"),
    valor_total_min=("valor_total_locacao", "min"),
    valor_total_medio=("valor_total_locacao", "mean"),
    valor_total_max=("valor_total_locacao", "max"),
    valor_total=("valor_total_locacao", "sum"),
    duracao_min=("duracao_locacao", "min"),
    duracao_media=("duracao_locacao", "mean"),
    duracao_max=("duracao_locacao", "max"),
    antecedencia_min=("dias_antecedencia", "min"),
    antecedencia_media=("dias_antecedencia", "mean"),
    antecedencia_max=("dias_antecedencia", "max"),
)

for col in [
    "diaria_media",
    "valor_total_min",
    "valor_total_medio",
    "valor_total_max",
    "valor_total",
    "duracao_media",
    "antecedencia_media",
]:
    statistics_stores[col] = statistics_stores[col].round(0)

total_geral = {
    "id_contrato_count": statistics_stores["id_contrato_count"].sum(),
    "diaria_media": statistics_stores["diaria_media"].mean().round(0),
    "valor_total_min": statistics_stores["valor_total_min"].min(),
    "valor_total_medio": statistics_stores["valor_total_medio"].mean().round(0),
    "valor_total_max": statistics_stores["valor_total_max"].max(),
    "valor_total": statistics_stores["valor_total"].sum(),
    "duracao_min": statistics_stores["duracao_min"].min(),
    "duracao_media": statistics_stores["duracao_media"].mean().round(0),
    "duracao_max": statistics_stores["duracao_max"].max(),
    "antecedencia_min": statistics_stores["antecedencia_min"].min(),
    "antecedencia_media": statistics_stores["antecedencia_media"].mean().round(0),
    "antecedencia_max": statistics_stores["antecedencia_max"].max(),
}

statistics_stores.loc["Total Geral"] = total_geral

statistics_stores.rename(
    columns={
        "id_contrato_count": "Quantidade de Contratos",
        "diaria_media": "Diária Média",
        "valor_total_min": "Valor Total Mínimo",
        "valor_total_medio": "Valor Total Médio",
        "valor_total_max": "Valor Total Máximo",
        "valor_total": "Montante Total",
        "duracao_min": "Duração Mínima",
        "duracao_media": "Duração Média",
        "duracao_max": "Duração Máxima",
        "antecedencia_min": "Antecedência Mínima",
        "antecedencia_media": "Antecedência Média",
        "antecedencia_max": "Antecedência Máxima",
    },
    inplace=True,
)

st.dataframe(statistics_stores)

### Plot 2
statistics_stores_filtered = statistics_stores.drop("Total Geral", errors="ignore")

fig = px.scatter(
    statistics_stores_filtered,
    x="Quantidade de Contratos",
    y="Montante Total",
    text=statistics_stores_filtered.index,
    title="Correlação: Quantidade de Contratos vs. Montante Total",
    labels={"Montante Total": "Montante Total (R$)"},
    trendline="ols",
)
fig.update_traces(textposition="top center")

st.plotly_chart(fig, use_container_width=True)

### Plot 3
st.subheader("Estatísticas das Categorias de Veículos")

df_filtered.rename(columns={"categoria_veiculo": "Categoria de Veículo"}, inplace=True)

statistics_vehicles = df_filtered.groupby("Categoria de Veículo").agg(
    id_contrato_count=("id_contrato", "count"),
    diaria_media=("diaria_media", "mean"),
    valor_total_min=("valor_total_locacao", "min"),
    valor_total_medio=("valor_total_locacao", "mean"),
    valor_total_max=("valor_total_locacao", "max"),
    valor_total=("valor_total_locacao", "sum"),
    duracao_min=("duracao_locacao", "min"),
    duracao_media=("duracao_locacao", "mean"),
    duracao_max=("duracao_locacao", "max"),
    antecedencia_min=("dias_antecedencia", "min"),
    antecedencia_media=("dias_antecedencia", "mean"),
    antecedencia_max=("dias_antecedencia", "max"),
)

for col in [
    "diaria_media",
    "valor_total_min",
    "valor_total_medio",
    "valor_total_max",
    "valor_total",
    "duracao_media",
    "antecedencia_media",
]:
    statistics_vehicles[col] = statistics_vehicles[col].round(0)

total_geral = {
    "id_contrato_count": statistics_vehicles["id_contrato_count"].sum(),
    "diaria_media": statistics_vehicles["diaria_media"].mean().round(0),
    "valor_total_min": statistics_vehicles["valor_total_min"].min(),
    "valor_total_medio": statistics_vehicles["valor_total_medio"].mean().round(0),
    "valor_total_max": statistics_vehicles["valor_total_max"].max(),
    "valor_total": statistics_vehicles["valor_total"].sum(),
    "duracao_min": statistics_vehicles["duracao_min"].min(),
    "duracao_media": statistics_vehicles["duracao_media"].mean().round(0),
    "duracao_max": statistics_vehicles["duracao_max"].max(),
    "antecedencia_min": statistics_vehicles["antecedencia_min"].min(),
    "antecedencia_media": statistics_vehicles["antecedencia_media"].mean().round(0),
    "antecedencia_max": statistics_vehicles["antecedencia_max"].max(),
}

statistics_vehicles.loc["Total Geral"] = total_geral

statistics_vehicles.rename(
    columns={
        "id_contrato_count": "Quantidade de Contratos",
        "diaria_media": "Diária Média",
        "valor_total_min": "Valor Total Mínimo",
        "valor_total_medio": "Valor Total Médio",
        "valor_total_max": "Valor Total Máximo",
        "valor_total": "Montante Total",
        "duracao_min": "Duração Mínima",
        "duracao_media": "Duração Média",
        "duracao_max": "Duração Máxima",
        "antecedencia_min": "Antecedência Mínima",
        "antecedencia_media": "Antecedência Média",
        "antecedencia_max": "Antecedência Máxima",
    },
    inplace=True,
)

st.dataframe(statistics_vehicles)

### Plot 4
st.subheader("Quantidade de Contratos")

df_ma_frequency = (
    df_filtered.groupby(df_filtered["data_inicio_locacao"].dt.date)
    .agg(total_contratos=("id_contrato", "count"))
    .reset_index()
)

df_ma_frequency.rename(
    columns={"data_inicio_locacao": "Data", "total_contratos": "Contratos"},
    inplace=True,
)
df_ma_frequency["Data"] = pd.to_datetime(df_ma_frequency["Data"])
df_ma_frequency.set_index("Data", inplace=True)

df_ma_frequency["Suavização 7 dias"] = (
    df_ma_frequency["Contratos"].rolling(window="7D").mean()
)
df_ma_frequency["Suavização 30 dias"] = (
    df_ma_frequency["Contratos"].rolling(window="30D").mean()
)
df_ma_frequency["Suavização 90 dias"] = (
    df_ma_frequency["Contratos"].rolling(window="90D").mean()
)

fig = px.line(
    df_ma_frequency,
    y=["Contratos", "Suavização 7 dias", "Suavização 30 dias", "Suavização 90 dias"],
    labels={"value": "Quantidade de Contratos", "Data": "Data"},
)
fig.update_traces(
    line=dict(width=1, color="rgba(192, 192, 192, 0.25)"),
    selector=dict(name="Contratos"),
)
fig.update_traces(
    line=dict(width=2, color="rgba(135, 206, 235, 0.75)"),
    selector=dict(name="Suavização 7 dias"),
)
fig.update_traces(
    line=dict(width=3, color="rgba(65, 105, 225, 1)"),
    selector=dict(name="Suavização 30 dias"),
)
fig.update_traces(
    line=dict(width=3, color="rgba(0, 0, 128, 1)"),
    selector=dict(name="Suavização 90 dias"),
)
fig.update_layout(legend_title_text="")

st.plotly_chart(fig, use_container_width=True)

### Plot 5
st.subheader("Diária Média")

df_ma_daily = (
    df_filtered.groupby(df_filtered["data_inicio_locacao"].dt.date)
    .agg(diaria_media=("diaria_media", "mean"))
    .reset_index()
)

df_ma_daily.rename(
    columns={"data_inicio_locacao": "Data", "diaria_media": "Diária Média"},
    inplace=True,
)
df_ma_daily["Data"] = pd.to_datetime(df_ma_daily["Data"])
df_ma_daily.set_index("Data", inplace=True)

df_ma_daily["Suavização 7 dias"] = (
    df_ma_daily["Diária Média"].rolling(window="7D").mean()
)
df_ma_daily["Suavização 30 dias"] = (
    df_ma_daily["Diária Média"].rolling(window="30D").mean()
)
df_ma_daily["Suavização 90 dias"] = (
    df_ma_daily["Diária Média"].rolling(window="90D").mean()
)

fig = px.line(
    df_ma_daily,
    y=["Diária Média", "Suavização 7 dias", "Suavização 30 dias", "Suavização 90 dias"],
    labels={"value": "Diária Média", "Data": "Data"},
)
fig.update_traces(
    line=dict(width=1, color="rgba(192, 192, 192, 0.25)"),
    selector=dict(name="Diária Média"),
)
fig.update_traces(
    line=dict(width=2, color="rgba(135, 206, 235, 0.75)"),
    selector=dict(name="Suavização 7 dias"),
)
fig.update_traces(
    line=dict(width=3, color="rgba(65, 105, 225, 1)"),
    selector=dict(name="Suavização 30 dias"),
)
fig.update_traces(
    line=dict(width=3, color="rgba(0, 0, 128, 1)"),
    selector=dict(name="Suavização 90 dias"),
)
fig.update_layout(legend_title_text="")

st.plotly_chart(fig, use_container_width=True)
