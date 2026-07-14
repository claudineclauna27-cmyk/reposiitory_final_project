from dataclasses import dataclass
from datetime import date
from typing import Optional
from src.entities.medicine import Medicine

@dataclass
class AddMedicineInput:
    id: int
    nom: str
    prix: float
    quantite: int
    date_expiration: Optional[date] = None

@dataclass
class AddMedicineOutput:
    success: bool
    medicine: Optional[Medicine] = None
    message: Optional[str] = None

class AddMedicineUseCase:
    def __init__(self, medicine_repository):
        self.repo = medicine_repository

    def execute(self, input_data: AddMedicineInput) -> AddMedicineOutput:
        try:
            medicine = Medicine(
                id=input_data.id,
                nom=input_data.nom.strip(),
                prix=input_data.prix,
                quantite=input_data.quantite,
                date_expiration=input_data.date_expiration
            )
            self.repo.save(medicine)
            return AddMedicineOutput(success=True, medicine=medicine)
        except Exception as e:
            return AddMedicineOutput(success=False, message=str(e))
