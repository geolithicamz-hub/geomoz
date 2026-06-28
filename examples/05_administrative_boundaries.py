#!/usr/bin/env python3
"""
Exemplo: Limites Administrativos de Moçambique
Demonstra uso de províncias, distritos, postos administrativos e aldeias
"""

import matplotlib.pyplot as plt
import geopandas as gpd
import geomoz
import numpy as np
from matplotlib.patches import Patch
import matplotlib.patches as mpatches


def example_1_provinces():
    """Exemplo 1: Visualizar todas as províncias"""

    print("=" * 60)
    print("EXEMPLO 1: Províncias de Moçambique")
    print("=" * 60)

    # Carregar todas as províncias
    provinces = geomoz.read_province()

    print(f"Total de províncias: {len(provinces)}")
    print(f"Colunas: {list(provinces.columns)}")

    # Criar figura
    fig, ax = plt.subplots(figsize=(12, 10))

    # Plotar cada província com cor diferente
    colors = plt.cm.tab20(np.linspace(0, 1, len(provinces)))

    for idx, (i, row) in enumerate(provinces.iterrows()):
        gpd.GeoSeries([row.geometry]).plot(
            ax=ax,
            color=colors[idx],
            edgecolor='black',
            linewidth=1,
            alpha=0.7,
            label=row['Provincia']
        )

    # Adicionar nomes das províncias
    for idx, row in provinces.iterrows():
        centroid = row.geometry.centroid
        ax.annotate(
            row['Provincia'],
            (centroid.x, centroid.y),
            fontsize=8,
            ha='center',
            fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7)
        )

    ax.set_title('Províncias de Moçambique', fontsize=16, fontweight='bold')
    ax.axis('off')

    # Legenda
    legend_elements = [Patch(facecolor=colors[i], label=provinces.iloc[i]['Provincia'], edgecolor='black')
                       for i in range(len(provinces))]
    ax.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1, 0.5), fontsize=8)

    plt.tight_layout()
    plt.savefig('01_provinces_mozambique.png', dpi=300, bbox_inches='tight')
    print("Mapa salvo: 01_provinces_mozambique.png")

    plt.show()

    return provinces


def example_2_districts_by_province():
    """Exemplo 2: Distritos de uma província específica"""

    print("\n" + "=" * 60)
    print("EXEMPLO 2: Distritos por Província")
    print("=" * 60)

    # Selecionar província
    province_name = "Nampula"
    province = geomoz.read_province(name_province=province_name)

    # Carregar todos os distritos
    all_districts = geomoz.read_district()

    # Filtrar distritos da província
    districts = all_districts[all_districts['Provincia'] == province_name]

    print(f"Província: {province_name}")
    print(f"Total de distritos: {len(districts)}")

    for idx, row in districts.iterrows():
        print(f"   • {row['Distrito']} (Código: {row['CodDist']})")

    # Criar figura
    fig, ax = plt.subplots(figsize=(12, 10))

    # Plotar província (fundo)
    province.boundary.plot(ax=ax, color='red', linewidth=2, label='Limite Provincial')

    # Plotar distritos com cores diferentes
    colors = plt.cm.Set3(np.linspace(0, 1, len(districts)))

    districts.plot(
        ax=ax,
        column='Distrito',
        cmap='tab20',
        edgecolor='black',
        linewidth=0.5,
        alpha=0.7,
        legend=True,
        legend_kwds={'loc': 'center left', 'bbox_to_anchor': (1, 0.5), 'title': 'Distritos'}
    )

    # Adicionar nomes dos distritos
    for idx, row in districts.iterrows():
        centroid = row.geometry.centroid
        ax.annotate(
            row['Distrito'][:15],
            (centroid.x, centroid.y),
            fontsize=7,
            ha='center',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='yellow', alpha=0.6)
        )

    ax.set_title(f'Distritos de {province_name}', fontsize=16, fontweight='bold')
    ax.axis('off')

    plt.tight_layout()
    plt.savefig(f'02_districts_{province_name.lower()}.png', dpi=300, bbox_inches='tight')
    print(f"Mapa salvo: 02_districts_{province_name.lower()}.png")

    plt.show()

    return districts


