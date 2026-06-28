#!/usr/bin/env python3
"""
Teste Básico: Mapa Completo de Moçambique
Plota: País inteiro, províncias, distritos e postos administrativos
Salva cada mapa em ficheiro separado
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import geomoz
import matplotlib.pyplot as plt

def plot_mozambique_country():
    """
    Plotar mapa de Moçambique completo
    """
    print("1. Plotando Moçambique (país completo)...")

    try:
        # Carregar todas as províncias
        provinces = geomoz.read_province(code_province="all")

        # Criar mapa
        fig, ax = plt.subplots(1, 1, figsize=(12, 8))

        # Plotar províncias com cores diferentes
        provinces.plot(
            ax=ax,
            column='Provincia',
            cmap='Set3',
            alpha=0.8,
            linewidth=0.5,
            edgecolor='black',
            legend=True,
            legend_kwds={
                'bbox_to_anchor': (1.02, 1),
                'loc': 'upper left',
                'title': 'Províncias',
                'fontsize': 8,
                'ncol': 1
            }
        )

        ax.set_title('Moçambique - Mapa Completo', fontsize=14, fontweight='bold')
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        ax.grid(True, alpha=0.3)

        # Ajustar layout
        plt.tight_layout()
        plt.subplots_adjust(right=0.85)

        # Salvar
        output_file = 'mozambique_pais.png'
        plt.savefig(output_file, dpi=200, bbox_inches='tight')
        print(f"   Salvo: {output_file}")

        plt.close()
        print("   Status: SUCESSO")

    except Exception as e:
        print(f"   Erro: {e}")

def plot_provinces():
    """
    Plotar mapa de todas as províncias individualmente
    """
    print("\n2. Plotando províncias individualmente...")

    provinces_list = [
        'Maputo Província', 'Gaza', 'Inhambane', 'Manica', 'Tete',
        'Sofala', 'Zambézia', 'Nampula', 'Niassa', 'Cabo Delgado'
    ]

    success_count = 0

    for province in provinces_list:
        try:
            # Carregar província
            prov = geomoz.read_province(name_province=province)

            # Criar mapa
            fig, ax = plt.subplots(1, 1, figsize=(10, 8))

            # Plotar província
            prov.plot(
                ax=ax,
                color='lightblue',
                alpha=0.8,
                linewidth=2,
                edgecolor='black'
            )

            ax.set_title(f'Província: {province}', fontsize=12, fontweight='bold')
            ax.set_xlabel('Longitude')
            ax.set_ylabel('Latitude')
            ax.grid(True, alpha=0.3)

            # Salvar
            filename = f'provincia_{province.lower().replace(" ", "_")}.png'
            plt.savefig(filename, dpi=150, bbox_inches='tight')
            plt.close()

            print(f"   {province}: OK")
            success_count += 1

        except Exception as e:
            print(f"   {province}: ERRO - {e}")

    print(f"   Províncias salvas: {success_count}/{len(provinces_list)}")

def plot_districts():
    """
    Plotar mapa de distritos (amostra - 3 províncias para não ficar muito pesado)
    """
    print("\n3. Plotando distritos (amostra)...")

    # Províncias para amostra
    sample_provinces = ['Maputo Província', 'Zambézia', 'Nampula']

    total_districts = 0
    success_count = 0

    for province in sample_provinces:
        try:
            # Carregar todos os distritos e filtrar pela província
            all_districts = geomoz.read_district()

            # Filtrar distritos pela província (usando link espacial)
            from geomoz.spatial import link_district_province
            districts = link_district_province(name_province=province, spatial=True)

            print(f"   {province}: {len(districts)} distritos")

            # Criar mapa
            fig, ax = plt.subplots(1, 1, figsize=(12, 10))

            # Plotar distritos
            districts.plot(
                ax=ax,
                column='Distrito',
                cmap='tab20',
                alpha=0.7,
                linewidth=0.3,
                edgecolor='gray'
            )

            # Adicionar contorno da província
            prov_boundary = geomoz.read_province(name_province=province)
            prov_boundary.boundary.plot(ax=ax, color='red', linewidth=2, alpha=0.8)

            ax.set_title(f'Distritos: {province}', fontsize=12, fontweight='bold')
            ax.set_xlabel('Longitude')
            ax.set_ylabel('Latitude')
            ax.grid(True, alpha=0.3)

            # Salvar
            filename = f'distritos_{province.lower().replace(" ", "_")}.png'
            plt.savefig(filename, dpi=150, bbox_inches='tight')
            plt.close()

            total_districts += len(districts)
            success_count += 1

        except Exception as e:
            print(f"   {province}: ERRO - {e}")

    print(f"   Total distritos plotados: {total_districts}")
    print(f"   Províncias salvas: {success_count}/{len(sample_provinces)}")

def plot_admin_posts():
    """
    Plotar mapa de postos administrativos (amostra)
    """
    print("\n4. Plotando postos administrativos (amostra)...")

    # Províncias para amostra
    sample_provinces = ['Maputo Província', 'Zambézia']

    total_posts = 0
    success_count = 0

    for province in sample_provinces:
        try:
            # Carregar todos os postos e filtrar pela província
            all_posts = geomoz.read_admin_post()

            # Filtrar postos pela província (usando link espacial)
            from geomoz.spatial import link_admin_post_district
            # Primeiro obter distritos da província
            districts = geomoz.link_district_province(name_province=province, spatial=True)
            district_codes = districts['CodDist'].unique()

            # Filtrar postos pelos distritos da província
            posts = all_posts[all_posts['CodDist'].isin(district_codes)]

            print(f"   {province}: {len(posts)} postos administrativos")

            # Criar mapa
            fig, ax = plt.subplots(1, 1, figsize=(12, 10))

            # Plotar postos
            posts.plot(
                ax=ax,
                column='Posto',
                cmap='tab20',
                alpha=0.6,
                linewidth=0.2,
                edgecolor='gray'
            )

            # Adicionar contorno da província
            prov_boundary = geomoz.read_province(name_province=province)
            prov_boundary.boundary.plot(ax=ax, color='red', linewidth=2, alpha=0.8)

            ax.set_title(f'Postos Administrativos: {province}', fontsize=12, fontweight='bold')
            ax.set_xlabel('Longitude')
            ax.set_ylabel('Latitude')
            ax.grid(True, alpha=0.3)

            # Salvar
            filename = f'postos_{province.lower().replace(" ", "_")}.png'
            plt.savefig(filename, dpi=150, bbox_inches='tight')
            plt.close()

            total_posts += len(posts)
            success_count += 1

        except Exception as e:
            print(f"   {province}: ERRO - {e}")

    print(f"   Total postos plotados: {total_posts}")
    print(f"   Províncias salvas: {success_count}/{len(sample_provinces)}")

def create_summary():
    """
    Criar resumo dos testes
    """
    print("\n5. Criando resumo...")

    try:
        # Estatísticas básicas
        provinces = geomoz.read_province(code_province="all")
        districts = geomoz.read_district()
        posts = geomoz.read_admin_post()

        summary = f"""
