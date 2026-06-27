#!/usr/bin/env python3
"""
Exemplo completo de uso da biblioteca GeoMoz
Seguindo a arquitetura da geobr para dados de Moçambique
"""

import sys
sys.path.insert(0, '.')

import geomoz

def main():
    """Exemplo completo de uso da GeoMoz"""
    
    print("=== GeoMoz - Exemplo Completo ===\n")
    
    # 1. Listar todos os datasets disponíveis
    print("1. Datasets disponíveis:")
    geomoz.list_geomoz()
    
    # 2. Listar geografias e anos disponíveis
    print(f"\n2. Geografias disponíveis: {geomoz.list_available_geographies()}")
    print(f"   Anos disponíveis: {geomoz.list_available_years()}")
    
    # 3. Carregar províncias
    print("\n3. Carregando províncias:")
    provinces = geomoz.read_province(verbose=True)
    print(f"   Total: {len(provinces)} províncias")
    print(f"   Colunas: {list(provinces.columns)}")
    print(f"   CRS: {provinces.crs}")
    
    # 4. Carregar província específica
    print("\n4. Província específica (Nampula):")
    nampula = geomoz.read_province(code_province=3, verbose=True)
    print(f"   Nome: {nampula.iloc[0]['Provincia']}")
    print(f"   Código: {nampula.iloc[0]['CodProv']}")
    
    # 5. Carregar distritos
    print("\n5. Carregando distritos:")
    districts = geomoz.read_district(verbose=True)
    print(f"   Total: {len(districts)} distritos")
    
    # 6. Distrito específico
    print("\n6. Distrito específico:")
    district = geomoz.read_district(code_district='01', verbose=True)
    print(f"   Nome: {district.iloc[0]['Distrito']}")
    print(f"   Província: {district.iloc[0]['Provincia']}")
    
    # 7. Posts administrativos
    print("\n7. Posts administrativos:")
    admin_posts = geomoz.read_admin_post(verbose=True)
    print(f"   Total: {len(admin_posts)} posts")
    
    # 8. Aldeias
    print("\n8. Aldeias:")
    villages = geomoz.read_village(verbose=True)
    print(f"   Total: {len(villages)} aldeias")
    print(f"   Colunas: {list(villages.columns)}")
    
    # 9. Geologia
    print("\n9. Geologia:")
    geology = geomoz.read_geology(verbose=True)
    print(f"   Total: {len(geology)} unidades geológicas")
    
    # 10. Unidade geológica específica
    print("\n10. Unidade geológica específica:")
    geo_unit = geomoz.read_geology(code_geology='P2Cd', verbose=True)
    print(f"    Código: {geo_unit.iloc[0]['code2006']}")
    print(f"    Nome: {geo_unit.iloc[0]['Legenda']}")
    
    # 11. Informações do dataset
    print("\n11. Informações do dataset:")
    info = geomoz.get_dataset_info('province', 2017)
    print(f"    Function: {info.iloc[0]['function']}")
    print(f"    Source: {info.iloc[0]['source']}")
    print(f"    File: {info.iloc[0]['filename']}")

    print("\n=== Exemplo concluído com sucesso! ===")

if __name__ == "__main__":
    main()
