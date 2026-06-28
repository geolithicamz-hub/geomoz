#!/usr/bin/env python3
"""
Demonstração das Funções de Plot Utilitárias
Exemplos de uso das funções helper de visualização
"""

import matplotlib.pyplot as plt
import geomoz
from geomoz import (
    plot_provinces,
    plot_districts_by_province,
    plot_administrative_hierarchy,
    plot_villages_with_names,
    plot_geology_by_area,
    create_comparison_plot,
    quick_map
)
import geopandas as gpd


def demo_1_quick_map():
    """Demonstrar quick_map - mapa rápido"""

    print("=" * 70)
    print("DEMO 1: quick_map() - Mapa Rápido")
    print("=" * 70)

    # Mapa rápido de províncias
    print("\nCriando mapa rápido de províncias...")
    provinces = geomoz.read_province()
    quick_map(provinces, column='Provincia',
              title='Províncias de Moçambique (quick_map)',
              save_path='07a_quick_map_provinces.png')
    print("Mapa salvo: 07a_quick_map_provinces.png")


def demo_2_plot_provinces():
    """Demonstrar plot_provinces"""

    print("\n" + "=" * 70)
    print("DEMO 2: plot_provinces() - Plot de Províncias")
    print("=" * 70)

    print("\nCriando mapa de províncias com nomes...")
    ax = plot_provinces(
        show_names=True,
        cmap='tab20',
        title='Províncias de Moçambique',
        save_path='07b_plot_provinces.png'
    )
    print("Mapa salvo: 07b_plot_provinces.png")
    plt.show()


def demo_3_plot_districts():
    """Demonstrar plot_districts_by_province"""

    print("\n" + "=" * 70)
    print("DEMO 3: plot_districts_by_province() - Distritos por Província")
    print("=" * 70)

    print("\nCriando mapa de distritos de Tete...")
    ax = plot_districts_by_province(
        province_name="Tete",
        show_names=True,
        cmap='tab20',
        save_path='07c_plot_districts_tete.png'
    )
    print("Mapa salvo: 07c_plot_districts_tete.png")
    plt.show()


def demo_4_hierarchy():
    """Demonstrar plot_administrative_hierarchy"""

    print("\n" + "=" * 70)
    print("DEMO 4: plot_administrative_hierarchy() - Hierarquia Completa")
    print("=" * 70)

    print("\nCriando visualização hierárquica de Sofala...")
    axes = plot_administrative_hierarchy(
        province_name="Sofala",
        save_path='07d_hierarchy_sofala.png'
    )
    print("Mapa salvo: 07d_hierarchy_sofala.png")
    plt.show()


def demo_5_plot_villages():
    """Demonstrar plot_villages_with_names"""

    print("\n" + "=" * 70)
    print("DEMO 5: plot_villages_with_names() - Aldeias com Nomes")
    print("=" * 70)

    print("\nCriando mapa de aldeias...")
    ax = plot_villages_with_names(
        post_name="Cidade de Lichinga",
        save_path='07e_villages_lichinga.png'
    )
    print("Mapa salvo: 07e_villages_lichinga.png")
    plt.show()


def demo_6_plot_geology():
    """Demonstrar plot_geology_by_area"""

    print("\n" + "=" * 70)
    print("DEMO 6: plot_geology_by_area() - Geologia por Área")
    print("=" * 70)

    print("\nCriando mapa geológico de Manica...")

    # Carregar dados
    province = geomoz.read_province(name_province="Manica")
    geology = geomoz.read_geology()

    # Interseção
    geology = geology.to_crs(province.crs)
    geo_province = gpd.overlay(geology, province, how='intersection')

    ax = plot_geology_by_area(
        geo_province,
        column='Legend',
        title='Geologia da Província de Manica',
        save_path='07f_geology_manica.png'
    )
    print("Mapa salvo: 07f_geology_manica.png")
    plt.show()


def demo_7_comparison():
    """Demonstrar create_comparison_plot"""

    print("\n" + "=" * 70)
    print("DEMO 7: create_comparison_plot() - Comparação de Mapas")
    print("=" * 70)

    print("\nCriando comparação de províncias...")

    # Carregar províncias para comparação
    tete = geomoz.read_province(name_province="Tete")
    nampula = geomoz.read_province(name_province="Nampula")
    sofala = geomoz.read_province(name_province="Sofala")

    axes = create_comparison_plot(
        [tete, nampula, sofala],
        ["Tete", "Nampula", "Sofala"],
        ncols=3,
        figsize=(18, 6),
        save_path='07g_comparison_provinces.png'
    )
    print("Mapa salvo: 07g_comparison_provinces.png")
    plt.show()


