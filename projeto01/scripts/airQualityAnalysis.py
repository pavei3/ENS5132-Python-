# -*- coding: utf-8 -*-
"""
Created on Tue Apr  8 13:48:11 2025

Este script será utilizado para analisar os dados de qualidade do ar disponibi-
lizados pela plataforma do Instituto Energia e Meio Ambiente.

 Abrir corretamente o dado
 Inserir coluna datetime 
 Criar coluna com estação do ano
 Filtrar dataframe
 Extrair estatísticas básicas
 Estatísticas por agrupamento
 Exportar estatísticas agrupadas
 Criar uma função para realizar as tarefas acima
 Criar função para gerar figuras
 Loop para qualquer arquivo dentro da pasta
 Estatística univariada e bivariada – função exclusiva
 Análise de dados usando o statsmodel

@author: bruno
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

#---------------------------------abrir os dados-------------------------------
uf='SP'
dataDir=r"C:\Users\bruno\OneDrive\Documentos\Documents\UFSC arquivos\Semestre 10\ENS5132-Python-\data\MQAR"+'/'+uf

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

#abrir os dados de apenas uma das estações
aqPath=r"C:\Users\bruno\OneDrive\Documentos\Documents\UFSC arquivos\Semestre 10\ENS5132-Python-\projeto01\inputs\SP\SP201501.csv"

aqData=pd.read_csv(aqPath,encoding='latin1')

#---------------------------inserir coluna datetime----------------------------
#criando coluna datatime
datetimeDf=pd.to_datetime(aqData.Data, format='%Y-%m-%d')

#criando coluna datetime dentro de aqData
aqData['datetime']=datetimeDf

#transformando a coluna de datetime em index
aqData=aqData.set_index(aqData['datetime'])

#Extrair o ano
aqData['year']=aqData.index.year
aqData['month']=aqData.index.month
aqData['day']=aqData.index.day

#extraindo a hora
horas=aqData.Hora.str.split(':')

horaDf=[]
for hora in horas:
    print(hora[0])
    horaDf.append(hora[0])

aqData['hour']=horaDf

#corrigindo a coluna datetime
aqData['datetime']=pd.to_datetime(aqData[['year','month','day','hour']],format='%Y%m%d %H')

#reiniciando minha index datetime
aqData=aqData.set_index(aqData['datetime'])


#-----------------------------------------estação do ano-----------------------
#criando uma coluna vazia com NaN
aqData['Estacao']=np.nan

#verão
aqData['Estacao'][(aqData.month==1) | (aqData.month==12) |
                  (aqData.month==2)]='Verão'

#outono
aqData['Estacao'][(aqData.month==3) | (aqData.month==4) |
                  (aqData.month==5)]='Outono'

#inverno
aqData['Estacao'][(aqData.month==6) | (aqData.month==7) |
                  (aqData.month==8)]='Inverno'

#primavera
aqData['Estacao'][(aqData.month==9) | (aqData.month==10) |
                  (aqData.month==11)]='Primavera'

#----------------------------------estatísticas básicas------------------------
#extrair o nome dos poluentes sem redundância
pollutants=np.unique(aqData.Poluente)

#lista de estações
stations=np.unique(aqData.Estacao)

#criando pasta para salvar
os.makedirs(r"C:\Users\bruno\OneDrive\Documentos\Documents\UFSC arquivos\Semestre 10\ENS5132-Python-\projeto01\outputs" +'/'+uf)

#loop para cada poluente e extrainndo as estatísticas básicas
for st in stations:
    print(st)
    statAll=[]
    for pol in pollutants:
        print(pol)
        basicStat=aqData['Valor'][(aqData.Poluente==pol) & 
                                  (aqData.estacao==st)].describe()
        basicStat=pd.DataFrame(basicStat)
        basicStat.columns=[pol]
        statAll.append(basicStat)
        
    #unindo as estatísticas por poluente        
    dfmerge=pd.concat(statAll,axis=1)

    #salva as estatísticas por estação
    basicStat.to_csv(r"C:\Users\bruno\OneDrive\Documentos\Documents\UFSC arquivos\Semestre 10\ENS5132-Python-\projeto01\outputs" 
                             +'/'+uf+'/basicStat_'+pol+'.csv')

#estística básica usando groupby
statGroup=aqData.groupby(['Estacao'])

