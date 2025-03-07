import os
import pandas as pd

def load_data(file_name):
    """Carrega dados de um arquivo CSV dentro do diretório correto."""
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))  # Caminho absoluto para data/
    file_path = os.path.join(base_path, file_name)  # Junta com o nome do arquivo CSV
    
    if not os.path.exists(file_path):  
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")  # Tratamento de erro

    data = pd.read_csv(file_path)
    data['date'] = pd.to_datetime(data['date'], dayfirst=True)
    return data
