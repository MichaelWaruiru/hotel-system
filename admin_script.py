from app import app
from models import db, User
from werkzeug.security import generate_password_hash

def create_admin():
  with app.app_context():
    admin = User(username="admin", password_hash=generate_password_hash("Xadmin2025"))
    db.session.add(admin)
    db.session.commit()
    print("Admin user created!")
    
if __name__ == "__main__":
  create_admin()