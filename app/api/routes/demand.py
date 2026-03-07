from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.demand import Demand
from app.schemas.demand_schema import DemandCreate
from app.core.security import require_vendor

router = APIRouter(prefix="/demand", tags=["Demand"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_demand(
    demand: DemandCreate,
    current_user = Depends(require_vendor),
    db: Session = Depends(get_db)
):
    new_demand = Demand(
        vendor_id=current_user.id,
        crop_type=demand.crop_type,
        category=demand.category,
        required_quantity=demand.required_quantity,
        offered_price=demand.offered_price,
    )

    db.add(new_demand)
    db.commit()
    db.refresh(new_demand)

    return {"message": "Demand created", "id": str(new_demand.id)}


@router.get("/")
def list_demands(db: Session = Depends(get_db)):
    demands = db.query(Demand).filter(Demand.status == "open").all()

    return [
        {
            "id": str(d.id),
            "crop_type": d.crop_type,
            "category": d.category,
            "required_quantity": d.required_quantity,
            "offered_price": d.offered_price,
            "status": d.status,
        }
        for d in demands
    ]
