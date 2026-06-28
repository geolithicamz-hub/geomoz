# Tutorial GeoMoz - Guia Educativo Passo a Passo

## Índice
1. [Introdução](#introdução)
2. [Instalação e Configuração](#instalação-e-configuração)
3. [Conceitos Básicos](#conceitos-básicos)
4. [Módulo 1: Divisões Administrativas](#módulo-1-divisões-administrativas)
5. [Módulo 2: Dados Geológicos](#módulo-2-dados-geológicos)
6. [Módulo 3: Visualização](#módulo-3-visualização)
7. [Módulo 4: Análise Espacial](#módulo-4-análise-espacial)
8. [Módulo 5: Mapas Web](#módulo-5-mapas-web)
9. [Exercícios Práticos](#exercícios-práticos)
10. [Dicas Avançadas](#dicas-avançadas)

---

## Introdução

### O que é o GeoMoz?

O **GeoMoz** é uma biblioteca Python que facilita o acesso a dados geográficos de Moçambique. Ele permite:

- Acessar divisões administrativas (províncias, distritos, postos, aldeias)
- Visualizar dados em mapas
- Analisar dados geológicos
- Criar mapas interativos para web
- Otimizar performance com cache

### Para quem é este tutorial?

- **Estudantes** de geologia, geografia, SIG
- **Pesquisadores** que trabalham com dados de Moçambique
- **Profissionais** em consultoria ambiental e geotecnologia
- **Desenvolvedores** que precisam de dados geoespaciais

---

## Instalação e Configuração

### Passo 1: Instalação Básica

```bash
# Via pip
pip install geomoz

# Ou com dependências completas
pip install geomoz geopandas matplotlib folium
```

### Passo 2: Verificação

```python
import geomoz
print(geomoz.__version__)

# Testar carregamento
provinces = geomoz.read_province()
print(f"GeoMoz funcionando! {len(provinces)} províncias carregadas.")
```

### Passo 3: Configuração de Cache (Opcional mas Recomendado)

```python
# O cache acelera carregamentos futuros
from geomoz.utils.cache import print_cache
print_cache() # Ver informações do cache
```

---

## Conceitos Básicos

### Estrutura de Dados

O GeoMoz trabalha com **GeoDataFrames** (do pacote GeoPandas). Um GeoDataFrame é como uma tabela do Excel, mas com uma coluna especial chamada `geometry` que contém formas geográficas.

```python
import geomoz

# Carregar províncias
provinces = geomoz.read_province()

# Ver estrutura
print(provinces.head())
print(provinces.columns)
print(type(provinces)) # <class 'geopandas.geodataframe.GeoDataFrame'>
```

### Sistema de Coordenadas (CRS)

Todos os dados usam **EPSG:4326** (WGS 84), que é o padrão internacional:

```python
# Verificar CRS
print(provinces.crs) # epsg:4326

# Converter para outro CRS se necessário
provinces_utm = provinces.to_crs(epsg=32736) # UTM zona 36S
```

---

## Módulo 1: Divisões Administrativas

### Lição 1.1: Províncias

**Conceito**: Moçambique tem 11 províncias. Cada província tem código e nome.

```python
import geomoz

# Carregar todas as províncias
provinces = geomoz.read_province()

# Ver informações
print(f"Total: {len(provinces)} províncias")
print("\nLista de províncias:")
for idx, row in provinces.iterrows():
    print(f" {row['CodProv']}: {row['Provincia']}")

# Carregar província específica
maputo = geomoz.read_province(name_province="Maputo Província")
nampula = geomoz.read_province(code_province="03")

# Plotar
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 8))
provinces.plot(ax=ax, column='Provincia', cmap='tab20', legend=True, legend_kwds={'loc': 'center left', 'bbox_to_anchor': (1, 0.5)})
ax.set_title('Províncias de Moçambique')
plt.show()
```

### Lição 1.2: Distritos

**Conceito**: Cada província tem vários distritos. Total: 161 distritos.

```python
# Carregar todos os distritos
districts = geomoz.read_district()
print(f"Total de distritos: {len(districts)}")

# Filtrar por província
nampula_districts = districts[districts['Provincia'] == 'Nampula']
print(f"Nampula tem {len(nampula_districts)} distritos:")
print(nampula_districts['Distrito'].tolist())

# Carregar distrito específico
lichinga = geomoz.read_district(name_district="Lichinga")
print(f"Lichinga: {lichinga.iloc[0]['Provincia']}")

# Plotar distritos de uma província
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 8))
nampula_districts.plot(ax=ax, column='Distrito', cmap='tab20')
ax.set_title('Distritos de Nampula')
plt.show()
```

**Exercício 1.2**: Liste todos os distritos da província de Tete.

### Lição 1.3: Postos Administrativos

**Conceito**: Os distritos são divididos em postos administrativos. Total: 459.

```python
posts = geomoz.read_admin_post()
print(f"Total de postos: {len(posts)}")

# Postos de um distrito específico
nampula_posts = posts[posts['Distrito'] == 'Nampula']
print(f"Distrito Nampula tem {len(nampula_posts)} postos:")
for idx, row in nampula_posts.iterrows():
    print(f" • {row['Posto']}")
```

### Lição 1.4: Aldeias (Localidades)

**Conceito**: Os postos são divididos em aldeias/localidades. Total: 11.524!

```python
# Usar cache para aldeias - são muitos dados!
from geomoz.utils.cache import CachedGeoMoz

villages = CachedGeoMoz.read_village()
print(f"Total de aldeias: {len(villages):,}")

# Aldeias de um posto
post_villages = villages[villages['Posto'] == 'Cidade de Nampula']
print(f"Cidade de Nampula tem {len(post_villages)} aldeias")

# Amostra de nomes
print("\nPrimeiras 10 aldeias:")
print(post_villages['Povoacao'].head(10).tolist())
```

**Dica**: Sempre use `CachedGeoMoz` para aldeias. Sem cache: ~10 segundos. Com cache: ~0.5 segundos.

---

## Módulo 2: Dados Geológicos

### Lição 2.1: Entendendo a Geologia

```python
geology = geomoz.read_geology()

# Estrutura
print(geology.columns.tolist())
# ['code2006', 'Legend', 'UNITNAME', 'ROCKTYPE1', 'ROCKTYPE2',
# 'SUITE', 'AGE1', 'ERA', 'geometry']

# Ver eras geológicas disponíveis
print(geology['ERA'].value_counts())
```

### Lição 2.2: Filtrar por Era

```python
# Eras geológicas
# - Archean (Arqueano): > 2.5 bilhões anos
# - Proterozoic (Proterozoico): 2.5B - 541M anos
# - Paleozoic (Paleozoico): 541M - 252M anos
# - Mesozoic (Mesozoico): 252M - 66M anos
# - Cenozoic (Cenozoico): < 66M anos

# Filtrar por era
proterozoic = geology[geology['ERA'].str.upper().str.contains('PROTEROZOIC', na=False)]
print(f"Unidades Proterozoicas: {len(proterozoic)}")

# Cores geologicamente corretas
era_colors = {
    'Archean': '#6b3d2e', # Marrom escuro (mais antigo)
    'Proterozoic': '#a0522d', # Marrom avermelhado
    'Paleozoic': '#4f81bd', # Azul
    'Mesozoic': '#f1c232', # Amarelo/dourado
    'Cenozoic': '#6aa84f', # Verde (mais recente)
}
```

### Lição 2.3: Geologia por Área

```python
import geopandas as gpd
from geomoz import read_province, read_geology

# Carregar dados
province = read_province(name_province="Tete")
geology = read_geology()

# Garantir mesmo CRS
geology = geology.to_crs(province.crs)

# Interseção: geologia dentro da província
geo_province = gpd.overlay(geology, province, how='intersection')

print(f"Unidades geológicas em Tete: {len(geo_province)}")
print(f"Por era:\n{geo_province['ERA'].value_counts()}")
```

---

## Módulo 3: Visualização

### Lição 3.1: Plot Básico

```python
import geomoz
import matplotlib.pyplot as plt

# Carregar dados
provinces = geomoz.read_province()

# Plot simples
provinces.plot()
plt.show()

# Plot com cores por atributo
provinces.plot(column='Provincia', cmap='tab20', legend=True, legend_kwds={'loc': 'center left', 'bbox_to_anchor': (1, 0.5)})
plt.title('Províncias de Moçambique')
plt.show()
```

### Lição 3.2: Utilitários de Plot

```python
from geomoz import (
    quick_map,
    plot_provinces,
    plot_districts_by_province,
    plot_administrative_hierarchy
)

# Mapa rápido
quick_map(provinces, column='Provincia')

# Províncias com nomes
plot_provinces(show_names=True, title='Províncias')

# Distritos
plot_districts_by_province("Sofala", show_names=True)

# Hierarquia completa (4 níveis)
plot_administrative_hierarchy("Nampula")
```

### Lição 3.3: Personalização Avançada

```python
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# Criar figura customizada
fig, ax = plt.subplots(figsize=(14, 10))

# Plotar com estilo personalizado
provinces.plot(
    ax=ax,
    column='Provincia',
    cmap='Set3',
    edgecolor='black',
    linewidth=1.5,
    alpha=0.8
)

# Adicionar anotações
for idx, row in provinces.iterrows():
    centroid = row.geometry.centroid
    ax.annotate(
        row['Provincia'],
        (centroid.x, centroid.y),
        fontsize=9,
        ha='center',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7)
    )

# Título e estilo
ax.set_title('Províncias de Moçambique', fontsize=18, fontweight='bold', pad=20)
ax.axis('off')

# Adicionar norte
ax.annotate('N', xy=(0.95, 0.95), xycoords='axes fraction',
            fontsize=16, ha='center', fontweight='bold')
ax.annotate('↑', xy=(0.95, 0.90), xycoords='axes fraction',
            fontsize=20, ha='center')

plt.tight_layout()
plt.savefig('mapa_personalizado.png', dpi=300, bbox_inches='tight')
plt.show()
```

---

## Módulo 4: Análise Espacial

### Lição 4.1: Interseção Espacial

```python
import geopandas as gpd
from geomoz import read_province, read_geology

# Carregar dados
province = read_province(name_province="Manica")
geology = read_geology()

# Interseção: o que está dentro da província
geology_in_province = gpd.overlay(
    geology,
    province,
    how='intersection' # Mantém apenas sobreposição
)

print(f"Unidades geológicas em Manica: {len(geology_in_province)}")
```

### Lição 4.2: Operações Espaciais

```python
from geomoz.spatial import (
    geology_by_province,
    geology_by_district,
    link_village_district
)

# Geologia por província (função utilitária)
geo_nampula = geology_by_province(name_province="Nampula")

# Geologia por distrito
geo_tete_city = geology_by_district(name_district="Cidade de Tete")

# Link villages to district
villages_with_district = link_village_district(name_district="Nampula")
```

### Lição 4.3: Cálculo de Área

```python
# Calcular área (precisa de CRS projetado para precisão)
province = geomoz.read_province(name_province="Nampula")

# Converter para UTM (metros)
province_utm = province.to_crs(epsg=32736)

# Calcular área em km²
area_km2 = province_utm.geometry.area / 1e6
print(f"Área de Nampula: {area_km2.iloc[0]:,.2f} km²")

# Para todas as províncias
provinces = geomoz.read_province()
provinces_utm = provinces.to_crs(epsg=32736)
provinces['area_km2'] = provinces_utm.geometry.area / 1e6

# Maior e menor
print(f"Maior: {provinces.loc[provinces['area_km2'].idxmax(), 'Provincia']}")
print(f"Menor: {provinces.loc[provinces['area_km2'].idxmin(), 'Provincia']}")
```

---

## Módulo 5: Mapas Web

### Lição 5.1: Mapa Interativo Básico

```python
import folium
from geomoz import read_province

# Carregar dados
province = read_province(name_province="Maputo Província")

# Criar mapa
m = folium.Map(location=[-25.5, 32.0], zoom_start=8)

# Adicionar província
folium.GeoJson(
    province,
    name="Maputo",
    style_function=lambda x: {
        'fillColor': 'lightgreen',
        'color': 'black',
        'weight': 2,
        'fillOpacity': 0.5
    }
).add_to(m)

# Controle de camadas
folium.LayerControl().add_to(m)

# Salvar
m.save('mapa_web.html')
print("Mapa salvo! Abra 'mapa_web.html' no navegador.")
```

### Lição 5.2: Mapa com Popups e Tooltips

```python
import folium
from geomoz import read_province, read_geology
import geopandas as gpd

# Carregar dados
province = read_province(name_province="Nampula")
geology = read_geology()

# Interseção
geology = geology.to_crs(province.crs)
geo_province = gpd.overlay(geology, province, how='intersection')

# Criar mapa
m = folium.Map(location=[-14.5, 39.0], zoom_start=7)

# Adicionar geologia com popup
for idx, row in geo_province.iterrows():
    popup_text = f"""
        <b>{row['Legend']}</b><br>
        Era: {row['ERA']}<br>
        Código: {row['code2006']}
    """

    folium.GeoJson(
        row.geometry.__geo_interface__,
        popup=folium.Popup(popup_text, max_width=200),
        tooltip=folium.Tooltip(row['Legend']),
        style_function=lambda x, era=row['ERA']: {
            'fillColor': era_colors.get(era, 'gray'),
            'fillOpacity': 0.6,
            'color': 'black',
            'weight': 1
        }
    ).add_to(m)

# Plugins adicionais
from folium import plugins
plugins.MiniMap().add_to(m)
plugins.Fullscreen().add_to(m)

m.save('mapa_geologico.html')
```

---

## Exercícios Práticos

### Exercício 1: Análise de Área
Calcule a área de todas as províncias e crie um ranking das 3 maiores e 3 menores.

<details>
<summary>Ver solução</summary>

```python
provinces = geomoz.read_province()
provinces_utm = provinces.to_crs(epsg=32736)
provinces['area_km2'] = provinces_utm.geometry.area / 1e6

# Ranking
top3 = provinces.nlargest(3, 'area_km2')[['Provincia', 'area_km2']]
bottom3 = provinces.nsmallest(3, 'area_km2')[['Provincia', 'area_km2']]

print("Top 3 maiores:")
print(top3)
print("\nTop 3 menores:")
print(bottom3)
```
</details>

### Exercício 2: Mapa de Calor de Aldeias
Crie um mapa mostrando a distribuição de aldeias por província.

<details>
<summary>Ver solução</summary>

```python
from geomoz.utils.cache import CachedGeoMoz

villages = CachedGeoMoz.read_village()
count_by_province = villages.groupby('Provincia').size()

# Plot
import matplotlib.pyplot as plt
count_by_province.plot(kind='barh', figsize=(10, 8))
plt.title('Aldeias por Província')
plt.xlabel('Número de Aldeias')
plt.show()
```
</details>

### Exercício 3: Análise Geológica
Determine qual província tem mais unidades do Mesozoico.

<details>
<summary>Ver solução</summary>

```python
import geopandas as gpd
from geomoz import read_province, read_geology

geology = read_geology()
provinces = read_province()

results = []
for idx, prov in provinces.iterrows():
    geo_in_prov = gpd.overlay(geology, gpd.GeoDataFrame([prov]), how='intersection')
    mesozoic_count = len(geo_in_prov[geo_in_prov['ERA'].str.upper().str.contains('MESOZOIC', na=False)])
    results.append({'Provincia': prov['Provincia'], 'Mesozoic': mesozoic_count})

import pandas as pd
results_df = pd.DataFrame(results)
print(results_df.nlargest(3, 'Mesozoic'))
```
</details>

---

## Dicas Avançadas

### Dica 1: Usar Cache Sempre

```python
from geomoz.utils.cache import CachedGeoMoz

# Bem rápido após a primeira vez
villages = CachedGeoMoz.read_village()
geology = CachedGeoMoz.read_geology()
posts = CachedGeoMoz.read_admin_post()
```

### Dica 2: Salvar Dados Filtrados

```python
# Salvar para usar depois
nampula_geo.to_file('nampula_geologia.geojson', driver='GeoJSON')

# Ou shapefile
nampula_geo.to_file('nampula_geologia.shp')
```

### Dica 3: Combinar com Outras Bibliotecas

```python
import seaborn as sns
import plotly.express as px

# Usar seaborn para estatísticas
sns.boxplot(data=villages, x='Provincia', y='area_km2')

# Usar plotly para interatividade
px.choropleth(provinces, geojson=provinces.geometry.__geo_interface__,
              locations=provinces.index, color='area_km2')
```

### Dica 4: Filtragem Eficiente

```python
# Lento: carregar tudo e filtrar
villages = geomoz.read_village()
nampula_villages = villages[villages['Provincia'] == 'Nampula']

# Mais rápido: filtrar durante carregamento (quando possível)
# Ou usar cache
from geomoz.utils.cache import CachedGeoMoz
villages = CachedGeoMoz.read_village() # Cache é mais rápido
nampula_villages = villages[villages['Provincia'] == 'Nampula']
```

---

## Conclusão

Você aprendeu:
- A instalar e configurar o GeoMoz
- A carregar divisões administrativas
- A trabalhar com dados geológicos
- A criar visualizações e mapas
- A fazer análises espaciais
- A criar mapas web interativos

### Próximos Passos

1. Explore os exemplos na pasta `examples/`
2. Experimente com seus próprios dados
3. Contribua com o projeto no GitHub

---

**GeoMoz** - Mapeando Moçambique, uma linha de código de cada vez!
