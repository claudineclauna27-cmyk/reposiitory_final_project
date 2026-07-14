from abc import ABC, abstractmethod
from typing import Optional, List
from src.entities.medicine import Medicine

class IMedicineRepository(ABC):
    """Interface abstraite pour gérer les médicaments."""

    @abstractmethod
    def add(self, medicine: Medicine) -> None:
        """Ajoute un nouveau médicament."""
        pass

    @abstractmethod
    def get_by_id(self, medic_id: int) -> Optional[Medicine]:
        """Récupère un médicament par son identifiant."""
        pass

    @abstractmethod
    def update(self, medicine: Medicine) -> None:
        """Met à jour un médicament existant."""
        pass

    @abstractmethod
    def delete(self, medicine_id: int) -> None:
        """Supprime un médicament par son identifiant."""
        pass

    @abstractmethod
    def list_all(self) -> List[Medicine]:
        """Retourne la liste de tous les médicaments."""
        pass
