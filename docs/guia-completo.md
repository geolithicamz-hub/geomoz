# GeoMoz - Pacote de Dados Geográficos de Moçambique

<p align="center">
  <img src="https://img.shields.io/badge/version-0.1.4-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/python-3.9%2B-blue.svg" alt="Python">
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
git clone https://github.com/geolithicamz-hub/geomoz.git
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
geo_tete = geology_by_district(name_district="Cidade de Tete")
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
- **Colunas normalizadas**: `Povoacao`, `Posto`, `Distrito`, `Provincia`, `Latitude`, `Longitude`, `geometry` (as colunas originais do dataset são mantidas em seguida)

```python
# Usar cache para aldeias (dados grandes!)
from geomoz.utils.cache import CachedGeoMoz
villages = CachedGeoMoz.read_village()
print(f"Total de aldeias: {len(villages)}") # 11.524
```

### Dados Geológicos

#### Geologia
- **Função**: `read_geology()`
- **Colunas principais**: `code2006`, `Legend`, `Legenda`, `EON`, `ERA`, `PERIOD`, `SUITE`, `Formation`, `geometry` (entre outras)

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
# Carregar tudo de uma província usando análise espacial
from geomoz import read_province, read_district, read_admin_post, read_village
import geopandas as gpd

province_name = "Nampula"

# 1. Província
province = read_province(name_province=province_name)
# Usar union_all() para evitar DeprecationWarning
area_provincia = province.geometry.union_all()

# 2. Distritos
districts = read_district()
province_districts = districts[districts.intersects(area_provincia)]

# 3. Postos
posts = read_admin_post()
province_posts = posts[posts.intersects(area_provincia)]

# 4. Aldeias
villages = read_village()
# Garantir que o CRS seja o mesmo para a operação espacial
villages = villages.to_crs(province.crs)
province_villages = villages[villages.intersects(area_provincia)]

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

# Plotar — legenda fora do mapa para não sobrepor a figura
provinces.plot(ax=ax, column='Provincia', cmap='tab20',
               edgecolor='black', linewidth=1, legend=True,
               legend_kwds={'loc': 'center left', 'bbox_to_anchor': (1, 0.5),
                            'title': 'Província'})

ax.set_title('Províncias de Moçambique', fontsize=16)
ax.axis('off')
plt.tight_layout()
plt.savefig('provincias.png', dpi=300, bbox_inches='tight')
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
import matplotlib.pyplot as plt
from geomoz.spatial import geology_by_province

# Recorta a geologia à província (o CRS é tratado internamente)
geo = geology_by_province(name_province="Tete")

# A coluna 'ERA' do dataset original mistura maiúsculas/minúsculas e
# subdivisões (MESOARCHEAN, NEOPROTEROZOIC, Cretaceous, ...); normalizamos
# para as grandes eras geológicas antes de mapear.
def classificar_era(valor):
    v = str(valor).upper()
    if "ARCHEAN" in v:
        return "Arqueano"
    if "PROTEROZOIC" in v:
        return "Proterozoico"
    if "PALEOZOIC" in v or v in ("CAMBRIAN", "ORDOVISIAN"):
        return "Paleozoico"
    if "MESOZOIC" in v or v in ("JURRASSIC", "CRETACEOUS"):
        return "Mesozoico"
    if "CENOZOIC" in v or v in ("TERTIARY", "QUATERNARY"):
        return "Cenozoico"
    return "Outro"

geo["Era"] = geo["ERA"].map(classificar_era)

# Plotar — a legenda fica FORA do mapa para não sobrepor a figura
fig, ax = plt.subplots(figsize=(12, 10))
geo.plot(
    ax=ax,
    column="Era",
    categorical=True,
    cmap="tab10",
    legend=True,
    legend_kwds={"loc": "center left", "bbox_to_anchor": (1, 0.5),
                 "title": "Era geológica"},
    edgecolor="black",
    linewidth=0.2,
)
ax.set_title("Geologia de Tete por Era", fontsize=16)
ax.axis("off")
plt.tight_layout()
plt.show()
```

### Exemplo 4: Mapa Web Interativo

```python
import folium
from folium import plugins
import geomoz
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from google.colab import files

# 1. Carregamento de Dados
geology = geomoz.read_geology()
province = geomoz.read_province(name_province='Maputo Província')

# 2. Processamento Espacial
geology = geology.to_crs(province.crs)
geo_province = gpd.overlay(geology, province, how='intersection')

# 3. Mapeamento de Cores Profissional
lithologies = geo_province['Legend'].unique()
cmap = plt.get_cmap('tab20', len(lithologies))
litho_colors_map = {l: colors.rgb2hex(cmap(i)) for i, l in enumerate(lithologies)}

