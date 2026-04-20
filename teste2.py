import geomoz
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd

def get_utm_zone_for_mozambique(longitude):
    """Determinar a zona UTM correta para Moçambique baseado na longitude"""
    if 30 <= longitude < 36:
        return 'EPSG:32733'  # UTM Zone 33S
    elif 36 <= longitude < 42:
        return 'EPSG:32736'  # UTM Zone 36S  
    elif 42 <= longitude < 48:
        return 'EPSG:32737'  # UTM Zone 37S
    else:
        return 'EPSG:32736'  # Default

print("=== GeoMoz - Mapa Completo: Todas as Camadas ===\n")

# 1. Carregar dados
province_name = "Zambézia"
print(f"1. Carregando geologia de {province_name}...")

geo = geomoz.geology_by_province(name_province=province_name)
zambezia = geomoz.read_province(name_province=province_name)

print(f"   Unidades geológicas: {len(geo)}")
print(f"   Província: {zambezia.iloc[0]['Provincia']}")
print(f"   CRS original: {geo.crs}")

# 1.1. Converter para CRS projetado para cálculos precisos
centroid = zambezia.geometry.centroid.iloc[0]
longitude = centroid.x
projected_crs = get_utm_zone_for_mozambique(longitude)

print(f"   Convertendo para CRS projetado: {projected_crs}")
print(f"   Longitude central: {longitude:.2f}°")
geo_projected = geo.to_crs(projected_crs)
zambezia_projected = zambezia.to_crs(projected_crs)
print(f"   CRS projetado: {geo_projected.crs}")

# 2. Estatísticas detalhadas
if 'Legend' in geo.columns:
    value_counts = geo['Legend'].value_counts()
    print(f"\n2. Estatísticas por Legend:")
    print(f"   Total de valores únicos: {len(value_counts)}")
    
    # Calcular área total usando CRS projetado
    total_area_km2 = geo_projected.geometry.area.sum() / 1_000_000
    print(f"   Área total: {total_area_km2:.2f} km²")
    
    print(f"\n   Top 15 unidades:")
    for i, (legend, count) in enumerate(value_counts.head(15).items(), 1):
        # Calcular área por categoria usando CRS projetado
        subset_area = geo_projected[geo_projected['Legend'] == legend].geometry.area.sum() / 1_000_000
        print(f"   {i:2d}. {legend}: {count} unidades ({subset_area:.2f} km²)")

# 3. Criar mapa com cores únicas para cada camada
print(f"\n3. Criando mapa com cores únicas para cada camada...")

# Preparar cores distintas para cada valor único
unique_values = geo['Legend'].unique()
n_values = len(unique_values)

# Gerar paleta de cores distinta
if n_values <= 12:
    colors = plt.cm.Set3(np.linspace(0, 1, n_values))
elif n_values <= 24:
    colors = plt.cm.tab24(np.linspace(0, 1, n_values))
else:
    # Para muitas categorias, usar colormap qualitativo
    colors = plt.cm.rainbow(np.linspace(0, 1, n_values))

# Criar mapa
fig, ax = plt.subplots(1, 1, figsize=(16, 10))

# Plotar contorno da província
zambezia.boundary.plot(ax=ax, color='black', linewidth=2, alpha=0.8)

# Plotar cada camada geológica com sua cor única
for i, value in enumerate(unique_values):
    subset = geo[geo['Legend'] == value]
    subset_projected = geo_projected[geo_projected['Legend'] == value]
    color = colors[i]
    
    # Verificar se subset não está vazio
    if not subset.empty:
        # Plotar a camada (CRS original para visualização)
        subset.plot(ax=ax, color=color, alpha=0.9, linewidth=0.3)

# Configurar o mapa
ax.set_title(f'Geologia Completa: {province_name}\n({n_values} camadas geológicas)', 
            fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Longitude', fontsize=12)
ax.set_ylabel('Latitude', fontsize=12)
ax.grid(True, alpha=0.2)

# Criar legenda personalizada (limitar para não ficar muito grande)
legend_elements = []
for i, value in enumerate(unique_values):
    if i < 30:  # Limitar legenda para não ficar muito grande
        legend_elements.append(plt.Rectangle((0, 0), 1, 1, 
                                            fc=colors[i], label=str(value)))

if legend_elements:
    # Configurar legenda em múltiplas colunas
    n_cols = 3 if len(legend_elements) > 15 else 2
    ax.legend(handles=legend_elements, 
             bbox_to_anchor=(1.02, 1), loc='upper left',
             title='Unidades Geológicas', fontsize=8,
             ncol=n_cols,
             frameon=True)

# Ajustar layout para acomodar legenda
plt.subplots_adjust(right=0.85, left=0.05, top=0.95, bottom=0.05)

# Salvar mapa
output_file = f'geology_{province_name.lower().replace(" ", "_")}_teste2.png'
plt.savefig(output_file, dpi=200, pad_inches=0.5)
print(f"\n4. Mapa salvo: {output_file}")

# 5. Resumo final
print(f"\n=== RESUMO FINAL ===")
print(f"Província: {province_name}")
print(f"Total de camadas geológicas: {len(geo)}")
print(f"Valores únicos: {n_values}")
print(f"Camadas na legenda: {min(30, n_values)}")
print(f"Área total: {total_area_km2:.2f} km² (calculada com CRS projetado)")
print(f"CRS original: {geo.crs}")
print(f"CRS projetado: {geo_projected.crs}")

# Mostrar o plot
plt.show()

print(f"\n*** Mapa completo de geologia de {province_name} concluído! ***")
print(f"*** Todas as {n_values} camadas plotadas com cores únicas! ***")
