import streamlit as st
from pages import dashboards, home  # Importer les pages d'accueil et de vue d'ensemble

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
        "Navigation",
        ["Accueil", "Dashboards", "Autre Page"],
        icons=["house", "bar-chart", "gear"],
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
elif page == "Autre Page":
    # Placeholder pour une page en construction
    st.write("Cette page est en construction...")
