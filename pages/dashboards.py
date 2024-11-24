from streamlit_extras.metric_cards import style_metric_cards
import streamlit as st
import data_loader as dl
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.metric_cards import style_metric_cards

import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space  # Si tu veux des espaces verticaux stylés

def display_dashboard():
    """
    Fonction principale pour gérer les onglets du Dashboard
    """
 
    # Création des onglets avec des emojis directement insérés dans les noms d'onglets
    tab1, tab2 = st.tabs(
        [
            "🔍  Vue d'ensemble  ",
            "🚬🥂  Focus : Tabac et Alcool  ",
        ]
    )

    # Section : Vue d'ensemble
    with tab1:
        st.markdown(
            """
            <h2 style="text-align: center; font-family: 'Helvetica'; color: #FF9800;font-size: 30px">
                Vue d'ensemble des Facteurs de Risque
            </h2>
            """,
            unsafe_allow_html=True,
        )
        #add_vertical_space(1)  # Optionnel, pour ajouter de l'espace vertical
        display_overview_content()  # Appelle la fonction pour la vue d'ensemble

    # Section : Focus sur Tabac et Alcool
    with tab2:
        st.markdown(
            """
            <h2 style="text-align: center; font-family: 'Helvetica'; color: #FF9800;font-size: 30px">
                Focus : Tabac et Alcool
            </h2>
            """,
            unsafe_allow_html=True,
        )
        add_vertical_space(1)  # Optionnel
        display_tobacco_alcohol()  # Appelle la fonction pour le focus sur Tabac et Alcool

    # Ajouter un pied de page
    st.write("---")
    st.markdown(
        """
        <footer style="text-align: center; font-size: 14px; font-family: 'Arial'; color: #777;">
            Créé par <strong>Fehizoro Randriamisanta</strong> • Données : OMS, Global Health Observatory
        </footer>
        """,
        unsafe_allow_html=True,
    )


def display_overview_content():
    """
    Fonction pour afficher uniquement le contenu de la vue d'ensemble
    """
    # Titre et introduction
    #st.write("---")
    # Charger les données
    evolution_data = dl.load_evolution_facteurs()

    # Ajouter un slider pour sélectionner l'année
    selected_year = st.slider(
        "Sélectionnez une année",
        int(evolution_data["year"].min()),
        int(evolution_data["year"].max()),
        int(evolution_data["year"].max()),
        key="overview_year"
    )

    # Filtrer les données pour le camembert en fonction de l'année et obtenir les valeurs en pourcentage
    pie_data = evolution_data[
        (evolution_data["metric"] == "%") & 
        (evolution_data["sex"] == "Les deux") & 
        (evolution_data["age"] == "Tout age") & 
        (evolution_data["year"] == selected_year) &
        (evolution_data["rei"].isin(["Risques métaboliques", "Risques comportementaux", "Risques environnementaux/professionnels"]))
    ][["rei", "val"]]
    pie_data.columns = ["Category", "Value"]  # Renommer les colonnes pour le graphique

    # Convertir les valeurs en pourcentage réel en multipliant par 100
    pie_data["Value"] *= 100

    # Calculer la part "Autres"
    autres_percentage = 100 - pie_data["Value"].sum()
    autres_row = pd.DataFrame({"Category": ["Autres"], "Value": [autres_percentage]})
    pie_data = pd.concat([pie_data, autres_row], ignore_index=True)

    # Définir les couleurs pour chaque catégorie
    category_colors = {
        "Risques métaboliques": "#1f77b4",
        "Risques comportementaux": "#ff7f0e",
        "Risques environnementaux/professionnels": "#2ca02c",
        "Autres": "#636363"
    }

    # Graphique camembert avec Plotly
    fig1 = px.pie(
        pie_data, values='Value', names='Category',
        title="facteurs de risque vs autres causes",
        hole=0.3, color='Category',
        color_discrete_map=category_colors
    )
    fig1.update_layout(
        title_font_size=20,
        margin=dict(t=40, b=40, l=20, r=20),
        template="plotly_dark",
        height=400,
    )
    fig1.update_traces(
        textposition='inside',
        textinfo='percent+label',
        marker=dict(line=dict(color='#333333', width=2))
    )

    # Filtrer pour obtenir les données globales en valeurs brutes pour le graphique en barres
    data_global_absolute = evolution_data[
        (evolution_data["metric"] == "#") & 
        (evolution_data["sex"] == "Les deux") & 
        (evolution_data["age"] == "Tout age") & 
        (evolution_data["year"] == selected_year)
    ]

    # Extraire les données pour hommes et femmes
    homme_data = evolution_data[
        (evolution_data["metric"] == "#") & 
        (evolution_data["sex"] == "Homme") & 
        (evolution_data["age"] == "Tout age") & 
        (evolution_data["year"] == selected_year)
    ][["rei", "val"]]
    homme_data.columns = ["rei", "Homme"]

    femme_data = evolution_data[
        (evolution_data["metric"] == "#") & 
        (evolution_data["sex"] == "Femme") & 
        (evolution_data["age"] == "Tout age") & 
        (evolution_data["year"] == selected_year)
    ][["rei", "val"]]
    femme_data.columns = ["rei", "Femme"]

    # Fusionner les données pour ajouter les colonnes "Homme" et "Femme"
    bar_data = data_global_absolute.merge(homme_data, on="rei", how="left").merge(femme_data, on="rei", how="left")

    # Catégories principales et sous-catégories pour le graphique en barres
    categories = {
        "Risques métaboliques": ["Haute tension artérielle systolique", "Indice de masse corporelle élevé", "Glycémie à jeun élevée", "Taux élevé de cholestérol LDL"],
        "Risques comportementaux": ["Tabac", "Consommation d’alcool", "Usage de drogues", "La fumée secondaire"],
        "Risques environnementaux/professionnels": ["Pollution de l’air", "Pollution de l’air domestique par les combustibles solides", "Exposition au plomb", "Exposition professionnelle aux substances cancérigènes"]
    }

    # Ajouter la catégorie et couleur correspondante
    bar_data["Category"] = bar_data["rei"].apply(
        lambda x: next((cat for cat, subcat in categories.items() if x in subcat), "Autres")
    )
    bar_data["Color"] = bar_data["Category"].map(category_colors)

    # Filtrer uniquement les sous-catégories que vous souhaitez afficher
    bar_data = bar_data[bar_data["rei"].isin(
        categories["Risques métaboliques"] + categories["Risques comportementaux"] + categories["Risques environnementaux/professionnels"]
    )]

    # Trier les données pour que les barres les plus grandes soient en haut
    bar_data = bar_data.sort_values(by="val", ascending=True)

    # Graphique en barres horizontales avec Plotly
    fig2 = go.Figure(go.Bar(
        x=bar_data["val"],
        y=bar_data["rei"],
        orientation='h',
        marker=dict(color=bar_data["Color"]),
        customdata=bar_data[["Homme", "Femme"]].round(1),
        hovertemplate="Total: %{x:.1f}<br>Homme: %{customdata[0]:.1f}<br>Femme: %{customdata[1]:.1f}"
    ))
    fig2.update_layout(
        title=f"Nombre de décès par sous-catégorie - {selected_year}",
        xaxis_title="Nombre de décès",
        yaxis_title="Facteurs de risque",
        height=400,
        font=dict(size=12),
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False),
        margin=dict(t=40, b=40, l=20, r=20),
        template="plotly_dark"
    )

    # Disposition en colonnes pour afficher le camembert et le graphique en barres côte à côte
    col1, col2 = st.columns([1, 1.2])
    with col1:
        st.plotly_chart(fig1, use_container_width=True, height=600)
    with col2:
        st.plotly_chart(fig2, use_container_width=True,height=600)

