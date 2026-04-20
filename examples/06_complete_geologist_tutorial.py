#!/usr/bin/env python3

"""
GeoMoz - Visualização Geológica Profissional

Inclui:
- Mapa geológico robusto
- Ordem estratigráfica correta
- Legenda geológica organizada
- Gráfico de litologias limpo
"""

import matplotlib.pyplot as plt
import geomoz
import textwrap
import matplotlib.patches as mpatches


# =====================================================
# NORMALIZAÇÃO DE ERA
# =====================================================
def normalize_era(geology):

    geology["ERA"] = (
        geology["ERA"]
        .fillna("UNKNOWN")
        .astype(str)
        .str.upper()
        .str.strip()
    )

    corrections = {
        "JURRASSIC": "MESOZOIC",
        "JURASSIC": "MESOZOIC",
        "CRETACEOUS": "MESOZOIC",
        "TRIASSIC": "MESOZOIC",

        "ORDOVISIAN": "PALEOZOIC",
        "ORDOVICIAN": "PALEOZOIC",
        "CAMBRIAN": "PALEOZOIC",

        "TERTIARY": "CENOZOIC",
        "QUATERNARY": "CENOZOIC",

        "MESOARCHEAN": "ARCHEAN",
        "NEOARCHEAN": "ARCHEAN",

        "MESOPROTEROZOIC": "PROTEROZOIC",
        "NEOPROTEROZOIC": "PROTEROZOIC",
        "PALEOPROTEROZOIC": "PROTEROZOIC",

        "PALEOZOIC/MESOZOIC": "MESOZOIC"
    }

    geology["ERA"] = geology["ERA"].replace(corrections)

    return geology


# =====================================================
# MAPA GEOLOGICO
# =====================================================
def create_geological_map():

    print("\n=== GERANDO MAPA GEOLOGICO ===")

    geology = geomoz.read_geology()
    geology = normalize_era(geology)

    # -------------------------
    # CORES GEOLOGICAS
    # -------------------------
    base_colors = {
        "ARCHEAN": "#8c510a",
        "PROTEROZOIC": "#bf812d",
        "PALEOZOIC": "#80cdc1",
        "MESOZOIC": "#dfc27d",
        "CENOZOIC": "#35978f",
        "UNKNOWN": "#cccccc"
    }

    # atribuição segura
    geology["color"] = geology["ERA"].apply(
        lambda x: base_colors[x] if x in base_colors else "#999999"
    )

    geology["color"] = geology["color"].fillna("#999999")

    print("Total de classes:", geology["ERA"].nunique())

    # -------------------------
    # ORDEM ESTRATIGRAFICA
    # -------------------------
    STRAT_ORDER = [
        "ARCHEAN",
        "PROTEROZOIC",
        "PALEOZOIC",
        "MESOZOIC",
        "CENOZOIC",
        "UNKNOWN"
    ]

    classes_present = [c for c in STRAT_ORDER if c in geology["ERA"].unique()]

    # -------------------------
    # PLOT
    # -------------------------
    fig, ax = plt.subplots(figsize=(12, 8))

    geology.plot(
        ax=ax,
        color=geology["color"],
        edgecolor="black",
        linewidth=0.2
    )

    ax.set_title(
        "Distribuição por Era Geológica",
        fontsize=14,
        fontweight="bold"
    )

    ax.axis("off")

    # -------------------------
    # LEGENDA ORDENADA
    # -------------------------
    legend_elements = [
        mpatches.Patch(
            color=base_colors.get(c, "#999999"),
            label=c
        )
        for c in classes_present
    ]

    # inverter → antigo em baixo, recente em cima
    legend_elements = legend_elements[::-1]

    ax.legend(
        handles=legend_elements,
        title="Eras Geológicas\n(antigo ↓ | recente ↑)",
        loc="center left",
        bbox_to_anchor=(1.02, 0.5),
        frameon=True
    )

    plt.tight_layout()
    plt.savefig("mapa_era_profissional.png", dpi=300, bbox_inches="tight")
    plt.show()


# =====================================================
# QUEBRAR TEXTO
# =====================================================
def wrap_label(text, width=40):
    return "\n".join(textwrap.wrap(str(text), width))


# =====================================================
# GRAFICO DE LITOLOGIAS
# =====================================================
def create_lithology_chart():

    print("\n=== GERANDO GRAFICO DE LITOLOGIAS ===")

    geology = geomoz.read_geology()

    top = geology["Legend"].value_counts().head(10)

    labels = [wrap_label(l, 40) for l in top.index]

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.barh(
        range(len(top)),
        top.values,
        height=0.8
    )

    ax.set_yticks(range(len(top)))
    ax.set_yticklabels(labels, fontsize=9)

    ax.set_title("Top Litologias", fontsize=13, fontweight="bold")
    ax.set_xlabel("Frequência")

    ax.invert_yaxis()
    ax.grid(axis='x', linestyle='--', alpha=0.3)

    plt.tight_layout()
    plt.savefig("grafico_litologias.png", dpi=300)
    plt.show()


# =====================================================
# MAIN
# =====================================================
def main():

    print("\n====================================")
    print("GeoMoz - Visualização Geológica")
    print("====================================")

    try:
        create_geological_map()
        create_lithology_chart()

        print("\nArquivos gerados:")
        print(" - mapa_era_profissional.png")
        print(" - grafico_litologias.png")

    except Exception as e:
        print("\nErro:", e)
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()