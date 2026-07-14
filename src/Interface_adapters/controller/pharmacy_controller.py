from uscases.add_medicine import AddMedicineInput, AddMedicineUseCase  
from src.uscases.delete_medicine import DeleteMedicineInput, DeleteMedicineUseCase
from src.uscases.update_medicine import updateMedicineInput, UpdateMedicineUseCase
from src.uscases.interfaces.medicine_repo import IMedicineRepository

class MedicamentController:
    def __init__(self, repo: IMedicineRepository):
        self.repo = repo

    def ajouter(self, id: int, nom: str, prix: float, quantite: int, date_expiration=None):
        input_data = AddMedicineInput(id=id, nom=nom, prix=prix, quantite=quantite, date_expiration=date_expiration)
        use_case = AddMedicineUseCase(self.repo)
        return use_case.execute(input_data)

    def supprimer(self, id: int):
        input_data = DeleteMedicineInput(id=id)
        use_case = DeleteMedicineUseCase(self.repo)
        return use_case.execute(input_data)

    def modifier(self, id: int, nom: str, prix: float, quantite: int, date_expiration=None):
        input_data = DeleteMedicineInput(id=id, nom=nom, prix=prix, quantite=quantite, date_expiration=date_expiration)
        use_case = DeleteMedicineUseCase(self.repo)
        return use_case.execute(input_data)
