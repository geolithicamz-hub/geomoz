#!/usr/bin/env python3
"""
Mapa completo: Todas as camadas geológicas com cores únicas por nome
"""

import sys
sys.path.insert(0, '.')

import geomoz
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import pandas as pd
import geopandas as gpd

def get_utm_zone_for_mozambique(longitude):
    """
    Determinar a zona UTM correta para Moçambique baseado na longitude
    
    Parameters
    ----------
    longitude : float
        Longitude em graus
        
    Returns
    -------
    str
        Código EPSG da zona UTM apropriada
    """
    if 30 <= longitude < 36:
        return 'EPSG:32733'  # UTM Zone 33S
    elif 36 <= longitude < 42:
        return 'EPSG:32736'  # UTM Zone 36S  
    elif 42 <= longitude < 48:
        return 'EPSG:32737'  # UTM Zone 37S
    else:
        # Default para Zambezia
        return 'EPSG:32736'

def plot_all_layers_with_unique_colors():
    """
    Plotar todas as camadas geológicas de uma província com cores únicas
    """
    
    print("=== GeoMoz - Mapa Completo: Todas as Camadas ===\n")
    
    # 1. Escolher província (pode mudar aqui)
    province_name = "Zambézia"  # Pode mudar para "Nampula", "Tete", etc.
    
    print(f"1. Carregando dados da província: {province_name}")
    
    # 2. Carregar geologia recortada
    geo = geomoz.geology_by_province(name_province=province_name)
    province = geomoz.read_province(name_province=province_name)
    
    print(f"   Unidades geológicas: {len(geo)}")
    print(f"   Província: {province.iloc[0]['Provincia']}")
    print(f"   CRS original: {geo.crs}")
    
    # 2.1. Determinar automaticamente a zona UTM correta
    # Calcular centróide da província para determinar longitude
    centroid = province.geometry.centroid.iloc[0]
    longitude = centroid.x
    projected_crs = get_utm_zone_for_mozambique(longitude)
    
    print(f"   Convertendo para CRS projetado: {projected_crs}")
    print(f"   Longitude central: {longitude:.2f}°")
    geo_projected = geo.to_crs(projected_crs)
    province_projected = province.to_crs(projected_crs)
    print(f"   CRS projetado: {geo_projected.crs}")
    
    # 3. Analisar colunas disponíveis
    print("\n2. Analisando colunas geológicas...")
    geology_columns = [col for col in geo.columns 
                    if col in ['Legend', 'Legenda', 'ERA', 'EON', 'PERIOD', 
                               'SUITE', 'Formation', 'Group_', 'COMPLEX']]
    print(f"   Colunas disponíveis: {geology_columns}")
    
    # 4. Escolher coluna principal para coloração
    primary_column = None
    if 'Legend' in geo.columns:
        primary_column = 'Legend'
        print("   Usando coluna 'Legend' para coloração")
    elif 'Legenda' in geo.columns:
        primary_column = 'Legenda'
        print("   Usando coluna 'Legenda' para coloração")
    elif 'ERA' in geo.columns:
        primary_column = 'ERA'
        print("   Usando coluna 'ERA' para coloração")
    else:
        primary_column = 'code2006'
        print("   Usando coluna 'code2006' para coloração")
    
    # 5. Estatísticas detalhadas
    print(f"\n3. Estatísticas por {primary_column}:")
    value_counts = geo[primary_column].value_counts()
    print(f"   Total de valores únicos: {len(value_counts)}")
    
    # Calcular área total usando CRS projetado (em km²)
    total_area_km2 = geo_projected.geometry.area.sum() / 1_000_000  # Converter de m² para km²
    print(f"   Área total: {total_area_km2:.2f} km²")
    
    # Mostrar todas as categorias
    print(f"\n   Todas as categorias ({len(value_counts)}):")
    for i, (value, count) in enumerate(value_counts.items(), 1):
        # Calcular área por categoria usando CRS projetado
        subset_area = geo_projected[geo_projected[primary_column] == value].geometry.area.sum() / 1_000_000
        print(f"   {i:2d}. {value}: {count} unidades ({subset_area:.2f} km²)")
    
    # 6. Criar mapa com cores únicas para cada camada
    print(f"\n4. Criando mapa com cores únicas para cada {primary_column}...")
    
    # Preparar cores distintas para cada valor único
    unique_values = geo[primary_column].unique()
    n_values = len(unique_values)
    
    # Gerar paleta de cores distinta
    if n_values <= 12:
        colors = plt.cm.Set3(np.linspace(0, 1, n_values))
    elif n_values <= 24:
        colors = plt.cm.tab24(np.linspace(0, 1, n_values))
    else:
        # Para muitas categorias, usar colormap qualitativo
        colors = plt.cm.rainbow(np.linspace(0, 1, n_values))
    
    # Criar mapa - usar CRS original para visualização, mas CRS projetado para cálculos
    fig, ax = plt.subplots(1, 1, figsize=(18, 12))
    
    # Plotar contorno da província (CRS original para visualização)
    province.boundary.plot(ax=ax, color='black', linewidth=2, alpha=0.8)
    
    # Plotar cada camada geológica com sua cor única
    for i, value in enumerate(unique_values):
        subset = geo[geo[primary_column] == value]
        subset_projected = geo_projected[geo_projected[primary_column] == value]
        color = colors[i]
        
        # Verificar se subset não está vazio
        if not subset.empty:
            # Plotar a camada (CRS original para visualização)
            subset.plot(ax=ax, color=color, alpha=0.9, linewidth=0.3)
            
            # Adicionar rótulo para camadas maiores (mais de 50 unidades)
            if len(subset) > 50:
                # Calcular centróide usando CRS projetado (preciso)
                centroid = subset_projected.geometry.centroid.iloc[0]
                # Converter centróide de volta para CRS original para plotagem
                centroid_original = gpd.GeoSeries([centroid], crs=projected_crs).to_crs(geo.crs).iloc[0]
                
                if not (pd.isna(centroid_original.x) or pd.isna(centroid_original.y)):
                    ax.annotate(f'{value}', 
                               xy=(centroid_original.x, centroid_original.y),
                               xytext=(3, 3), textcoords='offset points',
                               fontsize=7, fontweight='bold',
                               bbox=dict(boxstyle='round,pad=0.3', 
                                          facecolor='white', alpha=0.9),
                               arrowprops=dict(arrowstyle='->', color='black'))
    
    # Configurar o mapa
    ax.set_title(f'Geologia Completa: {province_name}\n({n_values} camadas geológicas)', 
                fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Longitude', fontsize=12)
    ax.set_ylabel('Latitude', fontsize=12)
    ax.grid(True, alpha=0.2)
    
    # Criar legenda personalizada
    legend_elements = []
    for i, value in enumerate(unique_values):
        if i < 30:  # Limitar legenda para não ficar muito grande
            legend_elements.append(plt.Rectangle((0, 0), 1, 1, 
                                                fc=colors[i], label=str(value)))
    
    if legend_elements:
        # Configurar legenda em múltiplas colunas se necessário
        n_cols = 3 if len(legend_elements) > 15 else 2
        ax.legend(handles=legend_elements, 
                 bbox_to_anchor=(1.02, 1), loc='upper left',
                 title=primary_column, fontsize=8,
                 ncol=n_cols,
                 frameon=True)
    
    # Ajustar layout manualmente para evitar erros
    plt.subplots_adjust(right=0.85, left=0.05, top=0.95, bottom=0.05)
    
    # Salvar o mapa sem bbox_inches para evitar problemas
    output_file = f'geology_{province_name.lower().replace(" ", "_")}_all_layers.png'
    plt.savefig(output_file, dpi=200, pad_inches=0.5)
    print(f"\n5. Mapa salvo como: {output_file}")
    
    # 6. Resumo final detalhado
    print(f"\n=== RESUMO DETALHADO ===")
    print(f"Província: {province_name}")
    print(f"Total de camadas geológicas: {len(geo)}")
    print(f"Coluna de coloração: {primary_column}")
    print(f"Valores únicos: {n_values}")
    print(f"Camadas com rótulos: {sum(1 for subset in [geo[geo[primary_column] == value] for value in unique_values] if len(subset) > 50)}")
    print(f"Área total: {total_area_km2:.2f} km² (calculada com CRS projetado)")
    print(f"CRS original: {geo.crs}")
    print(f"CRS projetado: {geo_projected.crs}")
    
    # Mostrar o plot
    plt.show()
    
    return geo, province

def create_province_comparison(provinces=["Zambézia", "Nampula", "Tete"]):
    """
    Criar comparação visual entre múltiplas províncias
    """
    print(f"\n=== Comparação entre Províncias ===")
    
    fig, axes = plt.subplots(1, len(provinces), figsize=(20, 6*len(provinces)))
    
    for i, province_name in enumerate(provinces):
        ax = axes[i] if len(provinces) > 1 else axes
        
        # Carregar dados
        geo = geomoz.geology_by_province(name_province=province_name)
        province = geomoz.read_province(name_province=province_name)
        
        # Plotar
        province.boundary.plot(ax=ax, color='black', linewidth=1, alpha=0.8)
        geo.plot(ax=ax, column='Legend', cmap='tab20', alpha=0.7, linewidth=0.3)
        
        ax.set_title(f'{province_name}', fontsize=12, fontweight='bold')
        ax.set_xlabel('Longitude', fontsize=10)
        ax.set_ylabel('Latitude', fontsize=10)
        ax.grid(True, alpha=0.2)
        
        print(f"{province_name}: {len(geo)} unidades")
    
    # Ajustar layout manualmente
    plt.subplots_adjust(wspace=0.3, hspace=0.3)
    plt.savefig('geology_provinces_comparison.png', dpi=200, pad_inches=0.5)
    print(f"\nComparação salva: geology_provinces_comparison.png")
    plt.show()

if __name__ == "__main__":
    # Executar mapa completo
    geo, province = plot_all_layers_with_unique_colors()
    
    # Opcional: criar comparação entre províncias
    # create_province_comparison()
    
    print(f"\n*** Mapa completo de geologia concluído! ***")
    print(f"*** Todas as {len(geo['Legend'].unique())} camadas plotadas com cores únicas! ***")
