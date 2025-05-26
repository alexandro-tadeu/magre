import streamlit as st
import requests
import py3Dmol
import os
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import pandas as pd
import Prog_Funcoes1

# Variáveis de controle e diretórios
graficos_gerados = set()
chain = " "
arquivo_base = "/home/lbcb/magre/"
arquivo_pdb = os.path.join(arquivo_base, "arquivos/pdb/")
arquivo_testes = os.path.join(arquivo_base, "arquivos/testes/")

# Certifique-se de que os diretórios necessários existem
os.makedirs(arquivo_pdb, exist_ok=True)
os.makedirs(arquivo_testes, exist_ok=True)

# Função para baixar o arquivo PDB
def baixa_pdb(codigo_pdb):
    url = f'https://files.rcsb.org/view/{codigo_pdb}.pdb'  # Corrigido a URL
    response = requests.get(url)
    if response.status_code == 200:
        st.write("Arquivo PDB baixado com sucesso.")
        return response.text
    else:
        st.warning("Não foi possível baixar o arquivo PDB. Verifique o código.")
        return None

# Função para salvar o arquivo PDB
def salva_pdb(codigo_pdb, conteudo):
    caminho = os.path.join(arquivo_pdb, f"{codigo_pdb}.pdb")
    with open(caminho, "w") as f:
        f.write(conteudo)
    return caminho

# Função para processar o arquivo PDB e gerar resultados
def processa_pdb(codigo_pdb, conteudo_pdb):
    global chain
    linhas = conteudo_pdb.splitlines()
    resultado = []
    for line in linhas:
        if len(line) < 1:
            continue
        elif line.startswith("ATOM") and line[21:22] != chain:
            chain = line[21:22]
            resultado = Prog_Funcoes1.movimenta(
                codigo_pdb + ".pdb", linhas, "", chain, codigo_pdb, 1
            )
            resultado = Prog_Funcoes1.avalia_ruido(resultado)
    return resultado

# Função para exibir a estrutura 3D da proteína com rótulos para os resíduos específicos
def exibir_estrutura_3d(codigo_pdb, resn_especifico=None, resi_especifico=None, estilo='cartoon'):
    try:
        # Baixar os dados do PDB
        url = f'https://files.rcsb.org/view/{codigo_pdb}.pdb'
        response = requests.get(url)
        if response.status_code != 200:
            st.error(f"Erro ao carregar o arquivo PDB para o código {codigo_pdb}")
            return

        pdb_data = response.text

        # Extrair todos os resíduos do arquivo PDB
        residues = []
        lines = pdb_data.splitlines()
        for line in lines:
            if line.startswith("ATOM"):
                resn = line[17:20].strip()  # Nome do resíduo (e.g., ALA, GLY, etc.)
                resi = int(line[22:26].strip())  # Número do resíduo
                chain = line[21:22].strip()  # Cadeia do resíduo
                if (resn, resi, chain) not in residues:
                    residues.append((resn, resi, chain))

        # Filtrar os resíduos específicos, se fornecido
        if resn_especifico or resi_especifico:
            residues = [(resn, resi, chain) for (resn, resi, chain) in residues 
                        if (not resn_especifico or resn == resn_especifico) 
                        and (not resi_especifico or resi == resi_especifico)]

        # Usar py3Dmol para renderizar a estrutura 3D
        viewer = py3Dmol.view(width=800, height=600)
        viewer.addModel(pdb_data, "pdb")

        # Definir o estilo com base na escolha do usuário
        if estilo == 'cartoon':
            viewer.setStyle({'cartoon': {'color': 'spectrum'}})
        elif estilo == 'stick':
            viewer.setStyle({'stick': {'colorscheme': 'element'}})
        elif estilo == 'sphere':
            viewer.setStyle({'sphere': {'scale': 0.3, 'colorscheme': 'element'}})

        # Adicionar rótulos para os resíduos encontrados
        for resn, resi, chain in residues:
            viewer.addResLabels({'resi': str(resi), 'resn': resn, 'chain': chain}, {'fontColor': 'white', 'backgroundColor': 'black'})

        # Ajustando a câmera
        viewer.zoomTo()
        viewer.setBackgroundColor('white')

        # Exibir o visualizador no Streamlit
        viewer_html = viewer._make_html()
        st.components.v1.html(viewer_html, height=600)
    except Exception as e:
        st.error(f"Erro ao exibir a estrutura 3D: {e}")

