from src.uscases.add_medicine import AddMedicineInput, AddMedicineUseCase  
from src.uscases.delete_medicine import DeleteMedicineInput, DeleteMedicineUseCase
from src.uscases.update_medicine import UpdateMedicineInput, UpdateMedicineUseCase
from src.uscases.interfaces.medicine_repo import IMedicineRepository
from src.Interface_adapters.presenters.pharmacy_presenters import MedicinePresenter

"""
=============================================================================
LAYER 3: INTERFACE ADAPTERS — Controller
=============================================================================

What does a Controller do?
    A Controller sits between a delivery mechanism (HTTP, CLI, API) and
    the use cases. It:
        1. Reçoit les données brutes (JSON, CLI args)
        2. Les valide et les convertit en Input DTO
        3. Appelle le bon Use Case
        4. Passe l’Output DTO au Presenter pour formatage
        5. Retourne le résultat formaté
=============================================================================
"""

from typing import Any, Dict, Optional
from src.uscases.add_medicine import AddMedicineInput, AddMedicineUseCase
from src.uscases.update_medicine import UpdateMedicineInput, UpdateMedicineUseCase
from src.uscases.delete_medicine import DeleteMedicineInput, DeleteMedicineUseCase
from src.Interface_adapters.presenters.pharmacy_presenters import MedicinePresenter
from src.uscases.interfaces.medicine_repo import IMedicineRepository


class MedicineController:
    """
    Orchestrates use cases for medicine-related actions.
    """

    def __init__(self, repository: IMedicineRepository) -> None:
        self.add_use_case = AddMedicineUseCase(repository)
        self.update_use_case = UpdateMedicineUseCase(repository)
        self.delete_use_case = DeleteMedicineUseCase(repository)
        
    def add_medicine(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if not data.get("nom"):
            return {"success": False, "error": "nom is required"}

        output = self.add_use_case.execute(
            AddMedicineInput(
                nom=data["nom"],
                prix=data.get("prix", 0.0),
                quantite=data.get("quantite", 0),
                date_expiration=data.get("date_expiration")
            )
        )
        return {"success": True, "medicine": MedicinePresenter.to_dict(output.medicine)}

   

    def update_medicine(self, medicine_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        output = self.update_use_case.execute(
            UpdateMedicineInput(
                medicine_id=medicine_id,
                nom=data.get("nom"),
                prix=data.get("prix"),
                quantite=data.get("quantite"),
                date_expiration=data.get("date_expiration"),
            )
        )
        if not output.success:
            return {"success": False, "error": output.message}
        return {"success": True, "medicine": MedicinePresenter.to_dict(output.medicine)}

    def delete_medicine(self, medicine_id: str) -> Dict[str, Any]:
        output = self.delete_use_case.execute(DeleteMedicineInput(medicine_id=medicine_id))
        return {"success": output.deleted, "message": output.message}
