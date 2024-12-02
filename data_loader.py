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


#----------------------------------------------------------------------------
# Fonction pour lire data_alcohol
def load_data_alcohol():
    """
    Charge et prépare les données sur les décès attribuables à l'alcool.
    """
    # URL de l'API pour les décès liés à l'alcool
    api_url = "https://ghoapi.azureedge.net/api/SA_0000001743"

    # Colonnes à extraire
    columns = ['SpatialDim', 'TimeDim', 'Value', 'NumericValue', 'Low', 'High',"Dim1"]

    # Charger les données depuis l'API
    data_alcohol = get_indicator_data(api_url, columns)

    # Renommer les colonnes pour les rendre plus compréhensibles
    noms_colonnes = {
        'SpatialDim': 'pays',
        'TimeDim': 'annee',
        'Value': 'valeur',
        'NumericValue': 'pourcentage_deces',
        'Low': 'borne_inferieure',
        'High': 'borne_superieure',
        "Dim1":"sexe"
    }
    data_alcohol = data_alcohol.rename(columns=noms_colonnes)

    # Nettoyer ou transformer les données si nécessaire (par exemple, retirer les valeurs nulles)
    data_alcohol = data_alcohol.dropna(subset=['pourcentage_deces'])

    return data_alcohol


#-----------------------------------------------------------------------------------------
# Fonction pour récupérer les données de manière plus précise et plus optimisées

def load_metabolic_risk_data(indicator_code):
    """
    Charge les données pour un indicateur de risque métabolique depuis l'API GHO de l'OMS.

    Paramètres :
    - indicator_code : code de l'indicateur à récupérer.

    Retourne :
    - pandas DataFrame avec les données récupérées.
    """
    import requests
    import pandas as pd

    # URL de l'API pour l'indicateur
    api_url = f"https://ghoapi.azureedge.net/api/{indicator_code}"

    # Colonnes à extraire
    columns = ['SpatialDim', 'TimeDim', 'Dim1', 'Value', 'Low', 'High']

    # Requête à l'API
    response = requests.get(api_url)
    if response.status_code != 200:
        print(f"Erreur lors de la récupération des données : {response.status_code}")
        return None

    # Charger les données JSON
    data = response.json()
    if 'value' not in data:
        print("Aucune donnée disponible dans la réponse de l'API.")
        return None

    # Convertir les données en DataFrame
    df = pd.DataFrame(data['value'])

    # Filtrer les colonnes nécessaires
    df = df[columns]

    # Renommer les colonnes pour simplifier la compréhension
    df.rename(columns={
        'SpatialDim': 'pays',
        'TimeDim': 'annee',
        'Dim1': 'sexe',
        'Value': 'valeur',
        'Low': 'borne_inferieure',
        'High': 'borne_superieure'
    }, inplace=True)

    # Nettoyer les valeurs : extraire uniquement la partie numérique de 'valeur'
    def extract_continuous_value(value):
        try:
            # Extraction de la première valeur avant le crochet
            return float(value.split(" ")[0].replace("[", "").replace("]", ""))
        except (ValueError, IndexError, AttributeError):
            return None  # Retourner None si l'extraction échoue

    df['valeur'] = df['valeur'].apply(extract_continuous_value)

    # Supprimer les lignes avec des valeurs non numériques après traitement
    df = df.dropna(subset=['valeur'])

    return df

