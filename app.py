import streamlit as st
import requests
from bs4 import BeautifulSoup

# Função para obter a sequência de aminoácidos a partir do código PDB
def obter_sequencia_por_codigo_pdb(codigo_pdb):
    url = f'http://amypro.net/search?query={codigo_pdb}'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Ajuste o seletor de classe aqui conforme a estrutura HTML do site AmyPro
        resultados_pesquisa = soup.find_all('div', class_='sequence-info')  # Altere para a classe correta, se necessário

        if resultados_pesquisa:
            sequencia = "\n".join([resultado.text.strip() for resultado in resultados_pesquisa])
            return sequencia
        else:
            return "Nenhuma sequência de aminoácidos encontrada para o código PDB fornecido."
    else:
        return f"Erro ao obter informações estruturais do site AmyPro para o código PDB {codigo_pdb}."

# Função principal do Streamlit
def main():
    st.title("Consulta de Sequência de Aminoácidos por Código PDB")

    # Campo de entrada para o código PDB
    codigo_pdb = st.text_input("Informe o código PDB da proteína:")

    # Botão para realizar a consulta
    if st.button("Buscar Sequência"):
        if codigo_pdb.strip():
            sequencia_proteina = obter_sequencia_por_codigo_pdb(codigo_pdb.strip())
            st.subheader("Sequência de Aminoácidos:")
            # Exibe a sequência de aminoácidos na área de texto
            st.text_area("Sequência da proteína:", value=sequencia_proteina, height=200)
        else:
            st.warning("Por favor, insira o código PDB da proteína.")

if __name__ == "__main__":
    main()
