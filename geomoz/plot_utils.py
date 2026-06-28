#!/usr/bin/env python3
"""
Utilitários de Plot para GeoMoz
Funções auxiliares para visualização de dados geográficos
"""

import matplotlib.pyplot as plt
import geopandas as gpd
import numpy as np
from matplotlib.patches import Patch
from typing import Optional, List, Tuple, Dict, Any
import matplotlib.patheffects as path_effects


def plot_provinces(
    ax: Optional[plt.Axes] = None,
    figsize: Tuple[int, int] = (12, 10),
    show_names: bool = True,
    cmap: str = 'tab20',
    title: str = 'Províncias de Moçambique',
    save_path: Optional[str] = None,
    show: bool = True
) -> plt.Axes:
    """
    Plotar todas as províncias de Moçambique

    Parameters
    ----------
    ax : matplotlib.axes.Axes, optional
        Eixo para plotar. Se None, cria novo.
    figsize : tuple, optional
        Tamanho da figura. Default (12, 10).
    show_names : bool, optional
        Mostrar nomes das províncias. Default True.
    cmap : str, optional
        Colormap. Default 'tab20'.
    title : str, optional
        Título do mapa.
    save_path : str, optional
        Caminho para salvar figura.

    Returns
    -------
    matplotlib.axes.Axes
        Eixo com o plot

    Examples
    --------
    >>> from geomoz.plot_utils import plot_provinces
    >>> ax = plot_provinces()
    >>> ax = plot_provinces(show_names=False, cmap='Set3')
    """
    from . import read_province

    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)

    provinces = read_province()

    # Plotar
    colors = plt.get_cmap(cmap)(np.linspace(0, 1, len(provinces)))

    for idx, (i, row) in enumerate(provinces.iterrows()):
        gpd.GeoSeries([row.geometry]).plot(
            ax=ax,
            color=colors[idx],
            edgecolor='black',
            linewidth=1,
            alpha=0.7
        )

    # Adicionar nomes
    if show_names:
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

    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.axis('off')

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    if show:
        plt.show()

    return ax


def plot_districts_by_province(
    province_name: str,
    ax: Optional[plt.Axes] = None,
    figsize: Tuple[int, int] = (12, 10),
    show_names: bool = True,
    cmap: str = 'tab20',
    save_path: Optional[str] = None
) -> plt.Axes:
    """
    Plotar distritos de uma província específica

    Parameters
    ----------
    province_name : str
        Nome da província (e.g., "Nampula", "Maputo Província")
    ax : matplotlib.axes.Axes, optional
        Eixo para plotar.
    figsize : tuple, optional
        Tamanho da figura.
    show_names : bool, optional
        Mostrar nomes dos distritos.
    cmap : str, optional
        Colormap.
    save_path : str, optional
        Caminho para salvar.

    Returns
    -------
    matplotlib.axes.Axes

    Examples
    --------
    >>> from geomoz.plot_utils import plot_districts_by_province
    >>> ax = plot_districts_by_province("Nampula")
    """
    from . import read_province, read_district

    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)

    province = read_province(name_province=province_name)
    all_districts = read_district()
    districts = all_districts[all_districts['Provincia'] == province_name]

    # Plotar
    districts.plot(
        ax=ax,
        column='Distrito',
        cmap=cmap,
        edgecolor='black',
        linewidth=0.5,
        alpha=0.7,
        legend=show_names,
        legend_kwds={'loc': 'center left', 'bbox_to_anchor': (1, 0.5)}
    )

    province.boundary.plot(ax=ax, color='red', linewidth=2)

    if show_names:
        for idx, row in districts.iterrows():
            centroid = row.geometry.centroid
            ax.annotate(
                row['Distrito'][:15],
                (centroid.x, centroid.y),
                fontsize=7,
                ha='center',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='yellow', alpha=0.6)
            )

    ax.set_title(f'Distritos de {province_name}', fontsize=14, fontweight='bold')
    ax.axis('off')

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    return ax