def example_3_admin_posts():
    """Exemplo 3: Postos Administrativos de um distrito"""

    print("\n" + "=" * 60)
    print("EXEMPLO 3: Postos Administrativos")
    print("=" * 60)

    # Selecionar distrito
    district_name = "Nampula"
    district = geomoz.read_district(name_district=district_name)

    # Carregar postos administrativos
    all_admin_posts = geomoz.read_admin_post()

    # Filtrar postos do distrito
    admin_posts = all_admin_posts[all_admin_posts['Distrito'] == district_name]

    print(f"Distrito: {district_name}")
    print(f"Total de postos administrativos: {len(admin_posts)}")

    for idx, row in admin_posts.iterrows():
        print(f"   • {row['Posto']} (Código: {row['CodPosto']})")

    # Criar figura
    fig, ax = plt.subplots(figsize=(12, 10))

    # Plotar distrito (fundo)
    district.boundary.plot(ax=ax, color='red', linewidth=2, label='Limite Distrital')

    # Plotar postos
    colors = plt.cm.Pastel1(np.linspace(0, 1, len(admin_posts)))

    for idx, (i, row) in enumerate(admin_posts.iterrows()):
        gpd.GeoSeries([row.geometry]).plot(
            ax=ax,
            color=colors[idx],
            edgecolor='black',
            linewidth=0.5,
            alpha=0.8
        )

    # Adicionar nomes
    for idx, row in admin_posts.iterrows():
        centroid = row.geometry.centroid
        ax.annotate(
            row['Posto'][:20],
            (centroid.x, centroid.y),
            fontsize=7,
            ha='center',
            fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8)
        )

    ax.set_title(f'Postos Administrativos - {district_name}', fontsize=16, fontweight='bold')
    ax.axis('off')

    # Legenda
    legend_elements = [Patch(facecolor=colors[i], label=admin_posts.iloc[i]['Posto'], edgecolor='black')
                       for i in range(len(admin_posts))]
    ax.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1, 0.5), fontsize=8, title='Postos')

    plt.tight_layout()
    plt.savefig(f'03_admin_posts_{district_name.lower()}.png', dpi=300, bbox_inches='tight')
    print(f"Mapa salvo: 03_admin_posts_{district_name.lower()}.png")

    plt.show()

    return admin_posts


def example_4_villages():
    """Exemplo 4: Aldeias (Villages) de um posto administrativo"""

    print("\n" + "=" * 60)
    print("EXEMPLO 4: Aldeias (Localidades)")
    print("=" * 60)

    # Selecionar posto administrativo
    admin_post_name = "Cidade de Nampula"

    # Carregar posto
    admin_post = geomoz.read_admin_post(name_admin_post=admin_post_name)

    # Carregar todas as aldeias
    all_villages = geomoz.read_village()

    # Filtrar aldeias do posto (usando interseção espacial)
    villages = gpd.sjoin(
        all_villages,
        admin_post,
        how='inner',
        predicate='within'
    )

    print(f"Posto Administrativo: {admin_post_name}")
    print(f"Total de aldeias: {len(villages)}")

    # Mostrar primeiras 10 aldeias
    print("\nPrimeiras 10 aldeias:")
    for idx, row in villages.head(10).iterrows():
        print(f"   • {row['Povoacao']}")

    # Criar figura
    fig, ax = plt.subplots(figsize=(14, 12))

    # Plotar posto (fundo)
    admin_post.boundary.plot(ax=ax, color='red', linewidth=3, label='Limite do Posto')

    # Plotar aldeias como pequenos polígonos coloridos
    colors = plt.cm.tab20(np.linspace(0, 1, len(villages)))

    villages.plot(
        ax=ax,
        color='lightblue',
        edgecolor='navy',
        linewidth=0.3,
        alpha=0.6
    )

    # Adicionar nomes das aldeias (amostra para não sobrecarregar)
    sample_size = min(20, len(villages))
    sample_villages = villages.sample(sample_size) if len(villages) > sample_size else villages

    for idx, row in sample_villages.iterrows():
        centroid = row.geometry.centroid
        ax.annotate(
            row['Povoacao'][:15],
            (centroid.x, centroid.y),
            fontsize=6,
            ha='center',
            bbox=dict(boxstyle='round,pad=0.15', facecolor='yellow', alpha=0.7, edgecolor='black', linewidth=0.5)
        )

    ax.set_title(f'Aldeias de {admin_post_name}\n(Total: {len(villages)} aldeias)',
                 fontsize=14, fontweight='bold')
    ax.axis('off')

    # Informação
    info_text = f"Total de aldeias: {len(villages)}\nMostrando nomes de {sample_size} aldeias"
    ax.text(0.02, 0.02, info_text, transform=ax.transAxes, fontsize=10,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8))

    plt.tight_layout()
    plt.savefig(f'04_villages_{admin_post_name.lower().replace(" ", "_")}.png', dpi=300, bbox_inches='tight')
    print(f"Mapa salvo: 04_villages_{admin_post_name.lower().replace(' ', '_')}.png")

    plt.show()

    return villages


