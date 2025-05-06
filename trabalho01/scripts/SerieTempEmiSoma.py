# -*- coding: utf-8 -*-
"""
Created on Tue May  6 10:32:30 2025

@author: bruno
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.ticker import LogLocator, FuncFormatter

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
# 3. CALCULAR SOMAS ANUAIS
# =============================================
dados_grafico = df.groupby(['num_ano', 'tipo_bebida'])['NMVOC (kg)'].sum().unstack()

print("\nSomas anuais por tipo de bebida:")
print(dados_grafico)

# =============================================
# 4. CRIAR GRÁFICO DE LINHAS COM ESCALA LOG
# =============================================
plt.figure(figsize=(12, 7))

# Plotar cada linha em escala log
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
plt.title('Soma Anual de Emissões por Tipo de Bebida (Escala Log)', fontsize=16, pad=20)
plt.xlabel('Ano', fontsize=14)
plt.ylabel('Emissões NMVOC (kg) - Soma (log)', fontsize=14)
plt.legend(title='Tipo de Bebida', fontsize=12)

# Configurar escala logarítmica no eixo Y
plt.yscale('log')

# Formatador personalizado para eixo Y
def log_format(y, _):
    if y >= 1e6:
        return f"{y/1e6:,.1f}M"
    elif y >= 1e3:
        return f"{y/1e3:,.1f}k"
    return f"{y:,.1f}"

plt.gca().yaxis.set_major_formatter(FuncFormatter(log_format))
plt.gca().yaxis.set_minor_formatter(FuncFormatter(log_format))

# Configurar ticks
plt.gca().yaxis.set_major_locator(LogLocator(base=10, numticks=6))
plt.gca().yaxis.set_minor_locator(LogLocator(base=10, subs=np.arange(0.1, 1, 0.1), numticks=1))

plt.grid(True, which="both", linestyle='--', alpha=0.3)

# Adicionar valores nos pontos (em formato normal)
for tipo in dados_grafico.columns:
    for ano, valor in zip(dados_grafico.index, dados_grafico[tipo]):
        if not np.isnan(valor):
            plt.text(
                ano, 
                valor*1.1,  # Ajuste de posição
                f'{valor/1e6:,.1f}M' if valor >= 1e6 else f'{valor/1e3:,.1f}k',
                ha='center',
                va='bottom',
                fontsize=9,
                color=palette[tipo],
                bbox=dict(facecolor='white', alpha=0.7, edgecolor='none')
            )

plt.tight_layout()
plt.savefig('soma_anual_emissoes_log_tipos_bebida.png', dpi=300, bbox_inches='tight')
plt.show()

print("\nGráfico gerado com sucesso: 'soma_anual_emissoes_log_tipos_bebida.png'")