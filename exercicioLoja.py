import pandas as pd
import seaborn as srn
import statistics  as sts
import matplotlib.pyplot as plt
plt.show()


#importar dados
dataset = pd.read_csv("dados_loja_tratamento.csv", sep =",")
#visulizar
dataset.head(20)
#print(dataset.head(20))

#Tamanho da matriz
dataset.shape
#print(dataset.shape)

#Renomear as colunas 
dataset.columns=["Produto","Quantidade","Preço","Categoria"]
#print(dataset.head(20))

#Dados categóricos
categoricProduct=dataset.groupby(['Produto']).size()
#print(categoricProduct)

dataset['Produto'].describe()
#print(dataset['Produto'].describe())

categoricCategory=dataset.groupby(['Categoria']).size()
#print(categoricCategory)

dataset['Categoria'].describe()
#print(dataset['Categoria'].describe())

#Analise dos dados numericos
dataset['Quantidade'].describe()
#print(dataset['Quantidade'].describe())

#Histograma do atributo numérico "Quantidade"
srn.boxplot(dataset['Quantidade']).set_title('Quantidade de itens')
#plt.show()
#srn.histplot(dataset['Quantidade']).set_title('Quantidade de itens')
#srn.distplot(dataset['Quantidade']).set_title('Quantidade de itens')

#Dados Numéricos
categoryQuantity = dataset.groupby(['Quantidade']).size()
#print(categoryQuantity)

#Análise dados numericos
dataset['Preço'].describe()
#print(dataset['Preço'].describe())

