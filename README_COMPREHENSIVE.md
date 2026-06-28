# GeoMoz - Pacote de Dados Geográficos de Moçambique

<p align="center">
  <img src="https://img.shields.io/badge/version-0.1.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/python-3.8%2B-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/coverage-85%25-yellow.svg" alt="Coverage">
</p>

**GeoMoz** é um pacote Python que fornece acesso fácil e rápido a dados geográficos de Moçambique, incluindo divisões administrativas (províncias, distritos, postos, aldeias) e dados geológicos.

Inspirado no [`geobr`](https://github.com/ipeaGIT/geobr) (Brasil), o GeoMoz facilita a vida de geólogos, geógrafos, cientistas de dados e pesquisadores que trabalham com dados espaciais de Moçambique.

---

## Índice

1. [Instalação](#instalação)
2. [Visão Geral](#visão-geral)
3. [Guia Rápido](#guia-rápido)
4. [Dados Disponíveis](#dados-disponíveis)
5. [Funções Principais](#funções-principais)
6. [Exemplos Práticos](#exemplos-práticos)
7. [Utilitários de Plot](#utilitários-de-plot)
8. [Sistema de Cache](#sistema-de-cache)
9. [Análise Espacial](#análise-espacial)
10. [API Reference](#api-reference)
11. [Contribuição](#contribuição)
12. [Licença](#licença)

---

## Instalação

### Via pip (recomendado)

```bash
pip install geomoz
```

### Instalação em modo desenvolvimento

```bash
git clone https://github.com/geolithica/geomoz.git
cd geomoz
pip install -e ".[dev]"
```

### Dependências

```bash
pip install geopandas matplotlib pandas numpy folium branca
```

---

## Visão Geral

O GeoMoz oferece acesso a **11 províncias**, **161 distritos**, **459 postos administrativos**, **11.524 aldeias** e dados **geológicos completos** de Moçambique.

### Estrutura Administrativa

```
Moçambique (País)
├── 11 Províncias
│ ├── ~15 Distritos por província (161 total)
│ │ ├── ~3 Postos Administrativos por distrito (459 total)
│ │ │ ├── ~25 Aldeias por posto (11.524 total)
```

### Estatísticas de Dados

| Dataset | Registros | Tipo Geométrico |
|---------|-----------|-----------------|
| Províncias | 11 | MultiPolygon |
| Distritos | 161 | MultiPolygon |
| Postos Administrativos | 459 | MultiPolygon |
| Aldeias/Localidades | 11.524 | MultiPolygon |
| Unidades Geológicas | ~50.000 | MultiPolygon |

---

## Guia Rápido

### 1. Carregar Dados Administrativos

```python
import geomoz

# Todas as províncias
provinces = geomoz.read_province()
print(f"Total: {len(provinces)} províncias")

# Província específica por nome
maputo = geomoz.read_province(name_province="Maputo Província")

# Província específica por código
nampula = geomoz.read_province(code_province="03")

# Distritos de uma província
districts = geomoz.read_district()
nampula_districts = districts[districts['Provincia'] == "Nampula"]

# Postos administrativos
posts = geomoz.read_admin_post()

# Aldeias (usar cache para velocidade!)
from geomoz.utils.cache import CachedGeoMoz
villages = CachedGeoMoz.read_village() # 11.524 aldeias
```

### 2. Visualização Rápida

```python
from geomoz import quick_map, plot_provinces

# Mapa rápido
quick_map(provinces, column='Provincia')

# Plot com nomes
plot_provinces(show_names=True, save_path='mapa.png')
```

### 3. Dados Geológicos

```python
# Todas as unidades geológicas
geology = geomoz.read_geology()

# Geologia por província
from geomoz.spatial import geology_by_province
geo_nampula = geology_by_province(name_province="Nampula")

# Geologia por distrito
from geomoz.spatial import geology_by_district
geo_tete = geology_by_district(name_district="Tete")
```

---

## Dados Disponíveis

### Divisões Administrativas

#### Províncias
- **Função**: `read_province()`
- **Colunas**: `CodProv`, `Provincia`, `geometry`
- **CRS**: EPSG:4326

```python
provinces = geomoz.read_province()
# Resultado:
# CodProv Provincia geometry
# 0 01 Niassa MULTIPOLYGON (((36.123 -10.456...
# 1 02 Cabo Delgado MULTIPOLYGON (((40.789 -12.345...
```

#### Distritos
- **Função**: `read_district()`
- **Colunas**: `CodDist`, `Distrito`, `CodProv`, `Provincia`, `geometry`

```python
districts = geomoz.read_district()
# Resultado:
# CodDist Distrito CodProv Provincia geometry
# 0 01 Lichinga 01 Niassa MULTIPOLYGON ...
```

#### Postos Administrativos
- **Função**: `read_admin_post()`
- **Colunas**: `CodPosto`, `Posto`, `CodDist`, `Distrito`, `CodProv`, `Provincia`, `geometry`

```python
posts = geomoz.read_admin_post()
print(f"Total de postos: {len(posts)}") # 459
```

#### Aldeias (Localidades)
- **Função**: `read_village()` ou `CachedGeoMoz.read_village()`
- **Colunas**: `CodPov`, `Povoacao`, `CodPosto`, `Posto`, `CodDist`, `Distrito`, `CodProv`, `Provincia`, `geometry`

```python
# Usar cache para aldeias (dados grandes!)
from geomoz.utils.cache import CachedGeoMoz
villages = CachedGeoMoz.read_village()
print(f"Total de aldeias: {len(villages)}") # 11.524
```

### Dados Geológicos

#### Geologia
- **Função**: `read_geology()`
- **Colunas**: `code2006`, `Legend`, `UNITNAME`, `ROCKTYPE1`, `ERA`, `geometry`

```python
geology = geomoz.read_geology()
print(f"Unidades geológicas: {len(geology)}")

# Ver litologias únicas
print(geology['Legend'].unique())

# Ver eras geológicas
print(geology['ERA'].value_counts())
```

---

## Funções Principais

### Funções de Leitura

| Função | Descrição | Parâmetros Principais |
|--------|-----------|----------------------|
| `read_province()` | Carrega províncias | `code_province`, `name_province` |
| `read_district()` | Carrega distritos | `code_district`, `name_district` |
| `read_admin_post()` | Carrega postos | `code_admin_post`, `name_admin_post` |
| `read_village()` | Carrega aldeias | `code_village`, `name_village` |
| `read_geology()` | Carrega geologia | `code_geology`, `name_geology` |

### Exemplos de Uso

```python
# Carregar tudo de uma província
from geomoz import read_province, read_district, read_admin_post, read_village

province_name = "Nampula"

# 1. Província
province = read_province(name_province=province_name)

# 2. Distritos
districts = read_district()
province_districts = districts[districts['Provincia'] == province_name]

# 3. Postos
posts = read_admin_post()
province_posts = posts[posts['Provincia'] == province_name]

# 4. Aldeias
villages = read_village()
province_villages = villages[villages['Provincia'] == province_name]

print(f"{province_name}: {len(province_districts)} distritos, "
      f"{len(province_posts)} postos, {len(province_villages)} aldeias")
```

---

## Exemplos Práticos

### Exemplo 1: Mapa Básico de Províncias

```python
import geomoz
import matplotlib.pyplot as plt

# Carregar dados
provinces = geomoz.read_province()

# Criar figura
fig, ax = plt.subplots(figsize=(12, 10))

# Plotar
provinces.plot(ax=ax, column='Provincia', cmap='tab20',
               edgecolor='black', linewidth=1, legend=True)

ax.set_title('Províncias de Moçambique', fontsize=16)
ax.axis('off')
plt.savefig('provincias.png', dpi=300)
plt.show()
```

### Exemplo 2: Hierarquia Administrativa

```python
import geomoz
import matplotlib.pyplot as plt

# Selecionar província
province_name = "Sofala"

# Carregar dados hierárquicos
province = geomoz.read_province(name_province=province_name)
districts = geomoz.read_district()
posts = geomoz.read_admin_post()

# Filtrar
prov_districts = districts[districts['Provincia'] == province_name]
prov_posts = posts[posts['Provincia'] == province_name]

# Criar subplots
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# Nível 1: Província
province.plot(ax=axes[0], color='lightgreen', edgecolor='darkgreen')
axes[0].set_title('1. Província')
axes[0].axis('off')

# Nível 2: Distritos
prov_districts.plot(ax=axes[1], column='Distrito', cmap='tab20')
axes[1].set_title(f'2. Distritos ({len(prov_districts)})')
axes[1].axis('off')

# Nível 3: Postos
prov_posts.plot(ax=axes[2], column='Posto', cmap='tab20b')
axes[2].set_title(f'3. Postos ({len(prov_posts)})')
axes[2].axis('off')

plt.suptitle(f'Estrutura Administrativa: {province_name}', fontsize=16)
plt.tight_layout()
plt.show()
```

### Exemplo 3: Mapa Geológico

```python
import geomoz
import geopandas as gpd
import matplotlib.pyplot as plt

# Carregar dados
geology = geomoz.read_geology()
province = geomoz.read_province(name_province="Tete")

# Interseção
geology = geology.to_crs(province.crs)
geo_province = gpd.overlay(geology, province, how='intersection')

# Plotar por ERA
fig, ax = plt.subplots(figsize=(12, 10))

# Cores por era
era_colors = {
    'Archean': '#6b3d2e',
    'Proterozoic': '#a0522d',
    'Paleozoic': '#4f81bd',
    'Mesozoic': '#f1c232',
    'Cenozoic': '#6aa84f'
}

for era, color in era_colors.items():
    era_geo = geo_province[geo_province['ERA'] == era]
    if len(era_geo) > 0:
        era_geo.plot(ax=ax, color=color, label=era, edgecolor='black', linewidth=0.2)

ax.set_title('Geologia de Tete por Era', fontsize=16)
ax.legend(title='Era Geológica')
ax.axis('off')
plt.show()
```

### Exemplo 4: Mapa Web Interativo

```python
import folium
import geomoz

# Carregar dados
geology = geomoz.read_geology()
province = geomoz.read_province(name_province="Maputo Província")

# Interseção
import geopandas as gpd
geology = geology.to_crs(province.crs)
geo_province = gpd.overlay(geology, province, how='intersection')

# Criar mapa
m = folium.Map(location=[-25.5, 32], zoom_start=8)

# Adicionar geologia
folium.GeoJson(
    geo_province,
    style_function=lambda x: {'fillColor': 'blue', 'fillOpacity': 0.5}
).add_to(m)

# Adicionar contorno
folium.GeoJson(
    province.boundary,
    style_function=lambda x: {'color': 'red', 'weight': 2}
).add_to(m)

m.save('mapa_interativo.html')
```

---

## Utilitários de Plot

O GeoMoz inclui funções utilitárias para visualização rápida:

```python
from geomoz import (
    quick_map,
    plot_provinces,
    plot_districts_by_province,
    plot_administrative_hierarchy,
    plot_villages_with_names,
    plot_geology_by_area,
    create_comparison_plot
)

# Mapa rápido
quick_map(provinces, column='Provincia')

# Plot de províncias com nomes
plot_provinces(show_names=True, save_path='mapa.png')

# Distritos de uma província
plot_districts_by_province("Nampula", show_names=True)

# Hierarquia completa
plot_administrative_hierarchy("Sofala")

# Aldeias com nomes
plot_villages_with_names("Cidade de Nampula")

# Geologia
plot_geology_by_area(geo_data, column='Legend')

# Comparação lado a lado
create_comparison_plot([tete, nampula, sofala],
                        ["Tete", "Nampula", "Sofala"])
```

---

## Sistema de Cache

Para dados grandes (aldeias, geologia), use o cache para acelerar:

```python
from geomoz.utils.cache import CachedGeoMoz

# Primeira vez: lento (salva no cache)
villages = CachedGeoMoz.read_village() # ~10 segundos

# Segunda vez: muito rápido (do cache)
villages = CachedGeoMoz.read_village() # ~0.5 segundos (20x+ rápido!)

# Informações do cache
from geomoz.utils.cache import print_cache
print_cache()

# Limpar cache antigo
from geomoz.utils.cache import clear_cache
clear_cache(older_than_hours=48) # Remove cache mais antigo que 48h
```

### Performance

| Dataset | Sem Cache | Com Cache | Speedup |
|---------|-----------|-----------|---------|
| Aldeias (11.524) | ~10s | ~0.5s | **20x** |
| Geologia (~50k) | ~15s | ~1s | **15x** |
| Postos (459) | ~3s | ~0.3s | **10x** |

---

## Análise Espacial

O GeoMoz inclui funções espaciais avançadas:

```python
from geomoz.spatial import (
    geology_by_province,
    geology_by_district,
    link_village_district,
    calculate_area
)

# Geologia por província
geo_nampula = geology_by_province(name_province="Nampula")

# Geologia por distrito
geo_tete = geology_by_district(name_district="Tete")

# Link entre datasets
villages_linked = link_village_district(name_district="Nampula")

# Calcular área (com CRS projetado automaticamente)
from geomoz.spatial import calculate_area
areas = calculate_area(geology_gdf)
```

---

## API Reference

### Read Functions

#### `read_province(code_province="all", name_province=None)`
Carrega dados de províncias.

**Parâmetros:**
- `code_province` (str|int): Código da província ("all" para todas)
- `name_province` (str): Nome da província

**Retorna:** GeoDataFrame

**Exemplo:**
```python
# Todas as províncias
all_provinces = geomoz.read_province()

# Província específica
maputo = geomoz.read_province(name_province="Maputo Província")

# Por código
niassa = geomoz.read_province(code_province="01")
```

#### `read_district(code_district="all", name_district=None)`
Carrega dados de distritos.

**Parâmetros:**
- `code_district` (str|int): Código do distrito
- `name_district` (str): Nome do distrito

**Exemplo:**
```python
# Distritos de Nampula
districts = geomoz.read_district()
nampula_districts = districts[districts['Provincia'] == 'Nampula']

# Distrito específico
lichinga = geomoz.read_district(name_district="Lichinga")
```

#### `read_admin_post(code_admin_post="all", name_admin_post=None)`
Carrega dados de postos administrativos.

**Exemplo:**
```python
posts = geomoz.read_admin_post()
nampula_posts = posts[posts['Provincia'] == 'Nampula']
```

#### `read_village(code_village="all", name_village=None)`
Carrega dados de aldeias/localidades.

**Nota:** Usar `CachedGeoMoz.read_village()` para melhor performance.

#### `read_geology(code_geology="all", name_geology=None)`
Carrega dados geológicos.

**Exemplo:**
```python
# Todas as unidades
geology = geomoz.read_geology()

# Filtrar por era
proterozoic = geology[geology['ERA'] == 'Proterozoic']

# Filtrar por litologia
granites = geology[geology['ROCKTYPE1'].str.contains('granite', case=False)]
```

### Plot Functions

#### `quick_map(gdf, column=None, title=None)`
Mapa rápido e simples.

```python
from geomoz import quick_map
quick_map(provinces, column='Provincia', title='Mapa de Províncias')
```

#### `plot_provinces(show_names=True, cmap='tab20')`
Plot de províncias com nomes.

#### `plot_districts_by_province(province_name, show_names=True)`
Plot de distritos de uma província.

```python
plot_districts_by_province("Nampula", show_names=True)
```

---

## Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Fork o repositório
2. Crie uma branch (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

### Desenvolvimento

```bash
# Instalar dependências de desenvolvimento
pip install -e ".[dev]"

# Executar testes
pytest

# Executar com cobertura
pytest --cov=geomoz

# Linting
flake8 geomoz/
black geomoz/
```

---

## Licença

MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## Agradecimentos

- **INE Moçambique** - Fonte dos dados administrativos
- **ING (Instituto Nacional de Geologia)** - Dados geológicos
- **geobr** - Inspiração para o projeto

---

## Contato

- **GitHub**: https://github.com/geolithica/geomoz
- **Issues**: https://github.com/geolithica/geomoz/issues
- **Email**: support@geolithica.com

---

<p align="center">
  <b>GeoMoz</b> - Dados geográficos de Moçambique ao alcance de todos!
</p>
