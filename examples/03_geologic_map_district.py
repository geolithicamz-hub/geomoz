#!/usr/bin/env python3
"""
Mapa Geológico a Nível Distrital
Usando a mesma lógica do mapa provincial, mas para distritos
"""

import matplotlib.pyplot as plt
import geopandas as gpd
import geomoz
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec


def create_district_geological_map():

    # -------------------------
    # DADOS - NÍVEL DISTRITAL
    # -------------------------
    geology = geomoz.read_geology()

    # Selecionar distrito específico (exemplo: Chimoio em Manica)
    district = geomoz.read_district(name_district="Mocuba")

    # Ou pode usar código:
    # district = geomoz.read_district(code_district="MA-01")

    geology = geology.to_crs(epsg=4326)
    district = district.to_crs(epsg=4326)

    # Interseção com distrito
    geology = gpd.overlay(geology, district, how='intersection')

    print(f"Total de unidades geológicas no distrito: {len(geology)}")

    # -------------------------
    # LIMPEZA - code2006
    # -------------------------
    column = "code2006"
    geology[column] = geology[column].fillna('Unknown').astype(str).str.strip()

    classes = sorted(geology[column].unique())
    print(f"Total de classes litológicas: {len(classes)}")

    # Mostrar distribuição
    print("\nDistribuição por litologia:")
    for cls, count in geology[column].value_counts().items():
        print(f"  {cls}: {count} unidades")

    # -------------------------
    # CORES
    # -------------------------
    cmap = plt.cm.get_cmap('tab20', len(classes))
    colors = {cls: cmap(i) for i, cls in enumerate(classes)}
    geology['color'] = geology[column].map(colors)

    # -------------------------
    # FIGURA COM GRID
    # -------------------------
    fig = plt.figure(figsize=(16, 10))
    gs = GridSpec(1, 2, width_ratios=[3, 1])

    ax_map = fig.add_subplot(gs[0])
    ax_leg = fig.add_subplot(gs[1])

    # -------------------------
    # MAPA DISTRITAL
    # -------------------------
    geology.plot(
        ax=ax_map,
        color=geology['color'],
        edgecolor='black',
        linewidth=0.15
    )

    # Contorno do distrito
    district.boundary.plot(ax=ax_map, color='black', linewidth=1.5)

    ax_map.set_title(
        "Mapa Geológico - Distrito de Mocuba",
        fontsize=14,
        fontweight='bold'
    )
    ax_map.axis('off')

    # -------------------------
    # LEGENDA
    # -------------------------
    ax_leg.axis('off')

    legend_elements = [
        mpatches.Patch(
            facecolor=colors[cls],
            label=cls[:40]
        )
        for cls in classes
    ]

    ax_leg.legend(
        handles=legend_elements,
        title="Litologias (code2006)",
        loc='center',
        ncol=3,
        fontsize=8,
        title_fontsize=10,
        frameon=True
    )

    # -------------------------
    # FINAL
    # -------------------------
    plt.tight_layout()

    plt.savefig(
        "mapa_geologico_distrital_Mocuba.png",
        dpi=300,
        bbox_inches='tight'
    )

    print("\nMapa distrital salvo: mapa_geologico_distrital_Mocuba.png")

    plt.show()


if __name__ == "__main__":
    create_district_geological_map()
