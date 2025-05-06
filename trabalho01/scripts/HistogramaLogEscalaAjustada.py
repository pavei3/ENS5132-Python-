# -*- coding: utf-8 -*-
"""
Created on Mon May  5 21:52:54 2025

@author: bruno
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.ticker import EngFormatter

# =============================================
# 1. CONFIGURAÇÃO INICIAL
# =============================================
plt.style.use('seaborn-v0_8')  # Estilo moderno
sns.set_theme(style="whitegrid")  # Tema do Seaborn
sns.set_palette("husl")  # Paleta de cores

# =============================================
# 2. CARREGAMENTO E PREPARAÇÃO DOS DADOS
# =============================================
caminho = r"C:\PythonBPG\Projetos\ENS5132-Python-\trabalho01\data\df_bebidas_para_analise.xlsx"
df = pd.read_excel(caminho)

# Classificação dos tipos de bebida
df['tipo_bebida'] = df['cod_produto'].apply(lambda x: 
    'Destilados' if str(x).startswith('1111') else
    'Vinho' if str(x).startswith('1112') else
    'Chope e Cerveja')

# Filtrar apenas os tipos principais
df = df[df['tipo_bebida'].isin(['Destilados', 'Vinho', 'Chope e Cerveja'])]

# =============================================
# 3. FUNÇÃO PARA CRIAR HISTOGRAMAS LOG
# =============================================
def criar_histograma_log(data, tipo, cor):
    plt.figure(figsize=(10, 6))
    
    # Configuração dos bins (5 classes logarítmicas)
    bins = np.logspace(
        np.log10(max(0.1, data['NMVOC (kg)'].min())),  # Evitar log(0)
        np.log10(data['NMVOC (kg)'].max()), 
        6  # 5 classes (6 bordas)
    )
    
    # Plotagem do histograma
    counts, bins, patches = plt.hist(
        data['NMVOC (kg)'],
        bins=bins,
        color=cor,
        edgecolor='black',
        alpha=0.7,
        log=True  # Escala log no eixo Y
    )
    
    # Formatação científica no eixo X
    formatter = EngFormatter(unit='kg', places=1)  # Ex: 10³ kg
    plt.gca().xaxis.set_major_formatter(formatter)
    plt.xscale('log')
    
    # Configurações estéticas
    plt.title(f'Distribuição de Emissões - {tipo}', fontsize=14, pad=20)
    plt.xlabel('Emissões NMVOC', fontsize=12)
    plt.ylabel('Frequência (log)', fontsize=12)
    plt.xticks(rotation=45, ha='right')  # Rótulos inclinados
    plt.grid(True, which="both", ls="--", alpha=0.3)
    
    # Adicionar contagens nas barras
    for count, patch in zip(counts, patches):
        if count > 0:
            plt.text(
                patch.get_x() + patch.get_width()/2,
                count,
                f'{int(count)}',
                ha='center',
                va='bottom',
                fontsize=10,
                bbox=dict(facecolor='white', alpha=0.7, edgecolor='none')
            )
    
    plt.tight_layout()
    plt.savefig(f'histograma_log_{tipo.lower().replace(" ", "_")}.png', 
                dpi=300, 
                bbox_inches='tight')
    plt.show()

# =============================================
# 4. GERAR GRÁFICOS INDIVIDUAIS
# =============================================
cores = {
    'Destilados': '#1f77b4',  # Azul
    'Vinho': '#d62728',       # Vermelho
    'Chope e Cerveja': '#2ca02c'  # Verde
}

for tipo, cor in cores.items():
    subset = df[df['tipo_bebida'] == tipo]
    if not subset.empty:
        print(f"\nGerando gráfico para {tipo}...")
        print(f"Estatísticas descritivas:\n{subset['NMVOC (kg)'].describe()}")
        criar_histograma_log(subset, tipo, cor)
    else:
        print(f"\nAtenção: Nenhum dado encontrado para {tipo}")

print("\nProcesso concluído! Gráficos salvos no diretório atual.")