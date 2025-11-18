from app.models import engine, Base, SessionLocal
from app.models import User
from werkzeug.security import generate_password_hash

Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    if not db.query(User).filter(User.username == "admin").first():
        user = User(
            username="admin",
            password_hash=generate_password_hash("changeme"),
            role="admin",
            active=True
        )
        db.add(user)
        db.commit()
        print("Admin criado: admin / changeme")
    else:
        print("Admin já existe")
finally:
    db.close()