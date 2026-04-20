#!/usr/bin/env python3
"""
Demonstração do Sistema de Cache
Mostra como usar cache para otimizar carregamento
"""

import time
import geomoz
from geomoz.utils.cache import CachedGeoMoz, cache_info, print_cache


def demo_cache():
    """Demonstrar vantagens do cache"""
    
    print("🚀 DEMONSTRAÇÃO: Sistema de Cache GeoMoz")
    print("=" * 70)
    
    # Teste SEM cache
    print("\n📊 TESTE 1: Sem Cache")
    print("-" * 40)
    t1 = time.time()
    v1 = geomoz.read_village()
    t1_elapsed = time.time() - t1
    print(f"✅ {len(v1):,} aldeias em {t1_elapsed:.2f}s")
    
    # Teste COM cache (primeira vez)
    print("\n📊 TESTE 2: Com Cache (1ª vez - cria cache)")
    print("-" * 40)
    t2 = time.time()
    v2 = CachedGeoMoz.read_village()
    t2_elapsed = time.time() - t2
    print(f"✅ {len(v2):,} aldeias em {t2_elapsed:.2f}s")
    
    # Teste COM cache (segunda vez)
    print("\n📊 TESTE 3: Com Cache (2ª vez - usa cache)")
    print("-" * 40)
    t3 = time.time()
    v3 = CachedGeoMoz.read_village()
    t3_elapsed = time.time() - t3
    print(f"✅ {len(v3):,} aldeias em {t3_elapsed:.2f}s ⚡")
    
    # Resumo
    print("\n" + "=" * 70)
    print("📈 RESUMO DE PERFORMANCE")
    print("=" * 70)
    print(f"Sem cache:    {t1_elapsed:.2f}s")
    print(f"Com cache 1ª: {t2_elapsed:.2f}s")
    print(f"Com cache 2ª: {t3_elapsed:.2f}s ⚡ {t1_elapsed/t3_elapsed:.1f}x mais rápido!")
    
    # Info do cache
    print("\n📦 Informações do Cache:")
    print_cache()


if __name__ == "__main__":
    demo_cache()