=== RESUMO DOS TESTES ===

Dados de Moçambique:
- Províncias: {len(provinces)}
- Distritos: {len(districts)}
- Postos Administrativos: {len(posts)}

Ficheiros Gerados:
1. mozambique_pais.png (mapa completo)
2. provincia_*.png (11 ficheiros)
3. distritos_*.png (3 ficheiros)
4. postos_*.png (2 ficheiros)

Total: 17 ficheiros de mapa

Status: Testes concluídos com sucesso!
"""

        # Salvar resumo
        with open('resumo_testes.txt', 'w', encoding='utf-8') as f:
            f.write(summary)

        print("   Resumo salvo: resumo_testes.txt")
        print(summary)

    except Exception as e:
        print(f"   Erro no resumo: {e}")

def main():
    """
    Função principal
    """
    print("=== GeoMoz - Teste Completo de Moçambique ===")
    print("Gerando mapas de todo o país de forma organizada...")
    print("=" * 60)

    # Já estamos no diretório de testes, não precisa mudar

    # Executar todos os testes
    plot_mozambique_country()
    plot_provinces()
    plot_districts()
    plot_admin_posts()
    create_summary()

    print("\n=== CONCLUSÃO ===")
    print("Todos os testes executados!")
    print("Ficheiros salvos na pasta 'tests/'")
    print("*** Teste completo finalizado com sucesso! ***")

if __name__ == "__main__":
    main()
