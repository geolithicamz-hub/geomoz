"""
Data utilities for GeoMoz - Hugging Face integration
"""

import warnings
from pathlib import Path

try:
    from huggingface_hub import hf_hub_download
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False
    warnings.warn(
        "huggingface_hub not installed. Install with: pip install huggingface_hub",
        ImportWarning
    )


# Cache directory for GeoMoz data
CACHE_DIR = Path.home() / ".cache" / "geomoz"


def get_data_path(filename: str, repo_id: str = "geolithicamz/geomoz-data") -> str:
    """
    Get data path from Hugging Face with automatic download and caching

    This function downloads geospatial data from Hugging Face datasets
    and caches them locally for future use.

    Parameters
    ----------
    filename : str
        Name of the file to download (e.g., "province_2017.gpkg")
    repo_id : str, optional
        Hugging Face repository ID. Default is "geolithicamz/geomoz-data"

    Returns
    -------
    str
        Local path to the downloaded file

    Raises
    ------
    ImportError
        If huggingface_hub is not installed
    FileNotFoundError
        If the file cannot be downloaded from Hugging Face

    Examples
    --------
    >>> from geomoz.utils.data import get_data_path
    >>>
    >>> # Get path to province data
    >>> province_path = get_data_path("province_2017.gpkg")
    >>> print(f"Province data: {province_path}")
    >>>
    >>> # Get path to geology data
    >>> geology_path = get_data_path("geology_2006.gpkg")
    >>> print(f"Geology data: {geology_path}")
    """
    if not HF_AVAILABLE:
        raise ImportError(
            "huggingface_hub is required but not installed. "
            "Install with: pip install huggingface_hub"
        )

    try:
        # Create cache directory if it doesn't exist
        CACHE_DIR.mkdir(parents=True, exist_ok=True)

        # Download file from Hugging Face (downloads are resumed by default
        # in recent huggingface_hub versions; the explicit flag was removed
        # because it is deprecated).
        file_path = hf_hub_download(
            repo_id=repo_id,
            filename=filename,
            repo_type="dataset",
            cache_dir=CACHE_DIR,
        )
    except Exception as e:
        # Fallback robusto com mensagem clara
        error_msg = f"""
Erro ao baixar dados do Hugging Face!

Arquivo: {filename}
Repositório: {repo_id}
URL: https://huggingface.co/{repo_id}

Possíveis causas:
• Sem conexão com a internet
• Hugging Face temporariamente offline
• Nome do arquivo incorreto
• Problemas de rede/firewall

Soluções:
1. Verifique sua conexão com a internet
2. Tente novamente em alguns minutos
3. Verifique se o arquivo existe em: https://huggingface.co/{repo_id}
4. Desative firewall/proxy temporariamente

Se o problema persistir:
• Abra issue em: https://github.com/geolithicamz-hub/geomoz/issues
• Email: heltrakinho@gmail.com

Erro original: {str(e)}
"""
        raise RuntimeError(error_msg)

    return file_path


def list_available_files(repo_id: str = "geolithicamz/geomoz-data") -> list:
    """
    List all available files in the Hugging Face dataset

    Parameters
    ----------
    repo_id : str, optional
        Hugging Face repository ID

    Returns
    -------
    list
        List of available filenames

    Examples
    --------
    >>> from geomoz.utils.data import list_available_files
    >>> files = list_available_files()
    >>> print("Available files:", files)
    """
    if not HF_AVAILABLE:
        return []

    try:
        from huggingface_hub import list_repo_files

        files = list_repo_files(
            repo_id=repo_id,
            repo_type="dataset"
        )

        # Filter for geopackage files
        gpkg_files = [f for f in files if f.endswith('.gpkg')]
        return gpkg_files

    except Exception:
        # Fallback to known files
        return [
            "province_2017.gpkg",
            "district_2017.gpkg",
            "adminpost_2017.gpkg",
            "village_2017.gpkg",
            "geology_2006.gpkg"
        ]


def clear_cache() -> None:
    """
    Clear the GeoMoz cache directory

    This removes all downloaded files from the local cache.
    Next time a file is requested, it will be downloaded again.

    Examples
    --------
    >>> from geomoz.utils.data import clear_cache
    >>> clear_cache()
    >>> print("Cache cleared")
    """
    try:
        if CACHE_DIR.exists():
            import shutil
            shutil.rmtree(CACHE_DIR)
            print(f"GeoMoz cache cleared: {CACHE_DIR}")
        else:
            print("No cache directory found")
    except Exception as e:
        print(f"Error clearing cache: {e}")


def get_cache_info() -> dict:
    """
    Get information about the current cache

    Returns
    -------
    dict
        Dictionary with cache information including size and file count

    Examples
    --------
    >>> from geomoz.utils.data import get_cache_info
    >>> info = get_cache_info()
    >>> print(f"Cache size: {info['size_mb']:.2f} MB")
    >>> print(f"Cached files: {info['file_count']}")
    """
    info = {
        'cache_dir': str(CACHE_DIR),
        'exists': CACHE_DIR.exists(),
        'size_bytes': 0,
        'size_mb': 0.0,
        'file_count': 0,
        'files': []
    }

    if CACHE_DIR.exists():
        try:
            import os
            total_size = 0
            file_count = 0
            files = []

            for root, _dirs, filenames in os.walk(CACHE_DIR):
                for filename in filenames:
                    if filename.endswith('.gpkg'):
                        file_path = Path(root) / filename
                        file_size = file_path.stat().st_size
                        total_size += file_size
                        file_count += 1
                        files.append({
                            'name': filename,
                            'path': str(file_path),
                            'size_bytes': file_size,
                            'size_mb': file_size / (1024 * 1024)
                        })

            info.update({
                'size_bytes': total_size,
                'size_mb': total_size / (1024 * 1024),
                'file_count': file_count,
                'files': files
            })

        except Exception as e:
            info['error'] = str(e)

    return info


def validate_data_file(filename: str) -> bool:
    """
    Validate if a data file exists and is accessible

    Parameters
    ----------
    filename : str
        Name of the file to validate

    Returns
    -------
    bool
        True if file is accessible, False otherwise

    Examples
    --------
    >>> from geomoz.utils.data import validate_data_file
    >>> if validate_data_file("province_2017.gpkg"):
    ...     print("File is accessible")
    """
    try:
        path = get_data_path(filename)
        return Path(path).exists() and Path(path).is_file()
    except Exception:
        return False
