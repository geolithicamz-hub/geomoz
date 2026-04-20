# Pasta de Testes GeoMoz

Esta pasta contém todos os testes e exemplos da biblioteca GeoMoz, organizados de forma estruturada.

## Estrutura dos Testes

### 1. Testes Principais

#### `test_mozambique_complete.py`
- **Descrição**: Teste completo que gera mapas de todo Moçambique
- **Funções**:
  - Mapa do país completo
  - Mapas individuais das 11 províncias
  - Mapas de distritos (amostra de 3 províncias)
  - Mapas de postos administrativos (amostra de 2 províncias)
- **Ficheiros gerados**: 17 ficheiros PNG
- **Execução**: `python3 test_mozambique_complete.py`

### 2. Testes de CRS e Zonas UTM

#### `crs_auto_example.py`
- **Descrição**: Demonstração de CRS automático no backend
- **Funcionalidades**: Detecção automática de zonas UTM, cálculos de área precisos
- **Execução**: `python3 crs_auto_example.py`

#### `utm_zones_demo.py`
- **Descrição**: Demonstração das zonas UTM corrigidas para Moçambique
- **Funcionalidades**: Zona 36S (30-36E) e Zona 37S (36-42E)
- **Execução**: `python3 utm_zones_demo.py`

#### `check_cross_zone.py`
- **Descrição**: Verificação de áreas que cruzam o limite entre zonas UTM
- **Funcionalidades**: Identificação de províncias/distritos que cruzam 36°E
- **Execução**: `python3 check_cross_zone.py`

#### `test_cross_zone_robust.py`
- **Descrição**: Teste robusto do tratamento de cruzamento de zonas UTM
- **Funcionalidades**: Validação do tratamento automático
- **Execução**: `python3 test_cross_zone_robust.py`

#### `final_demo_simple.py`
- **Descrição**: Demonstração final mostrando simplicidade para o usuário
- **Funcionalidades**: Exemplos de uso sem preocupação com CRS
- **Execução**: `python3 final_demo_simple.py`

### 3. Testes Legados

#### `test_geomoz.py`
- **Descrição**: Teste básico original da biblioteca
- **Funcionalidades**: Verificação de funções principais
- **Execução**: `python3 test_geomoz.py`

## Ficheiros Gerados

### Mapas (PNG)
- `mozambique_pais.png` - Mapa completo do país
- `provincia_*.png` - Mapas individuais das províncias (11 ficheiros)
- `distritos_*.png` - Mapas de distritos (3 ficheiros)
- `postos_*.png` - Mapas de postos administrativos (2 ficheiros)

### Relatórios
- `resumo_testes.txt` - Resumo dos testes executados

## Dados de Moçambique

- **Províncias**: 11
- **Distritos**: 161
- **Postos Administrativos**: 459

## Zonas UTM

- **Zona 36S**: 30°E a 36°E (sul e centro)
- **Zona 37S**: 36°E a 42°E (norte)

## Províncias que Cruzam Zonas

- **Sofala**: 33.38°E a 36.19°E
- **Zambézia**: 35.14°E a 39.14°E
- **Niassa**: 34.35°E a 38.49°E

## Como Executar

```bash
# Mudar para pasta de testes
cd tests

# Executar teste completo
python3 test_mozambique_complete.py

# Executar demonstração de CRS
python3 crs_auto_example.py

# Executar verificação de zonas
python3 check_cross_zone.py
```

## Funcionalidades Testadas

### CRS Automático
- Detecção automática de zona UTM
- Tratamento de cruzamento de zonas
- Cálculos de área precisos
- Conversão transparente para o usuário

### Mapeamento
- Geração de mapas em diferentes escalas
- Cores diferenciadas por unidade administrativa
- Legendas informativas
- Alta resolução (DPI 150-200)

### Robustez
- Tratamento de erros
- Verificação de consistência
- Validação de resultados

## Resumo

Todos os testes foram projetados para validar:
1. Funcionalidade básica da biblioteca
2. Tratamento robusto de CRS
3. Geração de mapas em diferentes escalas
4. Simplicidade para o usuário final

A pasta `tests/` contém um conjunto completo de validações para garantir que o GeoMoz funcione corretamente em todos os cenários de uso.
