# case-foco

# Desafio Técnico para Vaga de Cientista de Dados na Foco Aluguel de Carros

Este documento `README.md` detalha a solução para o desafio técnico proposto pela Foco Aluguel de Carros para a posição de Cientista de Dados. O projeto foi desenvolvido seguindo todas as etapas de um pipeline de ciência de dados, desde a análise exploratória até a interpretação dos resultados.

### Sobre a Foco Aluguel de Carros

A Foco Aluguel de Carros é uma empresa que, desde 2003, se destaca no mercado de aluguel de veículos por sua abordagem centrada no cliente. Fundada com a missão de simplificar o processo de locação de carros pela internet, a Foco se orgulha de oferecer um serviço de alta qualidade, preços justos e um atendimento que realmente entende as necessidades das pessoas. Com presença nas principais cidades do país, a empresa investe em uma frota de excelentes carros e na experiência do cliente, valores que correm em seu DNA empreendedor.

### Objetivo do Desafio

O objetivo deste desafio foi utilizar uma base de dados histórica fictícia de contratos de locação para projetar, por loja e por mês, dois indicadores-chave de negócio:

1.  **Diárias Locadas:** O total de diárias de locação por mês.
2.  **Diária Média:** O preço médio das diárias de locação por mês.

O período da projeção abrange de **julho/2024 a junho/2025**.

---

### Etapas do Projeto

O projeto seguiu o fluxo abaixo, com todos os detalhes e códigos documentados em um `Jupyter Notebook`.

#### 1. Análise Exploratória e Descritiva dos Dados (EDA)
Nesta fase, a base de dados foi cuidadosamente examinada para compreender a sua estrutura e as características das variáveis. As análises incluíram:

* **Distribuição das Variáveis:** Visualização da distribuição de variáveis-chave como `duracao_locacao`, `dias_antecedencia` e `diaria_media`.
* **Comparações de Agrupamentos:** Análise das diferenças de desempenho entre lojas, categorias de veículos e a influência da localização (`cidade`, `estado`).
* **Identificação de Tendências:** Observação do comportamento de longo prazo dos indicadores ao longo do tempo.
* **Padrões Sazonais:** Análise de repetições de padrões em intervalos regulares (semanal, mensal, anual), como picos de locação em feriados ou meses específicos.

#### 2. Modelagem Preditiva
Para a previsão dos indicadores, foram utilizados 4 modelos de machine learning, cada um com diferentes abordagens para séries temporais:

* **Modelos de Regressão:** `Random Forest Regressor` e `XGBoost Regressor` foram aplicados para capturar relações não lineares entre as variáveis e o tempo, utilizando técnicas de feature engineering para incluir a sazonalidade e a tendência.
* **Modelos de Séries Temporais Clássicos/Avançados:**
    * `Prophet` (da Meta): Um modelo robusto para séries temporais com múltiplas sazonalidades, feriados e tendências não lineares.
    * `ARIMA`: Um modelo estatístico clássico que utiliza a autocorrelação dos dados passados para fazer previsões.

Cada modelo foi avaliado com as métricas **RMSE**, **MAE** e **MAPE**, utilizando a técnica de backtesting para garantir uma validação rigorosa das projeções.

#### 3. Interpretação e Insights
Nesta etapa, o foco foi transformar os resultados da modelagem em insights acionáveis para a Foco.

* **Impacto das Variáveis:** Foram identificadas e destacadas as variáveis com maior poder preditivo, como sazonalidade anual e mensal.
* **Comparação de Modelos:** Uma análise comparativa das métricas de desempenho foi realizada para entender as vantagens e desvantagens de cada modelo. O `Prophet`, por exemplo, se mostrou eficaz em capturar a sazonalidade complexa, enquanto o `XGBoost` foi capaz de lidar com a complexidade das interações entre as features.
* **Recomendação Final:** Com base nas métricas de avaliação e na interpretabilidade, foi recomendada a utilização de um dos modelos como a principal ferramenta de previsão, justificando a escolha para a tomada de decisão executiva.

---

### Entrega

A entrega deste desafio consiste em dois documentos:

1.  **`notebook.ipynb`**: Um Jupyter Notebook completo, com todos os códigos, gráficos e análises comentados, detalhando cada etapa do pipeline.
2.  **`apresentacao_executiva.pdf`**: Um documento em formato PDF (ou slides) que resume os principais insights, resultados da modelagem e a recomendação final de forma clara e concisa, ideal para um público executivo.