def plot_administrative_hierarchy(
    province_name: str,
    district_name: Optional[str] = None,
    figsize: Tuple[int, int] = (16, 12),
    save_path: Optional[str] = None
) -> plt.Axes:
    """
    Plotar hierarquia administrativa completa

    Parameters
    ----------
    province_name : str
        Nome da província
    district_name : str, optional
        Nome do distrito para zoom
    figsize : tuple, optional
        Tamanho da figura
    save_path : str, optional
        Caminho para salvar

    Returns
    -------
    matplotlib.axes.Axes

    Examples
    --------
    >>> from geomoz.plot_utils import plot_administrative_hierarchy
    >>> ax = plot_administrative_hierarchy("Sofala")
    >>> ax = plot_administrative_hierarchy("Nampula", "Nampula")
    """
    from . import read_province, read_district, read_admin_post, read_village

    # Carregar dados
    province = read_province(name_province=province_name)
    districts = read_district()
    posts = read_admin_post()
    villages = read_village()

    # Filtrar
    prov_districts = districts[districts['Provincia'] == province_name]
    prov_posts = posts[posts['Provincia'] == province_name]
    prov_villages = villages[villages['Provincia'] == province_name]

    # Criar subplots
    fig, axes = plt.subplots(2, 2, figsize=figsize)

    # Nível 1: Província
    ax1 = axes[0, 0]
    province.plot(ax=ax1, color='lightgreen', edgecolor='darkgreen', linewidth=2)
    ax1.set_title(f'1. Província\n({province_name})', fontsize=12, fontweight='bold')
    ax1.axis('off')

    # Nível 2: Distritos
    ax2 = axes[0, 1]
    prov_districts.plot(ax=ax2, column='Distrito', cmap='tab20',
                        edgecolor='black', linewidth=0.5, legend=False)
    province.boundary.plot(ax=ax2, color='red', linewidth=2)
    ax2.set_title(f'2. Distritos\n({len(prov_districts)} distritos)',
                  fontsize=12, fontweight='bold')
    ax2.axis('off')

    # Nível 3: Postos
    ax3 = axes[1, 0]
    prov_districts.boundary.plot(ax=ax3, color='gray', linewidth=1, alpha=0.5)
    prov_posts.plot(ax=ax3, column='Posto', cmap='tab20b',
                    edgecolor='black', linewidth=0.3)
    ax3.set_title(f'3. Postos Administrativos\n({len(prov_posts)} postos)',
                  fontsize=12, fontweight='bold')
    ax3.axis('off')

    # Nível 4: Aldeias (amostra)
    ax4 = axes[1, 1]
    prov_districts.boundary.plot(ax=ax4, color='gray', linewidth=1)

    # Amostra de aldeias para visualização
    sample_villages = prov_villages.iloc[::max(1, len(prov_villages)//500)]
    sample_villages.plot(ax=ax4, color='red', markersize=1, alpha=0.5)

    ax4.set_title(f'4. Aldeias (Amostra)\n({len(prov_villages):,} total)',
                  fontsize=12, fontweight='bold')
    ax4.axis('off')

    plt.suptitle(f'Estrutura Administrativa de {province_name}',
                 fontsize=16, fontweight='bold')
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    return axes


def plot_villages_with_names(
    post_name: str,
    ax: Optional[plt.Axes] = None,
    figsize: Tuple[int, int] = (14, 10),
    max_villages: int = 20,
    save_path: Optional[str] = None
) -> plt.Axes:
    """
    Plotar aldeias de um posto administrativo com nomes

    Parameters
    ----------
    post_name : str
        Nome do posto administrativo
    ax : matplotlib.axes.Axes, optional
        Eixo para plotar
    figsize : tuple, optional
        Tamanho da figura
    max_villages : int, optional
        Máximo de aldeias para mostrar nomes
    save_path : str, optional
        Caminho para salvar

    Returns
    -------
    matplotlib.axes.Axes

    Examples
    --------
    >>> from geomoz.plot_utils import plot_villages_with_names
    >>> ax = plot_villages_with_names("Cidade de Nampula")
    """
    from . import read_village, read_admin_post

    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)

    villages = read_village()
    posts = read_admin_post()

    post_villages = villages[villages['Posto'] == post_name]
    post_boundary = posts[posts['Posto'] == post_name]

    if len(post_villages) == 0:
        print(f"Posto '{post_name}' não encontrado ou sem aldeias")
        return ax

    # Plotar limite
    post_boundary.boundary.plot(ax=ax, color='red', linewidth=2, label=f'Posto: {post_name}')

    # Plotar aldeias
    if len(post_villages) <= max_villages:
        colors = plt.cm.Set3(np.linspace(0, 1, len(post_villages)))
        for idx, (vill_idx, village) in enumerate(post_villages.iterrows()):
            gpd.GeoSeries([village.geometry]).plot(
                ax=ax, color=colors[idx], edgecolor='black',
                linewidth=0.5, alpha=0.8
            )

            centroid = village.geometry.centroid
            text = ax.annotate(
                village['Povoacao'],
                (centroid.x, centroid.y),
                fontsize=8, ha='center', fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8)
            )
            text.set_path_effects([path_effects.withStroke(linewidth=3, foreground='white')])
    else:
        post_villages.plot(ax=ax, color='lightblue', edgecolor='navy',
                          linewidth=0.3, alpha=0.6)

    ax.set_title(f'Aldeias do Posto: {post_name}\n({len(post_villages)} aldeias)',
                 fontsize=14, fontweight='bold')
    ax.axis('off')
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    return ax


