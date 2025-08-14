import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from statsmodels.tsa.seasonal import MSTL

# Constants and Config

st.set_page_config(
    page_title="Histórico de Locações",
    page_icon="📈",
    layout="wide",
)

AGGREGATION_DICT = {
    "id_contrato_count": ("id_contrato", "count"),
    "diaria_media": ("diaria_media", "mean"),
    "valor_total_min": ("valor_total_locacao", "min"),
    "valor_total_medio": ("valor_total_locacao", "mean"),
    "valor_total_max": ("valor_total_locacao", "max"),
    "valor_total": ("valor_total_locacao", "sum"),
    "duracao_min": ("duracao_locacao", "min"),
    "duracao_media": ("duracao_locacao", "mean"),
    "duracao_max": ("duracao_locacao", "max"),
    "antecedencia_min": ("dias_antecedencia", "min"),
    "antecedencia_media": ("dias_antecedencia", "mean"),
    "antecedencia_max": ("dias_antecedencia", "max"),
}

COLUMN_RENAMES = {
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
}

# Function


@st.cache_data
def load_data(file_path: str) -> pd.DataFrame:
    df = pd.read_excel(file_path)
    df["data_inicio_locacao"] = pd.to_datetime(df["data_inicio_locacao"])
    return df


def apply_filters(
    df: pd.DataFrame, stores: list, vehicles: list, date_range: tuple
) -> pd.DataFrame:
    df_filtered = df.copy()

    df_filtered = df_filtered[df_filtered["id_loja"].isin(stores)]
    df_filtered = df_filtered[df_filtered["categoria_veiculo"].isin(vehicles)]

    if len(date_range) == 2:
        start_date, end_date = date_range
        df_filtered = df_filtered[
            (df_filtered["data_inicio_locacao"].dt.date >= start_date)
            & (df_filtered["data_inicio_locacao"].dt.date <= end_date)
        ]
    return df_filtered


def generate_summary_table(df: pd.DataFrame, group_by_col: str, title: str):
    st.subheader(title)

    statistics_table = df.groupby(group_by_col).agg(**AGGREGATION_DICT)

    for col in [
        "diaria_media",
        "valor_total_medio",
        "duracao_media",
        "antecedencia_media",
    ]:
        statistics_table[col] = statistics_table[col].round(0)

    # Lógica de cálculo do Total Geral
    total_geral = statistics_table.agg(
        {
            "id_contrato_count": "sum",
            "diaria_media": "mean",
            "valor_total_min": "min",
            "valor_total_medio": "mean",
            "valor_total_max": "max",
            "valor_total": "sum",
            "duracao_min": "min",
            "duracao_media": "mean",
            "duracao_max": "max",
            "antecedencia_min": "min",
            "antecedencia_media": "mean",
            "antecedencia_max": "max",
        }
    ).round(0)
    total_geral["diaria_media"] = statistics_table["diaria_media"].mean().round(0)
    total_geral["valor_total_medio"] = (
        statistics_table["valor_total_medio"].mean().round(0)
    )
    total_geral["duracao_media"] = statistics_table["duracao_media"].mean().round(0)
    total_geral["antecedencia_media"] = (
        statistics_table["antecedencia_media"].mean().round(0)
    )

    statistics_table.loc["Total Geral"] = total_geral

    statistics_table.rename(columns=COLUMN_RENAMES, inplace=True)
    st.dataframe(statistics_table, use_container_width=True)


def generate_correlation_plot(df: pd.DataFrame):
    df_plot = df.copy()
    if "Total Geral" in df_plot.index:
        df_plot = df_plot.drop("Total Geral", errors="ignore")

    fig = px.scatter(
        df_plot,
        x="Quantidade de Contratos",
        y="Montante Total",
        text=df_plot.index,
        title="Correlação: Quantidade de Contratos vs. Montante Total",
        labels={"Montante Total": "Montante Total (R$)"},
        trendline="ols",
    )
    fig.update_traces(textposition="top center")
    st.plotly_chart(fig, use_container_width=True)


def generate_time_series_plot(df: pd.DataFrame, title: str, column: str, y_label: str):
    st.subheader(title)

    df_time_series = (
        df.groupby(df["data_inicio_locacao"].dt.date)
        .agg({column: "count" if column == "id_contrato" else "mean"})
        .reset_index()
    )
    df_time_series.rename(
        columns={"data_inicio_locacao": "Data", column: "Dados Brutos"}, inplace=True
    )
    df_time_series["Data"] = pd.to_datetime(df_time_series["Data"])
    df_time_series.set_index("Data", inplace=True)

    df_time_series["Suavização 7 dias"] = (
        df_time_series["Dados Brutos"].rolling(window="7D").mean()
    )
    df_time_series["Suavização 30 dias"] = (
        df_time_series["Dados Brutos"].rolling(window="30D").mean()
    )
    df_time_series["Suavização 90 dias"] = (
        df_time_series["Dados Brutos"].rolling(window="90D").mean()
    )

    fig = px.line(
        df_time_series,
        y=[
            "Dados Brutos",
            "Suavização 7 dias",
            "Suavização 30 dias",
            "Suavização 90 dias",
        ],
        labels={"value": y_label, "Data": "Data"},
    )

    colors = {
        "Dados Brutos": "rgba(192, 192, 192, 0.25)",
        "Suavização 7 dias": "rgba(135, 206, 235, 0.75)",
        "Suavização 30 dias": "rgba(65, 105, 225, 1)",
        "Suavização 90 dias": "rgba(0, 0, 128, 1)",
    }
    widths = {
        "Dados Brutos": 1,
        "Suavização 7 dias": 2,
        "Suavização 30 dias": 3,
        "Suavização 90 dias": 3,
    }

    for name in colors.keys():
        fig.update_traces(
            line=dict(width=widths[name], color=colors[name]),
            selector=dict(name=name),
        )
    fig.update_layout(legend_title_text="")

    st.plotly_chart(fig, use_container_width=True)


