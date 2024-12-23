import google.auth
from google.cloud import firestore
 
 
class FirestoreClient:
    """Wrapper autour d'une base de données Firestore"""
 
    client: firestore.Client
 
    def __init__(self) -> None:
        """Initialise le client Firestore."""
        credentials, _ = google.auth.default()
        self.client = firestore.Client(credentials=credentials)
 
    def create_or_update(self, collection_name: str, document_id: str, data: dict) -> None:
        """Crée ou met à jour un document dans Firestore.
        Args:
            collection_name: Nom de la collection
            document_id: ID du document
            data: Données à insérer ou mettre à jour
        """
        doc_ref = self.client.collection(collection_name).document(document_id)
        doc_ref.set(data)
        print(f"Document '{document_id}' ajouté/mis à jour dans '{collection_name}'.")
 

if __name__ == "__main__":
    try:
        firestore_client = FirestoreClient()
        data = {
            "n_estimators": 100,
            "criterion": "gini"
        }
 
        collection_name = "parameters"
        document_id = "parameters"
        firestore_client.create_or_update(collection_name, document_id, data)
 
        print("Collection et document créés avec succès dans Firestore.")
 
    except Exception as e:
        print(f"Erreur lors de la création des paramètres : {str(e)}")
 
 