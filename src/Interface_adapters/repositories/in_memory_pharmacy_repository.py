import copy
from typing import Optional, List
from src.entities.medicine import Medicine
from uscases.interfaces.medicine_repo import IMedicineRepository

class MedicineRepositoryInMemory(IMedicineRepository):
    def __init__(self):
        # dict : clé = id, valeur = Medicine
        self._storage: dict[int, Medicine] = {}

    def add(self, medicine: Medicine) -> None:
        if medicine.id in self._storage:
            raise ValueError("Un médicament avec cet ID existe déjà.")
        self._storage[medicine.id] = copy.deepcopy(medicine)

    def get_by_id(self, medicine_id: int) -> Optional[Medicine]:
        medicament = self._storage.get(medicine_id)
        return copy.deepcopy(medicament) if medicament else None

    def update(self, medicine: Medicine) -> None:
        if medicine.id not in self._storage:
            raise ValueError("Médicament introuvable pour mise à jour.")
        self._storage[medicine.id] = copy.deepcopy(medicine)

    def delete(self, medicine_id: int) -> None:
        if medicine_id not in self._storage:
            raise ValueError("Médicament introuvable pour suppression.")
        del self._storage[medicine_id]

    def list_all(self) -> List[Medicine]:
        return [copy.deepcopy(m) for m in self._storage.values()]
