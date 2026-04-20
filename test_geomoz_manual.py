#!/usr/bin/env python3
"""
Script de teste manual para a biblioteca GeoMoz
"""

import sys
sys.path.insert(0, '.')

import geomoz

def test_all_functions():
    """Testa todas as funções da biblioteca"""
    
    print("=== Testando GeoMoz ===\n")
    
    # Test 1: list_geometries
    print("1. Testando list_geometries():")
    geometries = geomoz.list_geometries()
    for key, value in geometries.items():
        print(f"   {key}: {value['description']}")
    print()
    
    # Test 2: read_province (todas)
    print("2. Testando read_province() - todas as províncias:")
    provinces = geomoz.read_province()
    print(f"   Total de províncias: {len(provinces)}")
    print(f"   Colunas: {list(provinces.columns)}")
    print(f"   CRS: {provinces.crs}")
    print(f"   Geometrias válidas: {provinces.is_valid.all()}")
    print()
    
    # Test 3: list_provinces
    print("3. Testando list_provinces():")
    province_list = geomoz.list_provinces()
    print(province_list.to_string(index=False))
    print()
    
    # Test 4: read_province (código específico)
    print("4. Testando read_province() - províncias específicas:")
    test_codes = ["01", "03", "11"]
    for code in test_codes:
        province = geomoz.read_province(code=code)
        name = province.iloc[0]["Provincia"]
        print(f"   Código {code}: {name}")
    print()
    
    # Test 5: Teste de erro
    print("5. Testando tratamento de erros:")
    try:
        invalid = geomoz.read_province(code="99")
        print("   ERRO: Deveria falhar!")
    except Exception as e:
        print(f"   OK: Erro esperado - {type(e).__name__}")
    print()
    
    # Test 6: Estatísticas básicas
    print("6. Estatísticas básicas:")
    print(f"   Área total (aproximada): {provinces.geometry.area.sum():.2f} graus²")
    print(f"   Bounding box: {provinces.total_bounds}")
    print()
    
    print("=== Todos os testes concluídos com sucesso! ===")

if __name__ == "__main__":
    test_all_functions()
