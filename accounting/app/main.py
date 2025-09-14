from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone
from . import db
from bson.objectid import ObjectId

app = FastAPI(title="Accounting Service", version="1.0")

DEFAULT_BASE_SALARY = 50_000
INCREMENT_PER_YEAR = 1500

class SalaryResponse(BaseModel):
    employee_id: int
    base_salary: float
    years: int
    computed_salary: float
    breakdown: dict
    source: str

@app.get("/health", tags=['Проверка'])
async def health():
    return {"status": "ok"}


@app.get("/salary/{employee_id}", response_model=SalaryResponse,
         tags=["Зарплата"], summary="Узнать зарплату сотрудника")
async def get_salary(employee_id: int, years: Optional[int] = Query(None, ge=0)):
    """
        Вернуть расчет зарплаты для сотрудника:
        - если в Mongo есть запись с base_salary, используем её,
          иначе берем DEFAULT_BASE_SALARY
        - years: количество полных лет стажа (если передан — используется; иначе считаем как 0)
        """
    coll = db.db.salaries
    # ищем ао employee_id
    doc = await coll.find_one({"employee_id":employee_id})
    if doc:
        base = float(doc.get("base_salary", DEFAULT_BASE_SALARY))
        source = "mongo"
    else:
        base = float(DEFAULT_BASE_SALARY)
        source = "default"

    yrs = int(years) if years is not None else 0

    computed = base + INCREMENT_PER_YEAR * yrs

    breakdown = {"base_salary": base,
                 "years": yrs,
                 "increment_per_year": INCREMENT_PER_YEAR,
                 "years_increment": INCREMENT_PER_YEAR * yrs}

    return SalaryResponse(employee_id=employee_id,
                          base_salary=base,
                          years=yrs,
                          computed_salary=round(computed, 2),
                          breakdown=breakdown,
                          source=source)

@app.post("/salary/{employee_id}/set", tags=["Зарплата"], summary="Изменить зарплату сотрудника")
async def set_base_salary(employee_id: int, base_salary: float):
    """Установить/обновить базовую ставку для сотрудника (запись в Mongo)"""

    coll = db.db.salaries
    now = datetime.now(timezone.utc)
    result = await coll.update_one({"employee_id": employee_id},
                                   {"$set": {"base_salary": float(base_salary), "updated_at": now}},
                                   upsert=True)
    return {"ok": result.acknowledged, "employee_id": employee_id, "base_salary": float(base_salary),
            "matched_count": result.matched_count, "modified_count":result.modified_count,
            "upserted_id": str(result.upserted_id) if result.upserted_id else None}


