# GeoMoz: Uma Biblioteca Open-Source para Democratizar o Acesso a Dados Geoespaciais de Moçambique

**Hélder Gonçalves Félix Traquinho**¹

¹ Geolithica — Chief Executive Officer. Av. 24 de Julho, N.º 119, 5.º andar, Maputo, Moçambique. (heltrakinho@gmail.com)

---

## Resumo

O acesso a dados geoespaciais de qualidade é um pilar para a pesquisa científica, o
planeamento territorial, a exploração de recursos naturais e a gestão ambiental em
Moçambique. Contudo, esses dados encontram-se frequentemente dispersos, em formatos
proprietários ou de difícil obtenção, criando uma barreira técnica para geocientistas,
investigadores e gestores públicos. Este artigo apresenta o **GeoMoz**, uma biblioteca
open-source, disponível em Python e R, que oferece acesso programático, reprodutível e
gratuito às divisões administrativas (11 províncias, 161 distritos, 459 postos
administrativos e 11.524 localidades) e à cartografia geológica nacional (~50.000
feições) de Moçambique. Inspirado no consagrado pacote `geobr` (Brasil), o GeoMoz
distribui os dados através da plataforma Hugging Face, com cache local automático, e
expõe uma API simples e consistente para leitura, filtragem, análise espacial e
visualização. Discutimos a motivação, a arquitetura, decisões de implementação,
validação e o roteiro de evolução da ferramenta.

**Palavras-chave:** dados geoespaciais; SIG; Moçambique; Python; R; open-source; geologia; recursos naturais.

---

## 1. Introdução

A informação geográfica é um insumo crítico para decisões de política pública,
investigação académica e investimento no setor extractivo. Em Moçambique — país com
vasto potencial mineral e grande diversidade geológica — a fragmentação do acesso a
dados espaciais limita a reprodutibilidade científica e atrasa análises que dependem de
fronteiras administrativas e unidades litológicas atualizadas.

Bibliotecas que encapsulam o acesso a dados oficiais já demonstraram enorme impacto
noutros contextos. O exemplo mais influente é o `geobr`, que transformou a forma como a
comunidade brasileira consome dados do IBGE, ao reduzir a barreira de entrada de horas
de preparação de *shapefiles* para uma única chamada de função. O GeoMoz nasce dessa
mesma filosofia, adaptada às especificidades de Moçambique: um único comando deve
devolver um `GeoDataFrame` (Python) ou `sf` (R) pronto para análise.

## 2. Trabalhos relacionados

O ecossistema de dados abertos georreferenciados conta com referências como o já citado
`geobr`, o `tigris` (EUA) e o `rnaturalearth` (mundial). Estas ferramentas partilham um
padrão de desenho: funções `read_*` por nível geográfico, *download* sob demanda, cache
local e devolução de objetos espaciais idiomáticos. O GeoMoz adota esse padrão e
acrescenta a integração com o Hugging Face Hub como camada de distribuição de dados,
beneficiando de versionamento, CDN global e hospedagem gratuita para conjuntos de dados.

## 3. Dados

O GeoMoz disponibiliza, na sua versão atual:

| Conjunto | Função | Feições | Ano | Fonte |
|---|---|---:|---|---|
| Províncias | `read_province` | 11 | 2017 | INE Moçambique |
| Distritos | `read_district` | 161 | 2017 | INE Moçambique |
| Postos administrativos | `read_admin_post` | 459 | 2017 | INE Moçambique |
| Localidades | `read_village` | 11.524 | 2017 | INE Moçambique |
| Geologia | `read_geology` | ~50.000 | 2006 | Conselho Nacional de Geologia (DNGM) |

Todos os dados são fornecidos no sistema de referência geodésico **WGS 84 (EPSG:4326)**,
em formato **GeoPackage (`.gpkg`)**, com colunas de código e nome normalizadas para
permitir filtragem determinística.

## 4. Arquitetura e implementação

A biblioteca segue uma arquitetura modular com separação clara de responsabilidades:

- **Camada de leitura** (`read_province`, `read_district`, `read_admin_post`,
  `read_village`, `read_geology`): valida parâmetros, resolve o ficheiro de dados e
  aplica filtros por código ou por nome (insensível a maiúsculas).
- **Camada de dados** (`utils/data.py`): faz o *download* a partir do repositório
  Hugging Face `geolithicamz/geomoz-data` e mantém um cache local em `~/.cache/geomoz`,
  garantindo uso offline após a primeira execução.
- **Camada de metadados** (`utils/utils.py`, `list_geomoz`): descreve os conjuntos
  disponíveis (geografia, ano, fonte, colunas), alimentando funções de descoberta como
  `list_available_geographies()` e `get_dataset_info()`.
- **Camada espacial** (`spatial.py`): operações de cruzamento hierárquico
  (e.g., `geology_by_province`, `link_village_district`) e cálculo de áreas.
- **Camada de visualização** (`plot_utils.py`): mapas temáticos sobre matplotlib.

### 4.1 Dependências opcionais e importação preguiçosa

