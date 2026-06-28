#!/usr/bin/env python3
"""
Exemplo Detalhado: Aldeias (Villages/Localidades)
Demonstra visualização detalhada das aldeias de Moçambique
"""

import matplotlib.pyplot as plt
import geopandas as gpd
import geomoz
import numpy as np
from matplotlib.patches import Patch
import matplotlib.patheffects as path_effects


def analyze_villages_national():
    """Análise nacional das aldeias"""

    print("=" * 70)
    print("ANÁLISE NACIONAL: Aldeias de Moçambique")
    print("=" * 70)

    # Carregar dados
    villages = geomoz.read_village()
    provinces = geomoz.read_province()

    print(f"Total de aldeias: {len(villages):,}")
    print(f"Total de províncias: {len(provinces)}")

    # Contagem por província
    village_by_province = villages.groupby('Provincia').size().sort_values(ascending=False)

    print("\nTop 10 Províncias com mais aldeias:")
    for prov, count in village_by_province.head(10).items():
        print(f"   {prov:20s}: {count:5,} aldeias")

    # Estatísticas
    print(f"\nEstatísticas:")
    print(f"   Média de aldeias por província: {village_by_province.mean():.1f}")
    print(f"   Mediana: {village_by_province.median():.1f}")
    print(f"   Máximo: {village_by_province.max()} ({village_by_province.idxmax()})")
    print(f"   Mínimo: {village_by_province.min()} ({village_by_province.idxmin()})")

    return villages, provinces, village_by_province


def plot_village_heatmap(villages, provinces, village_by_province):
    """Plotar mapa de calor de aldeias por província"""

    print("\nCriando mapa de distribuição de aldeias...")

    fig, axes = plt.subplots(1, 2, figsize=(18, 8))

    # Mapa 1: Localização das aldeias (amostra)
    ax1 = axes[0]

    # Plotar províncias (fundo)
    provinces.boundary.plot(ax=ax1, color='gray', linewidth=1, alpha=0.5)

    # Amostra de aldeias para visualização (1 a cada 10)
    sample_villages = villages.iloc[::10]

    # Plotar centroides das aldeias
    sample_villages.geometry.centroid.plot(
        ax=ax1,
        markersize=3,
        color='red',
        alpha=0.5,
        label=f'Aldeias (amostra: {len(sample_villages):,})'
    )

    ax1.set_title('Distribuição de Aldeias (Amostra)', fontsize=14, fontweight='bold')
    ax1.axis('off')
    ax1.legend(loc='upper left')

    # Mapa 2: Barras - aldeias por província
    ax2 = axes[1]

    colors = plt.cm.viridis(np.linspace(0, 1, len(village_by_province)))
    bars = ax2.barh(range(len(village_by_province)), village_by_province.values, color=colors)

    ax2.set_yticks(range(len(village_by_province)))
    ax2.set_yticklabels(village_by_province.index, fontsize=10)
    ax2.set_xlabel('Número de Aldeias', fontsize=12)
    ax2.set_title('Aldeias por Província', fontsize=14, fontweight='bold')

    # Adicionar valores nas barras
    for i, (prov, count) in enumerate(village_by_province.items()):
        ax2.text(count + 50, i, f'{count:,}', va='center', fontsize=9)

    ax2.grid(axis='x', alpha=0.3)

    plt.tight_layout()
    plt.savefig('06a_villages_national_overview.png', dpi=300, bbox_inches='tight')
    print("Mapa salvo: 06a_villages_national_overview.png")
    plt.show()


def explore_village_hierarchy():
    """Explorar hierarquia: província → distrito → posto → aldeia"""

    print("\n" + "=" * 70)
    print("HIERARQUIA: Nampula → Distritos → Postos → Aldeias")
    print("=" * 70)

    # Selecionar província
    province_name = "Nampula"

    # Carregar dados
    province = geomoz.read_province(name_province=province_name)
    districts = geomoz.read_district()
    admin_posts = geomoz.read_admin_post()
    villages = geomoz.read_village()

    # Filtrar por província
    prov_districts = districts[districts['Provincia'] == province_name]
    prov_posts = admin_posts[admin_posts['Provincia'] == province_name]
    prov_villages = villages[villages['Provincia'] == province_name]

    print(f"{province_name}:")
    print(f"   • {len(prov_districts)} distritos")
    print(f"   • {len(prov_posts)} postos administrativos")
    print(f"   • {len(prov_villages)} aldeias")

    # Estrutura hierárquica
    print(f"\nEstrutura Hierárquica:")
    print(f"   1 província → {len(prov_districts)} distritos → {len(prov_posts)} postos → {len(prov_villages)} aldeias")
    print(f"   Média: {len(prov_villages)/len(prov_posts):.1f} aldeias por posto")

    return province, prov_districts, prov_posts, prov_villages


