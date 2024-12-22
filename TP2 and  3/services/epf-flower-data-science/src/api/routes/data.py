import os
import json
import pandas as pd
import kaggle
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
#from src.services.cleaning import clean_dataset
from sklearn.model_selection import train_test_split
#from sklearn.tree import DecisionTreeClassifier
import requests
import joblib
from sklearn.metrics import accuracy_score

router = APIRouter()

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
 