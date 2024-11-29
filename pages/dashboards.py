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
                 Évolution des décès liés aux facteurs de risque dans le temps
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
    Fonction pour afficher uniquement le contenu de la vue d'ensemble avec filtres dynamiques pour le sexe.
    """
    # Charger les données
    evolution_data = dl.load_evolution_facteurs()

    # Ajouter un slider pour sélectionner l'année
    selected_year = st.slider(
        "Sélectionnez une année",
        min_value=int(evolution_data["year"].min()),
        max_value=int(evolution_data["year"].max()),
        value=int(evolution_data["year"].max()),
        key="overview_year"
    )

    # Ajouter des boutons radio pour sélectionner le sexe
    selected_sex = st.radio(
        "Sélectionnez le sexe :",
        options=["Les deux", "Homme", "Femme"],
        index=0,  # Par défaut sur "Les deux"
        horizontal=True  # Boutons alignés horizontalement
    )

    # Catégories principales et sous-catégories pour le graphique en barres
    categories = {
        "Risques métaboliques": ["Haute tension artérielle systolique", "Indice de masse corporelle élevé", 
                                 "Glycémie à jeun élevée", "Taux élevé de cholestérol LDL"],
        "Risques comportementaux": ["Tabac", "Consommation d’alcool", "Usage de drogues", "La fumée secondaire"],
        "Risques environnementaux/professionnels": ["Pollution de l’air", "Pollution de l’air domestique par les combustibles solides", 
                                                    "Exposition au plomb", "Exposition professionnelle aux substances cancérigènes"]
    }

    # Filtrer les données pour le camembert en fonction de l'année et du sexe sélectionnés
    pie_data = evolution_data[
        (evolution_data["metric"] == "%") & 
        (evolution_data["sex"] == selected_sex) &
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
        title=f"Répartition des décès ({selected_sex}) - {selected_year}",
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

    # Filtrer les données pour le graphique en barres et restreindre aux sous-catégories spécifiées
    bar_data = evolution_data[
        (evolution_data["metric"] == "#") & 
        (evolution_data["sex"] == selected_sex) & 
        (evolution_data["age"] == "Tout age") & 
        (evolution_data["year"] == selected_year) &
        (evolution_data["rei"].isin(
            categories["Risques métaboliques"] + 
            categories["Risques comportementaux"] + 
            categories["Risques environnementaux/professionnels"]
        ))
    ]

    # Ajouter la catégorie et couleur correspondante
    bar_data["Category"] = bar_data["rei"].apply(
        lambda x: next((cat for cat, subcat in categories.items() if x in subcat), "Autres")
    )
    bar_data["Color"] = bar_data["Category"].map(category_colors)

    # Trier les données pour que les barres les plus grandes soient en haut
    bar_data = bar_data.sort_values(by="val", ascending=True)

    # Graphique en barres horizontales avec Plotly
    fig2 = px.bar(
        bar_data,
        x="val",
        y="rei",
        color="Category",
        color_discrete_map=category_colors,
        orientation="h",
        labels={"val": "Nombre de décès", "rei": "Facteurs de risque"},
        title=f"Nombre de décès par sous-catégorie ({selected_sex}) - {selected_year}",
        template="plotly_dark"
    )
    fig2.update_layout(
        title_font_size=20,
        xaxis_title="Nombre de décès",
        yaxis_title="Facteurs de risque",
        height=400,
        margin=dict(t=40, b=40, l=20, r=20),
        showlegend=False  # Supprimer la légende
    )

    # Disposition en colonnes pour afficher le camembert et le graphique en barres côte à côte
    col1, col2 = st.columns([1, 1.2])
    with col1:
        st.plotly_chart(fig1, use_container_width=True, height=600)
    with col2:
        st.plotly_chart(fig2, use_container_width=True, height=600)



        # Graphique linéaire montrant l'évolution des décès liés aux différents types de risques
    st.write("---")
   

    # Filtrer les données pour obtenir les tendances temporelles
    trend_data = evolution_data[
        (evolution_data["metric"] == "#") &
        (evolution_data["sex"] == "Les deux") &
        (evolution_data["age"] == "Tout age") &
        (evolution_data["rei"].isin(["Risques métaboliques", "Risques comportementaux", "Risques environnementaux/professionnels"]))
    ][["year", "rei", "val"]]

    # Graphique linéaire interactif avec Plotly Express
    fig3 = px.line(
        trend_data,
        x="year",
        y="val",
        color="rei",
        labels={"year": "Année", "val": "Nombre de décès", "rei": "Type de risque"},
        title="Tendances des décès par type de risque",
        markers=True
    )

    # Mise à jour du style du graphique
    fig3.update_layout(
        title=dict(font=dict(size=20)),
        xaxis=dict(title="Année", showgrid=False),
        yaxis=dict(title="Nombre de décès", showgrid=True),
        legend=dict(title="Type de risque"),
        template="plotly_dark",
        margin=dict(t=40, b=40, l=20, r=20)
    )

    # Affichage du graphique
    st.plotly_chart(fig3, use_container_width=True)

        # Ajouter une séparation visuelle
    st.write("---")
    st.markdown(
        """
        <h3 style="text-align: center; color: #666;">🎯 Quiz : Comprenez-vous pourquoi les risques métaboliques augmentent ?</h3>
        """,
        unsafe_allow_html=True,
    )

    # Question 1
    question_1 = st.radio(
        "1️⃣ Quel est le principal facteur contribuant à l'augmentation des risques métaboliques dans le monde ?",
        options=[
            "A. Urbanisation rapide et mode de vie sédentaire",
            "B. Augmentation de l'espérance de vie",
            "C. Progrès dans le diagnostic médical",
            "D. Toutes les réponses"
        ],
        key="question_1"
    )

    # Vérification de la réponse à la question 1
    if st.button("Valider votre réponse", key="validate_1"):
        if question_1 == "D. Toutes les réponses":
            st.success("✅ Correct ! Tous ces facteurs contribuent à l'augmentation des risques métaboliques.")
        else:
            st.error("❌ Incorrect. La bonne réponse est : D. Toutes les réponses.")

    # Question 2
    st.write("")
    question_2 = st.radio(
        "2️⃣ Quels comportements peuvent réduire les risques métaboliques ?",
        options=[
            "A. Consommer plus de fruits et légumes",
            "B. Augmenter l'activité physique",
            "C. Réduire la consommation d'aliments transformés",
            "D. Toutes les réponses"
        ],
        key="question_2"
    )

    # Vérification de la réponse à la question 2
    if st.button("Valider votre réponse", key="validate_2"):
        if question_2 == "D. Toutes les réponses":
            st.success("✅ Correct ! Tous ces comportements aident à réduire les risques métaboliques.")
        else:
            st.error("❌ Incorrect. La bonne réponse est : D. Toutes les réponses.")



#-------------------------------------------------------------------------------------------
# Fonction pour le focus spécifique sur le tabac et la consommation d’alcool

import streamlit as st
import plotly.express as px

# Fonction pour le focus spécifique sur le tabac et la consommation d’alcool
import streamlit as st
import plotly.express as px

# Fonction pour le focus spécifique sur le tabac et la consommation d’alcool
def display_tobacco_alcohol():
    """
    Affiche les graphiques pour le tabac et l'alcool, y compris une carte interactive.
    """
    # Charger les données
    evolution_data = dl.load_evolution_facteurs()
    data_alcohol = dl.load_data_alcohol()  # Charger le DataFrame pour l'alcool

    # -- Afficher les metric cards avant le graphique --

    st.write("### Décès par catégorie de personne (2019)")

    # Filtrer les données pour le tabac et l'alcool pour l'année 2019
    data_tobacco_alcohol = evolution_data[
        (evolution_data["year"] == 2019) &
        (evolution_data["rei"].isin(["Tabac", "Consommation d’alcool"])) &
        (evolution_data["metric"] == "#")  # Utiliser les valeurs absolues
    ]

    # Mapper les codes de sexe vers des valeurs lisibles pour evolution_data si nécessaire
    sexe_mapping_evolution = {
        'Male': 'Homme',
        'Female': 'Femme',
        'Both': 'Tous',
        'Both sexes': 'Tous'
    }
    if 'sex' in data_tobacco_alcohol.columns:
        data_tobacco_alcohol['sex'] = data_tobacco_alcohol['sex'].map(sexe_mapping_evolution)

    # Vérifier les valeurs exactes pour la colonne 'age'
    # Si les valeurs sont en français, ajustez en conséquence
    age_all = 'All ages'  # Ou 'Tout âge' si vos données sont en français
    age_adolescents = '<20 years'  # Ou '< 20 ans' si vos données sont en français

    # Calculer les totaux pour chaque groupe démographique
    homme_total = data_tobacco_alcohol[
        (data_tobacco_alcohol["sex"] == "Homme") &
        (data_tobacco_alcohol["age"] == age_all)
    ]["val"].sum()

    femme_total = data_tobacco_alcohol[
        (data_tobacco_alcohol["sex"] == "Femme") &
        (data_tobacco_alcohol["age"] == age_all)
    ]["val"].sum()

    adolescent_total = data_tobacco_alcohol[
        data_tobacco_alcohol["age"] == age_adolescents  # Filtrer uniquement pour les adolescents
    ]["val"].sum()

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

    # -- Afficher la carte interactive après les metric cards --

    st.write("### Carte interactive : Pourcentage des décès attribuables à l'alcool (2019)")
    st.write(
        "Cette carte montre le pourcentage des décès attribuables à l'alcool pour l'année **2019**. "
        "Sélectionnez le sexe et survolez les pays pour afficher les détails."
    )

    # Mapper les codes de sexe vers des valeurs lisibles
    sexe_mapping = {
        'SEX_FMLE': 'Femme',
        'SEX_MLE': 'Homme',
        'SEX_BTSX': 'Tous'
    }
    data_alcohol['sexe'] = data_alcohol['sexe'].map(sexe_mapping)

    # Vérifier les sexes disponibles
    unique_sexes = data_alcohol["sexe"].unique()

    # Permettre de sélectionner le sexe avec des boutons radio alignés horizontalement
    selected_sex = st.radio(
        "Sélectionnez le sexe",
        options=unique_sexes,
        index=unique_sexes.tolist().index('Tous') if 'Tous' in unique_sexes else 0,
        horizontal=True
    )

    # Filtrer les données pour le sexe sélectionné
    data_alcohol_filtered = data_alcohol[
        data_alcohol["sexe"] == selected_sex
    ]

    # S'assurer que les données ne sont pas vides après le filtrage
    if data_alcohol_filtered.empty:
        st.write("Aucune donnée disponible pour les critères sélectionnés.")
    else:
        # Créer la carte avec Plotly Express
        fig_map = px.choropleth(
            data_alcohol_filtered,
            locations="pays",  # Colonne avec les codes pays ISO Alpha-3
            locationmode="ISO-3",  # Spécifie le format des codes pays
            color="pourcentage_deces",  # Donnée à afficher
            hover_name="pays",  # Nom des pays au survol
            hover_data={"pourcentage_deces": ":.2f", "sexe": True},  # Colonnes à afficher au survol
            title=f"Pourcentage des décès attribuables à l'alcool par pays (2019) - {selected_sex}",
            color_continuous_scale=px.colors.sequential.Plasma,  # Palette de couleurs
            labels={"pourcentage_deces": "Décès attribuables à l'alcool (%)"}
        )

        # Mise à jour du style de la carte
        fig_map.update_geos(
            showcoastlines=True, coastlinecolor="LightGray",
            showland=True, landcolor="whitesmoke",
            showocean=True, oceancolor="LightBlue",
            showlakes=True, lakecolor="LightBlue",
            projection_type="natural earth"
        )

        fig_map.update_layout(
            title=dict(font=dict(size=20), x=0.5),  # Centrer le titre
            margin=dict(t=40, b=20, l=20, r=20),  # Ajuster les marges
            coloraxis_colorbar=dict(
                title="Décès (%)",
                tickformat=".2f"
            )
        )

        # Afficher la carte
        st.plotly_chart(fig_map, use_container_width=True)
