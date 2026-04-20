# GeoMoz - Guia de Referência Rápida

## 🚀 Início Rápido

```python
import geomoz

# 1. Listar datasets disponíveis
geomoz.list_geomoz()

# 2. Carregar dados
provinces = geomoz.read_province()
districts = geomoz.read_district()
posts = geomoz.read_admin_post()
villages = geomoz.read_village()  # Usar cache!
geology = geomoz.read_geology()

# 3. Visualizar
from geomoz import quick_map
quick_map(provinces, column='Provincia')
```

---

## 📚 Funções de Leitura

### Províncias
```python
# Todas
all_provinces = geomoz.read_province()

# Por nome
maputo = geomoz.read_province(name_province="Maputo Província")

# Por código
nampula = geomoz.read_province(code_province="03")

# Colunas: CodProv, Provincia, geometry
```

### Distritos
```python
# Todas
districts = geomoz.read_district()

# Por nome
lichinga = geomoz.read_district(name_district="Lichinga")

# Filtrar por província
nampula_districts = districts[districts['Provincia'] == 'Nampula']

# Colunas: CodDist, Distrito, CodProv, Provincia, geometry
```

### Postos Administrativos
```python
posts = geomoz.read_admin_post()

# Filtrar
nampula_posts = posts[posts['Provincia'] == 'Nampula']
district_posts = posts[posts['Distrito'] == 'Nampula']

# Colunas: CodPosto, Posto, CodDist, Distrito, CodProv, Provincia, geometry
```

### Aldeias (Cache Recomendado!)
```python
# Usar cache para velocidade
from geomoz.utils.cache import CachedGeoMoz

villages = CachedGeoMoz.read_village()

# Filtrar
post_villages = villages[villages['Posto'] == 'Cidade de Nampula']

# Colunas: CodPov, Povoacao, CodPosto, Posto, CodDist, Distrito, CodProv, Provincia, geometry
```

### Geologia
```python
geology = geomoz.read_geology()

# Filtrar por era
proterozoic = geology[geology['ERA'] == 'Proterozoic']

# Filtrar por litologia
granites = geology[geology['Legend'].str.contains('granite', case=False)]

# Colunas: code2006, Legend, UNITNAME, ROCKTYPE1, ERA, geometry
```

---

## 🎨 Visualização

### Plot Básico
```python
import matplotlib.pyplot as plt
from geomoz import quick_map

# Mapa rápido
quick_map(provinces, column='Provincia', title='Mapa de Províncias')

# Plot personalizado
fig, ax = plt.subplots(figsize=(12, 10))
provinces.plot(ax=ax, column='Provincia', cmap='tab20', legend=True)
ax.set_title('Províncias de Moçambique')
plt.show()
```

### Utilitários de Plot
```python
from geomoz import (
    plot_provinces,
    plot_districts_by_province,
    plot_administrative_hierarchy,
    plot_villages_with_names,
    plot_geology_by_area,
    quick_map
)

# Províncias com nomes
plot_provinces(show_names=True, save_path='provincias.png')

# Distritos de uma província
plot_districts_by_province("Nampula", show_names=True)

# Hierarquia completa (4 níveis)
plot_administrative_hierarchy("Sofala")

# Aldeias com nomes
plot_villages_with_names("Cidade de Lichinga")

# Geologia por área
plot_geology_by_area(geo_data, column='Legend')

# Comparação lado a lado
create_comparison_plot([tete, nampula], ["Tete", "Nampula"])
```

---

## 🌐 Mapas Web (Folium)

```python
import folium
from folium import plugins

# Criar mapa base
m = folium.Map(location=[-18.5, 35.0], zoom_start=6)

# Adicionar camadas
folium.GeoJson(provinces, name="Províncias").add_to(m)
folium.GeoJson(districts, name="Distritos").add_to(m)

# Plugins
plugins.MiniMap().add_to(m)
plugins.Fullscreen().add_to(m)
plugins.LocateControl().add_to(m)

# Controle de camadas
folium.LayerControl().add_to(m)

# Salvar
m.save('mapa.html')
```

---

## 🎯 Análise Espacial

### Interseção
```python
import geopandas as gpd

# Geologia dentro de uma província
geo_in_province = gpd.overlay(geology, province, how='intersection')

# Interseção, união, diferença
result = gpd.overlay(gdf1, gdf2, how='intersection')  # ou 'union', 'difference'
```

### Funções Espaciais do GeoMoz
```python
from geomoz.spatial import (
    geology_by_province,
    geology_by_district,
    link_village_district
)

# Geologia por província
geo_nampula = geology_by_province(name_province="Nampula")

# Geologia por distrito
geo_tete = geology_by_district(name_district="Tete")

# Link entre datasets
linked_data = link_village_district(name_district="Nampula")
```

### Cálculo de Área
```python
# Converter para CRS projetado (metros)
gdf_utm = gdf.to_crs(epsg=32736)  # UTM zona 36S

# Calcular área em km²
area_km2 = gdf_utm.geometry.area / 1e6

# Adicionar como coluna
gdf['area_km2'] = area_km2
```

