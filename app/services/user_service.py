from werkzeug.security import generate_password_hash
from app.repositories.user_repository import UserRepository

class UserService:

    def __init__(self, db):
        self.repo = UserRepository(db)

    def list_users(self):
        return self.repo.get_all()
    
    def create_user(self, username, password, role):
        if self.repo.get_by_username(username):
            return None, "Usuário já existe"
        
        pw_hash = generate_password_hash(password)
        user = self.repo.create(username, pw_hash, role)
        return user, None
    
    def update_user(self, user_id, data):
        user = self.repo.get_by_id(user_id)
        if not user:
            return None, "Usuário não encontrado"
        
        if "password" in data:
            data["password_hash"] = generate_password_hash(data["password"])
            del data["password"]
        
        updated_user = self.repo.update(user, data)
        return updated_user, None


    def delete_user(self, user_id):
        user = self.repo.get_by_id(user_id)
        if not user:
            return "Usuário não encontrado"
        self.repo.delete(user)
        return None