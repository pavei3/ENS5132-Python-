# -*- coding: utf-8 -*-
"""
Created on Mon May  5 22:44:02 2025

@author: bruno
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.ticker import ScalarFormatter

# =============================================
# 1. CONFIGURAÇÃO INICIAL
# =============================================
plt.style.use('seaborn-v0_8')
sns.set_theme(style="whitegrid")
palette = {
    "Destilados": "#1f77b4",
    "Vinho": "#ff7f0e", 
    "Chope e Cerveja": "#2ca02c"
}

# =============================================
# 2. CARREGAR E PREPARAR OS DADOS
# =============================================
caminho = r"C:\PythonBPG\Projetos\ENS5132-Python-\trabalho01\data\df_bebidas_para_analise.xlsx"
df = pd.read_excel(caminho)

# Verificar colunas necessárias
colunas_necessarias = ['cod_produto', 'num_ano', 'NMVOC (kg)']
for col in colunas_necessarias:
    if col not in df.columns:
        raise KeyError(f"Coluna '{col}' não encontrada no DataFrame")

# Classificar os tipos de bebida
df['tipo_bebida'] = df['cod_produto'].apply(lambda x: 
    'Destilados' if str(x).startswith('1111') else 
    'Vinho' if str(x).startswith('1112') else 
    'Chope e Cerveja')

# Filtrar apenas os tipos principais
df = df[df['tipo_bebida'].isin(palette.keys())]

# =============================================
# 3. PROCESSAR DADOS PARA O GRÁFICO DE LINHAS
# =============================================
# Agrupar por ano e tipo, calculando a média de emissões
dados_grafico = df.groupby(['num_ano', 'tipo_bebida'])['NMVOC (kg)'].mean().unstack()

print("\nDados agrupados para o gráfico:")
print(dados_grafico.head())

# =============================================
# 4. CRIAR GRÁFICO DE LINHAS
# =============================================
plt.figure(figsize=(12, 7))

# Plotar cada linha
for tipo in dados_grafico.columns:
    plt.plot(
        dados_grafico.index,
        dados_grafico[tipo],
        label=tipo,
        color=palette[tipo],
        linewidth=2.5,
        marker='o',
        markersize=8
    )

# Configurações do gráfico
plt.title('Evolução das Emissões Médias por Tipo de Bebida', fontsize=16, pad=20)
plt.xlabel('Ano', fontsize=14)
plt.ylabel('Emissões NMVOC (kg) - Média', fontsize=14)
plt.legend(title='Tipo de Bebida', fontsize=12)

# Formatar eixo Y para melhor visualização
plt.yscale('log')
plt.gca().yaxis.set_major_formatter(ScalarFormatter())
plt.grid(True, which="both", linestyle='--', alpha=0.4)

# Adicionar valores nos pontos
for tipo in dados_grafico.columns:
    for ano, valor in zip(dados_grafico.index, dados_grafico[tipo]):
        if not np.isnan(valor):
            plt.text(
                ano, 
                valor*1.1,  # Ajuste de posição
                f'{valor:,.1f}',
                ha='center',
                va='bottom',
                fontsize=9,
                color=palette[tipo]
            )

plt.tight_layout()
plt.savefig('evolucao_emissoes_tipos_bebida.png', dpi=300, bbox_inches='tight')
plt.show()

print("\nGráfico gerado com sucesso: 'evolucao_emissoes_tipos_bebida.png'")