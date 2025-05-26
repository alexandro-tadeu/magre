import streamlit as st
import requests
import os
import numpy as np
import matplotlib.pyplot as plt
import Prog_Funcoes1

# Variável de controle para verificar se o gráfico já foi gerado
graficos_gerados = set()

# Variável global para armazenar a cadeia
chain = " "


# Função para plotar o gráfico
def Plota_Resultado(resultado1, CodigoPDB1, chain1):
    cor2 = "red"
    cor1 = "black"
    tamanho = len(resultado1)

    n = 6
    m = tamanho
    m1 = 20

    tabela1 = [[0] * m for i in range(n)]
    tabela = tabelaa = ""
    i1 = 0
    opcao = 1

    for i in range(0, len(resultado1), 1):
        tabela = resultado1[i].split(";")
        tabela1[3][i] = 0.5
        tabela1[0][i] = int(tabela[1])
        tabela1[1][i] = float(tabela[3])
        tabela1[2][i] = int(tabela[1]) - 1

    tabela1[2][i] = int(tabela[1])

    fig, ax = plt.subplots()
    ax.plot(tabela1[0], tabela1[1], color=cor1, label=CodigoPDB1 + "/" + chain1)
    ax.plot(tabela1[0], tabela1[1], ".", color="red")
    ax.plot(tabela1[2], tabela1[3], "--", color="green")

    ax.set_xlabel("Resíduos", fontweight="bold")
    ax.set_ylabel("Probabilidade", fontweight="bold")
    ax.set_xlim(int(tabela1[0][0]), int(tabela1[0][i]))

    ax.set_ylim(0, 1)

    ax.set_yticks(np.arange(0.0, 1.1, 0.1))

    ax.tick_params(axis="x", labelsize=6)
    ax.tick_params(axis="y", labelsize=6)

    ax.set_title(
        "Propensão de agregação/" + CodigoPDB1 + "-" + chain1, fontweight="bold"
    )

    st.pyplot(fig)


def main():
    st.title("Gerador de Gráfico de Agregação Estático")
    # Introdução
    st.markdown(
        """
        <p style='text-align: justify;'>
        O Gerador de Gráfico de Agregação Estático é uma ferramenta poderosa usada em ciências biológicas, farmacêuticas e de pesquisa para visualizar e analisar dados relacionados à agregação de proteínas. 
        A agregação de proteínas é um fenômeno importante que pode levar a doenças neurodegenerativas, como Alzheimer, Parkinson e outras. 
        Compreender e controlar esse processo é essencial para o desenvolvimento de terapias eficazes e o design de produtos farmacêuticos estáveis.
        </p>
        """,
        unsafe_allow_html=True,
    )
    # Subtítulo
    st.subheader("Como Funciona")
    
    st.markdown(
    """
    <p style='text-align: justify;'>
    Os usuários começam inserindo seus dados no gerador, que pode incluir informações sobre código PDB. Em seguida, o gerador gera gráfico(s) que mostram como essas variáveis da agregação de proteínas acontecem.
    </p>
    """,
    unsafe_allow_html=True,
)
    

    st.subheader("Visualização de Dados")
    
    st.markdown(
    """
    <p style='text-align: justify;'>
    Uma das características mais valiosas do Gerador de Gráfico de Agregação Estático é sua capacidade de criar visualizações claras e informativas. Os gráficos gerados podem incluir linhas de agregação de proteínas. Isso permite que os pesquisadores identifiquem tendências e padrões nos dados, o que é essencial para a tomada de decisões informadas.
    </p>
    """,
    unsafe_allow_html=True,
)    
    # Adicione um campo de entrada para o código PDB da proteína
    codigo_pdb = st.text_input("Informe o código PDB da proteína:")

    if st.button("Gerar Gráfico"):
        if not codigo_pdb:
            st.warning("Por favor, insira um código PDB válido.")
            return

        global chain  # Declarar chain como global para atualizá-lo

        arquivo = "/home/lbcb/magre/"
        arquivo1 = arquivo[0:17] + "/arquivos/pdb/"
        arquivo2 = arquivo[0:17] + "/arquivos/testes/"

        pdbr = "https://files.rcsb.org/view/" + codigo_pdb + ".pdb"

        st.write("Código Solicitado:", codigo_pdb)

        response = requests.get(pdbr)

        entrada = saida = arquivo1 + codigo_pdb + ".pdb"
        A = response.text
        proteinArq = ""
        pdbLines = ""
        A3DLines = ""

        lin = 81
        fim = int(len(A) / lin)

        contpdb = 0
        desliga = 0
        proteinArq = codigo_pdb + ".pdb"
        chamador = 1
        resultado = []

        if response.status_code == 200:
            arq_saida = open(saida, "w")
            for I in range(0, fim - 1, 1):
                words = A[lin * I : lin * (I + 1)]
                arq_saida.write(words)
            arq_saida.close()

        with open(entrada) as arq_entrada:
            pdbLines = arq_entrada.readlines()

        for line in pdbLines:
            words = line
            if len(words) < 1:
                pass
            elif words[0:4] == "ATOM" and words[21:22] != chain:
                chain = words[21:22]

                resultado = Prog_Funcoes1.movimenta(
                    proteinArq, pdbLines, A3DLines, chain, codigo_pdb, chamador
                )

                resultado = Prog_Funcoes1.avalia_ruido(resultado)

                PastaArq = arquivo2
                contatohpFilename = PastaArq + codigo_pdb[0:4] + "_" + chain + ".csv"
                with open(contatohpFilename, "w") as contatohpFile:
                    for line in resultado:
                        print(line, file=contatohpFile)

                # Verifique se o gráfico já foi gerado para este código PDB e cadeia
                if (codigo_pdb, chain) in graficos_gerados:
                    st.warning(
                        "O(s) gráfico(s) já foi(ram) gerado(s) para esta cadeia do código PDB. Não é possível gerar novamente."
                    )
                    return  # Finalize o código aqui
                else:
                    # Exiba o gráfico
                    Plota_Resultado(resultado, codigo_pdb, chain)
                    # Atualize a variável de controle para indicar que o gráfico foi gerado
                    graficos_gerados.add((codigo_pdb, chain))


if __name__ == "__main__":
    main()
