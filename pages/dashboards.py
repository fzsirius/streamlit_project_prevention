from streamlit_extras.metric_cards import style_metric_cards
import streamlit as st
import data_loader as dl
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.metric_cards import style_metric_cards
def display_dashboard():
    """
    Fonction principale pour gérer les onglets du Dashboard
    """

    # Création des onglets avec des emojis directement insérés dans les noms d'onglets
    tab1, tab2, tab3 = st.tabs(
        [
            "🔍  Vue d'ensemble  ",
            "🚬🥂  Focus : Tabac et Alcool  ",
            "🍔🩺  Focus : Risques Métaboliques  ",
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

    # Section : Focus sur Risques Métaboliques
    with tab3:
        st.markdown(
            """
            <h2 style="text-align: center; font-family: 'Helvetica'; color: #FF9800;font-size: 30px">
                Focus : Risques Métaboliques
            </h2>
            """,
            unsafe_allow_html=True,
        )
        add_vertical_space(1)  # Optionnel
        display_metabolic_risks()  # Appelle la fonction pour le focus sur les risques métaboliques

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
    # Afficher un titre

    # Affichage interactif du tableau de données
    with st.expander("Afficher les données brutes 📋"):
        st.write("Les données ci-dessous contiennent des informations détaillées sur les facteurs de risque au fil des années.")
        st.dataframe(evolution_data)  # Affiche le DataFrame dans une table interactive

    # Ajouter une option de téléchargement des données
    csv_data = evolution_data.to_csv(index=False)  # Convertir les données en format CSV
    st.download_button(
        label="📥 Télécharger les données",
        data=csv_data,
        file_name="facteurs_de_risque.csv",
        mime="text/csv",
    )

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
        title=f"Répartition des décès par facteur ({selected_sex}) - {selected_year}",
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
        key="quiz_question_1"  # Clé unique pour éviter les conflits
    )

    # Vérification de la réponse à la question 1
    if st.button("Valider votre réponse - Q1", key="validate_question_1"):  # Clé unique pour le bouton
        if question_1 == "D. Toutes les réponses":
            st.success("✅ Correct ! Tous ces facteurs contribuent à l'augmentation des risques métaboliques.")
        else:
            st.error("❌ Incorrect. La bonne réponse est : D. Toutes les réponses.")

    # Ajout d'un espace entre les questions
    st.write("")

    # Question 2
    question_2 = st.radio(
        "2️⃣ Quels comportements peuvent réduire les risques métaboliques ?",
        options=[
            "A. Consommer plus de fruits et légumes",
            "B. Augmenter l'activité physique",
            "C. Réduire la consommation d'aliments transformés",
            "D. Toutes les réponses"
        ],
        key="quiz_question_2"  # Clé unique pour éviter les conflits
    )

    # Vérification de la réponse à la question 2
    if st.button("Valider votre réponse - Q2", key="validate_question_2"):  # Clé unique pour le bouton
        if question_2 == "D. Toutes les réponses":
            st.success("✅ Correct ! Tous ces comportements aident à réduire les risques métaboliques.")
        else:
            st.error("❌ Incorrect. La bonne réponse est : D. Toutes les réponses.")



#-------------------------------------------------------------------------------------------
# Fonction pour le focus spécifique sur le tabac et la consommation d’alcool

import streamlit as st
import plotly.express as px


def display_tobacco_alcohol():
    """
    Affiche les métriques pour le tabac et l'alcool, un graphique d'évolution comparant les décès liés au tabac et à l'alcool,
    et une carte interactive pour l'alcool.
    """

    # Charger les données
    evolution_data = dl.load_evolution_facteurs()
    data_alcohol = dl.load_data_alcohol()  # Charger le DataFrame pour l'alcool

    # -- Afficher les metric cards avant le graphique --

    st.write("### Décès lié au tabac et alcool, par catégorie de personne")

    # Slider pour sélectionner l'année
    min_year = int(evolution_data["year"].min())
    max_year = int(evolution_data["year"].max())
    selected_year = st.slider(
        "Sélectionnez une année",
        min_value=min_year,
        max_value=max_year,
        value=max_year,  # Par défaut, l'année la plus récente
        key="metric_year"
    )

    # Filtrer les données pour l'année sélectionnée
    data_tobacco_alcohol = evolution_data[
        (evolution_data["year"] == selected_year) &
        (evolution_data["rei"].isin(["Tabac", "Consommation d’alcool"])) &
        (evolution_data["metric"] == "#")  # Utiliser les valeurs absolues
    ]

    # Standardiser la valeur 'Les deux' en 'Tous' pour uniformiser
    data_tobacco_alcohol['sex'] = data_tobacco_alcohol['sex'].replace({'Les deux': 'Tous'})

    # Vérifier les valeurs pour 'age'
    age_all_values = ['Tout âge', 'Tous les âges', 'Tout age', 'All ages']
    age_all = next((age for age in age_all_values if age in data_tobacco_alcohol['age'].unique()), None)
    if not age_all:
        st.write("Valeur inattendue pour 'age'. Veuillez vérifier les données.")
        return

    # Vérifier la valeur pour les adolescents
    age_adolescents_values = ['< 20 ans', '<20 ans', '<20 years']
    age_adolescents = next((age for age in age_adolescents_values if age in data_tobacco_alcohol['age'].unique()), None)
    if not age_adolescents:
        st.write("Valeur inattendue pour l'âge des adolescents. Veuillez vérifier les données.")
        adolescent_total = 0
    else:
        adolescent_total = data_tobacco_alcohol[
            data_tobacco_alcohol["age"] == age_adolescents
        ]["val"].sum()

    # Calculer les totaux pour chaque groupe démographique
    homme_total = data_tobacco_alcohol[
        (data_tobacco_alcohol["sex"] == "Homme") &
        (data_tobacco_alcohol["age"] == age_all)
    ]["val"].sum()

    femme_total = data_tobacco_alcohol[
        (data_tobacco_alcohol["sex"] == "Femme") &
        (data_tobacco_alcohol["age"] == age_all)
    ]["val"].sum()

    # Afficher les indicateurs en une ligne avec des colonnes et du style HTML/CSS natif
    st.markdown(
        """
        <style>
            .metric-card {
                background-color: #f0f2f6;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
                text-align: center;
                font-family: Arial, sans-serif;
            }
            .metric-title {
                font-size: 16px;
                font-weight: bold;
                color: #333333;
            }
            .metric-value {
                font-size: 24px;
                font-weight: bold;
                color: #1f77b4;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Total Hommes</div>
                <div class="metric-value">{homme_total:,.0f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Total Femmes</div>
                <div class="metric-value">{femme_total:,.0f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Total Adolescents (&lt;20 ans)</div>
                <div class="metric-value">{adolescent_total:,.0f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # -- Ajouter le graphique d'évolution comparant le tabac et l'alcool --

    st.write("### Évolution du nombre de décès liés au tabac et à l'alcool")

    # Filtrer les données pour obtenir les tendances temporelles
    data_evolution = evolution_data[
        (evolution_data["metric"] == "#") &
        (evolution_data["sex"] == "Les deux") &
        (evolution_data["age"] == "Tout age") &
        (evolution_data["rei"].isin(["Tabac", "Consommation d’alcool"]))
    ][["year", "rei", "val"]]

    # Vérifier si le DataFrame n'est pas vide
    if data_evolution.empty:
        st.write("Aucune donnée disponible pour l'évolution des décès liés au tabac et à l'alcool.")
    else:
        # Graphique linéaire interactif avec Plotly Express
        fig_evolution = px.line(
            data_evolution,
            x="year",
            y="val",
            color="rei",
            labels={"year": "Année", "val": "Nombre de décès", "rei": "Facteur de risque"},
            markers=True
        )

        # Afficher le graphique
        st.plotly_chart(fig_evolution, use_container_width=True)


    # -- Ajouter le graphique d'évolution comparant le tabac et l'alcool --

    st.write("### Évolution du nombre de décès liés au tabac et à l'alcool")

    # Filtrer les données pour obtenir les tendances temporelles
    data_evolution = evolution_data[
        (evolution_data["metric"] == "#") &
        (evolution_data["sex"] == "Les deux") &
        (evolution_data["age"] == "Tout age") &
        (evolution_data["rei"].isin(["Tabac", "Consommation d’alcool"]))
    ][["year", "rei", "val"]]

    # Vérifier si le DataFrame n'est pas vide
    if data_evolution.empty:
        st.write("Aucune donnée disponible pour l'évolution des décès liés au tabac et à l'alcool.")
    else:
        # Graphique linéaire interactif avec Plotly Express
        fig_evolution = px.line(
            data_evolution,
            x="year",
            y="val",
            color="rei",
            labels={"year": "Année", "val": "Nombre de décès", "rei": "Facteur de risque"},
            #title="Tendances des décès liés au tabac et à l'alcool",
            markers=True
        )

        # Afficher le graphique
        st.plotly_chart(fig_evolution, use_container_width=True)

    # -- Afficher la carte interactive après les metric cards et le graphique --

    st.write("### Carte interactive : Pourcentage des décès attribuables à l'alcool (2019)")
    st.write(
        "Cette carte montre le pourcentage des décès attribuables à l'alcool pour l'année **2019**. "
        "Sélectionnez le sexe et survolez les pays pour afficher les détails."
    )

    # Mapper les codes de sexe vers des valeurs lisibles pour data_alcohol
    sexe_mapping_alcohol = {
        'SEX_FMLE': 'Femme',
        'SEX_MLE': 'Homme',
        'SEX_BTSX': 'Tous'
    }
    data_alcohol['sexe'] = data_alcohol['sexe'].map(sexe_mapping_alcohol)

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


#------------------------------------------------------------------------
# Onglet riques métaboliques
def display_metabolic_risks():
    """
    Affiche le contenu pour le focus sur les risques métaboliques.
    """
    import streamlit as st
    import plotly.express as px
    import data_loader as dl  # Assurez-vous d'importer correctement votre module data_loader

    # Les indicateurs disponibles avec leurs codes correspondants
    indicators = {
        "Prévalence de l'obésité chez les adultes (IMC ≥30 kg/m²)": "NCD_BMI_30A",
        "Prévalence de l'hypertension artérielle (PAS ≥140 ou PAD ≥90 mmHg)": "BP_04",
        "Glycémie à jeun élevée (≥7.0 mmol/L ou ≥126 mg/dL)": "NCD_GLUC_04"
    }

    # Sélection de l'indicateur
    selected_indicator_name = st.selectbox(
        "Sélectionnez un indicateur de risque métabolique",
        list(indicators.keys())
    )
    indicator_code = indicators[selected_indicator_name]

    st.write("### Sélectionnez les filtres pour les données")

    # Chargement des données sans filtres pour déterminer les dimensions disponibles
    with st.spinner("Chargement des données pour déterminer les dimensions disponibles..."):
        sample_data = dl.load_metabolic_risk_data(indicator_code)

    if sample_data is None or sample_data.empty:
        st.warning("Aucune donnée disponible pour cet indicateur.")
        return

    # Vérifier les années et sexes disponibles
    years_available = sample_data['annee'].dropna().unique()
    sexes_available = sample_data['sexe'].dropna().unique()

    # Sélection de l'année
    selected_year = st.selectbox("Sélectionnez une année", sorted(years_available, reverse=True))

    # Sélection du sexe
    sex_labels = {"SEX_BTSX": "Les deux", "SEX_MLE": "Homme", "SEX_FMLE": "Femme"}
    sex_mapping = {v: k for k, v in sex_labels.items()}  # Inverser le mapping pour le filtre
    selected_sex_label = st.selectbox("Sélectionnez le sexe", list(sex_labels.values()))
    selected_sex = sex_mapping[selected_sex_label]

    # Filtrer les données en fonction des critères sélectionnés
    with st.spinner("Chargement des données avec les filtres..."):
        data = sample_data[
            (sample_data['annee'] == selected_year) &
            (sample_data['sexe'] == selected_sex)
        ]

    if data.empty:
        st.warning("Aucune donnée disponible pour les critères sélectionnés.")
        return

    # Afficher un aperçu des données
    with st.expander("Afficher les données brutes"):
        st.write(data)

    # Création de la carte interactive
    st.write(f"### {selected_indicator_name} en {selected_year} pour {selected_sex_label}")

    # Créer la carte avec Plotly Express
    fig_map = px.choropleth(
        data_frame=data,
        locations="pays",  # Colonne avec les codes pays ISO Alpha-3
        locationmode="ISO-3",  # Spécifie le format des codes pays
        color="valeur",  # Donnée à afficher
        hover_name="pays",  # Nom des pays au survol
        hover_data={
            "valeur": ":.2f",  # Valeur principale
            "borne_inferieure": ":.2f",  # Borne inférieure
            "borne_superieure": ":.2f"   # Borne supérieure
        },
        title=f"{selected_indicator_name} ({selected_year}, {selected_sex_label})",
        color_continuous_scale=px.colors.sequential.Plasma,  # Palette de couleurs
        labels={"valeur": "Valeur (%)"}
    )

    # Mise à jour du style de la carte
    fig_map.update_geos(
        showcoastlines=True, coastlinecolor="LightGray",
        showland=True, landcolor="whitesmoke",
        showocean=True, oceancolor="LightBlue",
        showlakes=True, lakecolor="LightBlue",
        projection_type="natural earth"
    )

    # Afficher la carte
    st.plotly_chart(fig_map, use_container_width=True)
     # Outil : Calculateur d'IMC
    st.write("---")
    st.header("📊 Calculateur d'Indice de Masse Corporelle (IMC)")
    weight = st.number_input("Entrez votre poids (kg)", min_value=1, max_value=300, value=70)
    height = st.number_input("Entrez votre taille (cm)", min_value=50, max_value=250, value=170)

    if height > 0:
        height_m = height / 100
        bmi = weight / (height_m ** 2)
        st.write(f"### Votre IMC est : {bmi:.1f}")
        if bmi < 18.5:
            st.info("Vous êtes en sous-poids. Consultez un professionnel de santé.")
        elif 18.5 <= bmi < 24.9:
            st.success("Votre IMC est dans la plage normale.")
        elif 25 <= bmi < 29.9:
            st.warning("Vous êtes en surpoids. Envisagez des mesures pour améliorer votre santé.")
        else:
            st.error("Vous êtes en situation d'obésité. Consultez un professionnel de santé pour des conseils adaptés.")
    else:
        st.warning("La taille doit être supérieure à zéro.")



