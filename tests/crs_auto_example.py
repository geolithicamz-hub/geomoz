#!/usr/bin/env python3
"""
Exemplo: GeoMoz com CRS automático - o usuário não precisa se preocupar com CRS!
"""

import sys
sys.path.insert(0, '.')

import geomoz

print("=== GeoMoz - CRS Automático (Backend) ===\n")

# 1. O usuário simplesmente solicita os dados - CRS é tratado automaticamente!
print("1. Obtendo geologia de Zambezia (CRS tratado automaticamente)...")
geo_zambezia = geomoz.geology_by_province(name_province="Zambézia")
print(f"   Unidades geológicas: {len(geo_zambezia)}")
print(f"   CRS (para visualização): {geo_zambezia.crs}")

# 2. Calcular área - a biblioteca converte automaticamente para CRS projetado
print("\n2. Calculando área precisa (conversão automática para UTM)...")
geo_with_area = geomoz.calculate_area(geo_zambezia, unit="km2")
total_area = geo_with_area['area_km2'].sum()
print(f"   Área total: {total_area:.2f} km²")
print("   (A biblioteca converteu automaticamente para UTM Zone 36S)")

# 3. Estatísticas por unidade geológica com áreas precisas
print("\n3. Estatísticas por unidade geológica:")
if 'Legend' in geo_with_area.columns:
    # Agrupar por Legend e somar áreas
    area_by_legend = geo_with_area.groupby('Legend')['area_km2'].sum().sort_values(ascending=False)
    
    print("   Top 10 unidades por área:")
    for i, (legend, area) in enumerate(area_by_legend.head(10).items(), 1):
        count = len(geo_with_area[geo_with_area['Legend'] == legend])
        print(f"   {i:2d}. {legend}: {area:.2f} km² ({count} polígonos)")

# 4. Comparar com diferentes províncias - CRS automático para cada uma
print("\n4. Comparando áreas de diferentes províncias:")
provinces = ["Zambézia", "Nampula", "Tete"]

for province in provinces:
    try:
        geo = geomoz.geology_by_province(name_province=province)
        geo_area = geomoz.calculate_area(geo, unit="km2")
        total = geo_area['area_km2'].sum()
        print(f"   {province}: {total:.2f} km²")
    except Exception as e:
        print(f"   {province}: Erro - {e}")

# 5. Exemplo com filtro específico
print("\n5. Geologia específica com área precisa:")
try:
    # Suite Malema em Zambezia
    geo_malema = geomoz.geology_by_province(name_province="Zambézia", SUITE="Malema")
    geo_malema_area = geomoz.calculate_area(geo_malema, unit="km2")
    malema_area = geo_malema_area['area_km2'].sum()
    print(f"   Suite Malema em Zambezia: {malema_area:.2f} km²")
    print(f"   Número de polígonos: {len(geo_malema)}")
except Exception as e:
    print(f"   Erro: {e}")

print(f"\n=== Vantagens do CRS Automático ===")
print("1. Usuário não precisa saber sobre CRS ou zonas UTM")
print("2. Cálculos de área são sempre precisos (usando UTM)")
print("3. Visualização permanece em CRS geográfico (WGS84)")
print("4. Funciona para qualquer província de Moçambique")
print("5. Sem avisos de CRS para o usuário")

print(f"\n*** CRS totalmente automático no backend! ***")
