# -*- coding: utf-8 -*-
"""
Created on Mon May  5 21:23:14 2025

@author: bruno
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Configuração de estilo
sns.set_theme(style="whitegrid")
sns.set_palette("husl")

# Carregar e preparar os dados
df = pd.read_excel(r"C:\PythonBPG\Projetos\ENS5132-Python-\trabalho01\data\df_bebidas_para_analise.xlsx")

# Classificar os tipos de bebida
df['tipo_bebida'] = df['cod_produto'].apply(lambda x: 
    'Destilados' if str(x).startswith('1111') else
    'Vinho' if str(x).startswith('1112') else
    'Chope e Cerveja')

# Filtrar apenas os 3 tipos principais
df = df[df['tipo_bebida'].isin(['Destilados', 'Vinho', 'Chope e Cerveja'])]

# Função para criar histogramas individuais
def criar_histograma(data, tipo, cor, num_bins=5):
    plt.figure(figsize=(10, 6))
    
    # Criar bins logarítmicos personalizados
    min_val = data['NMVOC (kg)'].min()
    max_val = data['NMVOC (kg)'].max()
    bins = np.logspace(np.log10(min_val), np.log10(max_val), num_bins+1)
    
    # Plotar histograma
    counts, bins, patches = plt.hist(
        data['NMVOC (kg)'],
        bins=bins,
        color=cor,
        edgecolor='black',
        alpha=0.7,
        log=True
    )
    
    # Configurações do gráfico
    plt.title(f'Distribuição de Emissões - {tipo}', fontsize=14)
    plt.xlabel('Emissões NMVOC (kg) - Escala Log', fontsize=12)
    plt.ylabel('Frequência (log)', fontsize=12)
    plt.xscale('log')
    plt.xticks(rotation=45)
    plt.grid(True, which="both", ls="--", alpha=0.3)
    
    # Formatador para eixos
    plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:,.1f}'))
    
    # Adicionar contagem nas barras
    for count, patch in zip(counts, patches):
        if count > 0:
            plt.text(
                patch.get_x() + patch.get_width()/2,
                count,
                f'{int(count)}',
                ha='center',
                va='bottom',
                fontsize=10
            )
    
    plt.tight_layout()
    plt.savefig(f'histograma_{tipo.lower().replace(" ", "_")}.png', dpi=300, bbox_inches='tight')
    plt.show()

# Gerar gráficos separados
for tipo, cor in [('Destilados', 'royalblue'), 
                  ('Vinho', 'crimson'), 
                  ('Chope e Cerveja', 'limegreen')]:
    subset = df[df['tipo_bebida'] == tipo]
    if not subset.empty:
        criar_histograma(subset, tipo, cor)
    else:
        print(f"Sem dados disponíveis para {tipo}")