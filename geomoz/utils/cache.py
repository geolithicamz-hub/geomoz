#!/usr/bin/env python3
"""
Sistema de Cache para GeoMoz
Otimiza carregamento de dados grandes (aldeias, postos)
"""

import os
import pickle
import hashlib
import time
from functools import wraps
from pathlib import Path
from typing import Optional, Callable, Any
import geopandas as gpd


# Diretório de cache
CACHE_DIR = Path.home() / ".geomoz_cache"
CACHE_DIR.mkdir(exist_ok=True)

# Tempo de expiração padrão (24 horas)
DEFAULT_CACHE_HOURS = 24


def get_cache_path(cache_key: str) -> Path:
    """Retorna o caminho do arquivo de cache"""
    return CACHE_DIR / f"{cache_key}.pkl"


def generate_cache_key(function_name: str, *args, **kwargs) -> str:
    """Gera uma chave única de cache baseada na função e argumentos"""
    # Criar string representativa
    key_string = f"{function_name}_{str(args)}_{str(kwargs)}"
    # Hash MD5 para nome de arquivo válido
    cache_key = hashlib.md5(key_string.encode()).hexdigest()
    return cache_key


def is_cache_valid(cache_path: Path, max_age_hours: float = DEFAULT_CACHE_HOURS) -> bool:
    """Verifica se o cache existe e é válido"""
    if not cache_path.exists():
        return False

    # Verificar idade do arquivo
    file_age = time.time() - cache_path.stat().st_mtime
    max_age_seconds = max_age_hours * 3600

    return file_age < max_age_seconds


def save_to_cache(data: Any, cache_path: Path) -> None:
    """Salva dados no cache"""
    try:
        with open(cache_path, 'wb') as f:
            pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception as e:
        print(f"Erro ao salvar cache: {e}")

