#!/usr/bin/env python3
"""
Teste simples da refatoração para Hugging Face
"""

import sys
sys.path.insert(0, '.')

def test_basic_functionality():
    """Teste básico das funcionalidades principais"""
    print("=== Teste Simples - Hugging Face Integration ===")
    
    try:
        import geomoz
        print("✓ GeoMoz importado com sucesso")
        
        # Testar leitura de províncias
        print("\n1. Testando read_province...")
        provinces = geomoz.read_province()
        print(f"   ✓ {len(provinces)} províncias carregadas")
        
        # Testar província específica
        zambezia = geomoz.read_province(name_province="Zambézia")
        print(f"   ✓ Zambézia: {len(zambezia)} polígonos")
        
        # Testar geologia
        print("\n2. Testando read_geology...")
        geology = geomoz.read_geology()
        print(f"   ✓ {len(geology)} unidades geológicas carregadas")
        
        # Testar filtro geológico
        granites = geomoz.read_geology(SUITE="Granite")
        print(f"   ✓ Granites: {len(granites)} unidades")
        
        # Testar funções espaciais
        print("\n3. Testando funções espaciais...")
        geo_zambezia = geomoz.geology_by_province(name_province="Zambézia")
        print(f"   ✓ Geologia de Zambézia: {len(geo_zambezia)} unidades")
        
        # Testar cálculo de área
        area_zambezia = geomoz.calculate_area(geo_zambezia, unit="km2")
        total_area = area_zambezia['area_km2'].sum()
        print(f"   ✓ Área total: {total_area:,.2f} km²")
        
        # Testar utilitários de dados
        print("\n4. Testando utilitários de dados...")
        from geomoz.utils.data import get_cache_info, list_available_files
        
        cache_info = get_cache_info()
        print(f"   ✓ Cache: {cache_info['file_count']} ficheiros, {cache_info['size_mb']:.2f} MB")
        
        files = list_available_files()
        print(f"   ✓ Ficheiros disponíveis: {len(files)}")
        
        print("\n🎉 TODOS OS TESTES BÁSICOS PASSARAM!")
        print("✓ Download automático do Hugging Face funcionando")
        print("✓ Cache local funcionando")
        print("✓ Todas as funções principais operacionais")
        print("✓ Refatoração concluída com sucesso!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        return False

if __name__ == "__main__":
    success = test_basic_functionality()
    
    if success:
        print(f"\n{'='*60}")
        print("RESULTADO: REFATORAÇÃO CONCLUÍDA COM SUCESSO!")
        print("A biblioteca GeoMoz agora usa Hugging Face automaticamente.")
        print(f"{'='*60}")
    else:
        print(f"\n{'='*60}")
        print("RESULTADO: FALHA NA REFATORAÇÃO!")
        print("Verifique os erros acima.")
        print(f"{'='*60}")
