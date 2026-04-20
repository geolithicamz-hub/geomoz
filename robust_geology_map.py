#!/usr/bin/env python3
"""
Mapa robusto: Geologia de Zambezia sem complicações de CRS
"""

import sys
sys.path.insert(0, '.')

import geomoz
import matplotlib.pyplot as plt
import numpy as np

def robust_geology_map():
    """
    Criar mapa de geologia de Zambezia de forma simples e robusta
    """
    
    print("=== GeoMoz - Mapa Robusto: Geologia de Zambezia ===\n")
    
    # 1. Carregar dados
    print("1. Carregando geologia recortada por Zambezia...")
    geo_zambezia = geomoz.geology_by_province(name_province="Zambézia")
    print(f"   Unidades geológicas: {len(geo_zambezia)}")
    
    # 2. Carregar contorno
    print("2. Carregando contorno...")
    zambezia = geomoz.read_province(name_province="Zambézia")
    print(f"   Província: {zambezia.iloc[0]['Provincia']}")
    
    # 3. Escolher coluna principal
    print("3. Analisando colunas disponíveis...")
    if 'Legend' in geo_zambezia.columns:
        color_column = 'Legend'
        print("   Usando 'Legend' para coloração")
    elif 'Legenda' in geo_zambezia.columns:
        color_column = 'Legenda'
        print("   Usando 'Legenda' para coloração")
    else:
        color_column = 'ERA'
        print("   Usando 'ERA' para coloração")
    
    # 4. Estatísticas básicas
    print(f"\n4. Estatísticas por {color_column}:")
    value_counts = geo_zambezia[color_column].value_counts()
    print(f"   Valores únicos: {len(value_counts)}")
    print(f"\n   Top 15 valores:")
    for i, (value, count) in enumerate(value_counts.head(15).items(), 1):
        print(f"   {i:2d}. {value}: {count} unidades")
    
    # 5. Criar mapa simples
    print(f"\n5. Criando mapa visual...")
    
    # Configurar plot
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    
    # Plotar contorno da província
    zambezia.boundary.plot(ax=ax, color='black', linewidth=2, alpha=0.8)
    
    # Plotar geologia com colormap
    # Limitar para valores com mais de 5 unidades para melhor visualização
    significant_values = value_counts[value_counts > 5].index
    geo_filtered = geo_zambezia[geo_zambezia[color_column].isin(significant_values)]
    
    # Plotar
    geo_filtered.plot(
        ax=ax, 
        column=color_column, 
        cmap='tab20', 
        alpha=0.8, 
        linewidth=0.5,
        legend=True,
        legend_kwds={
            'bbox_to_anchor': (1.02, 1), 
            'loc': 'upper left',
            'title': color_column,
            'fontsize': 9,
            'ncol': 1
        }
    )
    
    # Configurar o mapa
    ax.set_title(f'Geologia de Zambézia\n(colorido por {color_column})', 
                fontsize=14, fontweight='bold')
    ax.set_xlabel('Longitude', fontsize=11)
    ax.set_ylabel('Latitude', fontsize=11)
    ax.grid(True, alpha=0.3)
    
    # Ajustar layout
    plt.tight_layout()
    plt.subplots_adjust(right=0.85)
    
    # Salvar
    output_file = 'geology_zambezia_robust.png'
    plt.savefig(output_file, dpi=200, bbox_inches='tight')
    print(f"\n6. Mapa salvo: {output_file}")
    
    # 7. Resumo final
    print(f"\n=== RESUMO FINAL ===")
    print(f"Província: Zambézia")
    print(f"Total de unidades: {len(geo_zambezia)}")
    print(f"Unidades plotadas: {len(geo_filtered)}")
    print(f"Coluna de cor: {color_column}")
    print(f"Valores significativos: {len(significant_values)}")
    
    # Mostrar plot
    plt.show()
    
    return geo_zambezia

def plot_by_suite():
    """
    Exemplo específico: plotar por suite geológica
    """
    print(f"\n=== Exemplo: Geologia por Suite ===\n")
    
    # Carregar geologia
    geo_zambezia = geomoz.geology_by_province(name_province="Zambézia")
    
    if 'SUITE' in geo_zambezia.columns:
        # Filtrar apenas unidades com suite
        geo_with_suite = geo_zambezia[geo_zambezia['SUITE'].notna()]
        print(f"Unidades com suite: {len(geo_with_suite)}")
        
        # Estatísticas por suite
        suite_counts = geo_with_suite['SUITE'].value_counts()
        print(f"\nTop 10 suites:")
        for i, (suite, count) in enumerate(suite_counts.head(10).items(), 1):
            print(f"   {i}. {suite}: {count} unidades")
        
        # Plotar mapa por suite
        fig, ax = plt.subplots(1, 1, figsize=(12, 8))
        
        # Contorno
        zambezia = geomoz.read_province(name_province="Zambézia")
        zambezia.boundary.plot(ax=ax, color='gray', linewidth=1, alpha=0.5)
        
        # Plotar por suite (apenas top 10 para legenda)
        top_suites = suite_counts.head(10).index
        geo_top_suites = geo_with_suite[geo_with_suite['SUITE'].isin(top_suites)]
        
        geo_top_suites.plot(
            ax=ax, 
            column='SUITE', 
            cmap='Set3', 
            alpha=0.8, 
            linewidth=0.5,
            legend=True,
            legend_kwds={
                'bbox_to_anchor': (1.02, 1), 
                'loc': 'upper left',
                'title': 'Suites',
                'fontsize': 9
            }
        )
        
        ax.set_title('Geologia de Zambézia por Suite', fontsize=14, fontweight='bold')
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.subplots_adjust(right=0.8)
        plt.savefig('geology_zambezia_by_suite.png', dpi=200, bbox_inches='tight')
        plt.show()
        
        print(f"\nMapa por suite salvo: geology_zambezia_by_suite.png")
    else:
        print("Coluna 'SUITE' não encontrada")

if __name__ == "__main__":
    # Executar mapa robusto
    geo_data = robust_geology_map()
    
    # Opcional: mapa por suite
    plot_by_suite()
    
    print(f"\n*** Mapa robusto de geologia concluído! ***")
