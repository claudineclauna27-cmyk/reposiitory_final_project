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
    RESET = "\033[0m"
    BOLD = "\033[1m"
    GREEN = "\033[32m"
    RED = "\033[31m"
    CYAN = "\033[36m"


def _banner(text: str) -> None:
    print(f"\n{_C.BOLD}{_C.CYAN}{'=' * 50}{_C.RESET}")
    print(f"{_C.BOLD}{_C.CYAN}  {text}{_C.RESET}")
    print(f"{_C.BOLD}{_C.CYAN}{'=' * 50}{_C.RESET}\n")


def _ok(msg: str) -> None:
    print(f"{_C.GREEN}  ✓  {msg}{_C.RESET}")


def _err(msg: str) -> None:
    print(f"{_C.RED}  ✗  {msg}{_C.RESET}")


def _read_float(prompt: str, required: bool = True):
    raw = input(prompt).strip()
    if not raw:
        return None if not required else 0.0
    try:
        return float(raw)
    except ValueError:
        _err(f"Valeur numérique invalide: '{raw}'")
        return None


def _read_int(prompt: str, required: bool = True):
    raw = input(prompt).strip()
    if not raw:
        return None if not required else 0
    try:
        return int(raw)
    except ValueError:
        _err(f"Valeur entière invalide: '{raw}'")
        return None


def run_cli() -> None:
    """
    Point d'entrée du CLI interactif.
    """
    repository = MedicineRepositoryInMemory()
    controller = MedicineController(repository)

    _banner("Pharmacy CLI — Ajouter / Modifier / Supprimer")
    print("  Commands: add | update | delete | list | quit\n")

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
            if not nom:
                _err("Le nom est requis.")
                continue

            prix = _read_float("  Prix         : ")
            if prix is None:
                continue

            quantite = _read_int("  Quantité     : ")
            if quantite is None:
                continue

            date_expiration = input("  Date exp (YYYY-MM-DD, vide = aucune): ").strip() or None

            result = controller.add_medicine({
                "nom": nom,
                "prix": prix,
                "quantite": quantite,
                "date_expiration": date_expiration,
            })

            if result["success"]:
                _ok(f"Ajouté: {result['medicine']['nom']}")
            else:
                _err(result["error"])

        elif cmd == "update":
            med_id = input("  Medicine ID: ").strip()
            if not med_id.isdigit():
                _err("L'ID doit être un nombre.")
                continue

            nom = input("  Nouveau nom (laisser vide pour garder): ").strip() or None
            prix_raw = input("  Nouveau prix (laisser vide pour garder): ").strip()
            quantite_raw = input("  Nouvelle quantité (laisser vide pour garder): ").strip()
            date_expiration = input("  Nouvelle date exp (YYYY-MM-DD, laisser vide pour garder): ").strip() or None

            try:
                prix = float(prix_raw) if prix_raw else None
            except ValueError:
                _err(f"Prix invalide: '{prix_raw}'")
                continue

            try:
                quantite = int(quantite_raw) if quantite_raw else None
            except ValueError:
                _err(f"Quantité invalide: '{quantite_raw}'")
                continue

            result = controller.update_medicine(med_id, {
                "nom": nom,
                "prix": prix,
                "quantite": quantite,
                "date_expiration": date_expiration,
            })

            if result["success"]:
                _ok(f"Modifié: {result['medicine']['nom']}")
            else:
                _err(result["error"])

        elif cmd == "delete":
            med_id = input("  Medicine ID: ").strip()
            if not med_id.isdigit():
                _err("L'ID doit être un nombre.")
                continue

            result = controller.delete_medicine(med_id)
            if result["success"]:
                _ok(result["message"])
            else:
                _err(result["message"])

        elif cmd == "list":
            medicines = repository.list_all()
            if not medicines:
                print("  Aucun médicament enregistré.")
            else:
                from src.Interface_adapters.presenters.pharmacy_presenters import MedicinePresenter
                for m in medicines:
                    print(f"  [{m.id}] {MedicinePresenter.to_cli_row(m)}")

        else:
            print(f"  Unknown command: '{cmd}'")
            print("  Commands: add | update | delete | list | quit")