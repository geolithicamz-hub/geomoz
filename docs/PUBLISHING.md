# Publicação no PyPI

Guia para lançar uma nova versão do `geomoz` no PyPI.

## Pré-requisitos

```bash
pip install -e ".[dev]"   # inclui build e twine
```

Um token de API do PyPI com escopo do projeto `geomoz`
(https://pypi.org/manage/account/token/).

## Passos

1. **Atualizar a versão** (fonte única) em `geomoz/__init__.py`:

   ```python
   __version__ = "X.Y.Z"
   ```

   O `pyproject.toml` lê a versão daí automaticamente
   (`[tool.hatch.version]`).

2. **Atualizar o `CHANGELOG.md`** com as mudanças da versão.

3. **Rodar os testes** offline e verificar o import sem extras:

   ```bash
   pytest -m "not network"
   python -c "import geomoz; print(geomoz.__version__)"
   ```

4. **Construir** os artefactos limpos:

   ```bash
   rm -rf dist/ build/ *.egg-info
   python -m build
   ```

   O sdist deve ficar pequeno (apenas o pacote e metadados; os exemplos
   pesados são excluídos via `[tool.hatch.build.targets.sdist]`).

5. **Validar**:

   ```bash
   twine check dist/*
   ```

6. **Publicar**:

   ```bash
   twine upload dist/*
   # username: __token__
   # password: o token pypi-...
   ```

7. **Confirmar**:

   ```bash
   pip install --upgrade geomoz
   ```

## Notas

- O PyPI **não permite** reenviar uma versão já publicada; cada lançamento
  precisa de um número novo.
- O `README.md` é a descrição longa apresentada na página do PyPI.
- Para um ensaio sem afetar a produção, use o TestPyPI:
  `twine upload --repository testpypi dist/*`.
