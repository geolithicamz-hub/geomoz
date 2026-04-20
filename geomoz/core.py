"""
Funções principais da biblioteca GeoMoz
"""

import os
import geopandas as gpd
from typing import Optional, Union

# Diretório base dos dados
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

def list_geometries() -> dict:
    """
    Lista todas as geometrias disponíveis na biblioteca
    
    Returns:
        dict: Dicionário com informações sobre os dados disponíveis
    """
    available_data = {
        "province_2017": {
            "description": "Províncias de Moçambique (2017)",
            "path": os.path.join(DATA_DIR, "province_2017_cleaned.gpkg"),
            "type": "province",
            "year": 2017,
            "source": "INE Moçambique"
        }
    }
    
    return available_data

def read_province(
    year: int = 2017,
    code: Optional[Union[str, int]] = None,
    cleaned: bool = True
) -> gpd.GeoDataFrame:
    """
    Lê dados de províncias de Moçambique
    
    Parameters:
    -----------
    year : int, default=2017
        Ano dos dados a serem carregados
    code : str or int, optional
        Código da província específica para carregar
    cleaned : bool, default=True
        Usar dados limpos ou originais
    
    Returns:
    --------
    gpd.GeoDataFrame
        GeoDataFrame com os dados das províncias
    
    Examples:
    ---------
    >>> import geomoz
    >>> # Carregar todas as províncias
    >>> provinces = geomoz.read_province()
    >>> 
    >>> # Carregar província específica
    >>> nampula = geomoz.read_province(code="03")
    >>> 
    >>> # Usar dados originais (não limpos)
    >>> original = geomoz.read_province(cleaned=False)
    """
    
    # Determinar arquivo a usar
    if cleaned:
        file_path = os.path.join(DATA_DIR, f"province_{year}_cleaned.gpkg")
    else:
        file_path = os.path.join(DATA_DIR, f"province_{year}.gpkg")
    
    # Verificar se arquivo existe
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
    
    # Carregar dados
    gdf = gpd.read_file(file_path)
    
    # Filtrar por código se especificado
    if code is not None:
        if isinstance(code, int):
            code = str(code).zfill(2)  # Formatar como 2 dígitos
        
        if "codprov" in gdf.columns:
            gdf = gdf[gdf["codprov"] == code]
        elif "CodProv" in gdf.columns:
            gdf = gdf[gdf["CodProv"] == code]
        else:
            raise ValueError("Coluna de código de província não encontrada")
    
    return gdf.reset_index(drop=True)

def list_provinces() -> gpd.GeoDataFrame:
    """
    Lista todas as províncias disponíveis com seus códigos
    
    Returns:
    --------
    gpd.GeoDataFrame
        DataFrame com código e nome das províncias
    """
    gdf = read_province()
    
    # Selecionar apenas colunas relevantes (lidar com diferentes formatos)
    code_col = "codprov" if "codprov" in gdf.columns else "CodProv"
    name_col = "provincia" if "provincia" in gdf.columns else "Provincia"
    
    # Manter a coluna geometry para garantir GeoDataFrame
    result = gdf[[code_col, name_col, "geometry"]].sort_values(code_col)
    return result
