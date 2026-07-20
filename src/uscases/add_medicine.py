import time
from dataclasses import dataclass
from datetime import date
from typing import Optional
from src.entities.medicine import Medicine


@dataclass
class AddMedicineInput:
    nom: str
    prix: float
    quantite: int
    id: Optional[int] = None
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
            # Génère un id si aucun n'est fourni (au lieu de crasher sur input_data.id inexistant)
            medicine_id = (
                input_data.id if input_data.id is not None else int(time.time() * 1000)
            )

            medicine = Medicine(
                id=medicine_id,
                nom=input_data.nom.strip(),
                prix=input_data.prix,
                quantite=input_data.quantite,
                date_expiration=input_data.date_expiration,
            )

            # Le repository (in-memory et postgres) expose "add", pas "save"
            self.repo.add(medicine)

            return AddMedicineOutput(success=True, medicine=medicine)
        except Exception as e:
            return AddMedicineOutput(success=False, message=str(e))