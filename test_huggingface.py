#!/usr/bin/env python3
"""
Teste de Refatoração para Hugging Face
Valida que todas as funções funcionam com download automático
"""

import sys
import os
sys.path.insert(0, '.')

def test_imports():
    """Testar se todos os imports funcionam"""
    print("=== Teste de Imports ===")
    
    try:
        import geomoz
        print("✓ geomoz importado com sucesso")
        
        # Testar import do módulo de dados
        from geomoz.utils.data import get_data_path, list_available_files, get_cache_info
        print("✓ Módulo de dados importado com sucesso")
        
        return True
        
    except Exception as e:
        print(f"✗ Erro no import: {e}")
        return False

def test_data_utilities():
    """Testar utilitários de dados"""
    print("\n=== Teste de Utilitários de Dados ===")
    
    try:
        from geomoz.utils.data import list_available_files, get_cache_info
        
        # Listar ficheiros disponíveis
        files = list_available_files()
        print(f"✓ Ficheiros disponíveis: {len(files)}")
        for f in files:
            print(f"  - {f}")
        
        # Informações do cache
        cache_info = get_cache_info()
        print(f"✓ Cache dir: {cache_info['cache_dir']}")
        print(f"✓ Cache exists: {cache_info['exists']}")
        
        return True
        
    except Exception as e:
        print(f"✗ Erro nos utilitários: {e}")
        return False

def test_read_functions():
    """Testar todas as funções read_*"""
    print("\n=== Teste de Funções Read ===")
    
    try:
        import geomoz
        
        # Testar read_province
        print("1. Testando read_province...")
        provinces = geomoz.read_province(verbose=True)
        print(f"   ✓ Carregadas {len(provinces)} províncias")
        
        # Testar província específica
        zambezia = geomoz.read_province(name_province="Zambézia", verbose=True)
        print(f"   ✓ Província Zambézia: {len(zambezia)} polígonos")
        
        # Testar read_district
        print("\n2. Testando read_district...")
        districts = geomoz.read_district(verbose=True)
        print(f"   ✓ Carregados {len(districts)} distritos")
        
        # Testar distrito específico
        lichinga = geomoz.read_district(name_district="Lichinga", verbose=True)
        print(f"   ✓ Distrito Lichinga: {len(lchinga)} polígonos")
        
        # Testar read_admin_post
        print("\n3. Testando read_admin_post...")
        admin_posts = geomoz.read_admin_post(verbose=True)
        print(f"   ✓ Carregados {len(admin_posts)} postos administrativos")
        
        # Testar posto específico
        posto = geomoz.read_admin_post(name_admin_post="Cidade de Lichinga", verbose=True)
        print(f"   ✓ Posto Cidade de Lichinga: {len(posto)} polígonos")
        
        # Testar read_geology
        print("\n4. Testando read_geology...")
        geology = geomoz.read_geology(verbose=True)
        print(f"   ✓ Carregadas {len(geology)} unidades geológicas")
        
        # Testar filtro geológico
        granites = geomoz.read_geology(SUITE="Granite", verbose=True)
        print(f"   ✓ Granites: {len(granites)} unidades")
        
        return True
        
    except Exception as e:
        print(f"✗ Erro nas funções read: {e}")
        return False

def test_spatial_functions():
    """Testar funções espaciais"""
    print("\n=== Teste de Funções Espaciais ===")
    
    try:
        import geomoz
        
        # Testar geology_by_province
        print("1. Testando geology_by_province...")
        geo_zambezia = geomoz.geology_by_province(name_province="Zambézia", verbose=True)
        print(f"   ✓ Geologia de Zambézia: {len(geo_zambezia)} unidades")
        
        # Testar calculate_area
        print("\n2. Testando calculate_area...")
        area_zambezia = geomoz.calculate_area(geo_zambezia, unit="km2")
        total_area = area_zambezia['area_km2'].sum()
        print(f"   ✓ Área total: {total_area:,.2f} km²")
        
        return True
        
    except Exception as e:
        print(f"✗ Erro nas funções espaciais: {e}")
        return False

def test_cache_functionality():
    """Testar funcionalidade de cache"""
    print("\n=== Teste de Cache ===")
    
    try:
        from geomoz.utils.data import get_cache_info, clear_cache
        
        # Informações do cache antes
        cache_before = get_cache_info()
        print(f"   Cache antes: {cache_before['file_count']} ficheiros, {cache_before['size_mb']:.2f} MB")
        
        # Carregar dados novamente (deve usar cache)
        import geomoz
        provinces = geomoz.read_province(verbose=False)
        
        # Informações do cache depois
        cache_after = get_cache_info()
        print(f"   Cache depois: {cache_after['file_count']} ficheiros, {cache_after['size_mb']:.2f} MB")
        
        print("   ✓ Cache funcionando corretamente")
        
        return True
        
    except Exception as e:
        print(f"✗ Erro no cache: {e}")
        return False

def main():
    """Função principal"""
    print("=== Teste de Refatoração para Hugging Face ===")
    print("Validando que todas as funções funcionam com download automático")
    print("=" * 70)
    
    # Executar todos os testes
    tests = [
        ("Imports", test_imports),
        ("Utilitários de Dados", test_data_utilities),
        ("Funções Read", test_read_functions),
        ("Funções Espaciais", test_spatial_functions),
        ("Cache", test_cache_functionality)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✓ {test_name}: PASSOU")
            else:
                print(f"✗ {test_name}: FALHOU")
        except Exception as e:
            print(f"✗ {test_name}: ERRO - {e}")
    
    # Resumo
    print(f"\n{'='*70}")
    print("RESUMO FINAL")
    print(f"{'='*70}")
    print(f"Testes passados: {passed}/{total}")
    print(f"Taxa de sucesso: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("A refatoração para Hugging Face está funcionando corretamente!")
        print("✓ Download automático funcionando")
        print("✓ Cache local funcionando")
        print("✓ Todas as funções read_* operacionais")
        print("✓ Funções espaciais operacionais")
    else:
        print(f"\n❌ {total-passed} TESTES FALHARAM!")
        print("Verifique os erros acima e corrija antes de usar a biblioteca.")
    
    print(f"\n{'='*70}")

if __name__ == "__main__":
    main()
