# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.

Este script foi criado na terceira aula da disciplina ENS5132. Nesta aula, 
trabalharemos com:
    - Arrays numpy
    - Pandas dataframe
    - Matplotlib
    
    *requisitos: pip install numpy pandas matplotlib
"""
#%% Importação de pacotes

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt #pyplot são as funções de plotagem do matplotlib

#%% Relembrando listas

#criando uma lista com inteiros, string e float
listA = [1,2,3,'salve o corintians',20,5]
print(listA)

#criando uma lista com inteiros e float
listB=[1,2,3,20.5]

#%% Trabalhando com numpy

# Criando um array com numpy

arr = np.array([0.7,0.75,1.85,])
print(arr)

#criando um array numpy a partir de uma lista
arr2=np.array(listA)

#criando um array numpy a partir de uma lista apenas com números
arr3=np.array(listB)

#criando uma matriz
precip=np.array([[1.07,0.44,1.50],[0.27,1.33,1.72]])

#acessando valor da primeira linha e coluna
print(precip[0,0])

#acessando todos os valores da primeira linha
print(precip[0,:])
print(precip[:,0])
precipSlice=precip[:,0]

#extraindo os dois primeiros valores da primeira linha
print(precip[0,0:2])

#extraindo o último valor da última coluna
print(precip[-1,-1])

#---------------------------------------------------------------------

#criando matrizes com múltiplas dimensões

#criar um arranjo de dados com início, fim e passo
x=np.arange(1,16,1).reshape(1,15) 
y=np.arange(1,16,0.5)

xReshape=x.reshape(3,5)

print(xReshape.transpose())

#criando uma matriz de números aleatórios
matRand=np.random.rand(10,100,100)

#recortando a matriz
matRandSlice=matRand[0,:,:]

#dimensão da matriz
print(matRand.ndim)

#shape da matriz
print(matRand.shape)

#número de elementos
print(matRand.size)

#multiplicação escalar
print(matRand*3.9)

#abrir dados de um arquivo de texto
dataSample=np.loadtxt(r"C:\Users\bruno\OneDrive\Documentos\Documents\UFSC arquivos\Semestre 10\ENS5132-Python-\data\exemplo.txt")

#abrir arquivo .csv
dataSample2=np.loadtxt(r"C:\Users\bruno\OneDrive\Documentos\Documents\UFSC arquivos\Semestre 10\ENS5132-Python-\data\exemplo.csv",delimiter=',')

#%%
#criando uma matriz de números aleatórios 100x100
matriz2D100=np.random.rand(100,100)
print(matriz2D100)

matriz2D100Slice=matriz2D100[0,:]
print('Primeira linha:')
print(matriz2D100Slice)
print('Valor da última linha e coluna:')
print(matriz2D100[99,99])
#%%