def example_5_hierarchical_view():
    """Exemplo 5: Vista hierárquica completa"""

    print("\n" + "=" * 60)
    print("EXEMPLO 5: Vista Hierárquica Completa")
    print("=" * 60)

    # Selecionar província
    province_name = "Sofala"
    province = geomoz.read_province(name_province=province_name)

    # Carregar dados hierárquicos
    all_districts = geomoz.read_district()
    all_admin_posts = geomoz.read_admin_post()

    districts = all_districts[all_districts['Provincia'] == province_name]
    admin_posts = all_admin_posts[all_admin_posts['Provincia'] == province_name]

    print(f"Província: {province_name}")
    print(f"   • {len(districts)} distritos")
    print(f"   • {len(admin_posts)} postos administrativos")

    # Criar figura com subplots
    fig, axes = plt.subplots(2, 2, figsize=(16, 14))

    # 1. Província
    ax1 = axes[0, 0]
    province.plot(ax=ax1, color='lightgreen', edgecolor='darkgreen', linewidth=2)
    ax1.set_title(f'1. Província: {province_name}', fontweight='bold')
    ax1.axis('off')

    # 2. Distritos
    ax2 = axes[0, 1]
    districts.plot(ax=ax2, column='Distrito', cmap='tab20', edgecolor='black', linewidth=0.5, legend=False)
    province.boundary.plot(ax=ax2, color='red', linewidth=2)
    ax2.set_title(f'2. Distritos ({len(districts)})', fontweight='bold')
    ax2.axis('off')

    # 3. Postos Administrativos
    ax3 = axes[1, 0]
    districts.boundary.plot(ax=ax3, color='gray', linewidth=1, alpha=0.5)
    admin_posts.plot(ax=ax3, column='Posto', cmap='tab20b', edgecolor='black', linewidth=0.3, legend=False)
    ax3.set_title(f'3. Postos Administrativos ({len(admin_posts)})', fontweight='bold')
    ax3.axis('off')

    # 4. Resumo
    ax4 = axes[1, 1]
    ax4.axis('off')

    summary_text = f"""
    HIERARQUIA ADMINISTRATIVA

    {province_name}

    Nível 1: Província
    • 1 província

    Nível 2: Distritos
    • {len(districts)} distritos

    Nível 3: Postos Administrativos
    • {len(admin_posts)} postos

    Nível 4: Aldeias (Localidades)
    • ~{len(admin_posts) * 10} aldeias estimadas

    Total estimado de localidades:
    ~{len(admin_posts) * 10 + len(admin_posts) + len(districts) + 1}
    """

    ax4.text(0.1, 0.5, summary_text, transform=ax4.transAxes, fontsize=12,
             verticalalignment='center', fontfamily='monospace',
             bbox=dict(boxstyle='round,pad=1', facecolor='lightyellow', alpha=0.8))

    plt.suptitle(f'Estrutura Administrativa de {province_name}', fontsize=16, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.savefig(f'05_hierarchy_{province_name.lower()}.png', dpi=300, bbox_inches='tight')
    print(f"Mapa salvo: 05_hierarchy_{province_name.lower()}.png")

    plt.show()


def main():
    """Executar todos os exemplos"""

    print("EXEMPLOS: Limites Administrativos de Moçambique")
    print("=" * 70)

    try:
        # Executar exemplos
        provinces = example_1_provinces()
        districts = example_2_districts_by_province()
        admin_posts = example_3_admin_posts()
        villages = example_4_villages()
        example_5_hierarchical_view()

        print("\n" + "=" * 70)
        print("Todos os exemplos concluídos com sucesso!")
        print("=" * 70)
        print("\nArquivos gerados:")
        print("   • 01_provinces_mozambique.png")
        print("   • 02_districts_nampula.png")
        print("   • 03_admin_posts_nampula.png")
        print("   • 04_villages_cidade_de_nampula.png")
        print("   • 05_hierarchy_sofala.png")

        print("\nResumo das funções:")
        print("   • read_province() - Carrega províncias")
        print("   • read_district() - Carrega distritos")
        print("   • read_admin_post() - Carrega postos administrativos")
        print("   • read_village() - Carrega aldeias/localidades")

    except Exception as e:
        print(f"\nErro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
