import requests

def conversao(proteina, opcao):
    tabela = {
        "ALA": ["A", "01"],
        "ARG": ["R", "02"],
        "ASN": ["N", "03"],
        "ASP": ["D", "04"],
        "CYS": ["C", "05"],
        "GLN": ["Q", "06"],
        "GLU": ["E", "07"],
        "GLY": ["G", "08"],
        "HIS": ["H", "09"],
        "ILE": ["I", "10"],
        "LEU": ["L", "11"],
        "LYS": ["K", "12"],
        "MET": ["M", "13"],
        "PHE": ["F", "14"],
        "PRO": ["P", "15"],
        "SER": ["S", "16"],
        "THR": ["T", "17"],
        "TRP": ["W", "18"],
        "TYR": ["Y", "19"],
        "VAL": ["V", "20"]
    }

    if proteina in tabela:
        return tabela[proteina][1] if opcao == "number" else tabela[proteina][0]
    else:
        return "99"

class Atom:
    def __init__(self, line):
        self.atom_name = line[12:16].strip()
        self.res_name = line[17:20].strip()
        self.chain_id = line[21]
        self.res_number = int(line[22:26])
        self.coordinates = (
            float(line[30:38]),
            float(line[38:46]),
            float(line[46:54])
        )

def obter_cadeias_disponiveis(pdb_lines):
    cadeias = set()

    for line in pdb_lines:
        if line.startswith("ATOM"):
            cadeia = line[21]
            cadeias.add(cadeia)

    return sorted(list(cadeias))

def extrair_sequencia_convertida(pdb_lines, chain):
    sequencia_convertida = ""

    for line in pdb_lines:
        if line.startswith("ATOM") and line[21] == chain:
            atom = Atom(line)
            proteina_convertida = conversao(atom.res_name, "letter")
            sequencia_convertida += proteina_convertida

    return sequencia_convertida

def obter_codigo_pdb(codigo_pdb):
    url = f'https://files.rcsb.org/view/{codigo_pdb}.pdb'
    response = requests.get(url)

    if response.status_code == 200:
        return response.text.split('\n')
    else:
        print(f"Erro ao obter o código PDB {codigo_pdb}. Verifique o código e tente novamente.")
        return None

def main():
    codigo_pdb = input("Insira o código PDB: ").upper()
    pdb_lines = obter_codigo_pdb(codigo_pdb)

    if pdb_lines:
        cadeias_disponiveis = obter_cadeias_disponiveis(pdb_lines)

        if not cadeias_disponiveis:
            print("Nenhuma cadeia encontrada no arquivo PDB.")
            return

        print("Cadeias disponíveis:", cadeias_disponiveis)

        cadeia_desejada = input("Escolha a cadeia desejada: ").upper()

        if cadeia_desejada not in cadeias_disponiveis:
            print("Cadeia inválida. Escolha uma cadeia disponível.")
            return

        sequencia_convertida = extrair_sequencia_convertida(pdb_lines, cadeia_desejada)

        if sequencia_convertida:
            print(f"Sequência de Aminoácidos Convertida (Cadeia {cadeia_desejada}):", sequencia_convertida)

if __name__ == "__main__":
    main()
