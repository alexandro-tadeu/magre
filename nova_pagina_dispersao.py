import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def load_csv_data(file_path):
    # Função para carregar dados do CSV
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        st.warning(f"Erro ao carregar o arquivo CSV: {e}")
        return None

def plot_scatter(data, x_column, y_column, title, xlabel, ylabel, aggregation_column):
    fig, ax = plt.subplots()

    # Separando os dados em dois DataFrames: agregação e não agregação
    df_aggregation = data[data[aggregation_column] == 1]
    df_no_aggregation = data[data[aggregation_column] == 0]

    # Plotando os pontos de agregação e não agregação
    ax.scatter(df_aggregation[x_column], df_aggregation[y_column], color='blue', marker='o', label='Agregação')
    ax.scatter(df_no_aggregation[x_column], df_no_aggregation[y_column], color='red', marker='x', label='Não Agregação')

    ax.set_title(title, fontweight="bold")
    ax.set_xlabel(xlabel, fontweight="bold")
    ax.set_ylabel(ylabel, fontweight="bold")
    ax.legend()

    st.pyplot(fig)

def main():
    st.title("Visualização por Dispersão com Distinção de Agregação a partir de CSV")

    # Upload do arquivo CSV
    csv_file = st.file_uploader("Selecione um arquivo CSV", type=["csv"])

    if not csv_file:
        st.info("Por favor, faça o upload de um arquivo CSV.")
        return

    # Carregar dados do CSV
    df = load_csv_data(csv_file)

    if df is not None:
        st.write("Dados do arquivo CSV:")
        st.write(df.head())  # Exibe os primeiros registros do DataFrame

        # Seleção de colunas para X, Y e coluna de agregação
        x_column = st.selectbox("Selecione a coluna para o eixo X", df.columns)
        y_column = st.selectbox("Selecione a coluna para o eixo Y", df.columns)
        aggregation_column = st.selectbox("Selecione a coluna de Agregação", df.columns)

        title = f"Visualização por Dispersão ({x_column} vs {y_column})"
        xlabel = x_column
        ylabel = y_column

        # Chama a função para plotar o gráfico de dispersão com distinção de agregação
        plot_scatter(df, x_column, y_column, title, xlabel, ylabel, aggregation_column)

if __name__ == "__main__":
    main()
