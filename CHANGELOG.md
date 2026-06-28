# Changelog

Todas as mudanças relevantes deste projeto são documentadas neste ficheiro.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/),
e o projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

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

[0.1.2]: https://github.com/geolithicamz-hub/geomoz/releases/tag/v0.1.2
[0.1.1]: https://github.com/geolithicamz-hub/geomoz/releases/tag/v0.1.1