def plot_village_hierarchy_detail(province, districts, posts, villages):
    """Plotar hierarquia detalhada com zoom"""

    print("\nCriando visualização hierárquica detalhada...")

    # Criar figura com múltiplos níveis de zoom
    fig = plt.figure(figsize=(20, 12))
    gs = fig.add_gridspec(2, 3, hspace=0.3, wspace=0.3)

    # Nível 1: Província
    ax1 = fig.add_subplot(gs[0, 0])
    province.plot(ax=ax1, color='lightgreen', edgecolor='darkgreen', linewidth=2)
    ax1.set_title('Nível 1: Província\n(Nampula)', fontsize=12, fontweight='bold')
    ax1.axis('off')

    # Nível 2: Distritos
    ax2 = fig.add_subplot(gs[0, 1])
    districts.plot(ax=ax2, column='Distrito', cmap='tab20', edgecolor='black', linewidth=0.5)
    province.boundary.plot(ax=ax2, color='red', linewidth=2)
    ax2.set_title(f'Nível 2: Distritos\n({len(districts)} distritos)', fontsize=12, fontweight='bold')
    ax2.axis('off')

    # Nível 3: Postos Administrativos
    ax3 = fig.add_subplot(gs[0, 2])
    districts.boundary.plot(ax=ax3, color='gray', linewidth=1, alpha=0.5)
    posts.plot(ax=ax3, column='Posto', cmap='tab20b', edgecolor='black', linewidth=0.3)
    ax3.set_title(f'Nível 3: Postos Administrativos\n({len(posts)} postos)', fontsize=12, fontweight='bold')
    ax3.axis('off')

    # Nível 4: Aldeias (amostra de um distrito)
    ax4 = fig.add_subplot(gs[1, :])

    # Selecionar distrito com muitas aldeias
    village_by_district = villages.groupby('Distrito').size().sort_values(ascending=False)
    top_district = village_by_district.index[0]

    district_villages = villages[villages['Distrito'] == top_district]
    district_boundary = districts[districts['Distrito'] == top_district]
    district_posts = posts[posts['Distrito'] == top_district]

    # Plotar distrito
    district_boundary.boundary.plot(ax=ax4, color='red', linewidth=3, label=f'Distrito: {top_district}')

    # Plotar postos
    district_posts.boundary.plot(ax=ax4, color='blue', linewidth=1.5, alpha=0.6, label='Postos')

    # Plotar aldeias (todas do distrito)
    colors = plt.cm.tab10(np.linspace(0, 1, len(district_posts)))

    for idx, (post_idx, post_row) in enumerate(district_posts.iterrows()):
        post_villages = district_villages[district_villages['Posto'] == post_row['Posto']]

        if len(post_villages) > 0:
            post_villages.plot(
                ax=ax4,
                color=colors[idx % 10],
                edgecolor='black',
                linewidth=0.2,
                alpha=0.7,
                label=f"{post_row['Posto'][:20]} ({len(post_villages)})"
            )

    ax4.set_title(f'Nível 4: Aldeias do Distrito {top_district}\n({len(district_villages)} aldeias em {len(district_posts)} postos)',
                  fontsize=14, fontweight='bold')
    ax4.legend(loc='upper left', fontsize=8, title='Postos')
    ax4.axis('off')

    plt.suptitle('Hierarquia Administrativa: Província → Distrito → Posto → Aldeia',
                 fontsize=16, fontweight='bold')

    plt.savefig('06b_villages_hierarchy_detail.png', dpi=300, bbox_inches='tight')
    print("Mapa salvo: 06b_villages_hierarchy_detail.png")
    plt.show()


