from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.transaction import Transaction
from app.models.harvest import Harvest
from app.core.security import require_vendor

router = APIRouter(prefix="/transactions", tags=["Transactions"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/{harvest_id}")
def create_transaction(
    harvest_id: str,
    current_user = Depends(require_vendor),
    db: Session = Depends(get_db)
):
    harvest = db.query(Harvest).filter(Harvest.id == harvest_id).first()

    if not harvest:
        raise HTTPException(status_code=404, detail="Harvest not found")

    if harvest.status != "available":
        raise HTTPException(status_code=400, detail="Harvest not available")

    transaction = Transaction(
        harvest_id=harvest.id,
        vendor_id=current_user.id,
    )

    harvest.status = "sold"

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    return {"message": "Transaction created", "id": str(transaction.id)}
