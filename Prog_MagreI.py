import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

# Carregando os dados
# Certifique-se de substituir 'seu_caminho/aquivo_amyPDB.csv' pelo caminho real do seu arquivo
df = pd.read_csv('seu_caminho/aquivo_amyPDB.csv')

# Função para criar janelas de resíduos
def create_residue_windows(sequence, window_size=3):
    windows = [sequence[i:i+window_size] for i in range(len(sequence)-window_size+1)]
    return windows

# Adicionando a janela de resíduos ao redor de cada resíduo
window_size = 3  # ajuste conforme necessário
df['residue_windows'] = df['sequencia_primaria'].apply(lambda seq: create_residue_windows(seq, window_size))

# Concatenando a sequência da janela para vetorização
df['residue_windows_concatenated'] = df['residue_windows'].apply(lambda windows: ' '.join(windows))

# Preprocessamento dos dados
X = df['residue_windows_concatenated']
y = df['agregacao']

# Divisão em conjuntos de treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Vetorização das sequências primárias
vectorizer = CountVectorizer()
X_train_vectorized = vectorizer.fit_transform(X_train)
X_test_vectorized = vectorizer.transform(X_test)

# Treinamento do classificador (usando Naive Bayes como exemplo)
classifier = MultinomialNB()
classifier.fit(X_train_vectorized, y_train)

# Previsões no conjunto de teste
predictions = classifier.predict(X_test_vectorized)

# Adicionando coluna de previsões ao DataFrame de teste
df_test = df.loc[X_test.index].copy()
df_test['previsoes'] = predictions

# Exibindo sequência de aminoácidos, região de agregação e previsões
for index, row in df_test.iterrows():
    print(f"Sequência: {row['sequencia_primaria']}")
    print(f"Região de Agregação: {row['regiao_agregacao']}")
    print(f"Previsão do Modelo: {row['previsoes']}\n")
