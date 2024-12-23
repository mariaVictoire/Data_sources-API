from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import sys
from fastapi.responses import JSONResponse
sys.path.append(r"C:\Users\assel\.firebase_config")
from firebase_config import auth
from google.cloud import firestore
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import datetime

load_dotenv()
 
current_tokens = {}
router = APIRouter()

with open(r"C:/Users/assel/.secrets/jwt_secret.txt", "r") as file:
    SECRET_KEY = file.read().strip()
 

ALGORITHM = "HS256"
 
print("Clé secrète chargée avec succès :", SECRET_KEY[:5] + "..." + SECRET_KEY[-5:])
revoked_tokens = set()

db = firestore.Client()
 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class UserRegister(BaseModel):
    email: str
    password: str
    role: str = "user" 
 
class UserLogin(BaseModel):
    email: str
    password: str
 
@router.post("/register")
def register_user(user: UserRegister):
    try:
        user_info = auth.create_user_with_email_and_password(user.email, user.password)
        user_id = user_info['localId']
        db.collection("users").document(user_id).set({"email": user.email, "role": user.role})
 
        return {"message": "Utilisateur enregistré avec succès.", "user_id": user_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur lors de l'enregistrement : {str(e)}")
 
 
from fastapi.responses import RedirectResponse
 
@router.post("/login")
def login_user(user: UserLogin):
    try:
        user_info = auth.sign_in_with_email_and_password(user.email, user.password)
        user_id = user_info['localId']
        doc = db.collection("users").document(user_id).get()
 
        if not doc.exists:
            raise HTTPException(status_code=404, detail="Utilisateur introuvable.")
 
        role = doc.to_dict().get("role")

        expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        token = jwt.encode({"email": user.email, "role": role, "exp": expiration}, SECRET_KEY, algorithm=ALGORITHM)
        global swagger_token
        swagger_token = token
 
        print("Token Swagger injecté :", swagger_token[:5] + "..." + swagger_token[-5:])
        return JSONResponse(
            content={"token": token},
            headers={"Authorization": f"Bearer {token}"}
        )
 
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Erreur de connexion : {str(e)}")
 
 
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        if token.startswith("Bearer "):
            token = token.split(" ")[1] 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("email")
        role = payload.get("role")
        if email is None or role is None:
            raise HTTPException(status_code=401, detail="Token invalide.")
        print("Token décodé avec succès :", payload)
        return {"email": email, "role": role}
 
    except JWTError as e:
        print("Erreur JWT :", str(e))
        raise HTTPException(status_code=401, detail="Token invalide.")


@router.get("/users")
def get_users(user: dict = Depends(verify_token)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Accès interdit. Seuls les admins peuvent voir cette liste.")
 
    try:
        users = db.collection("users").stream()
        user_list = [{"email": u.to_dict().get("email"), "role": u.to_dict().get("role")} for u in users]
        return {"users": user_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des utilisateurs : {str(e)}")