from sqlmodel import Session, select
from .models import Transaction



class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, user_id: int, data) -> Transaction:
        tx = Transaction(user_id=user_id, **data.dict())
        self.db.add(tx)
        self.db.commit()
        self.db.refresh(tx)
        return tx

    def get_by_id(self, user_id: int, tx_id: int) -> Transaction | None:
        return self.db.exec(
            select(Transaction)
            .where(Transaction.id == tx_id)
            .where(Transaction.user_id == user_id)
        ).first()

    def list(self, user_id: int, filters: dict):
        query = select(Transaction).where(Transaction.user_id == user_id)

        if filters.get("type"):
            query = query.where(Transaction.type == filters["type"])

        if filters.get("status"):
            query = query.where(Transaction.status == filters["status"])

        if filters.get("category"):
            query = query.where(Transaction.category == filters["category"])

        return self.db.exec(query).all()

    def update(self, user_id: int, tx_id: int, data):
        tx = self.get_by_id(user_id, tx_id)
        if not tx:
            return None

        for key, value in data.dict(exclude_unset=True).items():
            setattr(tx, key, value)

        self.db.add(tx)
        self.db.commit()
        self.db.refresh(tx)
        return tx

    def delete(self, user_id: int, tx_id: int):
        tx = self.get_by_id(user_id, tx_id)
        if not tx:
            return False

        self.db.delete(tx)
        self.db.commit()
        return True
 