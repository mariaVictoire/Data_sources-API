import os
import json
import pandas as pd
import kaggle
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from src.services.cleaning import clean_dataset
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import requests
import joblib
from sklearn.metrics import accuracy_score
import traceback

router = APIRouter()
split_data = {"train": None,"test": None}


@router.get("/read-dataset/{filename}")
def read_dataset(filename: str):
    """
    Reads a dataset from the Data folder, loads it into a DataFrame, and returns its content as JSON.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_folder = os.path.abspath(os.path.join(current_dir, "../../data"))
    print(data_folder)
    file_path = os.path.join(data_folder, filename)
   
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"File '{filename}' not found in the Data folder.")
   
    try:
        if filename.endswith(".csv"):
            df = pd.read_csv(file_path)
        elif filename.endswith(".xlsx"):
            df = pd.read_excel(file_path)
        elif filename.endswith(".json"):
            df = pd.read_json(file_path)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format. Only .csv, .xlsx, and .json are supported.")
       
        return JSONResponse(content=df.to_dict(orient="records"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading the file: {str(e)}")

@router.post("/clean-dataset/{filename}")
def clean_dataset_endpoint(filename: str):
    """
    Calls the clean_csv function to clean a specified dataset.
    """
    try:
        cleaned_df = clean_dataset(filename)
        response = {
            "message": "Dataset cleaned successfully.",
            "cleaned_data": cleaned_df.to_dict(orient="records"),
        }
       
 
        return response
    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"Error cleaning the dataset: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
 

@router.post("/split-dataset/{filename}")
def split_dataset(filename: str):
    try:
        # Étape 1 : Appel au endpoint clean_dataset
        print("Appel à l'endpoint clean_dataset...")  
        response = requests.post(f"http://127.0.0.1:8080/data/clean-dataset/{filename}")
        print(f"Réponse reçue : {response.status_code}") 
 
        # Étape 2 : Vérifier la réponse
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail=f"Failed to clean dataset. Status code: {response.status_code}")
 
        # Étape 3 : Récupérer les données nettoyées
        print("Chargement des données nettoyées...")  
        cleaned_data = response.json().get('cleaned_data')
        df = pd.DataFrame(cleaned_data)
 
 
        # Étape 4 : Vérification des colonnes
        print(f"Colonnes disponibles : {df.columns}") 
        if 'Species' not in df.columns:
            raise HTTPException(status_code=500, detail="Column 'Species' is missing in the dataset.")
 
        # Étape 5 : Séparation des données
        print("Séparation des données en X et y...")  
        X = df.drop(columns=['Species'])
        y = df['Species']
 
        print("Division des ensembles d'entraînement et de test...")  
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
 
        # Étape 6 : Conversion en dictionnaires
        train_data = pd.concat([X_train, y_train], axis=1).to_dict(orient="records")
        test_data = pd.concat([X_test, y_test], axis=1).to_dict(orient="records")
 
        # Stocker les données dans la mémoire
        split_data["train"] = train_data
        split_data["test"] = test_data
 
        response = {
            "train": train_data,
            "test_data": test_data,
        }
        return response
   
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error splitting the dataset: {str(e)}")

@router.post("/train-model/")
def train_model():
    try:
        # Étape 1 : Vérifier si les données divisées sont disponibles
        if split_data["train"] is None or split_data["test"] is None:
            print("Les données de split ne sont pas disponibles. Veuillez exécuter /split-dataset d'abord.")
            raise HTTPException(
                status_code=500,
                detail="Les données de split ne sont pas disponibles. Veuillez exécuter /split-dataset d'abord."
            )
 
        # Étape 2 : Charger les paramètres du modèle
        print("Chargement des paramètres du modèle...")  # Log
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_folder = os.path.abspath(os.path.join(current_dir, "../../config/model_parameters.json"))
        print(data_folder)
        file_path = os.path.join(data_folder)
        with open(file_path, 'r') as file:
            config = json.load(file)
 
        model_params = config['parameters']
        print(f"Paramètres du modèle : {model_params}")
 
        # Étape 3 : Préparer les données d'entraînement
        print("Préparation des données...")  # Log
        train_df = pd.DataFrame(split_data["train"])
        test_df = pd.DataFrame(split_data["test"])
 
        # Préparation des données d'entraînement
        X_train = train_df.drop(columns=['Species'])
        y_train = train_df['Species']
        print(f"Dimensions X_train : {X_train.shape}, y_train : {y_train.shape}")
 
        # Préparation des données de test
        X_test = test_df.drop(columns=['Species'])
        y_test = test_df['Species']
        print(f"Dimensions X_test : {X_test.shape}, y_test : {y_test.shape}")
 
        # Étape 4 : Entraînement du modèle
        print("Entraînement du modèle...")
        model = DecisionTreeClassifier(**model_params)
        model.fit(X_train, y_train)
 
        # Étape 5 : Évaluation sur les données de test
        print("Évaluation du modèle...")
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Précision du modèle : {accuracy}")
 
        print("Sauvegarde du modèle...")
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_folder = os.path.abspath(os.path.join(current_dir, "../../models"))
        print(data_folder)
        model_dir = os.path.join(data_folder)
        os.makedirs(model_dir, exist_ok=True)
        model_path = os.path.join(model_dir, "classification_model.pkl")
        joblib.dump(model, model_path)
        print(f"Modèle sauvegardé à : {model_path}")  
 
        return {
            "message": "Modèle entraîné avec succès",
            "model_path": model_path,
            "accuracy": accuracy
        }
 
    except Exception as e:
        print(f"Erreur détectée : {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'entraînement : {str(e)}")
 
 