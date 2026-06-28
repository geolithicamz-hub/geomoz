# Changelog

Todas as mudanças relevantes deste projeto são documentadas neste ficheiro.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/),
e o projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [0.1.4] - 2026-06-28

### Corrigido
- `geology_by_district` e `geology_by_admin_post` passavam código **e**
  nome ao mesmo tempo para as funções de leitura, gerando
  `ValueError: Cannot specify both ...`. Agora passam apenas o filtro
  fornecido.
- `read_village` referenciava colunas inexistentes (`CodPov`/`Povoacao`),
  quebrando qualquer filtro. As colunas passam a ser **normalizadas** para
  `Povoacao`, `Posto`, `Distrito`, `Provincia`, `Latitude`, `Longitude`,
  consistentes com as outras camadas (ex.: `villages[villages["Provincia"]
  == "Nampula"]` agora funciona).
- `plot_provinces` usava `matplotlib.cm.get_cmap`, removido no matplotlib
  3.9+. Substituído por `plt.get_cmap`.

### Alterado
- As legendas dos utilitários de plot (`quick_map`,
  `plot_villages_with_names`) passam a ficar **fora** da área do mapa, para
  não sobrepor a figura.
- Guias de uso revistos: exemplos de mapa por era geológica agora
  normalizam a coluna `ERA` (que mistura maiúsculas/subdivisões) e
  desenham sempre um mapa; nomes de distrito corrigidos
  (ex.: `"Cidade de Tete"`); legendas colocadas fora do mapa.

### Adicionado
- Testes de integração (marcados como `network`) cobrindo os fluxos reais
  dos guias: filtragem por província, `geology_by_*`, classificação de
  eras e renderização dos utilitários de plot.

## [0.1.3] - 2026-06-28

### Corrigido
- Metadados de empacotamento no PyPI: o pacote publicado passa a declarar
  corretamente **Python >= 3.9** (a 0.1.2 no PyPI ainda anunciava >= 3.8,
  incompatível com `geopandas >= 0.14`).

### Alterado
- Mensagens de runtime (`print`/erros) sem emojis, para uma apresentação
  mais limpa.
- README com badges dinâmicos de CI e PyPI; documentação consolidada em
  `docs/`.

## [0.1.2] - 2026-06-28

### Corrigido
- `import geomoz` deixava de funcionar quando o matplotlib não estava
  instalado. As funções de plotagem passam a ser importadas de forma
  preguiçosa (PEP 562), com mensagem de erro acionável a apontar para
  `pip install 'geomoz[viz]'`.
- `list_geomoz`, `list_available_geographies` e `get_dataset_info`
  lançavam `KeyError` por falta de colunas (`function`, `geography`,
  `source`) nos metadados. Os metadados foram completados.
- Removida a flag `resume_download`, deprecada no `huggingface_hub`.

### Alterado
- Requisito mínimo passa para **Python >= 3.9**, alinhado à dependência
  `geopandas >= 0.14`.
- Versão mantida numa única fonte de verdade (`geomoz/__init__.py`).
- `numpy` declarado no extra opcional `viz`.
- Distribuição de código-fonte (sdist) reduzida de ~16 MB para ~22 KB,
  restringindo o conteúdo ao pacote e metadados essenciais.
- Documentação reorganizada na pasta `docs/`; emojis removidos de toda a
  documentação e das mensagens de runtime.

### Removido
- Módulos mortos `core.py` e `utils.py` (sombreado), os exports legados
  quebrados (`list_geometries`, `list_provinces`) e ficheiros `*_old.py`.

### Adicionado
- Integração contínua (GitHub Actions) testando Python 3.9, 3.10 e 3.12,
  com verificação de que o pacote importa sem os extras de visualização.
- Suíte de testes reescrita, separando testes offline de testes de rede
  (`pytest -m "not network"`).
- Artigo técnico `ARTIGO_GEOMOZ.md`.

## [0.1.1] - 2025

### Adicionado
- Primeira versão publicada no PyPI: leitura de províncias, distritos,
  postos administrativos, localidades e geologia de Moçambique, com
  download automático a partir do Hugging Face.

[0.1.4]: https://github.com/geolithicamz-hub/geomoz/releases/tag/v0.1.4
[0.1.3]: https://github.com/geolithicamz-hub/geomoz/releases/tag/v0.1.3
[0.1.2]: https://github.com/geolithicamz-hub/geomoz/releases/tag/v0.1.2
[0.1.1]: https://github.com/geolithicamz-hub/geomoz/releases/tag/v0.1.1
