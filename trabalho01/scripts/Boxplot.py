# -*- coding: utf-8 -*-
"""
Created on Mon May  5 22:38:43 2025

@author: bruno
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.ticker import LogFormatter, LogLocator

# =============================================
# 1. CONFIGURAÇÃO INICIAL
# =============================================
plt.style.use('seaborn-v0_8')
sns.set_theme(style="whitegrid")
palette = {
    "Destilados": "#1f77b4",
    "Vinho": "#ff7f0e", 
    "Cerveja e Chope": "#2ca02c"  # Corrigido para corresponder ao nome na coluna 'Tipo'
}

# =============================================
# 2. CARREGAR E DIVIDIR O DATAFRAME
# =============================================
def carregar_e_dividir_dados(caminho):
    try:
        # Carregar dados - USAR read_csv PARA ARQUIVO CSV
        df = pd.read_csv(caminho)
        
        # Verificar colunas necessárias
        colunas_necessarias = ['Tipo', 'NMVOC (kg)']
        for col in colunas_necessarias:
            if col not in df.columns:
                raise KeyError(f"Coluna '{col}' não encontrada no DataFrame")
        
        # Converter coluna NMVOC para numérico
        df['NMVOC (kg)'] = pd.to_numeric(df['NMVOC (kg)'], errors='coerce')
        
        # Remover valores inválidos
        df = df[df['NMVOC (kg)'].notna() & (df['NMVOC (kg)'] > 0)]
        
        # Dividir em DataFrames separados
        destilados = df[df['Tipo'] == 'Destilados'].copy()
        vinhos = df[df['Tipo'] == 'Vinho'].copy()
        cervejas = df[df['Tipo'] == 'Cerveja e Chope'].copy()  # Nome corrigido
        
        # Verificar se não estão vazios
        print("\nContagem de registros por tipo:")
        print(f"Destilados: {len(destilados)} registros")
        print(f"Vinhos: {len(vinhos)} registros")
        print(f"Cerveja e Chope: {len(cervejas)} registros")
        
        return destilados, vinhos, cervejas
    
    except Exception as e:
        print(f"Erro ao carregar e dividir dados: {e}")
        return None, None, None

# =============================================
# 3. FUNÇÃO PARA CRIAR BOXPLOTS
# =============================================
def criar_boxplot(data, tipo, cor):
    try:
        if data.empty:
            print(f"\nAviso: DataFrame vazio para {tipo}")
            return
        
        plt.figure(figsize=(10, 8))
        
        # Configurar escala log
        ax = sns.boxplot(
            y=data['NMVOC (kg)'],
            color=cor,
            width=0.6,
            showfliers=False
        )
        ax.set_yscale('log')
        
        # Formatar eixo Y
        class CustomLogFormatter(LogFormatter):
            def __call__(self, x, pos=None):
                if x < 1:
                    return f"{x:.1f}"
                return f"{x:,.0f}"  # Formato sem notação científica
        
        ax.yaxis.set_major_formatter(CustomLogFormatter(labelOnlyBase=False))
        
        # Adicionar outliers manualmente
        q1, q3 = data['NMVOC (kg)'].quantile([0.25, 0.75])
        iqr = q3 - q1
        outliers = data[data['NMVOC (kg)'] > q3 + 1.5*iqr]
        ax.scatter(
            x=np.random.normal(0, 0.05, size=len(outliers)),
            y=outliers['NMVOC (kg)'],
            color='#333333',
            alpha=0.5,
            s=30
        )
        
        # Adicionar estatísticas
        stats = data['NMVOC (kg)'].describe()
        textstr = (f"Média: {stats['mean']/1e6:,.2f} × 10⁶ kg\n"
                  f"Mediana: {stats['50%']:,.1f} kg\n"
                  f"Q1-Q3: {stats['25%']:,.1f}-{stats['75%']:,.1f} kg\n"
                  f"Outliers: {len(outliers)} pontos")
        
        plt.text(0.95, 0.95, textstr, transform=ax.transAxes,
                fontsize=10,
                bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'),
                verticalalignment='top', horizontalalignment='right')
        
        plt.title(f'Distribuição de Emissões - {tipo}', fontsize=14)
        plt.ylabel('Emissões NMVOC (kg) - Escala Log', fontsize=12)
        plt.xlabel('')
        plt.grid(True, axis='y', which='major', linestyle='--', alpha=0.5)
        
        plt.tight_layout()
        plt.savefig(f'boxplot_{tipo.lower().replace(" ", "_")}.png', dpi=300)
        plt.show()
        
    except Exception as e:
        print(f"Erro ao criar boxplot para {tipo}: {e}")

# =============================================
# 4. EXECUÇÃO PRINCIPAL
# =============================================
caminho = r"C:\PythonBPG\Projetos\ENS5132-Python-\trabalho01\data\df_bebidas_cnpj_agg.csv"

# Dividir o DataFrame principal em 3
destilados, vinhos, cervejas = carregar_e_dividir_dados(caminho)

# Verificar e gerar gráficos
if destilados is not None:
    print("\nGerando gráficos...")
    
    # Lista de DataFrames e suas configurações
    dados_graficos = [
        (destilados, "Destilados", palette["Destilados"]),
        (vinhos, "Vinho", palette["Vinho"]),
        (cervejas, "Cerveja e Chope", palette["Cerveja e Chope"])
    ]
    
    for df_tipo, nome_tipo, cor in dados_graficos:
        if df_tipo is not None and not df_tipo.empty:
            print(f"\nProcessando {nome_tipo}...")
            criar_boxplot(df_tipo, nome_tipo, cor)
        else:
            print(f"\nAviso: Nenhum dado válido para {nome_tipo}")

print("\nProcesso finalizado. Verifique os arquivos gerados:")
print("boxplot_destilados.png")
print("boxplot_vinho.png")
print("boxplot_cerveja_e_chope.png")