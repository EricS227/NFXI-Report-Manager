from app.models import User
from sqlalchemy.orm import Session


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(User).all()
    
    def get_by_username(self, username: str):
        return self.db.query(User).filter(User.username == username).first()
    
    def get_by_id(self, user_id: int):
        return self.db.query(User).get(user_id)
    
    
    def create(self, username: str, password_hash: str, role: str = "financeiro"):
        user = User(username=username, password_hash=password_hash, role=role, active=True)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user, data: dict):
        for key, value in data.items():
            setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def delete(self, user):
        self.db.delete(user)
        self.db.commit()