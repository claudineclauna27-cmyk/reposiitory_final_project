# 💊 Pharmacy Management System

Système de gestion de pharmacie développé en **Python** en suivant les principes de la **Clean Architecture** (Architecture Propre). Le projet permet de gérer un inventaire de médicaments (ajout, modification, suppression, consultation) via deux interfaces : une **CLI** interactive et une **API REST** (FastAPI).

---

## 📐 Architecture

Le projet est organisé en couches concentriques indépendantes, conformément à la Clean Architecture de Robert C. Martin :

```
┌─────────────────────────────────────────────────────────┐
│  LAYER 4 : Frameworks & Drivers                          │
│  (cli.py, fast_Api.py)                                   │
│  ┌───────────────────────────────────────────────────┐  │
│  │  LAYER 3 : Interface Adapters                      │  │
│  │  (Controller, Presenter, Repositories concrets)    │  │
│  │  ┌───────────────────────────────────────────────┐│  │
│  │  │  LAYER 2 : Use Cases                           ││  │
│  │  │  (Add / Update / Delete Medicine)              ││  │
│  │  │  ┌─────────────────────────────────────────┐  ││  │
│  │  │  │  LAYER 1 : Entities                      │  ││  │
│  │  │  │  (Medicine)                               │  ││  │
│  │  │  └─────────────────────────────────────────┘  ││  │
│  │  └───────────────────────────────────────────────┘│  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

La règle de dépendance est respectée : les couches internes (Entities, Use Cases) ne connaissent rien des couches externes (Frameworks, DB, API). La communication avec la persistance passe par une **interface abstraite** (`IMedicineRepository`), ce qui permet d'échanger l'implémentation (mémoire ↔ PostgreSQL) sans toucher à la logique métier.

---

## 📁 Structure du projet

```
src/
├── entities/
│   └── medicine.py                     # Entité métier Medicine
│
├── uscases/
│   ├── add_medicine.py                 # Use case : ajout
│   ├── update_medicine.py              # Use case : modification
│   ├── delete_medicine.py              # Use case : suppression
│   └── interfaces/
│       └── medicine_repo.py            # Interface abstraite du repository
│
├── Interface_adapters/
│   ├── controller/
│   │   └── pharmacy_controller.py      # Orchestration des use cases
│   ├── presenters/
│   │   └── pharmacy_presenters.py      # Formatage des données de sortie
│   └── repositories/
│       ├── in_memory_pharmacy_repository.py
│       └── postgresql_pharmacy_repo.py
│
├── fast_Api.py                         # Point d'entrée API REST
└── cli.py                              # Point d'entrée CLI interactif
```

---

## 🧩 Description des composants

### 1. Entities

**`Medicine`** — Entité métier centrale, implémentée en `dataclass` :
- Champs : `id`, `nom`, `prix`, `quantite`, `date_expiration`
- Validation automatique à la création (`__post_init__`) : nom non vide, prix et quantité non négatifs
- Méthode `est_expire()` pour vérifier si le médicament est périmé

### 2. Use Cases

| Use Case | Rôle |
|---|---|
| `AddMedicineUseCase` | Crée un nouveau médicament (génère un ID si non fourni) et l'ajoute au repository |
| `UpdateMedicineUseCase` | Met à jour uniquement les champs fournis d'un médicament existant |
| `DeleteMedicineUseCase` | Supprime un médicament après vérification de son existence |

Chaque use case fonctionne avec des DTO d'entrée/sortie (`*Input` / `*Output`) et reste indépendant du mode de persistance grâce à l'injection du repository.

### 3. Interface du Repository

**`IMedicineRepository`** (ABC) définit le contrat que toute implémentation de persistance doit respecter :
- `add`, `get_by_id`, `update`, `delete`, `list_all`

Deux implémentations sont fournies :
- **`MedicineRepositoryInMemory`** : stockage en dictionnaire, utile pour les tests et la CLI
- **`PostgresMedicineRepository`** : persistance réelle via PostgreSQL (`psycopg2`)

### 4. Presenter

**`MedicinePresenter`** formate les entités `Medicine` pour l'affichage :
- `to_dict` / `to_list` : format JSON pour l'API
- `to_cli_row` : format lisible pour la CLI

### 5. Controller

**`MedicineController`** fait le lien entre les mécanismes de livraison (CLI, API) et les use cases :
- Valide et convertit les données brutes en DTO
- Gère le parsing des dates (`YYYY-MM-DD`)
- Appelle le use case approprié et renvoie un résultat formaté

### 6. Frameworks & Drivers

- **`fast_Api.py`** : expose une API REST avec FastAPI (`GET /health`, `POST /medicines`, `PUT /medicines/{id}`, `DELETE /medicines/{id}`), connectée à PostgreSQL
- **`cli.py`** : interface en ligne de commande interactive avec les commandes `add`, `update`, `delete`, `list`, `quit`

---

## ⚙️ Prérequis

- Python 3.10+
- PostgreSQL (pour l'utilisation avec `PostgresMedicineRepository` / l'API)

### Dépendances

```
fastapi
uvicorn
pydantic
psycopg2
```

Installation :

```bash
pip install fastapi uvicorn pydantic psycopg2-binary
```

---

## 🚀 Utilisation

### Lancer la CLI (stockage en mémoire)

```bash
python -m src.cli
```

Commandes disponibles : `add`, `update`, `delete`, `list`, `quit`

### Lancer l'API REST (PostgreSQL)

Configurer les variables d'environnement :

```bash
export DB_NAME=my_database
export DB_USER=postgres
export DB_PASSWORD=your_password
export DB_HOST=localhost
export DB_PORT=5432
```

Démarrer le serveur :

```bash
uvicorn src.fast_Api:create_app --factory --reload
```

#### Endpoints disponibles

| Méthode | Route | Description |
|---|---|---|
| `GET` | `/health` | Vérifie que l'API fonctionne |
| `POST` | `/medicines` | Ajoute un médicament |
| `PUT` | `/medicines/{id}` | Modifie un médicament |
| `DELETE` | `/medicines/{id}` | Supprime un médicament |

**Exemple de requête d'ajout :**

```json
POST /medicines
{
  "nom": "Paracétamol",
  "prix": 4.5,
  "quantite": 100,
  "date_expiration": "2027-01-01"
}
```

---

## ✅ Points forts de l'architecture

- **Découplage total** entre logique métier et infrastructure (DB, framework web)
- **Testabilité** : le repository en mémoire permet de tester les use cases sans base de données
- **Extensibilité** : ajouter une nouvelle interface (ex. GUI) ou un nouveau type de stockage ne nécessite pas de modifier les use cases
- **Validation centralisée** au niveau de l'entité `Medicine`

## 🔧 Améliorations possibles

- Ajouter un use case `ListMedicines` / `GetMedicine` dédié (actuellement géré directement via le repository dans la CLI)
- Compléter `PostgresMedicineRepository.list_all()` (actuellement délègue à `super().list_all()`, qui est abstraite)
- Ajouter des tests unitaires pour chaque use case et repository
- Gérer un pool de connexions PostgreSQL plutôt qu'une connexion unique
