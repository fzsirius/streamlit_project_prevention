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

def load_metabolic_risk_data(indicator_code, countries=None, years=None, sexes=None):
    """
    Charge les données de risque métabolique depuis l'API GHO de l'OMS.

    Paramètres :
    - indicator_code : code de l'indicateur à récupérer
    - countries : liste des codes pays (codes ISO 2 lettres)
    - years : liste des années pour lesquelles récupérer les données
    - sexes : liste des sexes à récupérer ('SEX_MLE', 'SEX_FMLE', 'SEX_BTSX')

    Retourne :
    - pandas DataFrame avec les données
    """
    import requests
    import pandas as pd

    base_url = "https://ghoapi.azureedge.net/api/"
    url = f"{base_url}{indicator_code}"

    # Préparer les filtres pour l'API
    filter_conditions = []

    if countries:
        country_conditions = ' or '.join([f"SpatialDim eq '{country}'" for country in countries])
        filter_conditions.append(f"({country_conditions})")

    if years:
        year_conditions = ' or '.join([f"TimeDim eq {year}" for year in years])
        filter_conditions.append(f"({year_conditions})")

    if sexes:
        sex_conditions = ' or '.join([f"Dim1 eq '{sex}'" for sex in sexes])
        filter_conditions.append(f"({sex_conditions})")

    params = {}
    if filter_conditions:
        filter_query = ' and '.join(filter_conditions)
        params['$filter'] = filter_query

    params['$top'] = 5000  # Ajustez ce nombre si nécessaire

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"Erreur lors de la récupération des données : {response.status_code}")
        return None

    data = response.json()

    # Vérifier si les données contiennent les dimensions 'TimeDim' et 'Dim1'
    has_time_dim = any('TimeDim' in entry for entry in data.get('value', []))
    has_sex_dim = any('Dim1' in entry for entry in data.get('value', []))

    # Extraire les données
    data_rows = []

    if 'value' in data:
        for entry in data['value']:
            row = {
                'IndicatorCode': entry.get('IndicatorCode'),
                'IndicatorName': entry.get('IndicatorName'),
                'CountryCode': entry.get('SpatialDim'),
                'Country': entry.get('SpatialDimType'),
                'Value': entry.get('NumericValue')
            }

            if has_time_dim:
                row['Year'] = entry.get('TimeDim')
            else:
                row['Year'] = None  # Ou une valeur par défaut

            if has_sex_dim:
                row['Sex'] = entry.get('Dim1')
            else:
                row['Sex'] = None  # Ou une valeur par défaut

            data_rows.append(row)
    else:
        print("Aucune donnée trouvée dans la réponse de l'API.")

    df = pd.DataFrame(data_rows)

    return df
