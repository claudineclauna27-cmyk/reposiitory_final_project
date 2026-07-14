from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class Medicine:
    id: int
    nom: str
    prix: float
    quantite: int
    date_expiration: Optional[date] = None

    def __post_init__(self):
        if not self.nom or self.nom.strip() == "":
            raise ValueError("Le nom du médicament ne peut pas être vide ou composé uniquement d'espaces.")
        if self.prix < 0:
            raise ValueError("Le prix du médicament ne peut pas être négatif.")
        if self.quantite < 0:
            raise ValueError("La quantité du médicament ne peut pas être négative.")

    def est_expire(self) -> bool:
        if self.date_expiration is None:
            return False
        return self.date_expiration < date.today()
