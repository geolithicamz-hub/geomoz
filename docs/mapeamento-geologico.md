# GeoMoz - Exemplos de Mapeamento Geológico

## Arquivos de Mapeamento Criados

### 1. `geology_map_zambezia.py`
- **Função**: Mapa completo com estatísticas detalhadas
- **Características**:
  - Usa coluna `Legend` para coloração
  - Top 15 unidades geológicas
  - Legenda completa
- **Output**: `geology_zambezia_map.png` (1.8MB)

### 2. `simple_geology_map.py`
- **Função**: Versão simplificada e rápida
- **Características**:
  - Top 10 unidades apenas
  - Mapa mais limpo
  - Execução rápida
- **Output**: `geology_zambézia_simple.png`

### 3. `complete_geology_map.py`
- **Função**: Versão completa com todas as unidades
- **Características**:
  - Todas as camadas geológicas
  - Cores únicas para cada litologia
  - Rótulos para unidades grandes
- **Output**: `geology_zambezia_complete.png` (1.8MB)

### 4. `robust_geology_map.py` **(RECOMENDADO)**
- **Função**: Versão robusta e estável
- **Características**:
  - Sem problemas de CRS
  - Filtra unidades significativas (>5 ocorrências)
  - Mapa por suite adicional
- **Outputs**:
  - `geology_zambezia_robust.png` (1.3MB)
  - `geology_zambezia_by_suite.png` (597KB)

## Estatísticas de Zambezia

### Dados Geológicos
- **Total de unidades**: 2.129
- **Valores únicos (Legend)**: 74
- **Unidades com suite**: 866
- **Unidades significativas**: 48 (>5 ocorrências)

### Top 5 Unidades Geológicas
1. **Banded biotite gneiss and migmatite**: 172 unidades
2. **Undifferentiated**: 138 unidades
3. **Coastal sand dunes and beach sand**: 134 unidades
4. **Granite**: 127 unidades
5. **Alluvium, sand, silt, gravel**: 123 unidades

### Top 5 Suites Geológicas
1. **Mocuba**: 345 unidades
2. **Culicui**: 287 unidades
3. **Marrupula**: 116 unidades
4. **Murrupula**: 78 unidades
5. **Serra Morrombala**: 18 unidades

### Distribuição por ERA
- **Mesoproterozoic**: 801 unidades
- **CENOZOIC**: 505 unidades
- **MESOPROTEROZOIC**: 456 unidades
- **Cambrian**: 105 unidades
- **PALEOZOIC**: 94 unidades

## Como Usar

### Mapa Básico
```python
import geomoz
import matplotlib.pyplot as plt

# Carregar geologia recortada
geo = geomoz.geology_by_province(name_province="Zambézia")
province = geomoz.read_province(name_province="Zambézia")

# Plotar
fig, ax = plt.subplots(1, 1, figsize=(12, 8))
province.boundary.plot(ax=ax, color='black', linewidth=2)
geo.plot(ax=ax, column='Legend', cmap='tab20', alpha=0.8, legend=True, legend_kwds={'loc': 'center left', 'bbox_to_anchor': (1, 0.5)})
plt.show()
```

### Mapa por Suite Específica
```python
# Suite específica em Zambezia
geo_malema = geomoz.geology_by_province(
    name_province="Zambézia",
    SUITE="Malema"
)
print(f"Unidades Malema: {len(geo_malema)}")
```

### Mapa por Múltiplas Províncias
```python
# Comparar geologia entre províncias
provinces = ["Nampula", "Zambézia", "Tete"]
for province in provinces:
    geo = geomoz.geology_by_province(name_province=province)
    print(f"{province}: {len(geo)} unidades")
```

## Características Técnicas

### Integração Espacial
- **Overlay**: `gpd.overlay()` para recortar geologia pelos limites administrativos
- **CRS**: EPSG:4326 (WGS 84)
- **Resolução**: 200-300 DPI para imagens

### Colunas Disponíveis
- **Legend**: Descrição em inglês (principal para coloração)
- **Legenda**: Descrição em português
- **ERA**: Era geológica
- **SUITE**: Suite geológica
- **Formation**: Formação geológica
- **code2006**: Código geológico

### Visualização
- **Colormaps**: `tab20`, `Set3`, `rainbow`
- **Transparência**: 0.8 para sobreposição
- **Legendas**: Posicionadas lateralmente
- **Tamanhos**: 12-16 polegadas para boa resolução

## Aplicações Práticas

1. **Mineração**: Identificar áreas com unidades geológicas específicas
2. **Exploração**: Analisar distribuição de suites de interesse
3. **Pesquisa**: Estudar padrões geológicos regionais
4. **Educação**: Visualizar geologia para ensino
5. **Planejamento**: Integrar geologia com infraestrutura

## Próximos Passos

- [ ] Adicionar mapas 3D
- [ ] Integrar dados de mineração
- [ ] Criar mapas interativos
- [ ] Adicionar análise estatística avançada
- [ ] Exportar para outros formatos (GIS)

---

**GeoMoz - Integração Espacial de Dados Geológicos de Moçambique**
