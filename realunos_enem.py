# -*- coding: utf-8 -*-
"""ReAlunos_enem.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1t43-xy6r62zNScmXLlfvgmG98DUkbBWa
"""



# ALUNOS ENEM

import pandas as pd
import seaborn as srn
import statistics as sts

#importar dados
dataset = pd.read_csv("../../Downloads/Alunos_Enem.csv", sep =",")
#visulizar
dataset.head()

#Verificar se há objetos repetidos no dataset e eliminar
dataset[dataset.duplicated(['ID Aluno'],keep=False)]

#Excluir o duplicado pelo ID
dataset.drop_duplicates(subset="ID Aluno", keep='first',inplace=True)
#buscamos duplicados
dataset[dataset.duplicated(['ID Aluno'],keep= False)]

#Tratamento do atributo Região
agrupado = dataset.groupby(['Região']).size()
#agrupado

#Padronizar os estados: N , NE, S, SE, CO
dataset['Região'] = dataset['Região'].replace({
    'N': 'Norte',
    'NE': 'Nordeste',
    'S': 'Sul',
    'SE': 'Sudeste',
    'CO': 'Centro-Oeste',
    'Paraíba':'Nordeste',
    'Brasília':'Centro-Oeste'

})
dataset['Região'] = dataset['Região'].fillna("Não informado")
agrupado = dataset.groupby(['Região']).size()
agrupado

#Tratamento do atributo Sexo: preencher dados ausentes com a moda utilizando fillna e isnull
# Tratamento do atributo Sexo: padronizar e preencher dados ausentes com a moda
# Primeiro, padronizar os valores
dataset['Sexo'] = dataset['Sexo'].replace({
    'F': 'Feminino',
    'M': 'Masculino'
})

# Verificar a contagem após a padronização
agrupado = dataset.groupby(['Sexo']).size()
print(f"Contagem de registros por sexo após padronização:\n{agrupado}")

# Verificar dados ausentes
dadosausentes = dataset['Sexo'].isnull().sum()
print(f"Quantidade de dados ausentes na coluna 'Sexo': {dadosausentes}")

# Calcular a moda
modesex = dataset['Sexo'].mode()[0]
print(f"Moda do sexo: {modesex}")

# Preencher valores ausentes com a moda
dataset['Sexo'] = dataset['Sexo'].fillna(modesex)

# Verificar dados ausentes após preenchimento
dadosausentes_final = dataset['Sexo'].isnull().sum()
print(f"Quantidade de dados ausentes após o preenchimento: {dadosausentes_final}")

# Verificar contagem final
agrupado_final = dataset.groupby(['Sexo']).size()
print(f"Contagem final de registros por sexo:\n{agrupado_final}")

#Tratamento idade: a idade dos alunos deve ser considerada > 16 anos e menor que 60 anos
#utilizar a função loc para selecionar as idades e substituir pela mediana
# Calcular a mediana considerando apenas idades válidas
valid_ages = dataset.loc[(dataset['Idade'] > 16) & (dataset['Idade'] < 60), 'Idade']
mediana = valid_ages.median()  # ou sts.median(valid_ages) se preferir usar o stats
print(f"Mediana das idades válidas: {mediana}")

# Substituir idades inválidas pela mediana
dataset.loc[(dataset['Idade'] <= 16) | (dataset['Idade'] >= 60), 'Idade'] = mediana

# Preencher valores nulos com a mediana
dataset.fillna({'Idade':mediana},inplace=True)

# Converter para inteiro
dataset['Idade'] = dataset['Idade'].astype(int)

print(f"Quantidade total de alunos após tratamento: {len(dataset)}")
print(dataset.isnull().sum())

#Analise numérica do atributo IDADE
dataset['Idade'].describe()

#Calculo da Mediana do atributo IDADE
mediana = sts.median(dataset['Idade'])
mediana

srn.boxplot(dataset['Idade']).set_title('Idade ')

dataset['Idade'].describe()