def plot_geology_by_area(
    area_gdf: gpd.GeoDataFrame,
    column: str = 'code2006',
    ax: Optional[plt.Axes] = None,
    figsize: Tuple[int, int] = (14, 10),
    cmap: str = 'tab20',
    show_legend: bool = True,
    title: Optional[str] = None,
    save_path: Optional[str] = None
) -> plt.Axes:
    """
    Plotar geologia dentro de uma área específica

    Parameters
    ----------
    area_gdf : geopandas.GeoDataFrame
        Área de interesse (província, distrito, etc.)
    column : str, optional
        Coluna para colorir. Default 'code2006'.
    ax : matplotlib.axes.Axes, optional
        Eixo para plotar
    figsize : tuple, optional
        Tamanho da figura
    cmap : str, optional
        Colormap
    show_legend : bool, optional
        Mostrar legenda
    title : str, optional
        Título do mapa
    save_path : str, optional
        Caminho para salvar

    Returns
    -------
    matplotlib.axes.Axes

    Examples
    --------
    >>> from geomoz import read_geology, read_province
    >>> from geomoz.plot_utils import plot_geology_by_area
    >>> import geopandas as gpd
    >>>
    >>> province = read_province(name_province="Tete")
    >>> geology = read_geology()
    >>> geo_province = gpd.overlay(geology, province, how='intersection')
    >>> ax = plot_geology_by_area(province, geo_province, column='Legend')
    """
    from . import read_geology

    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)

    # Se não passar geologia filtrada, calcular
    if isinstance(area_gdf, gpd.GeoDataFrame) and 'code2006' not in area_gdf.columns:
        geology = read_geology()
        geology = geology.to_crs(area_gdf.crs)
        geo_area = gpd.overlay(geology, area_gdf, how='intersection')
    else:
        geo_area = area_gdf

    # Plotar
    geo_area.plot(
        ax=ax,
        column=column,
        cmap=cmap,
        edgecolor='black',
        linewidth=0.2,
        alpha=0.8,
        legend=show_legend,
        legend_kwds={'loc': 'center left', 'bbox_to_anchor': (1, 0.5), 'title': column}
    )

    # Contorno da área
    if isinstance(area_gdf, gpd.GeoDataFrame) and 'code2006' not in area_gdf.columns:
        area_gdf.boundary.plot(ax=ax, color='red', linewidth=2)

    if title:
        ax.set_title(title, fontsize=14, fontweight='bold')
    else:
        ax.set_title(f'Mapa Geológico ({len(geo_area)} unidades)', fontsize=14, fontweight='bold')

    ax.axis('off')

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    return ax