def load_from_cache(cache_path: Path) -> Optional[Any]:
    """Carrega dados do cache"""
    try:
        with open(cache_path, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        print(f"Erro ao carregar cache: {e}")
        return None


def cached(max_age_hours: float = DEFAULT_CACHE_HOURS,
           verbose: bool = False) -> Callable:
    """
    Decorador para cache de funções

    Parameters
    ----------
    max_age_hours : float, optional
        Tempo máximo de validade do cache em horas. Default 24.
    verbose : bool, optional
        Mostrar mensagens de debug. Default False.

    Returns
    -------
    Callable
        Função decorada com cache

    Examples
    --------
    >>> @cached(max_age_hours=12)
    ... def minha_funcao():
    ...     return dados_pesados()
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Gerar chave de cache
            cache_key = generate_cache_key(func.__name__, *args, **kwargs)
            cache_path = get_cache_path(cache_key)

            # Verificar cache válido
            if is_cache_valid(cache_path, max_age_hours):
                if verbose:
                    print(f"Cache: Carregando {func.__name__} do cache...")
                cached_data = load_from_cache(cache_path)
                if cached_data is not None:
                    return cached_data

            # Executar função
            if verbose:
                print(f"Cache: Executando {func.__name__}...")

            start_time = time.time()
            result = func(*args, **kwargs)
            elapsed = time.time() - start_time

            if verbose:
                print(f"Cache: {func.__name__} concluído em {elapsed:.2f}s")

            # Salvar no cache se for GeoDataFrame
            if isinstance(result, gpd.GeoDataFrame):
                save_to_cache(result, cache_path)
                if verbose:
                    print(f"Cache: Salvo em {cache_path}")

            return result

        return wrapper
    return decorator


def clear_cache(older_than_hours: Optional[float] = None) -> int:
    """
    Limpa arquivos de cache

    Parameters
    ----------
    older_than_hours : float, optional
        Se especificado, remove apenas arquivos mais antigos que X horas.
        Se None, remove todos.

    Returns
    -------
    int
        Número de arquivos removidos

    Examples
    --------
    >>> from geomoz.utils.cache import clear_cache
    >>> clear_cache()  # Remove todos
    >>> clear_cache(older_than_hours=48)  # Remove apenas antigos
    """
    removed = 0

    for cache_file in CACHE_DIR.glob("*.pkl"):
        if older_than_hours is not None:
            file_age = time.time() - cache_file.stat().st_mtime
            if file_age < older_than_hours * 3600:
                continue

        try:
            cache_file.unlink()
            removed += 1
        except Exception as e:
            print(f"Erro ao remover {cache_file}: {e}")

    print(f"Cache: {removed} arquivo(s) removido(s)")
    return removed


def get_cache_info() -> dict:
    """
    Retorna informações sobre o cache

    Returns
    -------
    dict
        Informações do cache

    Examples
    --------
    >>> from geomoz.utils.cache import get_cache_info
    >>> info = get_cache_info()
    >>> print(info['total_size_mb'])
    """
    cache_files = list(CACHE_DIR.glob("*.pkl"))

    total_size = sum(f.stat().st_size for f in cache_files)
    total_size_mb = total_size / (1024 * 1024)

    # Arquivos mais recentes
    recent_files = sorted(
        cache_files,
        key=lambda f: f.stat().st_mtime,
        reverse=True
    )[:10]

    return {
        'total_files': len(cache_files),
        'total_size_mb': round(total_size_mb, 2),
        'cache_dir': str(CACHE_DIR),
        'recent_files': [f.name for f in recent_files]
    }


def print_cache_info():
    """Imprime informações do cache de forma formatada"""
    info = get_cache_info()

    print("Informações do Cache GeoMoz")
    print("=" * 50)
    print(f"Diretório: {info['cache_dir']}")
    print(f"Arquivos: {info['total_files']}")
    print(f"Tamanho: {info['total_size_mb']:.2f} MB")

    if info['recent_files']:
        print("\nArquivos mais recentes:")
        for f in info['recent_files'][:5]:
            print(f"   • {f}")


# Funções específicas com cache para dados grandes

class CachedGeoMoz:
    """
    Versão com cache das funções de leitura do GeoMoz
    """

    @staticmethod
    @cached(max_age_hours=24, verbose=False)
    def read_village(code_village="all", name_village=None):
        """Ler aldeias com cache (11,524 aldeias = dados grandes)"""
        from ..read_village import read_village as _read_village
        return _read_village(code_village=code_village, name_village=name_village)

    @staticmethod
    @cached(max_age_hours=24, verbose=False)
    def read_admin_post(code_admin_post="all", name_admin_post=None):
        """Ler postos administrativos com cache (459 postos)"""
        from ..read_admin_post import read_admin_post as _read_admin_post
        return _read_admin_post(code_admin_post=code_admin_post, name_admin_post=name_admin_post)

    @staticmethod
    @cached(max_age_hours=24, verbose=False)
    def read_district(code_district="all", name_district=None):
        """Ler distritos com cache (161 distritos)"""
        from ..read_district import read_district as _read_district
        return _read_district(code_district=code_district, name_district=name_district)

    @staticmethod
    @cached(max_age_hours=24, verbose=False)
    def read_province(code_province="all", name_province=None):
        """Ler províncias com cache (11 províncias)"""
        from ..read_province import read_province as _read_province
        return _read_province(code_province=code_province, name_province=name_province)

    @staticmethod
    @cached(max_age_hours=24, verbose=False)
    def read_geology(code_geology="all", name_geology=None):
        """Ler geologia com cache (dados grandes)"""
        from ..read_geology import read_geology as _read_geology
        return _read_geology(code_geology=code_geology, name_geology=name_geology)


# Aliases para facilitar uso
cache_info = get_cache_info
print_cache = print_cache_info
clear_old_cache = clear_cache


if __name__ == "__main__":
    # Teste do sistema de cache
    print("Testando Sistema de Cache...")
    print_cache_info()

    print("\nPara usar cache nas funções:")
    print("   from geomoz.utils.cache import CachedGeoMoz")
    print("   villages = CachedGeoMoz.read_village()")