# 4. Inicialização do Mapa com Design Moderno
m = folium.Map(
    location=[-25.5, 32.5], 
    zoom_start=9, 
    tiles='cartodbpositron', # Fundo limpo e moderno
    control_scale=True
)

# 5. Adição de Plugins de Alta Performance
plugins.Fullscreen(position='topright', title='Tela Cheia', title_cancel='Sair').add_to(m)
plugins.LocateControl(auto_start=False).add_to(m)
plugins.MeasureControl(position='topleft', primary_length_unit='kilometers', secondary_length_unit='miles').add_to(m)
plugins.Draw(export=True).add_to(m)

# 6. Camada de Geologia com Interatividade Avançada
geo_layer = folium.GeoJson(
    geo_province,
    name='Geologia Detalhada',
    style_function=lambda x: {
        'fillColor': litho_colors_map.get(x['properties']['Legend'], '#cccccc'),
        'color': '#2c3e50',
        'weight': 0.5,
        'fillOpacity': 0.7
    },
    highlight_function=lambda x: {'weight': 3, 'color': 'white', 'fillOpacity': 0.9},
    popup=folium.GeoJsonPopup(
        fields=['Legend', 'ERA'],
        aliases=['Litologia:', 'Era Geológica:'],
        localize=True,
        labels=True,
        style="background-color: white; color: #333; font-family: sans-serif; font-size: 12px; padding: 10px;"
    )
).add_to(m)

# 7. Camada de Contorno da Província
folium.GeoJson(
    province.boundary,
    name='Limites Administrativos',
    style_function=lambda x: {'color': '#e74c3c', 'weight': 2.5, 'dashArray': '5, 5'}
).add_to(m)

# 8. Controle de Camadas
folium.LayerControl(collapsed=False).add_to(m)

# 9. Salvar e Baixar
nome_pro = 'geoportal_maputo_pro.html'
m.save(nome_pro)
files.download(nome_pro)

print(f'Aplicação Completa Gerada: {nome_pro}')
m
```

---

## Utilitários de Plot

O GeoMoz inclui funções utilitárias para visualização rápida:

```python
from geomoz import (
    read_province,
    read_district,
    read_admin_post,
    read_village,
    plot_provinces,
    plot_districts_by_province
)
import matplotlib.pyplot as plt

# 1. Carregar dados base
provincias = read_province()

# 2. Mapa Nacional
plot_provinces(show_names=True)

# 3. Distritos de Nampula
plot_districts_by_province("Nampula", show_names=True)

# 4. Solução para Hierarquia (Substituindo a função com erro por lógica manual)
prov_name = "Sofala"
prov_shape = read_province(name_province=prov_name)
area = prov_shape.geometry.union_all()

distritos = read_district()
postos = read_admin_post()
aldeias = read_village().to_crs(prov_shape.crs)

# Filtragem espacial correta
prov_dist = distritos[distritos.intersects(area)]
prov_post = postos[postos.intersects(area)]
prov_vill = aldeias[aldeias.intersects(area)]

fig, axes = plt.subplots(1, 3, figsize=(18, 6))
prov_shape.plot(ax=axes[0], color='lightgrey')
axes[0].set_title(f"Província: {prov_name}")
prov_dist.plot(ax=axes[1], column='Distrito', cmap='tab20')
axes[1].set_title(f"Distritos ({len(prov_dist)})")
prov_vill.plot(ax=axes[2], color='red', markersize=1)
axes[2].set_title(f"Aldeias ({len(prov_vill)})")
plt.show()

print(f"Análise de {prov_name} concluída com sucesso.")
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

# 1. Geologia por província
geo_nampula = geology_by_province(name_province="Nampula")

# 2. Geologia por distrito 
# Solução: Para evitar o erro de validação, usamos apenas o name_district e 
# garantimos que o code_district seja interpretado como o padrão aceito pela lib.
geo_zambezia = geology_by_district(code_district="all", name_district="Inhassunge")

# 3. Link entre datasets (Nampula)
villages_linked = link_village_district(name_district="Nampula")

# 4. Calcular área da geologia de Nampula
geo_nampula_com_area = calculate_area(geo_nampula)

print("Processamento concluído com sucesso.")
print(f"Área total mapeada em Nampula: {geo_nampula_com_area['area_km2'].sum():.2f} km²")
if not geo_manica.empty:
    print(f"Principais unidades em Manica:\n{geo_manica['Legend'].head()}")
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
proterozoic = geology[geology['ERA'].str.upper().str.contains('PROTEROZOIC', na=False)]

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
- **Email**: geolithicamz@gmail.com

---

<p align="center">
  <b>GeoMoz</b> - Dados geográficos de Moçambique ao alcance de todos!
</p>