def create_comparison_plot(
    gdf_list: List[gpd.GeoDataFrame],
    titles: List[str],
    figsize: Tuple[int, int] = (16, 8),
    ncols: int = 2,
    cmap: str = 'tab20',
    save_path: Optional[str] = None
) -> plt.Axes:
    """
    Criar comparação lado a lado de múltiplos mapas

    Parameters
    ----------
    gdf_list : list
        Lista de GeoDataFrames para comparar
    titles : list
        Lista de títulos
    figsize : tuple, optional
        Tamanho da figura
    ncols : int, optional
        Número de colunas
    cmap : str, optional
        Colormap
    save_path : str, optional
        Caminho para salvar

    Returns
    -------
    matplotlib.axes.Axes

    Examples
    --------
    >>> from geomoz import read_district
    >>> from geomoz.plot_utils import create_comparison_plot
    >>>
    >>> tete = read_district(name_district="Tete")
    >>> nampula = read_district(name_district="Nampula")
    >>> ax = create_comparison_plot([tete, nampula], ["Tete", "Nampula"])
    """
    nplots = len(gdf_list)
    nrows = (nplots + ncols - 1) // ncols

    fig, axes = plt.subplots(nrows, ncols, figsize=figsize)

    if nrows == 1 and ncols == 1:
        axes = [[axes]]
    elif nrows == 1:
        axes = [axes]
    elif ncols == 1:
        axes = [[ax] for ax in axes]

    for idx, (gdf, title) in enumerate(zip(gdf_list, titles)):
        row = idx // ncols
        col = idx % ncols
        ax = axes[row][col]

        gdf.plot(ax=ax, cmap=cmap, edgecolor='black', linewidth=0.5, alpha=0.7)
        ax.set_title(title, fontsize=12, fontweight='bold')
        ax.axis('off')

    # Esconder eixos vazios
    for idx in range(nplots, nrows * ncols):
        row = idx // ncols
        col = idx % ncols
        axes[row][col].axis('off')

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    return axes


def quick_map(
    gdf: gpd.GeoDataFrame,
    column: Optional[str] = None,
    figsize: Tuple[int, int] = (10, 8),
    title: Optional[str] = None,
    save_path: Optional[str] = None,
    show: bool = True
) -> plt.Axes:
    """
    Mapa rápido de um GeoDataFrame

    Parameters
    ----------
    gdf : geopandas.GeoDataFrame
        Dados para plotar
    column : str, optional
        Coluna para colorir
    figsize : tuple, optional
        Tamanho da figura
    title : str, optional
        Título
    save_path : str, optional
        Caminho para salvar
    show : bool, optional
        Mostrar o plot

    Returns
    -------
    matplotlib.axes.Axes

    Examples
    --------
    >>> from geomoz import read_province
    >>> from geomoz.plot_utils import quick_map
    >>>
    >>> provinces = read_province()
    >>> quick_map(provinces, column='Provincia')
    """
    fig, ax = plt.subplots(figsize=figsize)

    if column:
        # Place the legend outside the map area so it never overlaps the plot
        gdf.plot(ax=ax, column=column, cmap='tab20', edgecolor='black',
                linewidth=0.5, legend=True,
                legend_kwds={'loc': 'center left', 'bbox_to_anchor': (1, 0.5),
                             'title': column})
    else:
        gdf.plot(ax=ax, color='lightblue', edgecolor='black', linewidth=0.5)

    if title:
        ax.set_title(title, fontsize=14, fontweight='bold')

    ax.axis('off')

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    if show:
        plt.show()

    return ax


# Aliases para compatibilidade
plot_mozambique_provinces = plot_provinces
plot_districts = plot_districts_by_province
plot_hierarchy = plot_administrative_hierarchy
plot_villages = plot_villages_with_names
plot_geology = plot_geology_by_area
compare_maps = create_comparison_plot