def demo_8_combined_usage():
    """Demonstrar uso combinado das funções"""

    print("\n" + "=" * 70)
    print("DEMO 8: Uso Combinado - Dashboard Administrativo")
    print("=" * 70)

    print("\nCriando dashboard combinado...")

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    # 1. Províncias
    ax1 = axes[0, 0]
    provinces = geomoz.read_province()
    quick_map(provinces, column='Provincia', ax=ax1, show=False)
    ax1.set_title('Todas as Províncias', fontweight='bold')

    # 2. Distritos de uma província
    ax2 = axes[0, 1]
    plot_districts_by_province("Zambézia", ax=ax2, show_names=False)
    ax2.set_title('Zambézia - Distritos', fontweight='bold')

    # 3. Hierarquia (focada)
    ax3 = axes[1, 0]
    province = geomoz.read_province(name_province="Gaza")
    province.plot(ax=ax3, color='lightgreen', edgecolor='darkgreen', linewidth=2)
    ax3.set_title('Gaza - Província', fontweight='bold')
    ax3.axis('off')

    # 4. Resumo estatístico
    ax4 = axes[1, 1]
    ax4.axis('off')

    # Estatísticas
    districts = geomoz.read_district()
    posts = geomoz.read_admin_post()
    villages = geomoz.read_village()

    stats_text = f"""
    ESTATÍSTICAS NACIONAIS

    Divisões Administrativas:

    • 11 Províncias
    • {len(districts):,} Distritos
    • {len(posts):,} Postos Administrativos
    • {len(villages):,} Aldeias

    Médias:
    • ~{len(districts)/11:.0f} distritos/província
    • ~{len(posts)/len(districts):.0f} postos/distrito
    • ~{len(villages)/len(posts):.0f} aldeias/posto
    """

    ax4.text(0.1, 0.5, stats_text, transform=ax4.transAxes, fontsize=11,
             verticalalignment='center', fontfamily='monospace',
             bbox=dict(boxstyle='round,pad=1', facecolor='lightyellow', alpha=0.9))

    plt.suptitle('Dashboard Administrativo - GeoMoz', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('07h_dashboard_combined.png', dpi=300, bbox_inches='tight')
    print("Dashboard salvo: 07h_dashboard_combined.png")
    plt.show()


def main():
    """Executar todas as demonstrações"""

    print("DEMONSTRAÇÃO: Funções de Plot Utilitárias")
    print("=" * 70)

    try:
        # Executar demos
        demo_1_quick_map()
        demo_2_plot_provinces()
        demo_3_plot_districts()
        demo_4_hierarchy()
        demo_5_plot_villages()
        demo_6_plot_geology()
        demo_7_comparison()
        demo_8_combined_usage()

        print("\n" + "=" * 70)
        print("Todas as demonstrações concluídas!")
        print("=" * 70)
        print("\nArquivos gerados:")
        print("   • 07a_quick_map_provinces.png")
        print("   • 07b_plot_provinces.png")
        print("   • 07c_plot_districts_tete.png")
        print("   • 07d_hierarchy_sofala.png")
        print("   • 07e_villages_lichinga.png")
        print("   • 07f_geology_manica.png")
        print("   • 07g_comparison_provinces.png")
        print("   • 07h_dashboard_combined.png")

        print("\nFunções Demonstradas:")
        print("   • quick_map() - Mapa rápido e simples")
        print("   • plot_provinces() - Províncias com nomes")
        print("   • plot_districts_by_province() - Distritos")
        print("   • plot_administrative_hierarchy() - 4 níveis")
        print("   • plot_villages_with_names() - Aldeias detalhadas")
        print("   • plot_geology_by_area() - Mapa geológico")
        print("   • create_comparison_plot() - Comparação lado a lado")

        print("\nUso:")
        print("   from geomoz import quick_map, plot_provinces")
        print("   from geomoz.plot_utils import plot_districts_by_province")

    except Exception as e:
        print(f"\nErro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
