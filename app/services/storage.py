"""
Capa de almacenamiento en memoria (Sprint 1)
"""
from typing import Optional
from app.models import Release


class InMemoryStorage:
    """Almacenamiento simple en memoria"""
    
    def __init__(self):
        self._releases: dict[str, Release] = {}
    
    def save_release(self, release: Release) -> Release:
        """
        Guarda un release
        
        Args:
            release: Release a guardar
        
        Returns:
            El release guardado
        """
        self._releases[release.version] = release
        return release
    
    def get_release(self, version: str) -> Optional[Release]:
        """
        Obtiene un release por versión
        
        Args:
            version: Versión del release
        
        Returns:
            Release si existe, None si no
        """
        return self._releases.get(version)
    
    def list_releases(self) -> list[Release]:
        """
        Lista todos los releases
        
        Returns:
            Lista de releases ordenados por timestamp (más reciente primero)
        """
        releases = list(self._releases.values())
        releases.sort(key=lambda r: r.timestamp, reverse=True)
        return releases
    
    def delete_release(self, version: str) -> bool:
        """
        Elimina un release
        
        Args:
            version: Versión del release
        
        Returns:
            True si se eliminó, False si no existía
        """
        if version in self._releases:
            del self._releases[version]
            return True
        return False
    
    def clear(self):
        """Limpia todos los releases (útil para tests)"""
        self._releases.clear()


# Instancia global (singleton simple para Sprint 1)
storage = InMemoryStorage()