# import packages
import requests
import pandas as pd

def get_indicator_data(url, columns=None):
    """
    Récupère et filtre les données d'un indicateur de l'OMS depuis l'API.

    Paramètres :
    - url (str) : URL de l'indicateur dans l'API de l'OMS.
    - columns (list, optionnel) : Liste des colonnes à conserver. Si None, conserve toutes les colonnes.

    Retourne :
    - pd.DataFrame : DataFrame avec les données récupérées et filtrées.
      Retourne None si la requête échoue.
    """
    # Effectuer la requête vers l'API
    response = requests.get(url)
    
    if response.status_code == 200:
        # Charger les données JSON dans un DataFrame
        data = response.json()
        df = pd.DataFrame(data['value'])
        
        # Filtrer les colonnes si une liste est fournie
        if columns:
            existing_columns = [col for col in columns if col in df.columns]
            df_filtered = df[existing_columns]
        else:
            # Conserver toutes les colonnes si 'columns' est None
            df_filtered = df
        
        # Supprimer les lignes entièrement vides (optionnel)
        df_filtered = df_filtered.dropna(how='all')
        
        return df_filtered
    else:
        # Afficher un message d'erreur si la requête échoue
        print("Erreur lors de la récupération des données.")
        return None



# Evolution de chaque facteurs de risque
def load_evolution_facteurs(filepath="datas/evolution_chaque_facteurs/evolution_facteurs.csv"):
    import pandas as pd
    """Charge les données sur l'évolution des facteurs de risque."""
    return pd.read_csv(filepath, encoding="utf-8")  