def generate_mstl_decomposition_plots(df: pd.DataFrame, title_suffix: str, column: str):
    df_mstl = (
        df.groupby(df["data_inicio_locacao"].dt.date)
        .agg({column: "count" if column == "id_contrato" else "mean"})
        .reset_index()
    )
    df_mstl.rename(
        columns={"data_inicio_locacao": "Data", column: "Valor"}, inplace=True
    )
    df_mstl = df_mstl.set_index("Data")

    decomposition_mstl = MSTL(df_mstl["Valor"], periods=[182, 365]).fit()

    fig_trend = px.line(
        x=decomposition_mstl.trend.index,
        y=decomposition_mstl.trend.values,
        title=f"Tendência de {title_suffix}",
        labels={"x": "Data", "y": "Valor"},
    )
    st.plotly_chart(fig_trend, use_container_width=True)

    fig_seasonality_6m = px.line(
        x=decomposition_mstl.seasonal.index,
        y=decomposition_mstl.seasonal.iloc[:, 0].values,
        title=f"Padrão Sazonal de 6 Meses - {title_suffix}",
        labels={"x": "Data", "y": "Impacto Sazonal"},
    )
    st.plotly_chart(fig_seasonality_6m, use_container_width=True)

    fig_seasonality_12m = px.line(
        x=decomposition_mstl.seasonal.index,
        y=decomposition_mstl.seasonal.iloc[:, 1].values,
        title=f"Padrão Sazonal de 12 Meses - {title_suffix}",
        labels={"x": "Data", "y": "Impacto Sazonal"},
    )
    st.plotly_chart(fig_seasonality_12m, use_container_width=True)


# Execution


def main():
    df = load_data("../data/edited_dataset.xlsx")

    # Sidebar
    st.sidebar.title("Filtros")

    stores = sorted(df.id_loja.unique().tolist())
    vehicles = sorted(df.categoria_veiculo.unique().tolist())
    minimum_date = df["data_inicio_locacao"].min().date()
    maximum_date = df["data_inicio_locacao"].max().date()

    selec_stores = st.sidebar.multiselect(
        "Selecione as lojas:", options=stores, placeholder="Escolha uma (ou mais) opção"
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

    # Ajusta os filtros para "selecionar todos" se nada for escolhido
    if not selec_stores:
        selec_stores = stores
    if not selec_vehicles:
        selec_vehicles = vehicles

    # Aplica os filtros
    df_filtered = apply_filters(df, selec_stores, selec_vehicles, selec_date)

    # Exibição dos gráficos e tabelas
    st.title("Análise Exploratória de Locações")

    if not df_filtered.empty:
        # Tabela 1: Estatísticas das Lojas
        generate_summary_table(
            df_filtered.rename(columns={"id_loja": "Lojas"}, inplace=False),
            "Lojas",
            "Estatísticas das Lojas",
        )

        # Gráfico 1: Correlação Loja
        statistics_stores = (
            df_filtered.groupby("id_loja")
            .agg(**AGGREGATION_DICT)
            .rename(columns=COLUMN_RENAMES)
        )
        generate_correlation_plot(statistics_stores)

        # Tabela 2: Estatísticas de Veículos
        generate_summary_table(
            df_filtered.rename(
                columns={"categoria_veiculo": "Categoria de Veículo"}, inplace=False
            ),
            "Categoria de Veículo",
            "Estatísticas das Categorias de Veículos",
        )

        # Gráfico 2: Contagem de Contratos
        generate_time_series_plot(
            df_filtered,
            "Quantidade de Contratos",
            "id_contrato",
            "Quantidade de Contratos",
        )

        # Gráfico 3: Decomposição de Contratos
        generate_mstl_decomposition_plots(
            df_filtered, "Quantidade de Contratos", "id_contrato"
        )

        # Gráfico 4: Diária Média
        generate_time_series_plot(
            df_filtered, "Diária Média", "diaria_media", "Diária Média"
        )

        # Gráfico 5: Decomposição Diária Média
        generate_mstl_decomposition_plots(df_filtered, "Diária Média", "diaria_media")
    else:
        st.warning("Nenhum dado encontrado com os filtros selecionados.")


if __name__ == "__main__":
    main()