Uma decisão de desenho importante é a separação entre o *core* da biblioteca e a camada
de visualização. As dependências pesadas de plotagem (matplotlib, seaborn, folium,
contextily) são declaradas como um *extra* opcional `viz`. Para que `import geomoz`
nunca falhe na ausência desses pacotes, as funções de plotagem são expostas via
importação preguiçosa (PEP 562, `module-level __getattr__`): só carregam matplotlib no
primeiro uso e, se faltarem, emitem uma mensagem de erro acionável
(`pip install 'geomoz[viz]'`). Assim, ambientes de servidor ou de análise de dados que
não precisam de gráficos permanecem leves.

### 4.2 Distribuição e cache

O acoplamento com o Hugging Face Hub permite distribuir conjuntos de dados grandes (como
as ~50.000 feições geológicas) fora do pacote Python, mantendo o *wheel* pequeno. O
cache local evita re-*downloads*, e funções utilitárias (`get_cache_info`,
`clear_cache`) dão ao utilizador controlo sobre o armazenamento.

## 5. Uso

### 5.1 Instalação

```bash
pip install geomoz          # núcleo (leitura + análise espacial)
pip install 'geomoz[viz]'   # com suporte a visualização
```

### 5.2 Exemplo mínimo

```python
import geomoz

# Todas as províncias
provincias = geomoz.read_province()

# Filtragem por nome
nampula = geomoz.read_province(name_province="Nampula")

# Cruzamento geologia × província
geo_nampula = geomoz.geology_by_province("Nampula")

# Descoberta de conjuntos disponíveis (offline)
geomoz.list_geomoz()
```

### 5.3 Visualização

```python
from geomoz import plot_provinces   # carrega matplotlib sob demanda
plot_provinces(show_names=True, save_path="provincias.png")
```

## 6. Validação e qualidade de software

A biblioteca inclui uma suíte de testes automatizados dividida em testes **offline**
(API pública, metadados, importação preguiçosa) e testes **de rede** (marcados e
desativáveis com `pytest -m "not network"`), permitindo verificação rápida em ambientes
sem conectividade. A integração contínua (GitHub Actions) executa a suíte em múltiplas
versões de Python (3.8, 3.10 e 3.12) e confirma, a cada alteração, que o pacote importa
corretamente **sem** as dependências opcionais de visualização — um teste de regressão
para o desenho descrito na Secção 4.1. A versão do pacote é mantida numa única fonte de
verdade (`geomoz/__init__.py`), evitando divergências de metadados.

## 7. Resultados e impacto

O GeoMoz reduz a obtenção de uma camada administrativa ou geológica de Moçambique de um
fluxo manual (procura de *shapefiles*, conversão de projeções, limpeza de colunas) para
uma única chamada de função reprodutível. Está disponível via **PyPI** (Python) e em
processo de submissão ao **CRAN** (R, pacote `GeoMozR`). Os casos de uso diretos incluem
mapeamento geológico distrital, integração com dados de concessões mineiras, gestão de
recursos hídricos e planeamento urbano — todos beneficiando de fronteiras e litologias
consistentes e citáveis.

## 8. Limitações e trabalho futuro

As principais direções de evolução são: (i) ampliar a cobertura temporal das divisões
administrativas (séries históricas e censos mais recentes); (ii) acrescentar camadas de
hidrografia, infraestrutura e recursos minerais; (iii) publicar um catálogo de
metadados versionado; (iv) disponibilizar *tiles* vetoriais para visualização web
interativa; e (v) consolidar a paridade funcional entre as implementações Python e R.

## 9. Conclusão

O GeoMoz materializa o princípio de que dados públicos devem ser também *acessíveis* na
prática, e não apenas em teoria. Ao encapsular a complexidade de obtenção, projeção e
limpeza de dados geoespaciais de Moçambique numa API simples, reprodutível e gratuita, a
biblioteca remove barreiras técnicas e contribui para decisões baseadas em evidência no
contexto dos Objetivos de Desenvolvimento Sustentável. Sendo open-source, convida a
comunidade a contribuir com novos conjuntos de dados e funcionalidades.

## Disponibilidade

- **Código-fonte:** https://github.com/geolithicamz-hub/geomoz
- **Dados:** Hugging Face — `geolithicamz/geomoz-data`
- **Licença:** MIT

## Agradecimentos

Agradeço à equipa da Geolithica pelo apoio ao desenvolvimento desta ferramenta e à
comunidade open-source pelas bibliotecas (GeoPandas, Shapely, pandas, Hugging Face Hub)
que tornaram este projeto possível.

## Referências

1. Pereira, R. H. M.; Gonçalves, C. N. *et al.* **geobr: Loads Shapefiles of Official
   Spatial Data Sets of Brazil.** R package / Python package.
2. Jordahl, K. *et al.* **GeoPandas: Python tools for geographic data.**
3. Gillies, S. *et al.* **Shapely: manipulation and analysis of geometric objects.**
4. Instituto Nacional de Estatística (INE), Moçambique. **Divisões administrativas.**
5. Conselho Nacional de Geologia / Direção Nacional de Geologia e Minas (DNGM).
   **Carta Geológica de Moçambique (2006).**
6. Hugging Face. **Hub: hosting datasets and models.**
