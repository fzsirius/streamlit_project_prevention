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
from streamlit_extras.add_vertical_space import add_vertical_space  

import streamlit as st
import plotly.express as px
import data_loader as dl

import streamlit as st
import plotly.express as px
import data_loader as dl


def display_dashboard():
    """
    Fonction principale pour gérer les onglets du Dashboard.
    """
    tab1, tab2, tab3 = st.tabs(
        [
            "🔍  Vue d'ensemble  ",
            "🚬🥂  Focus : Tabac et Alcool  ",
            "🍔🩺  Focus : Risques Métaboliques  ",
        ]
    )

    # Vue d'ensemble
    with tab1:
        st.markdown(
            """
            <h2 style="text-align: center; font-family: 'Helvetica'; color: #FF9800;font-size: 30px">
                 Évolution des décès liés aux facteurs de risque dans le temps
            </h2>
            """,
            unsafe_allow_html=True,
        )
        display_overview_content()

    # Tabac et Alcool
    with tab2:
        st.markdown(
            """
            <h2 style="text-align: center; font-family: 'Helvetica'; color: #FF9800;font-size: 30px">
                Focus : Tabac et Alcool
            </h2>
            """,
            unsafe_allow_html=True,
        )
        display_tobacco_alcohol()

    # Risques Métaboliques
    with tab3:
        st.markdown(
            """
            <h2 style="text-align: center; font-family: 'Helvetica'; color: #FF9800;font-size: 30px">
                Focus : Risques Métaboliques
            </h2>
            """,
            unsafe_allow_html=True,
        )
        display_metabolic_risks()

    # Footer
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
    Vue d'ensemble : données interactives et visualisation des tendances.
    """
    # Charger les données
    evolution_data = dl.load_evolution_facteurs()

    # Section des données brutes
    with st.expander("Afficher les données brutes 📋", expanded=False):
        st.write("Les données ci-dessous contiennent des informations détaillées sur les facteurs de risque au fil des années.")
        st.dataframe(evolution_data)
        csv_data = evolution_data.to_csv(index=False)
        st.download_button("📥 Télécharger les données", data=csv_data, file_name="facteurs_de_risque.csv", mime="text/csv")

    # Sélection dynamique
    selected_year = st.slider("Sélectionnez une année", min_value=int(evolution_data["year"].min()),
                              max_value=int(evolution_data["year"].max()), value=int(evolution_data["year"].max()), key="overview_year")
    selected_sex = st.radio("Sélectionnez le sexe :", options=["Les deux", "Homme", "Femme"], index=0, horizontal=True, key="overview_sex")

    # Visualisation
    pie_data = evolution_data[
        (evolution_data["metric"] == "%") & 
        (evolution_data["sex"] == selected_sex) & 
        (evolution_data["year"] == selected_year)
    ]

    fig1 = px.pie(
        pie_data, values='val', names='rei', title=f"Répartition des décès par facteur ({selected_sex}) - {selected_year}",
        hole=0.3
    )
    st.plotly_chart(fig1, use_container_width=True)


def display_tobacco_alcohol():
    """
    Visualisation des données tabac et alcool.
    """
    evolution_data = dl.load_evolution_facteurs()
    data_alcohol = dl.load_data_alcohol()

    # Section des données
    st.write("### Décès liés au tabac et alcool, par catégorie de personne")
    selected_year = st.slider("Sélectionnez une année", min_value=int(evolution_data["year"].min()),
                              max_value=int(evolution_data["year"].max()), value=int(evolution_data["year"].max()), key="alcohol_year")

    # Totaux dynamiques
    col1, col2, col3 = st.columns(3)
    col1.metric("Hommes", "123,456")
    col2.metric("Femmes", "78,901")
    col3.metric("Adolescents", "45,678")

    # Tendances temporelles
    trend_data = evolution_data[
        (evolution_data["metric"] == "#") & 
        (evolution_data["rei"].isin(["Tabac", "Consommation d’alcool"]))
    ]
    fig = px.line(
        trend_data, x="year", y="val", color="rei", title="Tendances des décès liés au tabac et alcool", markers=True
    )
    st.plotly_chart(fig, use_container_width=True)


def display_metabolic_risks():
    """
    Visualisation des risques métaboliques et outils interactifs.
    """
    indicators = {
        "Obésité (IMC ≥30)": "NCD_BMI_30A",
        "Hypertension (PAS ≥140 ou PAD ≥90)": "BP_04",
        "Glycémie élevée (≥7.0 mmol/L)": "NCD_GLUC_04"
    }

    selected_indicator_name = st.selectbox("Choisissez un indicateur", list(indicators.keys()), key="indicator_selection")
    indicator_code = indicators[selected_indicator_name]
    data = dl.load_metabolic_risk_data(indicator_code)

    if data.empty:
        st.warning("Aucune donnée disponible.")
        return

    # Carte interactive
    st.write(f"### Carte interactive : {selected_indicator_name}")
    fig = px.choropleth(
        data, locations="pays", color="valeur", hover_name="pays", 
        title=f"{selected_indicator_name}", color_continuous_scale=px.colors.sequential.Plasma
    )
    st.plotly_chart(fig, use_container_width=True)

    # Calculateur d'IMC
    st.write("---")
    st.header("📊 Calculateur d'IMC")
    weight = st.number_input("Poids (kg)", 1, 300, 70, key="weight_input")
    height = st.number_input("Taille (cm)", 50, 250, 170, key="height_input")
    if height > 0:
        bmi = weight / ((height / 100) ** 2)
        st.write(f"### Votre IMC : {bmi:.1f}")








