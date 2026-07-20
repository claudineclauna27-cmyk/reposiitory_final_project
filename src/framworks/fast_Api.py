from fastapi import FastAPI, HTTPException, Request
from src.Interface_adapters.controller.pharmacy_controller import MedicineController
from src.Interface_adapters.repositories.postgresql_pharmacy_repo import PostgresMedicineRepository

def create_app(repository=None) -> FastAPI:
 
    app = FastAPI(title="Pharmacy Management API")

    # ------------------------------------------------------------------
    # Dependency Injection — wiring point
    # ------------------------------------------------------------------
    if repository is None:
        repository = PostgresMedicineRepository(
            dbname="my_database",
            user="postgres",
            password="40501522S",
            host="localhost",
            port="5432"
        )

    controller = MedicineController(repository)
    # ------------------------------------------------------------------

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.post("/medicines")
    async def create_medicine(request: Request):
        data = await request.json()
        result = controller.add_medicine(data)
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["error"])
        return result

    @app.put("/medicines/{medicine_id}")
    async def update_medicine(medicine_id: int, request: Request):
        data = await request.json()
        result = controller.update_medicine(medicine_id, data)
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["error"])
        return result

    @app.delete("/medicines/{medicine_id}")
    def delete_medicine(medicine_id: int):
        return controller.delete_medicine(medicine_id)

    return app

