#!/usr/bin/env python3
"""
Exemplo: Buscar geologia de Zambezia e criar mapa visual
"""

import sys
sys.path.insert(0, '.')

import geomoz
import matplotlib.pyplot as plt
import geopandas as gpd

def plot_geology_zambezia():
    """
    Busca geologia da província de Zambezia e cria um mapa visual
    """
    
    print("=== GeoMoz - Mapa de Geologia: Zambezia ===\n")
    
    # 1. Carregar geologia recortada por Zambezia
    print("1. Carregando geologia recortada por Zambezia...")
    geo_zambezia = geomoz.geology_by_province(name_province="Zambézia")
    print(f"   Unidades geológicas encontradas: {len(geo_zambezia)}")
    
    # 2. Carregar contorno da província para contexto
    print("\n2. Carregando contorno da província...")
    zambezia = geomoz.read_province(name_province="Zambézia")
    print(f"   Província: {zambezia.iloc[0]['Provincia']}")
    
    # 3. Estatísticas básicas
    print("\n3. Estatísticas das unidades geológicas:")
    if 'Legend' in geo_zambezia.columns:
        legend_counts = geo_zambezia['Legend'].value_counts().head(10)
        for legend, count in legend_counts.items():
            print(f"   {legend}: {count} unidades")
    
    if 'ERA' in geo_zambezia.columns:
        era_counts = geo_zambezia['ERA'].value_counts()
        print(f"\n   Distribuição por ERA:")
        for era, count in era_counts.items():
            print(f"   {era}: {count} unidades")
    
    # 4. Criar mapa
    print("\n4. Criando mapa visual...")
    
    # Configurar o plot
    fig, ax = plt.subplots(1, 1, figsize=(15, 12))
    
    # Plotar contorno da província
    zambezia.boundary.plot(ax=ax, color='black', linewidth=2, alpha=0.8)
    
    # Plotar unidades geológicas com cores diferentes
    if 'Legend' in geo_zambezia.columns:
        # Limitar para as 15 unidades mais comuns para melhor visualização
        top_legends = geo_zambezia['Legend'].value_counts().head(15).index
        geo_filtered = geo_zambezia[geo_zambezia['Legend'].isin(top_legends)]
        
        # Plotar com cores baseadas no Legend
        geo_filtered.plot(ax=ax, column='Legend', cmap='tab20', 
                         alpha=0.8, legend=True, linewidth=0.5,
                         legend_kwds={'bbox_to_anchor': (1.05, 1), 
                                     'loc': 'upper left',
                                     'title': 'Unidades Geológicas',
                                     'fontsize': 8})
    else:
        # Se não tiver Legend, usar ERA
        if 'ERA' in geo_zambezia.columns:
            geo_zambezia.plot(ax=ax, column='ERA', cmap='Set3', 
                             alpha=0.7, legend=True, linewidth=0.5)
        else:
            geo_zambezia.plot(ax=ax, color='brown', alpha=0.7, 
                             linewidth=0.5, edgecolor='black')
    
    # Configurar o mapa
    ax.set_title('Geologia da Província de Zambézia', fontsize=16, fontweight='bold')
    ax.set_xlabel('Longitude', fontsize=12)
    ax.set_ylabel('Latitude', fontsize=12)
    ax.grid(True, alpha=0.3)
    
    # Ajustar layout manualmente para evitar erros
    plt.subplots_adjust(right=0.8)
    
    # Salvar o mapa
    output_file = 'geology_zambezia_map.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\n5. Mapa salvo como: {output_file}")
    
    # Mostrar estatísticas finais
    print(f"\n=== RESUMO FINAL ===")
    print(f"Província: {zambezia.iloc[0]['Provincia']}")
    print(f"Total de unidades geológicas: {len(geo_zambezia)}")
    print(f"Área total: {geo_zambezia.geometry.area.sum():.2f} unidades²")
    print(f"CRS: {geo_zambezia.crs}")
    
    # Mostrar o plot
    plt.show()
    
    return geo_zambezia, zambezia

def plot_specific_suite_zambezia(suite_name="Malema"):
    """
    Exemplo específico: buscar uma suite geológica específica em Zambezia
    """
    
    print(f"\n=== Suite Geológica Específica: {suite_name} ===\n")
    
    # Carregar suite específica em Zambezia
    geo_suite = geomoz.geology_by_province(
        name_province="Zambézia", 
        **{suite_name: suite_name}
    )
    
    print(f"Unidades da suite {suite_name} em Zambézia: {len(geo_suite)}")
    
    if len(geo_suite) > 0:
        # Criar mapa focado na suite
        fig, ax = plt.subplots(1, 1, figsize=(12, 10))
        
        # Plotar contorno da província
        zambezia = geomoz.read_province(name_province="Zambézia")
        zambezia.boundary.plot(ax=ax, color='gray', linewidth=1, alpha=0.5)
        
        # Plotar apenas a suite específica
        geo_suite.plot(ax=ax, color='red', alpha=0.8, 
                     linewidth=0.8, edgecolor='darkred')
        
        ax.set_title(f'Suite {suite_name} - Zambézia', 
                   fontsize=14, fontweight='bold')
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        ax.grid(True, alpha=0.3)
        
        # Salvar
        output_file = f'suite_{suite_name.lower()}_zambezia.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Mapa salvo como: {output_file}")
        
        plt.show()
        
        return geo_suite
    else:
        print(f"Nenhuma unidade da suite {suite_name} encontrada em Zambézia")
        return None

if __name__ == "__main__":
    # Executar o mapa principal de geologia
    geo_zambezia, zambezia = plot_geology_zambezia()
    
    # Opcional: mostrar uma suite específica
    # plot_specific_suite_zambezia("Malema")
    
    print("\n=== Mapa de geologia de Zambézia concluído! ===")
