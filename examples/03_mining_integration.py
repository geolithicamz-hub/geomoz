#!/usr/bin/env python3
"""
Exemplo 03: Integração com Dados de Mineração
Demonstra como integrar dados geológicos com informações de mineração
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import geomoz
from matplotlib.colors import ListedColormap
import matplotlib.patches as mpatches

def create_mining_integration_map():
    """Criar mapa de integração geologia-mineração"""

    print("Criando mapa de integração geologia-mineração...")

    # Carregar dados
    print("Carregando dados geológicos...")
    geology = geomoz.read_geology()
    provinces = geomoz.read_province()

    # Dados de mineração simulados (exemplo)
    mining_data = {
        'Moatize': {
            'commodities': ['Carvão', 'Areia', 'Argila'],
            'companies': 5,
            'production': '2.5M toneladas/ano'
        },
        'Tete': {
            'commodities': ['Carvão', 'Titânio', 'Grafite'],
            'companies': 12,
            'production': '15.2M toneladas/ano'
        },
        'Manica': {
            'commodities': ['Ouro', 'Diamante', 'Cobre'],
            'companies': 8,
            'production': '0.8M toneladas/ano'
        },
        'Cabo Delgado': {
            'commodities': ['Gás Natural', 'Petróleo', 'Sal'],
            'companies': 3,
            'production': '1.2M barris/ano'
        },
        'Sofala': {
            'commodities': ['Carvão', 'Areia', 'Argila'],
            'companies': 7,
            'production': '3.1M toneladas/ano'
        },
        'Gaza': {
            'commodities': ['Areia', 'Argila'],
            'companies': 2,
            'production': '0.5M toneladas/ano'
        },
        'Inhambane': {
            'commodities': ['Carvão', 'Areia'],
            'companies': 4,
            'production': '1.8M toneladas/ano'
        },
        'Nampula': {
            'commodities': ['Titânio', 'Grafite', 'Areia'],
            'companies': 10,
            'production': '8.5M toneladas/ano'
        },
        'Niassa': {
            'commodities': ['Ouro', 'Diamante', 'Pedras preciosas'],
            'companies': 6,
            'production': '0.3M toneladas/ano'
        },
        'Maputo': {
            'commodities': ['Areia', 'Argila'],
            'companies': 15,
            'production': '4.2M toneladas/ano'
        }
    }

    # Integrar dados de mineração com geologia
    print("Integrando dados de mineração com geologia...")

    for _, province in provinces.iterrows():
        prov_name = province['Provincia']
        if prov_name in mining_data:
            # Simular integração dos dados
            mining_info = mining_data[prov_name]
            province['mining_companies'] = mining_info['companies']
            province['mining_production'] = mining_info['production']
            province['mining_commodities'] = ', '.join(mining_info['commodities'])

    # Interceptar geologia com províncias (para análise)
    print("Interceptando geologia com províncias...")
    geology_with_provinces = gpd.sjoin(geology, provinces, how='inner', predicate='within')

    print(f"   {len(geology_with_provinces)} unidades geológicas com dados de mineração")

    return geology_with_provinces, provinces

def create_mining_analysis():
    """Criar análise detalhada de mineração por geologia"""

    print("\nCriando análise de mineração por geologia...")

    # Carregar dados integrados
    geology_with_provinces, provinces = create_mining_integration_map()

    # Análise por unidade geológica
    print("Analisando produção por unidade geológica...")

    # Agrupar por ERA e calcular estatísticas
    analysis = geology_with_provinces.groupby(['ERA', 'Legend']).agg({
        'mining_companies': 'sum',
        'mining_production': 'sum',
        'area_km2': 'sum',
        'count': 'count'
    }).reset_index()

    # Ordenar por produção
    analysis_sorted = analysis.sort_values('mining_production', ascending=False)

    print("\nTop 10 Unidades Geológicas por Produção Mineração:")
    for i, (_, row) in enumerate(analysis_sorted.head(10).iterrows()):
        print(f"   {i+1:2d}. {row['Legend']} ({row['ERA']})")
        print(f"       Empresas: {row['mining_companies']}")
        print(f"       Produção: {row['mining_production']:.1f}M ton/ano")
        print(f"       Área: {row['area_km2']:.0f} km²")
        print()

    # Análise por ERA geológica
    print("\nAnálise por Era Geológica:")
    era_analysis = geology_with_provinces.groupby('ERA').agg({
        'mining_companies': 'sum',
        'mining_production': 'sum',
        'count': 'count'
    }).sort_values('mining_production', ascending=False)

    for era, row in era_analysis.iterrows():
        print(f"   {era}:")
        print(f"     Empresas: {row['mining_companies']}")
        print(f"     Produção: {row['mining_production']:.1f}M ton/ano")
        print(f"     Unidades: {row['count']}")
        print()

    return analysis_sorted

def create_mining_potential_map():
    """Criar mapa de potencial mineração por geologia"""

    print("\nCriando mapa de potencial mineração...")

    # Carregar análise
    analysis = create_mining_analysis()

    # Definir potencial por tipo de rocha
    geology_potential = {
        'Sedimentary': {
            'coal': 0.8,      # Alto potencial para carvão
            'limestone': 0.6,   # Bom potencial para calcário
            'sandstone': 0.7,  # Bom potencial para arenito
            'shale': 0.5       # Médio potencial para folhelho
        },
        'Igneous': {
            'gold': 0.3,       # Médio potencial para ouro
            'copper': 0.7,     # Bom potencial para cobre
            'tin': 0.4,         # Baixo potencial para estanho
            'tungsten': 0.6     # Bom potencial para tungstênio
        },
        'Metamorphic': {
            'graphite': 0.8,     # Alto potencial para grafite
            'marble': 0.5,       # Médio potencial para mármore
            'quartzite': 0.4     # Baixo potencial para quartzito
        }
    }

    # Mapear potencial para geologia
    print("Mapeando potencial mineração...")
    geology = geomoz.read_geology()

    def get_potential(legend):
        """Calcular potencial médio para unidade geológica"""
        legend_lower = str(legend).lower()

        potential_score = 0.0
        count = 0

        for rock_type, potentials in geology_potential.items():
            for mineral, score in potentials.items():
                if mineral.lower() in legend_lower:
                    potential_score += score
                    count += 1
                    break

        return potential_score / count if count > 0 else 0.0

    geology['mining_potential'] = geology['Legend'].apply(get_potential)

    # Criar mapa de potencial
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))

    geology.plot(
        ax=ax,
        column='mining_potential',
        cmap='YlOrRd',
        legend=True,
        edgecolor='black',
        linewidth=0.5
    )

    ax.set_title('Potencial Mineração por Unidade Geológica', fontsize=14, fontweight='bold')
    ax.set_xlabel('Longitude', fontsize=12)
    ax.set_ylabel('Latitude', fontsize=12)

    # Adicionar barra de cores
    sm = plt.cm.ScalarMappable(cmap='YlOrRd', norm=plt.Normalize(vmin=0, vmax=1))
    cbar = plt.colorbar(sm, ax=ax, orientation='vertical', shrink=0.8)
    cbar.set_label('Potencial Mineração', fontsize=10)

    plt.tight_layout()
    plt.savefig('mozambique_mining_potential_map.png', dpi=300, bbox_inches='tight')
    print("Mapa de potencial salvo como: mozambique_mining_potential_map.png")

    plt.show()

    return geology

def create_mining_dashboard():
    """Criar dashboard de mineração"""

    print("\nCriando dashboard de mineração...")

    # Carregar dados
    analysis = create_mining_analysis()

    # Criar figura com múltiplos gráficos
    fig = plt.figure(figsize=(16, 12))

    # 1. Gráfico de barras - Top unidades
    ax1 = plt.subplot(2, 2, 1)
    top_10 = analysis.head(10)

    bars = ax1.bar(range(len(top_10)), top_10['mining_production'])
    ax1.set_title('Top 10 Unidades Geológicas - Produção Mineração', fontweight='bold')
    ax1.set_xlabel('Unidade Geológica')
    ax1.set_ylabel('Produção (M ton/ano)')
    ax1.set_xticks(range(len(top_10)))
    ax1.set_xticklabels(top_10['Legend'], rotation=45, ha='right')
    ax1.grid(True, alpha=0.3)

    # 2. Gráfico de pizza - Distribuição por ERA
    ax2 = plt.subplot(2, 2, 2)
    era_production = analysis.groupby('ERA')['mining_production'].sum()

    colors = ['#ff9999', '#66c2a5', '#ffcc99', '#99ff99', '#66ff66', '#33cc33', '#3366cc', '#0066cc', '#000066']

    wedges, texts, autotexts = ax2.pie(
        era_production.values,
        labels=era_production.index,
        colors=colors[:len(era_production)],
        autopct='%1.1f%%',
        startangle=90
    )

    ax2.set_title('Distribuição da Produção por Era Geológica', fontweight='bold')

    # 3. Gráfico de dispersão - Empresas vs Produção
    ax3 = plt.subplot(2, 2, 3)
    scatter = ax3.scatter(
        analysis['mining_companies'],
        analysis['mining_production'],
        alpha=0.6,
        s=50,
        c=analysis['area_km2'],
        cmap='viridis'
    )

    ax3.set_title('Empresas vs Produção', fontweight='bold')
    ax3.set_xlabel('Número de Empresas')
    ax3.set_ylabel('Produção (M ton/ano)')
    ax3.grid(True, alpha=0.3)

    # Adicionar barra de cores para o gráfico de dispersão
    cbar = plt.colorbar(scatter, ax=ax3)
    cbar.set_label('Área (km²)')

    plt.tight_layout()
    plt.savefig('mozambique_mining_dashboard.png', dpi=300, bbox_inches='tight')
    print("Dashboard salvo como: mozambique_mining_dashboard.png")

    plt.show()

def main():
    """Função principal"""
    print("Exemplo 03: Integração com Dados de Mineração")
    print("=" * 60)

    try:
        # Criar mapa de integração
        geology_with_provinces, provinces = create_mining_integration_map()

        # Criar análise detalhada
        analysis = create_mining_analysis()

        # Criar mapa de potencial
        geology_potential = create_mining_potential_map()

        # Criar dashboard
        create_mining_dashboard()

        print("\nExemplo concluído com sucesso!")
        print("Arquivos gerados:")
        print("   - mozambique_mining_integration_map.png")
        print("   - mozambique_mining_potential_map.png")
        print("   - mozambique_mining_dashboard.png")
        print("   - Análise detalhada de mineração por geologia")

        print("\nAplicações:")
        print("   - Planeamento de exploração mineral")
        print("   - Análise de correlação geologia-mineração")
        print("   - Identificação de áreas de alto potencial")
        print("   - Estudos de viabilidade econômica")

    except Exception as e:
        print(f"\nErro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