# Função para gerar a visualização da sequência com cores
def exibe_sequencia(resultado):
    st.subheader("Detecção de Agregação")
    agregam_count = 0
    nao_agregam_count = 0

    sequence_elements = []
    for linha in resultado:
        dados = linha.split(";")
        posicao = int(dados[1])
        valor = float(dados[3])
        residuo = dados[4]

        # Define a cor vermelha para valores maiores que 0.5 (agrega) e preta para menores ou iguais a 0.5 (não agrega)
        color = "red" if valor > 0.5 else "black"
        tooltip = "Este aminoácido agrega." if valor > 0.5 else "Este aminoácido não agrega."

        span_style = f"color: {color}; font-size: 20px; background-color: #F0F0F0; border: 1px solid #CCCCCC; border-radius: 4px; padding: 2px 6px; margin: 2px"
        sequence_elements.append(
            f'<span style="{span_style}" title="{tooltip}">{residuo}</span>'
        )

        if valor > 0.5:
            agregam_count += 1
        else:
            nao_agregam_count += 1

    sequence_html = " ".join(sequence_elements)
    st.markdown(sequence_html, unsafe_allow_html=True)

    st.subheader("Resumo")
    st.write(f"Número de aminoácidos que agregam: {agregam_count}")
    st.write(f"Número de aminoácidos que não agregam: {nao_agregam_count}")

# Função para gerar o gráfico usando Plotly
def plota_resultado_plotly(resultado, codigo_pdb, chain):
    tamanho = len(resultado)
    tabela1 = [[0] * tamanho for _ in range(2)]

    for i, linha in enumerate(resultado):
        tabela = linha.split(";")
        tabela1[0][i] = int(tabela[1])
        tabela1[1][i] = float(tabela[3])

    limite_inferior, limite_superior = 0.2, 0.8
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=tabela1[0], y=tabela1[1], mode="lines+markers",
                             line=dict(color="black"), name=f"{codigo_pdb}/{chain}"))
    fig.add_trace(go.Scatter(
        x=[tabela1[0][i] for i in range(tamanho) if tabela1[1][i] >= limite_superior],
        y=[tabela1[1][i] for i in range(tamanho) if tabela1[1][i] >= limite_superior],
        mode="markers", marker=dict(color="red", size=10), name="Agregação Forte"))
    fig.add_trace(go.Scatter(
        x=[tabela1[0][i] for i in range(tamanho) if tabela1[1][i] <= limite_inferior],
        y=[tabela1[1][i] for i in range(tamanho) if tabela1[1][i] <= limite_inferior],
        mode="markers", marker=dict(color="orange", size=10), name="Agregação Fraca"))
    fig.update_layout(
        title=f"Propensão de agregação/{codigo_pdb}-{chain}",
        xaxis_title="Resíduo",
        yaxis_title="Probabilidade"
    )
    st.plotly_chart(fig)

# Função principal
def main():
    st.title("Gerador de Gráfico, Detecção de Agregação e Visualização 3D")

    codigo_pdb = st.text_input("Informe o código PDB da proteína:")

    if st.button("Gerar Análise"):
        if not codigo_pdb:
            st.warning("Por favor, insira um código PDB válido.")
            return

        conteudo_pdb = baixa_pdb(codigo_pdb)
        if conteudo_pdb:
            caminho_pdb = salva_pdb(codigo_pdb, conteudo_pdb)
            resultado = processa_pdb(codigo_pdb, conteudo_pdb)
            exibe_sequencia(resultado)
            plota_resultado_plotly(resultado, codigo_pdb, chain)
            exibir_estrutura_3d(codigo_pdb)

if __name__ == "__main__":
    main()
