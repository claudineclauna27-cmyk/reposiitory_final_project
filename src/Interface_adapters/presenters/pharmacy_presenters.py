from datetime import datetime, timezone
from src.entities.medicine import Medicine
from typing import Dict, Any, List

class MedicinePresenter:
    @staticmethod
    def to_dict(medicine: Medicine) -> Dict[str, Any]:
        return {
            "id": medicine.id,
            "nom": medicine.nom,
            "prix": medicine.prix,
            "quantite": medicine.quantite,
            "date_expiration": str(medicine.date_expiration) if medicine.date_expiration else None,
            "est_expire": medicine.est_expire()
        }

    @staticmethod
    def to_list(medicines: List[Medicine]) -> List[Dict[str, Any]]:
        return [MedicinePresenter.to_dict(m) for m in medicines]

    @staticmethod
    def to_cli_row(medicine: Medicine) -> str:
        status = "EXPIRÉ" if medicine.est_expire() else "VALIDE"
        return f"{medicine.id:<5} | {medicine.nom:<20} | {medicine.prix:>6.2f} | {medicine.quantite:>3} | {status}"

