from sqlmodel import Session
from fastapi import HTTPException

from .schemas import TransactionCreate, TransactionUpdate
from .repository import TransactionRepository


class TransactionService:
    def __init__(self, db: Session):
        self.repo = TransactionRepository(db)

    def create(self, user_id: int, data: TransactionCreate):
        return self.repo.create(user_id, data)

    def list(self, user_id: int, filters: dict):
        return self.repo.list(user_id, filters)

    def get(self, user_id: int, tx_id: int):
        tx = self.repo.get_by_id(user_id, tx_id)
        if not tx:
            raise HTTPException(404, "Transação não encontrada")
        return tx

    def update(self, user_id: int, tx_id: int, data: TransactionUpdate):
        tx = self.get(user_id, tx_id)
        return self.repo.update(user_id, tx_id, data)

    def delete(self, user_id: int, tx_id: int):
        tx = self.get(user_id, tx_id)
        self.repo.delete(user_id, tx_id)
        return {"detail": "Transação deletada com sucesso"}
