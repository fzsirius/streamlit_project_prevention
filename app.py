import streamlit as st
from pages.dashboards import home


# Importer la bibliothèque de menu optionnel
from streamlit_option_menu import option_menu

# Configurer la page principale
st.set_page_config(
    page_title="Application de Prévention des Facteurs de Risque",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Barre latérale avec le menu de navigation
with st.sidebar:
    page = option_menu(
        "Menu",
        ["Accueil", "Dashboards", "Quiz"],
        icons=["house", "bar-chart", "question-circle"],  # Remplace "quiz" par "question-circle"
        menu_icon="cast",
        default_index=0,
    )

# Navigation entre les pages
if page == "Accueil":
    # Appelle la page d'accueil depuis le module `home.py`
    home.display_home()
elif page == "Dashboards":
    # Appelle la fonction principale des dashboards avec les onglets
    dashboards.display_dashboard()  # Utilise `display_dashboard` au lieu de `display_overview`
elif page == "Quiz":
    # Placeholder pour une page en construction
    st.write("Bienvenue sur la page Quiz!")
