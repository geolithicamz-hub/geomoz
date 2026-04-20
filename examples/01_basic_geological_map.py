#!/usr/bin/env python3
"""
Mapa Geológico de Moçambique (CORRIGIDO)
Classificação baseada em ERA (cronoestratigrafia)
"""

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import geopandas as gpd
import pandas as pd
import geomoz
import matplotlib.patches as mpatches


def create_geological_map():

    print("🗺️ Criando mapa geológico CORRETO...")

    # -------------------------
    # 📥 CARREGAR DADOS
    # -------------------------
    geology = geomoz.read_geology()
    provinces = geomoz.read_province()

    # Garantir CRS
    geology = geology.to_crs(epsg=4326)
    provinces = provinces.to_crs(epsg=4326)

    # -------------------------
    # 🧠 CLASSIFICAÇÃO CORRETA (ERA)
    # -------------------------
    def classify_geology(row):
        era = str(row['ERA']).lower() if pd.notna(row['ERA']) else ''

        if 'archean' in era:
            return 'Archean'
        elif 'proterozoic' in era:
            return 'Proterozoic'
        elif 'paleozoic' in era:
            return 'Paleozoic'
        elif 'mesozoic' in era:
            return 'Mesozoic'
        elif 'cenozoic' in era:
            return 'Cenozoic'
        else:
            return 'Other'

    geology['class'] = geology.apply(classify_geology, axis=1)

    # Debug (opcional)
    print("\n📊 Distribuição por ERA:")
    print(geology['class'].value_counts())

    # -------------------------
    # 🎨 CORES GEOLOGICAMENTE CORRETAS
    # -------------------------
    colors = {
        'Archean': '#6b3d2e',
        'Proterozoic': '#a0522d',
        'Paleozoic': '#4f81bd',
        'Mesozoic': '#f1c232',
        'Cenozoic': '#6aa84f',
        'Other': '#cccccc'
    }

    # -------------------------
    # 🗺️ MAPA
    # -------------------------
    fig = plt.figure(figsize=(14, 10))
    ax = plt.axes(projection=ccrs.PlateCarree())

    # Base
    ax.add_feature(cfeature.LAND, facecolor="#f5f5f5")
    ax.add_feature(cfeature.OCEAN, facecolor="#dceaf7")
    ax.add_feature(cfeature.COASTLINE, linewidth=0.8)
    ax.add_feature(cfeature.BORDERS, linestyle=":", alpha=0.5)

    # -------------------------
    # 🎨 PLOT GEOLOGIA (por classe)
    # -------------------------
    for geo_class, color in colors.items():
        subset = geology[geology['class'] == geo_class]

        if not subset.empty:
            subset.plot(
                ax=ax,
                color=color,
                edgecolor='black',
                linewidth=0.2,
                alpha=0.85
            )

    # -------------------------
    # 🧭 PROVÍNCIAS (overlay)
    # -------------------------
    provinces.boundary.plot(ax=ax, color='black', linewidth=0.8)

    # -------------------------
    # 📍 EXTENSÃO CORRETA
    # -------------------------
    ax.set_extent([30, 41, -27, -10])

    # -------------------------
    # 🏷️ TÍTULO
    # -------------------------
    ax.set_title(
        "Mapa Geológico de Moçambique (por Era)",
        fontsize=16,
        fontweight='bold'
    )

    # -------------------------
    # 🌐 GRID
    # -------------------------
    gl = ax.gridlines(draw_labels=True, linestyle='--', linewidth=0.3)
    gl.top_labels = False
    gl.right_labels = False

    # -------------------------
    # 📋 LEGENDA LIMPA
    # -------------------------
    legend_elements = [
        mpatches.Patch(color=color, label=label)
        for label, color in colors.items()
    ]

    ax.legend(
        handles=legend_elements,
        title="Era Geológica",
        loc='lower left',
        fontsize=10,
        frameon=True
    )

    # -------------------------
    # ℹ️ INFO
    # -------------------------
    plt.figtext(
        0.01, 0.01,
        f"Unidades: {len(geology)} | Fonte: GeoMoz | CRS: EPSG:4326",
        fontsize=8
    )

    # -------------------------
    # 💾 SALVAR
    # -------------------------
    output_file = "mozambique_geological_map_correct.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')

    print(f"\n💾 Mapa salvo: {output_file}")
    print("✅ Agora sim — geologicamente coerente!")

    plt.show()


def main():
    create_geological_map()


if __name__ == "__main__":
    main()