#Os demais atributos qualitativos devem ter seus dados ausentes substituidos pela moda
# Contagem de registros por 'Ensino Médio'
# Lista de atributos qualitativos que precisam ser tratados
atributos_qualitativos = ['Ensino Médio','Cor/Raça', 'Estado Civil', 'Necessidade Especial declarada', 'Taxa de Inscrição']

# Tratamento para cada atributo
for atributo in atributos_qualitativos:
    print(f"\n----- Tratamento do atributo '{atributo}' -----")

    # Contagem de registros
    agrupado = dataset.groupby([atributo]).size()
    print(f"Contagem de registros por '{atributo}':\n{agrupado}")

    # Verificando dados ausentes
    dadosausentes = dataset[atributo].isnull().sum()
    print(f"Quantidade de dados ausentes na coluna '{atributo}': {dadosausentes}")

    # Calculando a moda
    if dadosausentes > 0:
        moda = dataset[atributo].mode()[0]
        print(f"Moda do '{atributo}': {moda}")

        # Preenchendo valores ausentes com a moda
        dataset[atributo] = dataset[atributo].fillna(moda)

        # Verificando se ainda há dados ausentes após o preenchimento
        dadosausentes_final = dataset[atributo].isnull().sum()
        print(f"Quantidade de dados ausentes após o preenchimento: {dadosausentes_final}")

        # Contagem de registros após o preenchimento
        agrupado_final = dataset.groupby([atributo]).size()
        print(f"Contagem de registros por '{atributo}' após o preenchimento:\n{agrupado_final}")
    else:
        print(f"Não há dados ausentes na coluna '{atributo}'.")

#O atributo data deve estar no formato dd/mm/aaaa
# Primeiro, verifique os formatos atuais
print("Valores únicos na coluna 'Data conclusão EM':")
print(dataset['Data conclusão EM'].unique())

# Importar biblioteca para manipulação de datas
import pandas as pd
from datetime import datetime

# Função para padronizar as datas
def padronizar_data(data_str):
    if pd.isna(data_str):
        return data_str

    # Para datas no formato "dd/mm/yy"
    try:
        data = datetime.strptime(data_str, '%d/%m/%y')
        return data.strftime('%d/%m/%Y')
    except:
        pass

    # Para datas no formato "dd de mês de aaaa"
    try:
        # Substituir nomes dos meses por números
        meses = {'janeiro': '01', 'fevereiro': '02', 'março': '03', 'abril': '04',
                 'maio': '05', 'junho': '06', 'julho': '07', 'agosto': '08',
                 'setembro': '09', 'outubro': '10', 'novembro': '11', 'dezembro': '12'}

        for mes_nome, mes_num in meses.items():
            if mes_nome in data_str.lower():
                partes = data_str.lower().replace(" de ", " ").split()
                dia = partes[0].zfill(2)  # Adiciona zero à esquerda se necessário
                ano = partes[2]
                if len(ano) == 2:  # Se o ano estiver no formato 'aa'
                    ano = '20' + ano  # Assumindo que todos os anos são do século 21
                return f"{dia}/{mes_num}/{ano}"
    except:
        pass

    # Se nenhum formato conhecido funcionar, retorna o original
    return data_str

# Aplicar a função à coluna de data
dataset['Data conclusão EM'] = dataset['Data conclusão EM'].apply(padronizar_data)

# Verificar o resultado
print("\nValores após padronização:")
print(dataset['Data conclusão EM'].unique())

# Preencher valores nulos com uma data padrão ou a moda
if dataset['Data conclusão EM'].isnull().sum() > 0:
    # Calcular a moda das datas
    moda_data = dataset['Data conclusão EM'].mode()[0]
    print(f"\nModa da data: {moda_data}")

    # Preencher valores nulos
    dataset['Data conclusão EM'] = dataset['Data conclusão EM'].fillna(moda_data)

    print(f"Quantidade de dados ausentes após o preenchimento: {dataset['Data conclusão EM'].isnull().sum()}")

display(dataset)