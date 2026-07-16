import psycopg2
from src.entities.medicine import Medicine
from src.uscases.interfaces.medicine_repo import IMedicineRepository 

class PostgresMedicineRepository(IMedicineRepository):
    def __init__(self, dbname, user, password, host="localhost", port="5432"):
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS medicament (
            id SERIAL PRIMARY KEY,
            nom VARCHAR(100),
            prix FLOAT,
            quantite INT,
            date_expiration DATE
        )
        """)
        self.conn.commit()

    def add(self, medicine: Medicine):
        self.cursor.execute("""
        INSERT INTO medicament (nom, prix, quantite, date_expiration)
        VALUES (%s, %s, %s, %s)
        """, (medicine.nom, medicine.prix, medicine.quantite, medicine.date_expiration))
        self.conn.commit()

    def update(self, medicine: Medicine):
        self.cursor.execute("""
        UPDATE medicament SET nom=%s, prix=%s, quantite=%s, date_expiration=%s
        WHERE id=%s
        """, (medicine.nom, medicine.prix, medicine.quantite, medicine.date_expiration, medicine.id))
        self.conn.commit()

    def delete(self, medicine_id: int):
        self.cursor.execute("DELETE FROM medicament WHERE id=%s", (medicine_id,))
        self.conn.commit()

    def get_by_id(self, medicine_id: int) -> Medicine:
        self.cursor.execute("SELECT id, nom, prix, quantite, date_expiration FROM medicament WHERE id=%s", (medicine_id,))
        row = self.cursor.fetchone()
        if row:
            return Medicine(*row)
        return None

    def get_all(self) -> list[Medicine]:
        self.cursor.execute("SELECT id, nom, prix, quantite, date_expiration FROM medicament")
        rows = self.cursor.fetchall()
        return [Medicine(*row) for row in rows]
