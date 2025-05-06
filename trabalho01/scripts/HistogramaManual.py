# -*- coding: utf-8 -*-
"""
Created on Mon May  5 21:41:26 2025

@author: bruno
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Carregar os dados
df = pd.read_excel(r"C:\PythonBPG\Projetos\ENS5132-Python-\trabalho01\data\df_bebidas_para_analise.xlsx")

# Classificação dos tipos de bebida
df['tipo_bebida'] = df['cod_produto'].apply(lambda x: 
    'Destilados' if str(x).startswith('1111') else 
    'Vinho' if str(x).startswith('1112') else 
    'Chope e Cerveja')

# Filtrar apenas os tipos principais
df = df[df['tipo_bebida'].isin(['Destilados', 'Vinho', 'Chope e Cerveja'])]

# Definir classes MANUALMENTE (ajuste esses valores conforme seus dados)
classes = [0, 20000, 40000, 60000, 80000, 100000]  # Exemplo: 5 classes (0-1k, 1k-5k, etc.)

# Configurar os gráficos
fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=True)
fig.suptitle('Distribuição de Emissões por Tipo de Bebida (Classes Manuais)', fontsize=14)

# Função para plotar com classes manuais
def plot_manual_bins(ax, data, tipo, cor):
    counts, bins, patches = ax.hist(
        data['NMVOC (kg)'],
        bins=classes,
        color=cor,
        edgecolor='black',
        alpha=0.7
    )
    
    ax.set_title(tipo)
    ax.set_xlabel('Emissões NMVOC (kg)')
    ax.set_ylabel('Frequência')
    ax.grid(True, linestyle='--', alpha=0.3)
    
    # Adicionar rótulos com contagem
    for count, rect in zip(counts, patches):
        height = rect.get_height()
        if height > 0:
            ax.text(
                rect.get_x() + rect.get_width()/2,
                height,
                f'{int(count)}',
                ha='center',
                va='bottom'
            )

# Plotar os 3 histogramas
tipos_cores = [
    ('Destilados', 'royalblue'),
    ('Vinho', 'firebrick'),
    ('Chope e Cerveja', 'limegreen')
]

for ax, (tipo, cor) in zip(axes, tipos_cores):
    subset = df[df['tipo_bebida'] == tipo]
    plot_manual_bins(ax, subset, tipo, cor)

plt.tight_layout()
plt.show()