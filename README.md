# GeoMoz - Dados Geográficos de Moçambique

<p align="center">
  <a href="https://github.com/geolithicamz-hub/geomoz/actions/workflows/ci.yml"><img src="https://github.com/geolithicamz-hub/geomoz/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://pypi.org/project/geomoz/"><img src="https://img.shields.io/pypi/v/geomoz.svg" alt="PyPI"></a>
  <a href="https://pypi.org/project/geomoz/"><img src="https://img.shields.io/pypi/pyversions/geomoz.svg" alt="Python"></a>
  <img src="https://img.shields.io/badge/R-4.0%2B-blue.svg" alt="R">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
</p>

**GeoMoz** é um pacote Python que fornece acesso fácil a dados geográficos de Moçambique, incluindo divisões administrativas (11 províncias, 161 distritos, 459 postos, 11.524 aldeias) e dados geológicos completos.

Inspirado no [`geobr`](https://github.com/ipeaGIT/geobr) (Brasil).

> **Agora também disponível em R!** Veja a pasta [`R/`](https://github.com/geolithicamz-hub/geomoz/tree/main/R) para o pacote **GeoMozR**.

---

## Versões Disponíveis

| Linguagem | Instalação | Pasta |
|-----------|-----------|-------|
| **Python** | `pip install geomoz` | Raiz do projeto |
| **R** | `devtools::install_github("geolithicamz-hub/geomoz", subdir="R")` | [`R/`](https://github.com/geolithicamz-hub/geomoz/tree/main/R) |

---

## Instalação

```bash
pip install geomoz
```

Com dependências completas:
```bash
pip install geomoz geopandas matplotlib folium
```

---

## Uso Rápido

```python
import geomoz
import matplotlib.pyplot as plt

# Carregar dados
provincias = geomoz.read_province()
print(f"{len(provincias)} províncias carregadas")

# Criar figura
fig, ax = plt.subplots(figsize=(8, 12))

# Plot — a legenda é colocada FORA do mapa para não sobrepor a figura
provincias.plot(
    ax=ax,
    column="Provincia",
    cmap="tab20",
    edgecolor="black",
    linewidth=0.8,
    legend=True,
    legend_kwds={
        "loc": "center left",
        "bbox_to_anchor": (1.02, 0.5),  # à direita, fora do mapa
        "title": "Província",
    },
)

# Ajustes
ax.set_title("Províncias de Moçambique", fontsize=14)
ax.axis("off")

plt.tight_layout()
plt.show()
```

---

## Dados Disponíveis

| Dataset | Registros | Função |
|---------|-----------|--------|
| **Províncias** | 11 | `read_province()` |
| **Distritos** | 161 | `read_district()` |
| **Postos Administrativos** | 459 | `read_admin_post()` |
| **Aldeias** | 11.524 | `read_village()` / `CachedGeoMoz.read_village()` |
| **Geologia** | ~50.000 | `read_geology()` |

---

## Exemplos

### Mapa de Províncias
```python
from geomoz import plot_provinces
plot_provinces(show_names=True, save_path='mapa.png')
```

### Geologia por Província
```python
import geopandas as gpd
from geomoz import read_province, read_geology

province = read_province(name_province="Tete")
geology = read_geology()
geo_tete = gpd.overlay(geology, province, how='intersection')
print(f"Unidades geológicas em Tete: {len(geo_tete)}")
```

### Mapa Web Interativo
```python
import folium
from geomoz import read_province

province = read_province(name_province="Nampula")
m = folium.Map(location=[-14.5, 39], zoom_start=7)
folium.GeoJson(province).add_to(m)
m.save('mapa.html')
```

---

## Documentação

- **[Guia Completo](https://github.com/geolithicamz-hub/geomoz/blob/main/docs/guia-completo.md)** - Documentação detalhada
- **[Tutorial Educativo](https://github.com/geolithicamz-hub/geomoz/blob/main/docs/tutorial.md)** - Guia passo a passo
- **[Referência Rápida](https://github.com/geolithicamz-hub/geomoz/blob/main/docs/referencia-rapida.md)** - Cheat sheet
- **[Mapeamento Geológico](https://github.com/geolithicamz-hub/geomoz/blob/main/docs/mapeamento-geologico.md)** - Exemplos de mapas
- **[Exemplos](https://github.com/geolithicamz-hub/geomoz/tree/main/examples)** - Códigos de exemplo
- **[Artigo Técnico](https://github.com/geolithicamz-hub/geomoz/blob/main/ARTIGO_GEOMOZ.md)** - Visão geral da biblioteca
- **[Changelog](https://github.com/geolithicamz-hub/geomoz/blob/main/CHANGELOG.md)** - Histórico de versões

---

## Desenvolvimento

```bash
git clone https://github.com/geolithicamz-hub/geomoz.git
cd geomoz
pip install -e ".[dev]"
pytest -m "not network"
```

---

## Licença

MIT License - veja [LICENSE](https://github.com/geolithicamz-hub/geomoz/blob/main/LICENSE)

---

**GeoMoz** - Dados geográficos de Moçambique ao alcance de todos!