#-------------------------------------------------------------------------------------------
# Fonction pour le focus spécifique sur le tabac et la consommation d’alcool

def display_tobacco_alcohol():
    # Charger les données
    evolution_data = dl.load_evolution_facteurs()

    # Slider pour sélectionner l'année avec un identifiant unique
    selected_year = st.slider(
        "Sélectionnez une année",
        min_value=int(evolution_data["year"].min()),
        max_value=int(evolution_data["year"].max()),
        value=int(evolution_data["year"].max()),
        key="tobacco_alcohol_year"  # Ajout d'une clé unique
    )

    # Filtrer les données pour le tabac et l'alcool pour l'année sélectionnée
    data_tobacco_alcohol = evolution_data[
        (evolution_data["year"] == selected_year) &
        (evolution_data["rei"].isin(["Tabac", "Consommation d’alcool"]))
    ]

    # Calculer les totaux pour chaque groupe démographique
    homme_total = data_tobacco_alcohol[data_tobacco_alcohol["sex"] == "Homme"]["val"].sum()
    femme_total = data_tobacco_alcohol[data_tobacco_alcohol["sex"] == "Femme"]["val"].sum()
    adolescent_total = data_tobacco_alcohol[data_tobacco_alcohol["age"] == "< 20 ans"]["val"].sum()

    # Afficher les indicateurs en une ligne
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Hommes", f"{homme_total:,.0f}")
    col2.metric("Total Femmes", f"{femme_total:,.0f}")
    col3.metric("Total Adolescents (<20 ans)", f"{adolescent_total:,.0f}")

    # Appliquer le style des metric cards
    style_metric_cards(
        background_color="#f0f2f6",
        border_size_px=2,
        border_color="#e0e3e7",
        border_radius_px=10,
        border_left_color="#1f77b4",
        box_shadow=True
    )

    # Graphique de comparaison entre tabac et alcool en valeurs absolues pour l'année sélectionnée
    fig = px.bar(
        data_tobacco_alcohol,
        x="rei",
        y="val",
        color="rei",
        labels={"val": "Nombre de décès", "rei": "Facteur de risque"},
        title=f"Nombre de décès liés au tabac et à l'alcool - {selected_year}",
        template="plotly_dark"
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