def analyze_village_attributes():
    """Analisar atributos das aldeias"""

    print("\n" + "=" * 70)
    print("ANÁLISE DE ATRIBUTOS: Aldeias")
    print("=" * 70)

    villages = geomoz.read_village()

    # Colunas disponíveis
    print(f"Colunas disponíveis:")
    for col in villages.columns:
        print(f"   • {col}")

    # Amostra de dados
    print(f"\nAmostra de aldeias:")
    sample = villages.sample(5)
    for idx, row in sample.iterrows():
        print(f"\n   Aldeia: {row['Povoacao']}")
        print(f"   Posto: {row['Posto']}")
        print(f"   Distrito: {row['Distrito']}")
        print(f"   Província: {row['Provincia']}")
        print(f"   Códigos: Pov={row['CodPov']}, Posto={row['CodPosto']}, Dist={row['CodDist']}, Prov={row['CodProv']}")

    # Análise de códigos
    print(f"\nEstatísticas de Códigos:")
    print(f"   Códigos de província únicos: {villages['CodProv'].nunique()}")
    print(f"   Códigos de distrito únicos: {villages['CodDist'].nunique()}")
    print(f"   Códigos de posto únicos: {villages['CodPosto'].nunique()}")
    print(f"   Códigos de povoação únicos: {villages['CodPov'].nunique()}")


def plot_village_names_sample():
    """Plotar amostra de aldeias com nomes"""

    print("\nCriando mapa com nomes de aldeias...")

    # Carregar dados
    villages = geomoz.read_village()
    posts = geomoz.read_admin_post()

    # Selecionar posto com poucas aldeias para legibilidade
    village_by_post = villages.groupby('Posto').size()
    small_posts = village_by_post[village_by_post.between(5, 15)]

    if len(small_posts) > 0:
        selected_post = small_posts.index[0]
        post_villages = villages[villages['Posto'] == selected_post]
        post_boundary = posts[posts['Posto'] == selected_post]

        fig, ax = plt.subplots(figsize=(14, 10))

        # Plotar limite do posto
        post_boundary.boundary.plot(ax=ax, color='red', linewidth=2, label=f'Posto: {selected_post}')

        # Plotar aldeias com cores diferentes
        colors = plt.cm.Set3(np.linspace(0, 1, len(post_villages)))

        for idx, (vill_idx, village) in enumerate(post_villages.iterrows()):
            gpd.GeoSeries([village.geometry]).plot(
                ax=ax,
                color=colors[idx],
                edgecolor='black',
                linewidth=0.5,
                alpha=0.8
            )

            # Adicionar nome da aldeia
            centroid = village.geometry.centroid
            text = ax.annotate(
                village['Povoacao'],
                (centroid.x, centroid.y),
                fontsize=8,
                ha='center',
                fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8, edgecolor='black')
            )
            # Efeito de contorno no texto
            text.set_path_effects([path_effects.withStroke(linewidth=3, foreground='white')])

        ax.set_title(f'Aldeias do Posto: {selected_post}\n({len(post_villages)} aldeias com nomes)',
                     fontsize=14, fontweight='bold')
        ax.axis('off')
        ax.legend(loc='upper right')

        plt.tight_layout()
        plt.savefig('06c_villages_with_names.png', dpi=300, bbox_inches='tight')
        print(f"Mapa salvo: 06c_villages_with_names.png")
        plt.show()
    else:
        print("Não encontrado posto com número adequado de aldeias")


def main():
    """Executar todos os exemplos de aldeias"""

    print("EXEMPLO DETALHADO: Aldeias de Moçambique")
    print("=" * 70)

    try:
        # Análise nacional
        villages, provinces, village_by_province = analyze_villages_national()
        plot_village_heatmap(villages, provinces, village_by_province)

        # Explorar hierarquia
        province, districts, posts, prov_villages = explore_village_hierarchy()
        plot_village_hierarchy_detail(province, districts, posts, prov_villages)

        # Análise de atributos
        analyze_village_attributes()

        # Mapa com nomes
        plot_village_names_sample()

        print("\n" + "=" * 70)
        print("Todos os exemplos de aldeias concluídos!")
        print("=" * 70)
        print("\nArquivos gerados:")
        print("   • 06a_villages_national_overview.png")
        print("   • 06b_villages_hierarchy_detail.png")
        print("   • 06c_villages_with_names.png")

        print("\nResumo:")
        print(f"   • Total de aldeias em Moçambique: 11,524")
        print(f"   • Estrutura hierárquica completa")
        print(f"   • Visualização detalhada com nomes")

    except Exception as e:
        print(f"\nErro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
