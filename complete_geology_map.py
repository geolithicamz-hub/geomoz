#!/usr/bin/env python3
"""
Mapa completo: Todas as camadas geológicas de Zambezia com cores únicas
"""

import sys
sys.path.insert(0, '.')

import geomoz
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

def plot_complete_geology_zambezia():
    """
    Plotar todas as unidades geológicas de Zambezia com cores únicas
    """
    
    print("=== GeoMoz - Mapa Completo: Geologia de Zambezia ===\n")
    
    # 1. Carregar dados
    print("1. Carregando geologia recortada por Zambezia...")
    geo_zambezia = geomoz.geology_by_province(name_province="Nampula")
    print(f"   Unidades geológicas encontradas: {len(geo_zambezia)}")
    
    # 2. Carregar contorno
    print("2. Carregando contorno da província...")
    zambezia = geomoz.read_province(name_province="Nampula")
    print(f"   Província: {zambezia.iloc[0]['Provincia']}")
    
    # 3. Analisar colunas disponíveis
    print("3. Analisando colunas geológicas...")
    geology_columns = [col for col in geo_zambezia.columns 
                    if col in ['Legend', 'Legenda', 'ERA', 'EON', 'PERIOD', 
                               'SUITE', 'Formation', 'Group_', 'COMPLEX']]
    print(f"   Colunas geológicas: {geology_columns}")
    
    # 4. Escolher coluna principal para coloração
    primary_column = None
    if 'Legend' in geo_zambezia.columns:
        primary_column = 'Legend'
        print(f"   Usando coluna 'Legend' para coloração")
    elif 'Legenda' in geo_zambezia.columns:
        primary_column = 'Legenda'
        print(f"   Usando coluna 'Legenda' para coloração")
    elif 'ERA' in geo_zambezia.columns:
        primary_column = 'ERA'
        print(f"   Usando coluna 'ERA' para coloração")
    else:
        primary_column = 'code2006'
        print(f"   Usando coluna 'code2006' para coloração")
    
    # 5. Estatísticas
    print(f"\n4. Estatísticas por {primary_column}:")
    value_counts = geo_zambezia[primary_column].value_counts()
    print(f"   Valores únicos: {len(value_counts)}")
    print(f"   Top 10:")
    for i, (value, count) in enumerate(value_counts.head(10).items(), 1):
        print(f"   {i}. {value}: {count} unidades")
    
    # 6. Criar mapa com cores únicas
    print(f"\n5. Criando mapa com cores únicas por {primary_column}...")
    
    # Preparar cores
    unique_values = geo_zambezia[primary_column].unique()
    n_values = len(unique_values)
    
    # Gerar cores distintas
    if n_values <= 10:
        colors = plt.cm.tab10(np.linspace(0, 1, n_values))
    elif n_values <= 20:
        colors = plt.cm.tab20(np.linspace(0, 1, n_values))
    else:
        # Para muitas categorias, usar colormap qualitativo
        colors = plt.cm.rainbow(np.linspace(0, 1, n_values))
    
    # Criar mapa
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    
    # Plotar contorno da província
    zambezia.boundary.plot(ax=ax, color='black', linewidth=2, alpha=0.8)
    
    # Plotar cada unidade geológica com sua cor
    for i, value in enumerate(unique_values):
        subset = geo_zambezia[geo_zambezia[primary_column] == value]
        color = colors[i]
        
        # Plotar a unidade
        subset.plot(ax=ax, color=color, alpha=0.8, linewidth=0.5)
        
        # Adicionar rótulo para as maiores unidades
        if len(subset) > 50:  # Unidades grandes
            centroid = subset.geometry.centroid.iloc[0]
            ax.annotate(f'{value}', 
                       xy=(centroid.x, centroid.y),
                       xytext=(3, 3), textcoords='offset points',
                       fontsize=8, fontweight='bold',
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
    
    # Configurar o mapa
    ax.set_title(f'Geologia Completa: Zambézia\n({n_values} unidades geológicas)', 
                fontsize=16, fontweight='bold')
    ax.set_xlabel('Longitude', fontsize=12)
    ax.set_ylabel('Latitude', fontsize=12)
    ax.grid(True, alpha=0.3)
    
    # Criar legenda personalizada
    legend_elements = []
    for i, value in enumerate(unique_values):
        if i < 20:  # Limitar legenda para não ficar muito grande
            legend_elements.append(plt.Rectangle((0, 0), 1, 1, 
                                                fc=colors[i], label=str(value)))
    
    if legend_elements:
        ax.legend(handles=legend_elements, 
                 bbox_to_anchor=(1.02, 1), loc='upper left',
                 title=primary_column, fontsize=8,
                 ncol=2 if len(legend_elements) > 10 else 1)
    
    # Ajustar layout
    plt.subplots_adjust(right=0.85)
    
    # Salvar o mapa
    output_file = 'geology_zambezia_complete.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\n6. Mapa salvo como: {output_file}")
    
    # 7. Resumo final
    print(f"\n=== RESUMO FINAL ===")
    print(f"Província: {zambezia.iloc[0]['Provincia']}")
    print(f"Total de unidades geológicas: {len(geo_zambezia)}")
    print(f"Coluna usada para coloração: {primary_column}")
    print(f"Valores únicos: {n_values}")
    print(f"Área aproximada: {geo_zambezia.geometry.area.sum():.2f} graus²")
    print(f"CRS: {geo_zambezia.crs}")
    
    # Mostrar o plot
    plt.show()
    
    return geo_zambezia, zambezia

def plot_by_formation():
    """
    Exemplo específico: plotar por formação geológica
    """
    print(f"\n=== Exemplo: Geologia por Formação ===\n")
    
    # Carregar geologia por formação
    geo_zambezia = geomoz.geology_by_province(name_province="Zambézia")
    
    if 'Formation' in geo_zambezia.columns:
        # Estatísticas por formação
        formation_counts = geo_zambezia['Formation'].value_counts()
        print(f"Formações únicas: {len(formation_counts)}")
        print("\nTop 15 formações:")
        for i, (formation, count) in enumerate(formation_counts.head(15).items(), 1):
            print(f"   {i}. {formation}: {count} unidades")
        
        # Plotar por formação
        fig, ax = plt.subplots(1, 1, figsize=(14, 10))
        
        # Contorno
        zambezia = geomoz.read_province(name_province="Nampula")
        zambezia.boundary.plot(ax=ax, color='black', linewidth=1, alpha=0.5)
        
        # Apenas formações com dados
        geo_with_formation = geo_zambezia[geo_zambezia['Formation'].notna()]
        geo_with_formation.plot(ax=ax, column='Formation', cmap='Set3', 
                              alpha=0.8, legend=True, linewidth=0.5,
                              legend_kwds={'bbox_to_anchor': (1.05, 1), 
                                          'loc': 'upper left',
                                          'title': 'Formações',
                                          'fontsize': 9,
                                          'ncol': 2})
        
        ax.set_title('Geologia de Zambézia por Formação', 
                    fontsize=14, fontweight='bold')
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        ax.grid(True, alpha=0.3)
        
        plt.subplots_adjust(right=0.8)
        plt.savefig('geology_zambezia_by_formation.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"\nMapa por formação salvo: geology_zambezia_by_formation.png")
    else:
        print("Coluna 'Formation' não encontrada nos dados")

if __name__ == "__main__":
    # Executar o mapa completo
    geo_zambezia, zambezia = plot_complete_geology_zambezia()
    
    # Opcional: mapa por formação
    plot_by_formation()
    
    print(f"\n*** Mapa completo de geologia de Zambézia concluído! ***")
