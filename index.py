import streamlit as st
from nova_pagina import (
    Plota_Resultado,
    main as NovaPaginaMain,
)  
from nova_pagina_dinamica import (
    main as NovaPaginaDinamicaMain,
)  
from nova_pagina_sequencia import main as NovaPaginaSequenciaMain
from nova_pagina_estrutura import main as NovaPaginaEstruturaMain  
from nova_pagina_contato import main as NovaPaginaContatoMain
from appSeqPdb import main as AppPdbMain  # Importação da nova página
from appSeqAmypro import main as AppAmyproMain  # Importação da nova página
from appTransforme import main as AppTransformeMain  # Importação da nova página
from appEstrutura3D import main as AppEstrutura3DMain  # Importação da nova página 3D

# Define um menu de navegação
st.sidebar.title("Menu de Páginas")
pages = {
    "Inicial": "inicial",
    "Gráfico Estático": "grafico_estatico",
    "Gráfico Dinâmico": "grafico_dinamico",
    "Sequência Aminoácidos": "nova_pagina_sequencia",
    "Sequência Aminoácidos PDB": "appSeqPdb",
    "Sequência Aminoácidos Amypro": "appSeqAmypro",
    "Sequência Linear Aminoácido": "appTransforme",  # Adição da nova opção no menu
    "Estrutura 3D com Rotulagem": "appEstrutura3D",  # Adição da nova página 3D
    "Estrutura 3D sem Rotulagem": "nova_pagina_estrutura",
    "Contato": "contato",
}
page = st.sidebar.selectbox("Ir para", list(pages.keys()))

# Função para criar um card
def create_card(title, text, image_url):
    st.subheader(title)
    st.image(image_url, use_container_width=True)
    st.write(text)

# Lista de imagens com links individuais
imagens = [
    {"title": "Card 1", "text": "Este é um subtexto explicativo para o Card 1.", "url": "img/amino.png"},
    {"title": "Card 2", "text": "Este é um subtexto explicativo para o Card 2.", "url": "img/beta.png"},
    {"title": "Card 3", "text": "Este é um subtexto explicativo para o Card 3.", "url": "img/helice.png"},
    {"title": "Card 4", "text": "Este é um subtexto explicativo para o Card 4.", "url": "img/helice.png"},
    {"title": "Card 5", "text": "Este é um subtexto explicativo para o Card 5.", "url": "img/helice.png"},
    {"title": "Card 6", "text": "Este é um subtexto explicativo para o Card 6.", "url": "img/helice.png"},
]

# Crie o aplicativo Streamlit
def main():
    if page == "Inicial":
        # Título da Página
        st.title("Proteínas e Agregação de Proteínas: Uso de Preditores")

        # Conteúdo da página inicial
        st.markdown(
            """
            <p style='text-align: justify;'>As proteínas desempenham um papel fundamental em inúmeras funções biológicas...</p>
            """,
            unsafe_allow_html=True,
        )

        # Divide a página em duas colunas
        col1, col2, col3 = st.columns(3)

        # Crie 3 cards na primeira linha
        with col1:
            create_card(title=imagens[0]["title"], text=imagens[0]["text"], image_url=imagens[0]["url"])

        with col2:
            create_card(title=imagens[1]["title"], text=imagens[1]["text"], image_url=imagens[1]["url"])

        with col3:
            create_card(title=imagens[2]["title"], text=imagens[2]["text"], image_url=imagens[2]["url"])

        # Crie 3 cards na segunda linha
        with col1:
            create_card(title=imagens[3]["title"], text=imagens[3]["text"], image_url=imagens[3]["url"])

        with col2:
            create_card(title=imagens[4]["title"], text=imagens[4]["text"], image_url=imagens[4]["url"])

        with col3:
            create_card(title=imagens[5]["title"], text=imagens[5]["text"], image_url=imagens[5]["url"])

    elif page == "Gráfico Estático":
        NovaPaginaMain()

    elif page == "Gráfico Dinâmico":
        NovaPaginaDinamicaMain()

    elif page == "Sequência Aminoácidos":
        NovaPaginaSequenciaMain()
        
    elif page == "Sequência Aminoácidos PDB":
        AppPdbMain()  # Correção aqui
    
    elif page == "Sequência Aminoácidos Amypro":
        AppAmyproMain()  # Correção aqui
        
    elif page == "Sequência Linear Aminoácido":
        AppTransformeMain()
        
    elif page == "Estrutura 3D com Rotulagem":
        AppEstrutura3DMain()  # Chama a função principal da página de Estrutura 3D
        
    elif page == "Estrutura 3D sem Rotulagem":
        NovaPaginaEstruturaMain()

    elif page == "Contato":
        NovaPaginaContatoMain()
        
if __name__ == "__main__":
    main()
