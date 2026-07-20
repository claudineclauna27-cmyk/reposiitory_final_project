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
        4. Passe l'Output DTO au Presenter pour formatage
        5. Retourne le résultat formaté
=============================================================================
"""

from datetime import date
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

    @staticmethod
    def _parse_date(value) -> Optional[date]:
        """Convertit une chaîne 'YYYY-MM-DD' (ou 'YYYY-M-D') en objet date.
        Retourne None si la valeur est vide/None, et laisse passer un objet
        date déjà valide tel quel."""
        if not value:
            return None
        if isinstance(value, date):
            return value
        try:
            y, m, d = str(value).strip().split("-")
            return date(int(y), int(m), int(d))
        except (ValueError, AttributeError):
            raise ValueError(
                f"Format de date invalide: '{value}'. Utilisez YYYY-MM-DD."
            )

    def add_medicine(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if not data.get("nom"):
            return {"success": False, "error": "nom is required"}

        try:
            parsed_date = self._parse_date(data.get("date_expiration"))
        except ValueError as e:
            return {"success": False, "error": str(e)}

        output = self.add_use_case.execute(
            AddMedicineInput(
                nom=data["nom"],
                prix=data.get("prix", 0.0),
                quantite=data.get("quantite", 0),
                date_expiration=parsed_date,
            )
        )

        if not output.success:
            return {"success": False, "error": output.message}

        return {"success": True, "medicine": MedicinePresenter.to_dict(output.medicine)}

    def update_medicine(self, medicine_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            parsed_date = self._parse_date(data.get("date_expiration"))
        except ValueError as e:
            return {"success": False, "error": str(e)}

        output = self.update_use_case.execute(
            UpdateMedicineInput(
                id=int(medicine_id),
                nom=data.get("nom"),
                prix=data.get("prix"),
                quantite=data.get("quantite"),
                date_expiration=parsed_date,
            )
        )
        if not output.success:
            return {"success": False, "error": output.message}
        return {"success": True, "medicine": MedicinePresenter.to_dict(output.medicament)}

    def delete_medicine(self, medicine_id: str) -> Dict[str, Any]:
        output = self.delete_use_case.execute(DeleteMedicineInput(id=int(medicine_id)))
        return {"success": output.success, "message": output.message}