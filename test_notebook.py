#!/usr/bin/env python3
"""
Exemplo de uso da GeoMoz como se fosse um notebook
"""

import sys
sys.path.insert(0, '.')

import geomoz
import geopandas as gpd

# Cell 1: Import e lista de dados
print("=== Cell 1: Import e dados disponíveis ===")
print("import geomoz")
print()
geometries = geomoz.list_geometries()
print("Dados disponíveis:")
for key, info in geometries.items():
    print(f"- {key}: {info['description']} ({info['year']})")

# Cell 2: Carregar dados
print("\n=== Cell 2: Carregar dados ===")
print("provinces = geomoz.read_province()")
provinces = geomoz.read_province()
print(f"Shape: {provinces.shape}")
print(f"Columns: {list(provinces.columns)}")
print(f"CRS: {provinces.crs}")

# Cell 3: Explorar dados
print("\n=== Cell 3: Explorar dados ===")
print("provinces.head()")
print(provinces.head())

print("\nprovinces['Provincia'].tolist()")
print(provinces['Provincia'].tolist())

# Cell 4: Filtrar dados
print("\n=== Cell 4: Filtrar dados ===")
print("nampula = geomoz.read_province(code='03')")
nampula = geomoz.read_province(code='03')
print(f"Província: {nampula.iloc[0]['Provincia']}")
print(f"Código: {nampula.iloc[0]['CodProv']}")

# Cell 5: Operações espaciais básicas
print("\n=== Cell 5: Operações espaciais ===")
print("Centróides:")
centroids = provinces.geometry.centroid
for i, row in provinces.iterrows():
    print(f"{row['Provincia']}: ({centroids.iloc[i].x:.2f}, {centroids.iloc[i].y:.2f})")

print("\n=== Teste concluído ===")
