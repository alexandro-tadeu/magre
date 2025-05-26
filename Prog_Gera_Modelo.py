# -*- coding: utf-8 -*-

import pickle
import datetime
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn import metrics
import pandas as pd
import warnings
import glob, os
from imblearn.under_sampling import AllKNN
from imblearn.under_sampling import TomekLinks
from imblearn.under_sampling import RandomUnderSampler
from imblearn.under_sampling import EditedNearestNeighbours
from imblearn.under_sampling import NearMiss
from collections import Counter

# Obtendo o diretório atual
arq = os.getcwd() 

# Definindo diretórios de saída e modelos
arq1 = arq[0:17] + "/arquivos/saida/"
arq2 = arq[0:17] + "/arquivos/modelos/"

# Obtendo a data e hora atual
data = datetime.datetime.now()

# Configurando o caminho do arquivo de entrada
Arquivo = "arquivos/saida/Agrupados.csv"  

# Lendo o arquivo CSV e armazenando os dados no DataFrame df_train
df_train = pd.read_csv(Arquivo, delimiter=';')
train = df_train

# Obtendo rótulos e dados
labels = train.columns[1:21]
X = train[labels]
y = train['Agrega']

# Aplicando o método AllKNN para reamostragem
knn = AllKNN(n_neighbors=4)
print(datetime.datetime.now())   
print("vai distribuir")       
X_knn, y_knn = knn.fit_resample(X, y)

# Exibindo a distribuição das classes após reamostragem
print('Allknn Distribution %s' % Counter(y_knn))

# Definindo parâmetros para otimização do modelo
forest_params = [{'n_estimators': [100, 200, 300, 400, 500, 600], 'max_depth': list(range(10, 20, 30))}]

# Criando um modelo GradientBoostingRegressor
rfc = GradientBoostingRegressor()

print(datetime.datetime.now())  
print("val montarr") 

# Configurando um classificador GridSearchCV para otimização
clf = GridSearchCV(rfc, forest_params, cv=5, scoring='r2')

print(datetime.datetime.now())   
print("val classificar ")

# Treinando o modelo usando os dados reamostrados
Resultado = clf.fit(X_knn, y_knn)
print(datetime.datetime.now())   
print("vai gravar")

# Salvando o modelo treinado em um arquivo
filename = arq2 + "Mod_Oficial.sav"
pickle.dump(clf, open(filename, 'wb'))
print(filename)
