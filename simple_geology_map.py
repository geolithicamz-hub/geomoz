#!/usr/bin/env python3
"""
Versão simplificada: Mapa de geologia por província usando Legend
"""

import sys
sys.path.insert(0, '.')

import geomoz
import matplotlib.pyplot as plt

def simple_geology_map(province_name="Zambézia"):
    """
    Criar um mapa simples de geologia por província usando Legend
    """
    
    print(f"=== Mapa Simples: Geologia de {province_name} ===\n")
    
    # 1. Carregar dados
    print("1. Carregando dados...")
    geo = geomoz.geology_by_province(name_province=province_name)
    province = geomoz.read_province(name_province=province_name)
    
    print(f"   Unidades geológicas: {len(geo)}")
    print(f"   Província: {province.iloc[0]['Provincia']}")
    
    # 2. Estatísticas rápidas
    print(f"\n2. Top 10 unidades geológicas:")
    top_units = geo['Legend'].value_counts().head(10)
    for i, (legend, count) in enumerate(top_units.items(), 1):
        print(f"   {i}. {legend}: {count} unidades")
    
    # 3. Criar mapa simples
    print(f"\n3. Criando mapa...")
    
    fig, ax = plt.subplots(1, 1, figsize=(12, 10))
    
    # Plotar contorno da província
    province.boundary.plot(ax=ax, color='black', linewidth=2, alpha=0.8)
    
    # Plotar apenas as 10 unidades mais comuns para melhor visualização
    top_legends = geo['Legend'].value_counts().head(2129).index
    geo_top = geo[geo['Legend'].isin(top_legends)]
    
    # Plotar com cores
    geo_top.plot(ax=ax, column='Legend', cmap='tab10', 
                alpha=0.8, legend=True, linewidth=0.5,
                legend_kwds={'bbox_to_anchor': (1.05, 1), 
                            'loc': 'upper left',
                            'title': 'Top 10 Unidades',
                            'fontsize': 9})
    
    # Configurações
    ax.set_title(f'Geologia: {province_name} (Top 10 Unidades)', 
                fontsize=14, fontweight='bold')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.grid(True, alpha=0.3)
    
    # Ajustar e salvar
    plt.subplots_adjust(right=0.75)
    filename = f'geology_{province_name.lower().replace(" ", "_")}_simple.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"   Mapa salvo: {filename}")
    
    # Estatísticas finais
    print(f"\n=== RESUMO ===")
    print(f"Província: {province_name}")
    print(f"Total unidades: {len(geo)}")
    print(f"Top 10 mostradas: {len(geo_top)}")
    print(f"Unidades não mostradas: {len(geo) - len(geo_top)}")
    
    plt.show()
    
    return geo, province

if __name__ == "__main__":
    # Testar com Zambezia
    geo, province = simple_geology_map("Zambézia")
    
    print(f"\n*** Mapa simples concluído! ***")