---

## ⚡ Cache

```python
from geomoz.utils.cache import (
    CachedGeoMoz,
    cache_info,
    print_cache,
    clear_cache
)

# Usar versões cacheadas (muito mais rápido!)
villages = CachedGeoMoz.read_village()      # 20x+ rápido na 2ª vez
geology = CachedGeoMoz.read_geology()       # 15x+ rápido
posts = CachedGeoMoz.read_admin_post()     # 10x+ rápido

# Ver informações do cache
print_cache()

# Limpar cache antigo
clear_cache(older_than_hours=48)
```

---

## 📊 Cores Geológicas Padrão

```python
era_colors = {
    'Archean': '#6b3d2e',      # Marrom escuro
    'Proterozoic': '#a0522d',   # Marrom
    'Paleozoic': '#4f81bd',     # Azul
    'Mesozoic': '#f1c232',      # Amarelo
    'Cenozoic': '#6aa84f',      # Verde
    'Other': '#cccccc'          # Cinza
}
```

---

## 🔧 Transformações de CRS

```python
# CRS padrão (WGS 84 - graus)
print(gdf.crs)  # epsg:4326

# Converter para UTM (metros - bom para cálculos)
gdf_utm = gdf.to_crs(epsg=32736)  # Zona 36S (Moçambique)

# Zonas UTM para Moçambique:
# - Oeste (Cabo Delgado, Niassa): epsg:32735 (Zona 35S)
# - Centro/Leste: epsg:32736 (Zona 36S)
```

---

## 💾 Exportação

```python
# GeoJSON
provinces.to_file('provinces.geojson', driver='GeoJSON')

# Shapefile
provinces.to_file('provinces.shp')

# Excel (sem geometria)
provinces.drop('geometry', axis=1).to_excel('provinces.xlsx', index=False)

# CSV (sem geometria)
provinces.drop('geometry', axis=1).to_csv('provinces.csv', index=False)
```

---

## 📈 Estatísticas Rápidas

```python
# Contagem
print(f"Total: {len(gdf)}")

# Por categoria
print(gdf['ERA'].value_counts())

# Estatísticas descritivas
print(gdf['area_km2'].describe())

# Group by
summary = gdf.groupby('Provincia').agg({
    'area_km2': ['count', 'sum', 'mean']
})
```

---

## 🐍 Snippets Comuns

### Criar mapa com legenda
```python
fig, ax = plt.subplots(figsize=(12, 10))

gdf.plot(ax=ax, column='Legend', cmap='tab20', 
         legend=True, legend_kwds={'title': 'Litologia', 
                                   'bbox_to_anchor': (1.05, 1)})
ax.set_title('Mapa Geológico')
ax.axis('off')
plt.tight_layout()
plt.show()
```

### Adicionar nomes no mapa
```python
for idx, row in gdf.iterrows():
    centroid = row.geometry.centroid
    ax.annotate(
        row['Provincia'],
        (centroid.x, centroid.y),
        fontsize=8, ha='center',
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.7)
    )
```

### Mapa com múltiplos níveis
```python
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Província
province.plot(ax=axes[0, 0])
axes[0, 0].set_title('1. Província')

# Distritos
districts.plot(ax=axes[0, 1], column='Distrito', cmap='tab20')
axes[0, 1].set_title('2. Distritos')

# Postos
posts.plot(ax=axes[1, 0], column='Posto', cmap='tab20b')
axes[1, 1].set_title('3. Postos')

# Aldeias (amostra)
sample = villages.iloc[::10]
sample.plot(ax=axes[1, 1], markersize=1)
axes[1, 1].set_title('4. Aldeias (amostra)')

plt.tight_layout()
plt.show()
```

---

## 🆘 Resolução de Problemas

### Erro: Dados demais para aldeias
```python
# ❌ Lento
villages = geomoz.read_village()

# ✅ Rápido
from geomoz.utils.cache import CachedGeoMoz
villages = CachedGeoMoz.read_village()
```

### Erro: CRS diferentes
```python
# Garantir mesmo CRS
gdf1 = gdf1.to_crs(gdf2.crs)
result = gpd.overlay(gdf1, gdf2, how='intersection')
```

### Erro: Memória
```python
# Processar em chunks
for prov in provinces['Provincia']:
    geo_in_prov = gpd.overlay(geology, 
                               provinces[provinces['Provincia']==prov], 
                               how='intersection')
    # Salvar/processar
```

### Erro: Nome de província
```python
# Verificar nomes válidos
print(provinces['Provincia'].tolist())
# Use exatamente o nome da lista!
```

---

## 📚 Recursos Adicionais

- **README Completo**: `README_COMPREHENSIVE.md`
- **Tutorial Educativo**: `TUTORIAL.md`
- **Exemplos**: Pasta `examples/`
- **Documentação API**: Docstrings nas funções

---

**GeoMoz** - Referência rápida para trabalho eficiente! 🚀
