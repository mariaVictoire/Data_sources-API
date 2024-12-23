from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from google.cloud import firestore
import google.auth
 
router = APIRouter()

class ParametersModel(BaseModel):
    n_estimators: int
    criterion: str | int | float
 
class FirestoreClient:
    """Wrapper autour de Firestore."""
 
    def __init__(self):
        """Initialise la connexion à Firestore."""
        # Vérifie les identifiants par défaut
        credentials, _ = google.auth.default()
        self.client = firestore.Client(credentials=credentials)
 
    def get_document(self, collection_name: str, document_id: str) -> dict:
        """Récupère un document spécifique depuis Firestore."""
        try:
            doc_ref = self.client.collection(collection_name).document(document_id)
            doc = doc_ref.get()
 
            if doc.exists:
                return doc.to_dict()
            else:
                raise ValueError(f"Aucun document trouvé avec l'ID : {document_id}")
 
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération des données : {str(e)}")
       
    def create_or_update_document(self, collection_name: str, document_id: str, data: dict) -> None:
        """Crée ou met à jour un document Firestore."""
        try:
            doc_ref = self.client.collection(collection_name).document(document_id)
            doc_ref.set(data)  # Crée ou met à jour
        except Exception as e:
            raise Exception(f"Erreur lors de la mise à jour des données : {str(e)}")
       
 
# Créez une instance du client Firestore
firestore_client = FirestoreClient()
 
@router.get("/get-parameters")
def get_parameters():
    """Endpoint pour récupérer les paramètres depuis Firestore."""
    try:
        # Récupère les paramètres dans la collection "parameters"
        data = firestore_client.get_document("parameters", "parameters")
        return {"parameters": data}
 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des paramètres : {str(e)}")
 
# **Endpoint pour ajouter ou mettre à jour des paramètres**
@router.post("/update-parameters")
def update_parameters(parameters: ParametersModel):
    """Endpoint pour ajouter ou mettre à jour des paramètres dans Firestore."""
    try:
        # Préparer les données
        data = parameters.dict()
 
        # Mettre à jour ou ajouter dans Firestore
        firestore_client.create_or_update_document("parameters", "parameters", data)
 
        return {"message": "Paramètres ajoutés/mis à jour avec succès."}
 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la mise à jour des paramètres : {str(e)}")
 
 