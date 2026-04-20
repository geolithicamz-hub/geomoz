#!/usr/bin/env python3

import matplotlib.pyplot as plt
import geopandas as gpd
import geomoz
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec


def create_full_geological_map():

    # -------------------------
    # DADOS
    # -------------------------
    geology = geomoz.read_geology()
    province = geomoz.read_province(name_province="Manica")

    geology = geology.to_crs(epsg=4326)
    province = province.to_crs(epsg=4326)

    geology = gpd.overlay(geology, province, how='intersection')

    # -------------------------
    # LIMPEZA
    # -------------------------
    column = "code2006"
    geology[column] = geology[column].fillna('Unknown').astype(str).str.strip()

    classes = sorted(geology[column].unique())
    print(f"Total de classes: {len(classes)}")

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
    gs = GridSpec(1, 2, width_ratios=[3, 1])  # mapa maior

    ax_map = fig.add_subplot(gs[0])
    ax_leg = fig.add_subplot(gs[1])

    # -------------------------
    # MAPA
    # -------------------------
    geology.plot(
        ax=ax_map,
        color=geology['color'],
        edgecolor='black',
        linewidth=0.15
    )

    province.boundary.plot(ax=ax_map, color='black', linewidth=1)

    ax_map.set_title(
        "Mapa Geológico - Província de Tete",
        fontsize=14,
        fontweight='bold'
    )
    ax_map.axis('off')

    # -------------------------
    # LEGENDA (EM EIXO SEPARADO)
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
        ncol=4,  # 🔥 MAIS COLUNAS AQUI
        fontsize=8,
        title_fontsize=10,
        frameon=True
    )

    # -------------------------
    # FINAL
    # -------------------------
    plt.tight_layout()

    plt.savefig(
        "mapa_geologico_completo_tete.png",
        dpi=300,
        bbox_inches='tight'
    )

    plt.show()


if __name__ == "__main__":
    create_full_geological_map()