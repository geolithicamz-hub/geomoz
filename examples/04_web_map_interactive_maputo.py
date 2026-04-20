#!/usr/bin/env python3
"""
Mapa Web Interativo - Maputo
Visualização web com folium para exploração interativa da geologia
"""

import folium
from folium import plugins
import geopandas as gpd
import geomoz
import pandas as pd
from branca.colormap import linear


def create_interactive_web_map():

    print("🌐 Criando mapa web interativo para Maputo...")

    # -------------------------
    # DADOS - MAPUTO
    # -------------------------
    geology = geomoz.read_geology()
    province = geomoz.read_province(name_province="Maputo Província")

    # Converter CRS
    geology = geology.to_crs(epsg=4326)
    province = province.to_crs(epsg=4326)

    # Interseção com província de Maputo
    geology = gpd.overlay(geology, province, how='intersection')

    print(f"📊 {len(geology)} unidades geológicas em Maputo")

    # -------------------------
    # PREPARAR DADOS
    # -------------------------
    # Limpar code2006
    geology['code2006'] = geology['code2006'].fillna('Unknown').astype(str).str.strip()
    geology['Legend'] = geology['Legend'].fillna('Unknown').astype(str).str.strip()
    geology['ERA'] = geology['ERA'].fillna('Unknown').astype(str).str.strip()

    # Criar popup text
    geology['popup_text'] = geology.apply(
        lambda row: f"""
        <b>Litologia:</b> {row['Legend']}<br>
        <b>Código:</b> {row['code2006']}<br>
        <b>Era:</b> {row['ERA']}<br>
        <b>Área:</b> {row.geometry.area:.2f} km²
        """,
        axis=1
    )

    # -------------------------
    # CORES POR ERA
    # -------------------------
    era_colors = {
        'Archean': '#6b3d2e',
        'Proterozoic': '#a0522d',
        'Paleozoic': '#4f81bd',
        'Mesozoic': '#f1c232',
        'Cenozoic': '#6aa84f',
        'Other': '#cccccc'
    }

    # Mapear cores
    geology['color'] = geology['ERA'].map(lambda x: era_colors.get(x, '#cccccc'))

    # -------------------------
    # CRIAR MAPA FOLIUM
    # -------------------------
    
    # Centro do mapa (Maputo)
    center_lat = -25.5
    center_lon = 32.0

    # Criar mapa base
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=8,
        tiles='OpenStreetMap'
    )

    # Adicionar tiles alternativos
    folium.TileLayer(
        tiles='CartoDB positron',
        name='CartoDB (claro)',
        control=True
    ).add_to(m)

    folium.TileLayer(
        tiles='CartoDB dark_matter',
        name='CartoDB (escuro)',
        control=True
    ).add_to(m)

    # Adicionar camada de satélite (ESRI)
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Satélite',
        control=True
    ).add_to(m)

    # -------------------------
    # ADICIONAR GEOLOGIA
    # -------------------------
    print("🎨 Adicionando camadas geológicas...")

    # Criar feature group para cada era
    era_groups = {}
    for era in geology['ERA'].unique():
        if era:
            era_groups[era] = folium.FeatureGroup(name=f"🪨 {era}")

    # Adicionar features ao mapa
    for idx, row in geology.iterrows():
        era = row['ERA'] if row['ERA'] else 'Other'
        
        if era in era_groups:
            # Criar popup
            popup = folium.Popup(row['popup_text'], max_width=300)
            
            # Criar tooltip (hover)
            tooltip = folium.Tooltip(
                f"{row['Legend']} ({row['code2006']})"
            )

            # Adicionar geometria
            geo_json = folium.GeoJson(
                row.geometry.__geo_interface__,
                style_function=lambda x, color=row['color']: {
                    'fillColor': color,
                    'color': 'black',
                    'weight': 1,
                    'fillOpacity': 0.7
                },
                popup=popup,
                tooltip=tooltip
            )
            
            geo_json.add_to(era_groups[era])

    # Adicionar todos os grupos ao mapa
    for era, group in era_groups.items():
        group.add_to(m)

    # -------------------------
    # CONTORNO DE MAPUTO
    # -------------------------
    folium.GeoJson(
        province.geometry.__geo_interface__,
        name="📍 Limite de Maputo",
        style_function=lambda x: {
            'color': 'red',
            'weight': 3,
            'fillOpacity': 0
        }
    ).add_to(m)

    # -------------------------
    # CONTROLES ADICIONAIS
    # -------------------------
    
    # Controle de camadas
    folium.LayerControl(collapsed=False).add_to(m)

    # Mini mapa
    minimap = plugins.MiniMap()
    m.add_child(minimap)

    # Fullscreen
    plugins.Fullscreen().add_to(m)

    # Localização em tempo real (GPS)
    plugins.LocateControl(
        auto_start=False,
        position='topright',
        strings={
            'title': "📍 Mostrar minha localização",
            'popup': "Você está aqui"
        }
    ).add_to(m)

    # Medição de distância
    plugins.MeasureControl(
        position='bottomleft',
        primary_length_unit='kilometers',
        secondary_length_unit='meters'
    ).add_to(m)

    # Fit bounds para mostrar toda a área
    m.fit_bounds(m.get_bounds())

    # Draw (desenhar no mapa)
    plugins.Draw(
        export=True,
        filename='minha_anotacao.geojson'
    ).add_to(m)

    # -------------------------
    # LEGENDA HTML
    # -------------------------
    legend_html = '''
    <div style="position: fixed;
                bottom: 50px; right: 50px;
                background-color: white;
                border: 2px solid grey;
                border-radius: 5px;
                padding: 10px;
                font-size: 12px;
                z-index: 9999;
                box-shadow: 2px 2px 5px rgba(0,0,0,0.3);">
        <b>🪨 Eras Geológicas</b><br>
        <i style="color: #6b3d2e;">●</i> Archean<br>
        <i style="color: #a0522d;">●</i> Proterozoic<br>
        <i style="color: #4f81bd;">●</i> Paleozoic<br>
        <i style="color: #f1c232;">●</i> Mesozoic<br>
        <i style="color: #6aa84f;">●</i> Cenozoic<br>
        <i style="color: #cccccc;">●</i> Other
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))

    # -------------------------
    # SALVAR
    # -------------------------
    output_file = "mapa_interativo_maputo.html"
    m.save(output_file)

    print(f"\n✅ Mapa web salvo: {output_file}")
    print("\n📋 Instruções:")
    print("   1. Abra o arquivo no navegador")
    print("   2. Passe o mouse sobre as áreas para ver litologia")
    print("   3. Clique em 📍 para ver sua localização GPS")
    print("   4. Use o controle de camadas para filtrar eras")
    print("   5. Meça distâncias com a ferramenta de medição")
    print("   6. Desenhe e exporte anotações")

    return m


def create_web_map_with_search():
    """
    Versão avançada com busca de distritos
    """
    
    print("\n🔍 Criando mapa com busca de distritos...")
    
    # Carregar distritos de Maputo
    districts = geomoz.read_district()
    
    # Filtrar apenas Maputo
    maputo_districts = districts[districts['Distrito'].str.contains('Maputo|Boane|Marracuene|Namaacha', case=False, na=False)]
    
    print(f"📍 {len(maputo_districts)} distritos encontrados em Maputo")
    
    # Criar mapa
    m = folium.Map(location=[-25.5, 32.0], zoom_start=9)
    
    # Adicionar distritos
    for idx, district in maputo_districts.iterrows():
        folium.GeoJson(
            district.geometry.__geo_interface__,
            name=district['Distrito'],
            popup=district['Distrito'],
            tooltip=district['Distrito'],
            style_function=lambda x: {
                'color': 'blue',
                'weight': 2,
                'fillOpacity': 0.1
            }
        ).add_to(m)
    
    # Adicionar busca
    plugins.Search(
        layer=folium.GeoJson(maputo_districts),
        search_label='Distrito',
        placeholder='Buscar distrito...'
    ).add_to(m)
    
    m.save("mapa_maputo_distritos.html")
    print(f"✅ Mapa com distritos salvo: mapa_maputo_distritos.html")


def main():
    print("🗺️ Mapa Web Interativo - Maputo")
    print("=" * 60)
    
    try:
        # Mapa principal
        m = create_interactive_web_map()
        
        # Mapa com busca (opcional)
        # create_web_map_with_search()
        
        print("\n🎉 Mapas web criados com sucesso!")
        print("\n💡 Abra os arquivos HTML no navegador para explorar!")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
