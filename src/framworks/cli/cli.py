"""
=============================================================================
LAYER 4: FRAMEWORKS & DRIVERS — Command-Line Interface
=============================================================================

CLI simplifié pour gérer les médicaments avec Clean Architecture.
Use cases inclus : ajouter, modifier, supprimer.
=============================================================================
"""

from src.Interface_adapters.controller.pharmacy_controller import MedicineController
from src.Interface_adapters.repositories.in_memory_pharmacy_repository import MedicineRepositoryInMemory

# ANSI couleurs
class _C:
    RESET  = "\033[0m"
    BOLD   = "\033[1m"
    GREEN  = "\033[32m"
    RED    = "\033[31m"
    CYAN   = "\033[36m"

def _banner(text: str) -> None:
    print(f"\n{_C.BOLD}{_C.CYAN}{'=' * 50}{_C.RESET}")
    print(f"{_C.BOLD}{_C.CYAN}  {text}{_C.RESET}")
    print(f"{_C.BOLD}{_C.CYAN}{'=' * 50}{_C.RESET}\n")

def _ok(msg: str) -> None:
    print(f"{_C.GREEN}  ✓  {msg}{_C.RESET}")

def _err(msg: str) -> None:
    print(f"{_C.RED}  ✗  {msg}{_C.RESET}")

def run_cli() -> None:
    """
    Point d’entrée du CLI interactif.
    """
    repository = MedicineRepositoryInMemory()
    controller = MedicineController(repository)

    _banner("Pharmacy CLI — Ajouter / Modifier / Supprimer")
    print("  Commands: add | update | delete | quit\n")

    while True:
        try:
            cmd = input(f"{_C.BOLD}> {_C.RESET}").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print("\nBye!")
            break

        if cmd in ("quit", "exit", "q"):
            print("Bye!")
            break

        elif cmd == "add":
            nom = input("  Nom          : ").strip()
            prix = float(input("  Prix         : ").strip())
            quantite = int(input("  Quantité     : ").strip())
            date_expiration = input("  Date exp (YYYY-MM-DD): ").strip()
            result = controller.add_medicine({
                "nom": nom,
                "prix": prix,
                "quantite": quantite,
                "date_expiration": date_expiration
            })
            if result["success"]:
                _ok(f"Ajouté: {result['medicine']['nom']}")
            else:
                _err(result["error"])

        elif cmd == "update":
            med_id = input("  Medicine ID: ").strip()
            nom = input("  Nouveau nom (laisser vide pour garder): ").strip() or None
            prix = input("  Nouveau prix: ").strip() or None
            quantite = input("  Nouvelle quantité: ").strip() or None
            date_expiration = input("  Nouvelle date exp: ").strip() or None
            result = controller.update_medicine(med_id, {
                "nom": nom,
                "prix": float(prix) if prix else None,
                "quantite": int(quantite) if quantite else None,
                "date_expiration": date_expiration
            })
            if result["success"]:
                _ok(f"Modifié: {result['medicine']['nom']}")
            else:
                _err(result["error"])

        elif cmd == "delete":
            med_id = input("  Medicine ID: ").strip()
            result = controller.delete_medicine(med_id)
            if result["success"]:
                _ok(result["message"])
            else:
                _err(result["message"])

        else:
            print(f"  Unknown command: '{cmd}'")
            print("  Commands: add | update | delete | quit")
