import pytest
from fastapi.testclient import TestClient


class TestData:
    @pytest.fixture
    def client(self) -> TestClient:
        """Initialisation du client TestClient."""
        from main import get_application
        app = get_application()
        return TestClient(app, base_url="http://127.0.0.1:8080")

    def test_split_dataset(self, client):
        """Test pour diviser un dataset."""
        url = "v0/data/split-dataset/Iris.csv"

        # Appel de l'endpoint
        response = client.post(url)

        # Logs pour debug
        print("\nStatut de la réponse :", response.status_code)
        print("Contenu de la réponse :", response.json())

        # Vérifications
        assert response.status_code == 200
        assert "train" in response.json()
        assert "test_data" in response.json()

         # Vérifications
        assert response.status_code == 200, f"Échec avec statut {response.status_code} et contenu {response.json()}"
        assert "train" in response.json()
        assert "test_data" in response.json()


    def test_split_dataset_file_not_found(self, client):
        """Test pour un fichier manquant."""
        url = "v0/data/split-dataset/fichier_inexistant.csv"

        response = client.post(url)
        assert response.status_code == 500
        assert "detail" in response.json()


   