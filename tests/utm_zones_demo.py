#!/usr/bin/env python3
"""
Demonstração: Zonas UTM Corrigidas para Moçambique
Moçambique está entre duas zonas UTM: 36S (30-36E) e 37S (36-42E)
"""

import sys
sys.path.insert(0, '.')

import geomoz
import matplotlib.pyplot as plt

print("=== GeoMoz - Zonas UTM Corrigidas para Moçambique ===")
print("Zona 36S: 30°E a 36°E (sul e centro)")
print("Zona 37S: 36°E a 42°E (norte)")
print("=" * 60)

# Mapeamento de províncias por zona
provinces_zone_36s = ['Maputo Província', 'Gaza', 'Inhambane', 'Manica', 'Tete', 'Sofala']
provinces_zone_37s = ['Zambézia', 'Nampula', 'Niassa', 'Cabo Delgado']

print("\n1. Províncias na Zona 36S (30-36E):")
total_area_36s = 0
for province in provinces_zone_36s:
    try:
        geo = geomoz.geology_by_province(name_province=province)
        geo_area = geomoz.calculate_area(geo, unit="km2")
        area = geo_area['area_km2'].sum()
        total_area_36s += area
        print(f"   {province:15s}: {area:8,.2f} km²")
    except Exception as e:
        print(f"   {province:15s}: Erro - {e}")

print(f"\n   Total Zona 36S: {total_area_36s:,.2f} km²")

print("\n2. Províncias na Zona 37S (36-42E):")
total_area_37s = 0
for province in provinces_zone_37s:
    try:
        geo = geomoz.geology_by_province(name_province=province)
        geo_area = geomoz.calculate_area(geo, unit="km2")
        area = geo_area['area_km2'].sum()
        total_area_37s += area
        print(f"   {province:15s}: {area:8,.2f} km²")
    except Exception as e:
        print(f"   {province:15s}: Erro - {e}")

print(f"\n   Total Zona 37s: {total_area_37s:,.2f} km²")

print(f"\n3. Resumo:")
print(f"   Área total Moçambique: {total_area_36s + total_area_37s:,.2f} km²")
print(f"   Zona 36S (sul/centro):  {total_area_36s:,.2f} km² ({(total_area_36s/(total_area_36s+total_area_37s)*100):.1f}%)")
print(f"   Zona 37S (norte):       {total_area_37s:,.2f} km² ({(total_area_37s/(total_area_36s+total_area_37s)*100):.1f}%)")

# Criar mapa visual das zonas
print("\n4. Criando mapa visual das zonas UTM...")

fig, ax = plt.subplots(1, 1, figsize=(12, 8))

# Plotar todas as províncias
colors = []
for province in provinces_zone_36s + provinces_zone_37s:
    try:
        prov = geomoz.read_province(name_province=province)
        color = 'lightblue' if province in provinces_zone_36s else 'lightcoral'
        prov.plot(ax=ax, color=color, alpha=0.7, edgecolor='black', linewidth=1)
    except:
        pass

# Adicionar legenda manual
import matplotlib.patches as mpatches
patch_36s = mpatches.Patch(color='lightblue', label='Zona 36S (30-36E)')
patch_37s = mpatches.Patch(color='lightcoral', label='Zona 37S (36-42E)')
ax.legend(handles=[patch_36s, patch_37s], loc='upper right')

ax.set_title('Moçambique: Distribuição das Zonas UTM\n36S (sul/centro) | 37S (norte)',
            fontsize=14, fontweight='bold')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('mozambique_utm_zones.png', dpi=200)
print("   Mapa salvo: mozambique_utm_zones.png")

plt.show()

print("\n=== Conclusão ===")
print("As zonas UTM para Moçambique foram corrigidas:")
print("Zona 36S (EPSG:32736): Províncias do sul e centro (30-36°E)")
print("Zona 37S (EPSG:32737): Províncias do norte (36-42°E)")
print("\nA biblioteca GeoMoz detecta automaticamente a zona correta!")
print("*** Cálculos precisos para todo Moçambique! ***")
