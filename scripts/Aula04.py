# -*- coding: utf-8 -*-
"""
Created on Tue Apr  1 13:42:34 2025

Este script utilizei durante a aula 04 no dia 01/04/2025

@author: bruno
"""
#%%Sessão de importação
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
#%%Revisão numpy

#Criando um vetor com um arranjo de dados
x=np.arange(-10,20,0.15)
print(x)

#Brincando com indexação
print('Está é a quarta posição do meu vetor x:'+str(x[3])+'\n')
print(f'Está é outra forma de mostrar a quarta posição de x que é:{x[3]}\n')
print(f'Estes são os 3 primeiros valores:{x[0:3]}')

#Substituir um valor na mtriz
x[9]=99999999
x[11]=-99999999

#Extraindo a média
meanX=np.mean(x)
print(f'A média de X é:{meanX}')

#Operação booleana
vecBool=(x>20) | (x<-10) #símbolo | também significa or

#Extraindo valores errados usando lógica booleana
valErrado=x[vecBool]

#Substituindo os valores errados por 0
x2=x.copy() #Criando uma cópia independente, se n usar o .copy o que alterar em
            #um também vai alterar no outro
x2[vecBool]=0
print(f'Está é a média de x substituindo valores errados por 0:{np.mean(x2)}')

#substituindo por Nan - Not a Number
x3=x.copy()#criando uma cópia independente
x3[vecBool]=np.nan
print(f'Está é a média usando np.nanmean de x substituindo valores errados:\
      {np.nanmean(x3)}') 
    #se usar apenas np.mean ele não funciona por ter os valores nan no meio
    
#substituindo pela média
x4=x.copy()#criando uma cópia independente
x4[vecBool]=np.nanmean(x3)
print(f'Está é a média de x substituindo valores errados por nan:{np.mean(x4)}')    

#%% Usando matplotlib para inspecionar os vetores

fig,ax=plt.subplots(4)
ax[0].plot(x)
ax[1].plot(x2)
ax[2].plot(x3)
ax[3].plot(x4)

#%%Loops em pythonnn

for ii in range(0,10):
    val=2**ii
    print(val)
    
#%%Loop utilizando Range e acumulando o valor de val em um vetor
vetorAcumulado=[]
val=0
for ii in range(0,10):
    val=val+2**ii
    vetorAcumulado.append(val)
    print(vetorAcumulado)
    
#loop utilizando uma lista
alunas=['Mariana','Bianca','Ana Júlia','Mariah']

for aluna in alunas:
    print(f'A nota da {aluna} é: {np.random.rand(1)*(10)}')
    
#%%trabalhando com Pandas!!

#criando um dataframe manualmente
df=pd.DataFrame(columns=['date','NH3'], 
                data=[
                    ['2025/04/01',0.35],
                    ['2025/04/02',1.01],
                    ])

#criando mais coisas dentro do df
df['NO3']=np.nan
df['O2']=[2,10]
df['SO4']=np.nan
df['SO4'][0]=10
print(df)

#%%Trabalhando com dado real

#abrir este link https://energiaeambiente.org.br/qualidadedoar/ e baixar um dado de algum estado e dar unzip e jogar no dataframe no python?
#colocar na pasta data dentro de ENS5132 depois MQAR depois pasta com o dado tipo SP ou BH
#pode ser qualquer dado, não precisa ser de qualidade do ar, pode ser coisa aleatória do IBGE ou da ANA

UF='SP'
dataDir=r"C:\Users\bruno\OneDrive\Documentos\Documents\UFSC arquivos\Semestre 10\ENS5132-Python-\data\MQAR"+'/'+UF

#listando arquivos dentro da pasta
datalist=os.listdir(dataDir)

#movendo para a pasta de dados/UF
os.chdir(dataDir)

allFiles=[]
#loop na lista datalist
for fileInList in datalist:
    print(fileInList)
    dfConc=pd.read_csv(fileInList, encoding='Latin1')
    allFiles.append(dfConc)

#concatenando meus dataframes
allFiles=pd.concat(allFiles)

#extraindo nomes das estações sem redundância
sations=pd.unique(allFiles['Estacao'])

#usando lógica
stationDf=allFiles[allFiles['Estacao']==sations[0]]

#criando coluna datatime
datetimeDf=pd.to_datetime(stationDf.Data, format='%Y-%m-%d')

#criando coluna datetime dentro de stationDf
stationDf['datetime']=datetimeDf

#transformando a coluna de datetime em index
stationDf=stationDf.set_index(stationDf['datetime'])

#Extrair o ano
stationDf['year']=stationDf.index.year
stationDf['month']=stationDf.index.month
stationDf['day']=stationDf.index.day

#extraindo a hora
horas=stationDf.Hora.str.split(':')

for hora in horas:
    print(hora[0])
