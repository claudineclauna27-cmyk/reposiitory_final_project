from dataclasses import dataclass
from typing import Optional
from src.entities.medicine import Medicine

@dataclass
class DeleteMedicineInput:
    id: int

@dataclass
class DeleteMedicineOutput:
    success: bool
    message: Optional[str] = None

class DeleteMedicineUseCase:
    def __init__(self, medicine_repository):
        self.repo = medicine_repository

    def execute(self, input_data: DeleteMedicineInput) -> DeleteMedicineOutput:
        medicament = self.repo.get_by_id(input_data.id)
        if medicament is None:
            return DeleteMedicineOutput(success=False, message="Médicament introuvable")
        self.repo.delete(input_data.id)
        return DeleteMedicineOutput(success=True, message="Médicament supprimé avec succès")
