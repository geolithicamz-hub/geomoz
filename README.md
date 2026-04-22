# GeoMoz - Dados Geográficos de Moçambique

<p align="center">
  <img src="https://img.shields.io/badge/version-0.1.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/python-3.8%2B-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
</p>

**GeoMoz** é um pacote Python que fornece acesso fácil a dados geográficos de Moçambique, incluindo divisões administrativas (11 províncias, 161 distritos, 459 postos, 11.524 aldeias) e dados geológicos completos.

Inspirado no [`geobr`](https://github.com/ipeaGIT/geobr) (Brasil).

---

## 🚀 Instalação

```bash
pip install geomoz
```

Com dependências completas:
```bash
pip install geomoz geopandas matplotlib folium
```

---

## ⚡ Uso Rápido

```python
import geomoz
import matplotlib.pyplot as plt

# Carregar dados
provincias = geomoz.read_province()
print(f"✅ {len(provincias)} províncias carregadas")

# Criar figura
fig, ax = plt.subplots(figsize=(8, 12))

# Plot
provincias.plot(
    ax=ax,
    column="Provincia",
    cmap="tab20",
    edgecolor="black",
    linewidth=0.8,
    legend=True,
    legend_kwds={"loc": "upper left", "title": "Provincias"}
)

# Ajustes
ax.set_title("Províncias de Moçambique", fontsize=14)
ax.axis("off")

# Mover legenda
leg = ax.get_legend()
leg.set_bbox_to_anchor((1.05, 1))  # fora do mapa

plt.tight_layout()
plt.show()
```

---

## 📊 Dados Disponíveis

| Dataset | Registros | Função |
|---------|-----------|--------|
| **Províncias** | 11 | `read_province()` |
| **Distritos** | 161 | `read_district()` |
| **Postos Administrativos** | 459 | `read_admin_post()` |
| **Aldeias** | 11.524 | `read_village()` / `CachedGeoMoz.read_village()` |
| **Geologia** | ~50.000 | `read_geology()` |

---

## 🎨 Exemplos

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

## 📚 Documentação

- **📖 [README Completo](README_COMPREHENSIVE.md)** - Documentação detalhada
- **🎓 [Tutorial Educativo](TUTORIAL.md)** - Guia passo a passo
- **📋 [Referência Rápida](QUICK_REFERENCE.md)** - Cheat sheet
- **💻 [Exemplos](examples/)** - Códigos de exemplo

---

## 🛠️ Desenvolvimento

```bash
git clone https://github.com/geolithica/geomoz.git
cd geomoz
pip install -e ".[dev]"
pytest
```

---

## 📄 Licença

MIT License - veja [LICENSE](LICENSE)

---

**GeoMoz** - Dados geográficos de Moçambique ao alcance de todos! 🗺️🇲🇿
