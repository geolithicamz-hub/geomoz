#!/usr/bin/env python3
"""
Demonstração Final: GeoMoz Simples e Robusto
O usuário não precisa saber nada sobre zonas UTM ou cruzamento de limites!
"""

import sys
sys.path.insert(0, '.')

import geomoz

def demo_final_simples():
    """
    Demonstração final mostrando que o usuário não precisa se preocupar com CRS
    """
    print("=== GeoMoz: Simples e Automático ===")
    print("O usuário não precisa saber sobre zonas UTM ou cruzamento de limites!")
    print("=" * 65)

    # Lista de províncias para teste (incluindo as que cruzam zonas)
    provinces = ['Sofala', 'Zambézia', 'Niassa', 'Inhambane', 'Nampula']

    print(f"\n1. CÁLCULO DE ÁREAS (tudo automático):")
    print("Província    | Área (km²)  | Complexidade | Status")
    print("-" * 50)

    for province in provinces:
        try:
            # Simples: o usuário só pede os dados!
            geo = geomoz.geology_by_province(name_province=province)

            # Simples: calcula área automaticamente!
            geo_area = geomoz.calculate_area(geo, unit="km2")
            total_area = geo_area['area_km2'].sum()

            # Verificar complexidade interna (usuário não vê)
            from geomoz.spatial import _check_cross_zone_boundary
            zone_info = _check_cross_zone_boundary(geo)

            if zone_info['crosses_boundary']:
                complexity = "Cruza 2 zonas"
                status = "Tratado"
            else:
                complexity = "1 zona só"
                status = "Normal"

            print(f"{province:11s} | {total_area:10,.2f} | {complexity:11s} | {status}")

        except Exception as e:
            print(f"{province:11s} | ERRO: {e}")

    # Exemplo com filtros
    print(f"\n2. FILTROS ESPECÍFICOS (tudo automático):")

    try:
        # Suite específica em província que cruza zonas
        geo_mocuba = geomoz.geology_by_province(name_province="Zambézia", SUITE="Mocuba")
        area_mocuba = geomoz.calculate_area(geo_mocuba, unit="km2")
        total_mocuba = area_mocuba['area_km2'].sum()

        print(f"   Suite Mocuba em Zambézia: {total_mocuba:,.2f} km²")
        print(f"   (Zambézia cruza 2 zonas UTM, mas o tratamento é automático)")

    except Exception as e:
        print(f"   Erro no filtro: {e}")

    # Comparação entre províncias
    print(f"\n3. COMPARAÇÃO ENTRE PROVÍNCIAS:")

    try:
        # Província que cruza zonas vs província normal
        geo_sofala = geomoz.geology_by_province(name_province="Sofala")
        geo_inhambane = geomoz.geology_by_province(name_province="Inhambane")

        area_sofala = geomoz.calculate_area(geo_sofala, unit="km2")
        area_inhambane = geomoz.calculate_area(geo_inhambane, unit="km2")

        total_sofala = area_sofala['area_km2'].sum()
        total_inhambane = area_inhambane['area_km2'].sum()

        print(f"   Sofala (cruza zonas):     {total_sofala:10,.2f} km²")
        print(f"   Inhambane (zona única):    {total_inhambane:10,.2f} km²")
        print(f"   Diferença:                 {abs(total_sofala - total_inhambane):10,.2f} km²")

    except Exception as e:
        print(f"   Erro na comparação: {e}")

    # Estatísticas geológicas
    print(f"\n4. ESTATÍSTICAS GEOLÓGICAS (automáticas):")

    try:
        # Província complexa (cruza zonas)
        geo_zambezia = geomoz.geology_by_province(name_province="Zambézia")
        geo_area_zambezia = geomoz.calculate_area(geo_zambezia, unit="km2")

        # Top 5 unidades por área
        if 'Legend' in geo_area_zambezia.columns:
            stats = geo_area_zambezia.groupby('Legend')['area_km2'].sum().sort_values(ascending=False).head(5)

            print("   Top 5 unidades geológicas em Zambézia:")
            for i, (legend, area) in enumerate(stats.items(), 1):
                legend_short = legend[:40] + "..." if len(legend) > 40 else legend
                print(f"   {i}. {legend_short:40s}: {area:8,.2f} km²")

    except Exception as e:
        print(f"   Erro nas estatísticas: {e}")

    # Resumo final
    print(f"\n=== RESUMO PARA O USUÁRIO ===")
    print("O GeoMoz resolve automaticamente:")
    print("1. Detecção de zonas UTM (36S ou 37S)")
    print("2. Tratamento de áreas que cruzam o limite 36°E")
    print("3. Conversão para CRS projetado para cálculos precisos")
    print("4. Manutenção de CRS original para visualização")
    print("5. Cálculos de área sempre corretos")

    print(f"\nO usuário só precisa:")
    print("1. Pedir os dados: geomoz.geology_by_province()")
    print("2. Calcular área: geomoz.calculate_area()")
    print("3. Usar os resultados!")

    print(f"\n*** GeoMoz: Simples, robusto e automático! ***")
    print("*** Complexidade técnica totalmente transparente! ***")

if __name__ == "__main__":
    demo_final_simples()
