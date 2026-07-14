from dataclasses import dataclass
from datetime import date
from typing import Optional
from src.entities.medicine import Medicine

@dataclass
class UpdateMedicineInput:
    id: int
    nom: str
    prix: float
    quantite: int
    date_expiration: Optional[date] = None

@dataclass
class UpdateMedicineOutput:
    success: bool
    medicament: Optional[Medicine] = None
    message: Optional[str] = None

class UpdateMedicineUseCase:
    def __init__(self, medicament_repository):
        self.repo = medicament_repository

    def execute(self, input_data: UpdateMedicineInput) -> UpdateMedicineOutput:
        medicament = self.repo.get_by_id(input_data.id)
        if medicament is None:
            return UpdateMedicineOutput(success=False, message="Médicament introuvable")

        try:
            medicament.nom = input_data.nom.strip()
            medicament.prix = input_data.prix
            medicament.quantite = input_data.quantite
            medicament.date_expiration = input_data.date_expiration

            self.repo.update(medicament)
            return UpdateMedicineOutput(success=True, medicament=medicament)
        except Exception as e:
            return UpdateMedicineOutput(success=False, message=str(e))
