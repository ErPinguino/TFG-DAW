import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal
from Models.user import UserORM

def promote_to_admin():
    username = input("👑 Introduce el nombre de usuario para hacerlo ADMIN: ")
    db = SessionLocal()
    
    try:
        user = db.query(UserORM).filter(UserORM.username == username).first()
        
        if user:
            user.is_admin = True
            db.commit()
            print(f"---")
            print(f"✅ ¡LISTO! El usuario '{username}' ahora es ADMINISTRADOR.")
            print(f"---")
        else:
            print(f"---")
            print(f"❌ ERROR: El usuario '{username}' no existe.")
            print(f"Asegúrate de haberlo registrado primero en el Swagger.")
            print(f"---")
            
    except Exception as e:
        print(f"⚠️ Error inesperado: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    promote_to_admin()