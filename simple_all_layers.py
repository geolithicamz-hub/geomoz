#!/usr/bin/env python3
"""
Mapa simples: Todas as camadas geológicas com cores únicas
"""

import sys
sys.path.insert(0, '.')

import geomoz
import matplotlib.pyplot as plt

def plot_all_layers_simple():
    """
    Plotar todas as camadas geológicas de forma simples e robusta
    """
    
    print("=== GeoMoz - Mapa Simples: Todas as Camadas ===\n")
    
    # 1. Carregar dados
    province_name = "Zambézia"
    print(f"1. Carregando geologia de {province_name}...")
    
    geo = geomoz.geology_by_province(name_province=province_name)
    province = geomoz.read_province(name_province=province_name)
    
    print(f"   Unidades geológicas: {len(geo)}")
    print(f"   Província: {province.iloc[0]['Provincia']}")
    
    # 2. Analisar coluna Legend
    if 'Legend' not in geo.columns:
        print("ERRO: Coluna 'Legend' não encontrada")
        return None, None
    
    # 3. Estatísticas básicas
    print(f"\n2. Estatísticas por Legend:")
    value_counts = geo['Legend'].value_counts()
    print(f"   Valores únicos: {len(value_counts)}")
    
    print(f"\n   Top 15 valores:")
    for i, (legend, count) in enumerate(value_counts.head(15).items(), 1):
        print(f"   {i:2d}. {legend}: {count} unidades")
    
    # 4. Criar mapa simples
    print(f"\n3. Criando mapa...")
    
    # Limitar para valores com mais de 3 unidades para melhor visualização
    significant_values = value_counts[value_counts > 3].index
    geo_filtered = geo[geo['Legend'].isin(significant_values)]
    
    # Criar mapa
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    
    # Plotar contorno da província
    province.boundary.plot(ax=ax, color='black', linewidth=2, alpha=0.8)
    
    # Plotar geologia com cores
    geo_filtered.plot(
        ax=ax, 
        column='Legend', 
        cmap='tab20', 
        alpha=0.8, 
        linewidth=0.5,
        legend=True,
        legend_kwds={
            'bbox_to_anchor': (1.02, 1), 
            'loc': 'upper left',
            'title': 'Unidades Geológicas',
            'fontsize': 9,
            'ncol': 2
        }
    )
    
    # Configurar o mapa
    ax.set_title(f'Geologia de {province_name}\n({len(geo_filtered)} camadas)', 
                fontsize=14, fontweight='bold')
    ax.set_xlabel('Longitude', fontsize=11)
    ax.set_ylabel('Latitude', fontsize=11)
    ax.grid(True, alpha=0.3)
    
    # Salvar sem tight_layout para evitar erros
    output_file = f'geology_{province_name.lower().replace(" ", "_")}_simple.png'
    plt.savefig(output_file, dpi=200)
    print(f"\n4. Mapa salvo: {output_file}")
    
    # 5. Resumo final
    print(f"\n=== RESUMO ===")
    print(f"Província: {province_name}")
    print(f"Total de unidades: {len(geo)}")
    print(f"Unidades plotadas: {len(geo_filtered)}")
    print(f"Valores únicos: {len(value_counts)}")
    print(f"Valores significativos: {len(significant_values)}")
    
    # Mostrar o plot
    plt.show()
    
    return geo, province

def list_all_legends(province_name="Zambézia"):
    """
    Listar todas as legendas geológicas de uma província
    """
    print(f"\n=== Listagem: Legendas de {province_name} ===")
    
    geo = geomoz.geology_by_province(name_province=province_name)
    
    if 'Legend' in geo.columns:
        legends = geo['Legend'].value_counts()
        print(f"Total de legendas: {len(legends)}\n")
        
        for i, (legend, count) in enumerate(legends.items(), 1):
            print(f"{i:2d}. {legend}: {count} unidades")
        
        return legends
    else:
        print("Coluna 'Legend' não encontrada")
        return None

if __name__ == "__main__":
    # Executar mapa simples
    geo, province = plot_all_layers_simple()
    
    # Opcional: listar todas as legendas
    legends = list_all_legends(province_name)
    
    print(f"\n*** Mapa simples concluído! ***")
    print(f"*** {len(geo['Legend'].unique())} legendas geológicas plotadas! ***")
