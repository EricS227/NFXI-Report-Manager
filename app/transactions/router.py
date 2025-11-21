from fastapi import APIRouter, Depends , HTTPException
from sqlmodel import Session

from app.models import get_db
from app.auth.dependencies import get_current_user

from .service import TransactionService
from .schemas import TransactionCreate, TransactionRead, TransactionUpdate

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.post("/", response_model=TransactionRead)
def create_transaction(
    data: TransactionCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return TransactionService(db).create(user.id, data)


@router.get("/", response_model=list[TransactionRead])
def list_transactions(
    type: str | None = None,
    status: str | None = None,
    category: str | None = None,
    db : Session = Depends(get_db),
    user=Depends(get_current_user)
):
    filters = {"type": type, "status": status, "category": category}
    return TransactionService(db).list(user.id, filters)

@router.get("/{tx_id}", response_model=TransactionRead)
def get_transaction(
    tx_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)

):
    
    tx = TransactionService(db).get(user.id, tx_id)
    if not tx:
        raise HTTPException(404, "Transaction not found")
    return tx
    #return TransactionService(db).get(user.id, tx_id)

@router.put("/{tx_id}", response_model=TransactionRead)
def update_transaction(
    tx_id: int,
    data: TransactionUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return TransactionService(db).update(user.id, tx_id, data)

@router.delete("/{tx_id}")
def delete_transaction(
    tx_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    ok = TransactionService(db).delete(user.id, tx_id)
    if not ok:
        raise HTTPException(404, "Transaction not found")
    return {"deleted": True}
    #return TransactionService(db).delete(user.id, tx_id)