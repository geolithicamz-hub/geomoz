#!/usr/bin/env python3
"""
Exemplo final: GeoMoz simples - usuário não precisa se preocupar com CRS!
"""

import sys
sys.path.insert(0, '.')

import geomoz
import matplotlib.pyplot as plt

print("=== GeoMoz - Simples e Automático ===\n")

# 1. Carregar geologia - CRS automático!
print("1. Carregando geologia de Zambezia...")
geo = geomoz.geology_by_province(name_province="Zambézia")
zambezia = geomoz.read_province(name_province="Zambézia")

print(f"   Unidades geológicas: {len(geo)}")
print(f"   CRS: {geo.crs} (WGS84 para visualização)")

# 2. Calcular área - automático e preciso!
print("\n2. Calculando área (conversão automática para UTM)...")
geo_com_area = geomoz.calculate_area(geo, unit="km2")
area_total = geo_com_area['area_km2'].sum()
print(f"   Área total: {area_total:,.2f} km²")

# 3. Estatísticas simples
print("\n3. Top 10 unidades geológicas:")
if 'Legend' in geo_com_area.columns:
    stats = geo_com_area.groupby('Legend').agg({
        'area_km2': 'sum',
        'Legend': 'count'
    }).rename(columns={'Legend': 'poligonos'})
    stats = stats.sort_values('area_km2', ascending=False).head(10)
    
    for i, (legend, row) in enumerate(stats.iterrows(), 1):
        print(f"   {i:2d}. {legend[:40]}...: {row['area_km2']:,.2f} km² ({row['poligonos']} polígonos)")

# 4. Criar mapa simples
print("\n4. Criando mapa visual...")

fig, ax = plt.subplots(1, 1, figsize=(14, 10))

# Contorno da província
zambezia.boundary.plot(ax=ax, color='black', linewidth=2, alpha=0.8)

# Geologia com cores (limitar para melhor visualização)
top_legends = geo['Legend'].value_counts().head(15).index
geo_top = geo[geo['Legend'].isin(top_legends)]

geo_top.plot(
    ax=ax, 
    column='Legend', 
    cmap='tab20', 
    alpha=0.8, 
    linewidth=0.5,
    legend=True,
    legend_kwds={
        'bbox_to_anchor': (1.02, 1), 
        'loc': 'upper left',
        'title': 'Unidades Geológicas',
        'fontsize': 9,
        'ncol': 2
    }
)

ax.set_title(f'Geologia de Zambezia\n({len(geo_top)} unidades principais)', 
            fontsize=14, fontweight='bold')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.grid(True, alpha=0.3)

plt.subplots_adjust(right=0.85)
plt.savefig('geology_zambezia_simples.png', dpi=200)
print("   Mapa salvo: geology_zambezia_simples.png")

plt.show()

# 5. Resumo final
print(f"\n=== RESUMO ===")
print(f"Província: Zambezia")
print(f"Total de unidades: {len(geo)}")
print(f"Unidades no mapa: {len(geo_top)}")
print(f"Área total: {area_total:,.2f} km²")
print(f"CRS visualização: {geo.crs}")
print(f"CRS cálculos: Automático (UTM)")

print(f"\n*** GeoMoz: CRS totalmente transparente para o usuário! ***")
print(f"*** Cálculos precisos sem complicação! ***")
