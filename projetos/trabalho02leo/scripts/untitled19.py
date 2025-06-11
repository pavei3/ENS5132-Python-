# -*- coding: utf-8 -*-
"""
Created on Mon Jun  9 11:32:36 2025

@author: bruno
"""

import numpy as np
import rasterio
import matplotlib.pyplot as plt
import geopandas as gpd
from rasterio.mask import mask
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
import os

# --- Caminhos Fixos ---
CaminhoBaseRaster = r"C:\PythonBPG\Projetos\ENS5132-Python-\data\ColnizaMT"
CaminhoShape = r"C:\PythonBPG\Projetos\ENS5132-Python-\data\LimiteColniza.shp"

# Anos que você quer processar
anos = [2000, 2010, 2020, 2021, 2022, 2023]

# Abrir shapefile (uma vez)
colniza = gpd.read_file(CaminhoShape)

# Definir colormap (0 = verde, 1 = vermelho)
cores = ["green", "red"]
cmap = ListedColormap(cores)

# --- Função para gerar o mapa ---
def gerar_mapa_recortado(ano, colniza_gdf, colormap):
    """
    Gera um mapa de área queimada recortado pelo limite municipal para um dado ano,
    incluindo a contagem de pixels queimados na legenda.

    Args:
        ano (int): O ano do raster a ser processado.
        colniza_gdf (geopandas.GeoDataFrame): O GeoDataFrame com o limite municipal.
        colormap (matplotlib.colors.ListedColormap): O colormap para o raster.
    """
    print(f"Processando ano: {ano}...")

    caminho_raster_ano = f"{CaminhoBaseRaster}{ano}.tif"

    if not os.path.exists(caminho_raster_ano):
        print(f"Aviso: Raster para o ano {ano} não encontrado em {caminho_raster_ano}. Pulando este ano.")
        return

    try:
        with rasterio.open(caminho_raster_ano) as src:
            if colniza_gdf.crs != src.crs:
                colniza_reprojetado = colniza_gdf.to_crs(src.crs)
            else:
                colniza_reprojetado = colniza_gdf

            nodata_value = 255 # Valor nodata para o recorte

            recorte_arr, recorte_transform = mask(src, colniza_reprojetado.geometry, crop=True, nodata=nodata_value)
            
            # Selecionar a primeira banda e converter para float32 para lidar com NaN
            data_plot = recorte_arr[0].astype(np.float32)
            
            # --- Contagem de pixels queimados ---
            # Antes de substituir nodata_value por NaN, contamos os pixels '1'.
            # Isso garante que não contemos NaN's ou nodata como '1'.
            # A contagem é feita APENAS para os pixels dentro do limite do shapefile,
            # ou seja, aqueles que NÃO SÃO o nodata_value.
            
            # Criamos uma cópia temporária para contar antes de introduzir NaNs
            data_temp_for_count = recorte_arr[0]
            
            # Filtra apenas os pixels que não são o nodata_value e que são iguais a 1
            pixels_queimados = np.sum((data_temp_for_count == 1) & (data_temp_for_count != nodata_value))
            
            # Agora, substitua o valor nodata por NaN para transparência no plot
            data_plot[data_plot == nodata_value] = np.nan

            # --- Visualização ---
            fig, ax = plt.subplots(figsize=(10, 10))

            img = ax.imshow(data_plot, cmap=colormap, interpolation='none',
                            extent=rasterio.plot.plotting_extent(data_plot, recorte_transform),
                            origin='upper', vmin=0, vmax=1)

            colniza_reprojetado.boundary.plot(ax=ax, edgecolor='black', linewidth=1.5)

            # --- Legenda personalizada com contagem de pixels ---
            legenda = [
                Patch(color='red', label=f'Área Queimada ({pixels_queimados})'), # Adiciona a contagem aqui
                Patch(color='green', alpha=0.3, label='Território Colniza'),
            ]
            ax.legend(handles=legenda, loc='upper right')

            # Título e eixos
            ax.set_title(f"Áreas Queimadas - Colniza/MT ({ano})")
            ax.set_xlabel("Longitude")
            ax.set_ylabel("Latitude")
            plt.grid(True)
            plt.tight_layout()
            plt.show()

    except Exception as e:
        print(f"Erro ao processar o ano {ano}: {e}")

# --- Loop para gerar os mapas ---
for ano in anos:
    # A função agora não precisa mais receber a 'legenda' pois ela é criada dentro
    gerar_mapa_recortado(ano, colniza, cmap)

print("Processamento de todos os mapas concluído.")