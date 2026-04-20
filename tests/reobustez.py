#!/usr/bin/env python3

import matplotlib.pyplot as plt
import geopandas as gpd
import geomoz
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import time
import warnings

# Ignorar warnings desnecessários (HF e geopandas)
warnings.filterwarnings("ignore")


# =====================================================
# 🔹 FUNÇÃO PRINCIPAL
# =====================================================
def create_geological_map(column="code2006", province_name="Tete"):

    print("\n=== GEOLOGICAL MAP GENERATION ===")
    start_time = time.time()

    # -------------------------
    # CARREGAR DADOS
    # -------------------------
    print("Carregando dados...")
    geology = geomoz.read_geology()
    province = geomoz.read_province(name_province=province_name)

    # -------------------------
    # CRS
    # -------------------------
    if geology.crs != province.crs:
        geology = geology.to_crs(province.crs)

    # -------------------------
    # FILTRO ESPACIAL RÁPIDO
    # -------------------------
    print("Filtrando e recortando geometria...")
    province_geom = province.unary_union 
    # filtro rápido
    geology = geology[geology.intersects(province_geom)]

    # corte real (ESSENCIAL)
    geology = gpd.clip(geology, province)
    

    if len(geology) == 0:
        raise ValueError("Nenhum dado encontrado após filtro espacial")

    # -------------------------
    # VALIDAR COLUNA
    # -------------------------
    if column not in geology.columns:
        raise ValueError(f"Coluna '{column}' não existe no dataset")

    # -------------------------
    # LIMPEZA
    # -------------------------
    geology[column] = geology[column].fillna('Unknown').astype(str).str.strip()

    # Corrigir geometrias inválidas
    invalid = ~geology.is_valid
    if invalid.any():
        print(f"Corrigindo {invalid.sum()} geometrias inválidas...")
        geology.loc[invalid, "geometry"] = geology.loc[invalid].buffer(0)

    classes = sorted(geology[column].unique())

    print(f"Coluna: {column}")
    print(f"Total de classes: {len(classes)}")

    # -------------------------
    # CORES
    # -------------------------
    cmap = plt.cm.get_cmap('tab20', len(classes))
    colors = {cls: cmap(i) for i, cls in enumerate(classes)}
    geology["color"] = geology[column].map(colors)

    # -------------------------
    # FIGURA
    # -------------------------
    fig = plt.figure(figsize=(16, 10))
    gs = GridSpec(1, 2, width_ratios=[4, 1.5])

    ax_map = fig.add_subplot(gs[0])
    ax_leg = fig.add_subplot(gs[1])

    # -------------------------
    # MAPA
    # -------------------------
    geology.plot(
        ax=ax_map,
        color=geology["color"],
        edgecolor="black",
        linewidth=0.15
    )

    province.boundary.plot(ax=ax_map, color="black", linewidth=1)

    ax_map.set_title(
        f"Mapa Geológico - {province_name} ({column})",
        fontsize=14,
        fontweight="bold"
    )

    ax_map.axis("off")

    # -------------------------
    # LEGENDA EXTERNA
    # -------------------------
    ax_leg.axis("off")

    legend_elements = [
        mpatches.Patch(
            facecolor=colors[cls],
            label=cls[:40]
        )
        for cls in classes
    ]

    ax_leg.legend(
        handles=legend_elements,
        title=f"Litologias ({column})",
        loc="center",
        ncol=3,              # 🔥 ajusta conforme nº de classes
        fontsize=8,
        title_fontsize=10,
        frameon=True
    )

    # -------------------------
    # ESTATÍSTICAS
    # -------------------------
    print("\n=== ESTATÍSTICAS ===")

    try:
        geology_utm = geology.to_crs(epsg=32736)
        province_utm = province.to_crs(epsg=32736)

        geo_area = geology_utm.area.sum()
        prov_area = province_utm.area.sum()

        print(f"Área geológica: {geo_area/1e6:.2f} km²")
        print(f"Área província: {prov_area/1e6:.2f} km²")
        print(f"Cobertura: {(geo_area/prov_area)*100:.2f}%")

    except Exception as e:
        print(f"Erro no cálculo de área: {e}")

    # -------------------------
    # TEMPO
    # -------------------------
    end_time = time.time()
    print(f"\nTempo total: {end_time - start_time:.2f}s")

    # -------------------------
    # EXPORTAR
    # -------------------------
    output_file = f"mapa_geologico_{province_name.lower()}_{column}.png"

    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches="tight")

    print(f"\nMapa salvo: {output_file}")

    plt.show()


# =====================================================
# 🔹 TESTES AUTOMÁTICOS
# =====================================================
def run_tests():

    print("\n================ TESTES ================")

    columns = ["code2006", "Legend", "ERA"]
    provinces = ["Tete", "Nampula", "Zambézia"]

    for p in provinces:
        for col in columns:
            try:
                print(f"\nTestando {p} - {col}")
                create_geological_map(column=col, province_name=p)
                print("OK")

            except Exception as e:
                print(f"ERRO: {e}")


# =====================================================
# 🔹 EXECUÇÃO
# =====================================================
if __name__ == "__main__":

    # Execução simples
    create_geological_map(column="code2006", province_name="Tete")

    # Para testar tudo:
    # run_tests()