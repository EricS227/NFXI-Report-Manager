from werkzeug.security import generate_password_hash, check_password_hash
from app.repositories.user_repository import UserRepository
import jwt
from datetime import datetime, timedelta
from app.config import Config

class AuthService:
    def __init__(self, db):
        self.repo = UserRepository(db)
    
    def authenticate(self, username, password):
        user = self.repo.get_by_username(username)
        if not user or not user.active:
            return None
        if check_password_hash(user.password_hash, password):
            return user
        return None

    def __generate_jwt(self, user):
        payload = {
            "sub": user.id,
            "username": user.username,
            "role": user.role,
            "exp": datetime.utcnow() + timedelta(seconds=Config.JWT_EXPIRATION)
        }
        return jwt.encode(payload, Config.SECRET_KEY, algorithm ="HS256")
    
    def create_user(self, username, password, role="financeiro"):
        pw_hash = generate_password_hash(password)
        return self.repo.create(username=username, password_hash=pw_hash, role=role)