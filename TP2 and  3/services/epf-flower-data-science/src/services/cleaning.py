import pandas as pd
import os
 
def clean_dataset(filename: str):
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_folder = os.path.abspath(os.path.join(current_dir, "../Data"))
        file_path = os.path.join(data_folder, filename)
        df = pd.read_csv(file_path, on_bad_lines='skip', encoding='utf-8')
        print("Avant suppression de la colonne 'ID':")
        print(df.head())
        if 'Id' in df.columns:
            df_cleaned = df.drop(columns=['Id'])
        else:
            df_cleaned = df 
        print("Après suppression de la colonne 'ID':")
        print(df_cleaned.head())
 
        return df_cleaned
 
    except FileNotFoundError:
        raise ValueError(f"File '{filename}' not found in the Data folder.")
    except pd.errors.ParserError as e:
        raise ValueError(f"Erreur de parsing : {str(e)}")
    except Exception as e:
        raise ValueError(f"Error cleaning the dataset: {str(e)}")
 
 