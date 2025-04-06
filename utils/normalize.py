"""
Módulo de normalización
"""
import unicodedata

def remove_accents(text: str) -> str:
    """
    Remover acentos de cadenas de texto
    """
    nfkd = unicodedata.normalize('NFKD', text)
    return ''.join([c for c in nfkd if not unicodedata.combining(c)])