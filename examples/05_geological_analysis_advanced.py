#!/usr/bin/env python3
"""
Exemplo 05: Análises Geológicas Avançadas
Demonstra análises quantitativas para geólogos e pesquisadores
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import geomoz
from scipy import stats
import seaborn as sns
from matplotlib.patches import Rectangle
import matplotlib.patches as mpatches

def perform_statistical_analysis():
    """Realizar análise estatística dos dados geológicos"""

    print("Realizando análise estatística dos dados geológicos...")

    # Carregar dados
    geology = geomoz.read_geology()

    # Adicionar cálculos de área
    geology_projected = geology.to_crs('EPSG:32736')  # UTM zona 36S
    geology['area_km2'] = geology_projected.geometry.area / 1_000_000

    print(f"Estatísticas básicas:")
    print(f"   Total de unidades: {len(geology)}")
    print(f"   Área total: {geology['area_km2'].sum():.2f} km²")
    print(f"   Área média: {geology['area_km2'].mean():.2f} km²")
    print(f"   Área mediana: {geology['area_km2'].median():.2f} km²")
    print(f"   Desvio padrão: {geology['area_km2'].std():.2f} km²")

    # Análise por ERA
    print(f"\nAnálise por Era Geológica:")
    era_stats = geology.groupby('ERA').agg({
        'area_km2': ['count', 'sum', 'mean', 'std'],
        'Legend': lambda x: x.nunique()
    }).round(2)

    era_stats.columns = ['Count', 'Total_Area', 'Mean_Area', 'Std_Area', 'Unique_Types']
    print(era_stats)

    # Teste de normalidade
    print(f"\nTestes de Normalidade (Shapiro-Wilk):")
    for era in geology['ERA'].unique():
        if era and era != 'Unknown':
            era_data = geology[geology['ERA'] == era]['area_km2'].dropna()
            if len(era_data) > 3 and len(era_data) <= 5000:  # Limite do teste
                stat, p_value = stats.shapiro(era_data)
                print(f"   {era}: W={stat:.4f}, p={p_value:.4f} ({'Normal' if p_value > 0.05 else 'Não Normal'})")

    return geology, era_stats

def create_correlation_analysis():
    """Criar análise de correlação entre variáveis geológicas"""

    print("\nCriando análise de correlação...")

    geology = geomoz.read_geology()

    # Adicionar variáveis numéricas
    geology['area_km2'] = geology.geometry.area / 1_000_000
    geology['perimeter_km'] = geology.geometry.length / 1000
    geology['centroid_lon'] = geology.geometry.centroid.x
    geology['centroid_lat'] = geology.geometry.centroid.y

    # Selecionar variáveis para correlação
    numeric_vars = ['area_km2', 'perimeter_km', 'centroid_lon', 'centroid_lat']

    # Criar matriz de correlação
    correlation_matrix = geology[numeric_vars].corr()

    # Visualizar
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # 1. Matriz de correlação
    ax1 = axes[0, 0]
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0,
                square=True, ax=ax1, cbar_kws={'shrink': 0.8})
    ax1.set_title('Matriz de Correlação - Variáveis Geológicas', fontweight='bold')

    # 2. Scatter plot - Área vs Perímetro
    ax2 = axes[0, 1]
    ax2.scatter(geology['area_km2'], geology['perimeter_km'], alpha=0.6, s=30)
    ax2.set_xlabel('Área (km²)')
    ax2.set_ylabel('Perímetro (km)')
    ax2.set_title('Área vs Perímetro', fontweight='bold')
    ax2.grid(True, alpha=0.3)

    # Calcular correlação
    corr_coef = geology['area_km2'].corr(geology['perimeter_km'])
    ax2.text(0.05, 0.95, f'r = {corr_coef:.3f}', transform=ax2.transAxes,
             bbox=dict(boxstyle="round", facecolor="yellow", alpha=0.7))

    # 3. Distribuição de áreas
    ax3 = axes[1, 0]
    ax3.hist(geology['area_km2'], bins=50, alpha=0.7, edgecolor='black')
    ax3.set_xlabel('Área (km²)')
    ax3.set_ylabel('Frequência')
    ax3.set_title('Distribuição de Áreas Geológicas', fontweight='bold')
    ax3.set_yscale('log')
    ax3.grid(True, alpha=0.3)

    # 4. Box plot por ERA
    ax4 = axes[1, 1]
    era_data = [geology[geology['ERA'] == era]['area_km2'].dropna()
                for era in geology['ERA'].unique() if era]
    era_labels = [era for era in geology['ERA'].unique() if era]

    if era_data:
        bp = ax4.boxplot(era_data, labels=era_labels, patch_artist=True)
        for patch in bp['boxes']:
            patch.set_facecolor('lightblue')
        ax4.set_ylabel('Área (km²)')
        ax4.set_title('Distribuição de Áreas por Era', fontweight='bold')
        ax4.set_yscale('log')
        ax4.grid(True, alpha=0.3, axis='y')
        plt.setp(ax4.get_xticklabels(), rotation=45, ha='right')

    plt.tight_layout()
    plt.savefig('mozambique_geological_correlation_analysis.png', dpi=300, bbox_inches='tight')
    print("Análise de correlação salva como: mozambique_geological_correlation_analysis.png")

    plt.show()

    return correlation_matrix

def perform_spatial_analysis():
    """Realizar análise espacial avançada"""

    print("\nRealizando análise espacial...")

    geology = geomoz.read_geology()
    provinces = geomoz.read_province()

    # Análise espacial por província
    print("Análise espacial por província:")

    spatial_results = []

    for _, province in provinces.iterrows():
        prov_name = province['Provincia']

        # Interceptar geologia com província
        prov_geology = gpd.overlay(geology, gpd.GeoDataFrame([province], crs=geology.crs), how='intersection')

        if len(prov_geology) > 0:
            prov_geology['area_km2'] = prov_geology.geometry.area / 1_000_000

            result = {
                'province': prov_name,
                'n_units': len(prov_geology),
                'total_area': prov_geology['area_km2'].sum(),
                'mean_area': prov_geology['area_km2'].mean(),
                'n_eras': prov_geology['ERA'].nunique(),
                'dominant_era': prov_geology['ERA'].mode().iloc[0] if not prov_geology['ERA'].mode().empty else 'Unknown'
            }

            spatial_results.append(result)

            print(f"   {prov_name}:")
            print(f"     Unidades: {result['n_units']}")
            print(f"     Área total: {result['total_area']:.2f} km²")
            print(f"     Era dominante: {result['dominant_era']}")

    return pd.DataFrame(spatial_results)

def create_geological_diversity_index():
    """Criar índice de diversidade geológica por província"""

    print("\nCriando índice de diversidade geológica...")

    geology = geomoz.read_geology()
    provinces = geomoz.read_province()

    # Calcular índice de diversidade para cada província
    diversity_results = []

    for _, province in provinces.iterrows():
        prov_name = province['Provincia']

        # Interceptar
        prov_geology = gpd.overlay(geology, gpd.GeoDataFrame([province], crs=geology.crs), how='intersection')

        if len(prov_geology) > 0:
            # Índice de diversidade de Shannon
            era_counts = prov_geology['ERA'].value_counts()
            total = era_counts.sum()

            shannon_diversity = -sum((count/total) * np.log(count/total)
                                  for count in era_counts if count > 0)

            # Índice de Simpson
            simpson_diversity = 1 - sum((count/total)**2 for count in era_counts)

            # Índice de riqueza (número de eras)
            richness = len(era_counts)

            diversity_results.append({
                'province': prov_name,
                'shannon_diversity': shannon_diversity,
                'simpson_diversity': simpson_diversity,
                'richness': richness,
                'n_units': len(prov_geology),
                'total_area': prov_geology.geometry.area.sum() / 1_000_000
            })

    diversity_df = pd.DataFrame(diversity_results)

    # Visualizar
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # 1. Diversidade de Shannon
    ax1 = axes[0, 0]
    diversity_df_sorted = diversity_df.sort_values('shannon_diversity', ascending=True)
    bars1 = ax1.barh(diversity_df_sorted['province'], diversity_df_sorted['shannon_diversity'])
    ax1.set_xlabel('Índice de Shannon')
    ax1.set_title('Diversidade Geológica (Shannon)', fontweight='bold')
    ax1.grid(True, alpha=0.3, axis='x')

    # 2. Diversidade de Simpson
    ax2 = axes[0, 1]
    diversity_df_sorted2 = diversity_df.sort_values('simpson_diversity', ascending=True)
    bars2 = ax2.barh(diversity_df_sorted2['province'], diversity_df_sorted2['simpson_diversity'])
    ax2.set_xlabel('Índice de Simpson')
    ax2.set_title('Diversidade Geológica (Simpson)', fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='x')

    # 3. Riqueza vs Número de Unidades
    ax3 = axes[1, 0]
    ax3.scatter(diversity_df['richness'], diversity_df['n_units'], s=100, alpha=0.7)
    for _, row in diversity_df.iterrows():
        ax3.annotate(row['province'], (row['richness'], row['n_units']),
                    fontsize=8, alpha=0.8)
    ax3.set_xlabel('Riqueza (número de eras)')
    ax3.set_ylabel('Número de unidades')
    ax3.set_title('Riqueza vs Número de Unidades', fontweight='bold')
    ax3.grid(True, alpha=0.3)

    # 4. Top províncias por diversidade
    ax4 = axes[1, 1]
    top_5 = diversity_df.nlargest(5, 'shannon_diversity')
    bars4 = ax4.bar(range(len(top_5)), top_5['shannon_diversity'])
    ax4.set_xticks(range(len(top_5)))
    ax4.set_xticklabels(top_5['province'], rotation=45, ha='right')
    ax4.set_ylabel('Índice de Shannon')
    ax4.set_title('Top 5 Províncias por Diversidade', fontweight='bold')
    ax4.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig('mozambique_geological_diversity_index.png', dpi=300, bbox_inches='tight')
    print("Índice de diversidade salvo como: mozambique_geological_diversity_index.png")

    plt.show()

    # Imprimir resultados
    print(f"\nTop 5 Províncias por Diversidade Geológica:")
    for i, (_, row) in enumerate(diversity_df.nlargest(5, 'shannon_diversity').iterrows(), 1):
        print(f"   {i}. {row['province']}: Shannon={row['shannon_diversity']:.3f}, "
              f"Simpson={row['simpson_diversity']:.3f}, Riqueza={row['richness']}")

    return diversity_df

def main():
    """Função principal"""
    print("Exemplo 05: Análises Geológicas Avançadas")
    print("=" * 60)

    try:
        # Análise estatística
        geology, era_stats = perform_statistical_analysis()

        # Análise de correlação
        correlation_matrix = create_correlation_analysis()

        # Análise espacial
        spatial_results = perform_spatial_analysis()

        # Índice de diversidade
        diversity_df = create_geological_diversity_index()

        print("\nTodas as análises geológicas concluídas com sucesso!")
        print("Arquivos gerados:")
        print("   - mozambique_geological_correlation_analysis.png")
        print("   - mozambique_geological_diversity_index.png")

        print("\nAnálises realizadas:")
        print("   - Estatísticas descritivas por era geológica")
        print("   - Testes de normalidade (Shapiro-Wilk)")
        print("   - Matriz de correlação entre variáveis")
        print("   - Análise espacial por província")
        print("   - Índices de diversidade (Shannon, Simpson)")
        print("   - Riqueza geológica por região")

    except Exception as e:
        print(f"\nErro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
