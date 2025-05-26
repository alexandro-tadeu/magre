import requests
from bs4 import BeautifulSoup

def obter_informacoes_estruturais_por_nome_proteina(nome_proteina):
    url = f'http://amypro.net/search?query={nome_proteina}'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        resultados_pesquisa = soup.find_all('div', class_='structural-info')

        if resultados_pesquisa:
            for resultado in resultados_pesquisa:
                print(resultado.text.strip())
        else:
            print("Nenhuma informação estrutural encontrada para o nome da proteína.")
    else:
        print(f"Erro ao obter informações estruturais do site AmyPro para a proteína {nome_proteina}.")

def main():
    nome_proteina = input("Insira o nome da proteína: ")

    # Obtendo informações estruturais do site AmyPro pelo nome da proteína
    obter_informacoes_estruturais_por_nome_proteina(nome_proteina)

if __name__ == "__main__":
    main()
