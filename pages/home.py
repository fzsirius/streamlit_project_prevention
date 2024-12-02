import streamlit as st
import plotly.express as px

def display_home():
    """
    Page d'accueil de l'application
    """
    # En-tête visuel avec emojis
    st.markdown(
        """
        <h1 style="text-align: center; font-family: 'Helvetica'; color: #4CAF50;">
            🌟 Bienvenue sur FacteurSanté 🌟
        </h1>
        <p style="text-align: center; font-size: 16px; font-family: 'Arial'; color: #666;">
            Informer, sensibiliser et encourager des choix de santé positifs grâce à des données claires et interactives.
        </p>
        """,
        unsafe_allow_html=True,
    )
    st.write("---")  # Ligne de séparation esthétique

    # Section Objectifs
    st.markdown(
        """
        <h3 style="text-align: center; color: #FF9800;">🌱 Objectifs de l'application</h3>
        <ul style="font-size: 16px; font-family: 'Arial'; line-height: 1.6;">
            <li><strong>Informer :</strong> Visualisez les principaux facteurs de risque de manière intuitive.</li>
            <li><strong>Sensibiliser :</strong> Comprenez l'impact des risques à l'échelle mondiale et régionale.</li>
            <li><strong>Encourager :</strong> Prenez des décisions de santé éclairées grâce à des données fiables.</li>
        </ul>
        """,
        unsafe_allow_html=True,
    )

    # Espacement pour aérer la page
    st.write("")

    # Introduction au Sunburst
    st.markdown(
        """
        <h3 style="text-align: center; color: #FF9800;">🤔 Qu'est-ce qu'un facteur de risque ?</h3>
        <p style="font-size: 16px; font-family: 'Arial'; line-height: 1.6; color: #555;">
            Un facteur de risque est un élément, un attribut ou un comportement qui augmente la probabilité de développer 
            une maladie ou de subir une blessure. Cela inclut des comportements modifiables tels que le tabagisme, 
            la consommation d'alcool, le surpoids, ou des expositions environnementales comme la pollution.
        </p>
        """,
        unsafe_allow_html=True,
    )

    # Section Diagramme Sunburst
    st.markdown(
        """
        <h3 style="text-align: center; color: #FF9800;">📊 Principaux Facteurs de Risque et Sous-Catégories</h3>
        """,
        unsafe_allow_html=True,
    )

    # Données pour le diagramme en sunburst
    categories = {
        "Risques métaboliques": ["Hypertension", "IMC élevé", "Glycémie élevée", "Cholestérol élevé"],
        "Risques comportementaux": ["Tabagisme", "Consommation d'alcool", "Usage de drogues", "Fumée secondaire"],
        "Risques environnementaux<br>professionnels": ["Pollution de l'air", "Pollution domestique", "Exposition au plomb", "Exposition à l'amiante"]
    }

    # Préparation des données pour le diagramme en sunburst
    labels = ["Facteurs de Risque"] + list(categories.keys()) + [item for sublist in categories.values() for item in sublist]
    parents = [""] + ["Facteurs de Risque"] * len(categories) + [cat for cat, subcats in categories.items() for _ in subcats]

    # Création du diagramme Sunburst avec Plotly
    fig = px.sunburst(
        names=labels,
        parents=parents,
        maxdepth=2,  # Limite la profondeur affichée
        color=labels,  # Couleurs basées sur les labels
        color_discrete_sequence=px.colors.qualitative.Set2  # Palette douce
    )

    # Mise à jour de la mise en page et des traces
    fig.update_layout(
        title=dict(
            x=0.5,  # Centrer le titre horizontalement
            y=0.9,  # Ajuster la hauteur du titre
            font=dict(size=20, family="Helvetica", color="#4CAF50")
        ),
        margin=dict(t=40, l=40, r=40, b=40),  # Marges uniformes
        paper_bgcolor="white",
        font=dict(size=14, family="Arial", color="#333")  # Style général du texte
    )

    fig.update_traces(
        textinfo="label",  # Affiche uniquement les labels
        textfont=dict(size=14),  # Taille du texte adaptée
        marker=dict(line=dict(color="white", width=2))  # Contours blancs pour séparer les sections
    )

    # Affichage du diagramme
    st.plotly_chart(fig, use_container_width=True)


        # Résumé des sources
    st.write("---")
    st.markdown(
        """
        <h3 style="text-align: center; font-family: 'Arial'; color: #FF9800;">📚 Sources de données</h3>
        <p style="text-align: justify; font-size: 16px; font-family: 'Arial'; line-height: 1.6; color: #555;">
            Les données utilisées dans cette application proviennent des sources fiables suivantes :
        </p>
        <ul style="font-size: 16px; font-family: 'Arial'; line-height: 1.6;">
            <li>
                <strong>Organisation Mondiale de la Santé (OMS)</strong> : Données issues de l'Observatoire de la Santé Mondiale (<a href="https://www.who.int/data/gho" target="_blank">WHO</a>).
            </li>
            <li>
                <strong>API OMS</strong> : Accès direct aux données via l'API OMS (<a href="https://ghoapi.azureedge.net/api/" target="_blank">Lien API</a>).
            </li>
            <li>
                <strong>Études de référence</strong> : Statistiques globales sur les facteurs de risque comme l'IMC, le tabagisme, la consommation d'alcool, etc.
            </li>
        </ul>
        """,
        unsafe_allow_html=True,
    )

    # Lien pour explorer davantage
    st.markdown(
        """
        <div style="text-align: center;">
            <a href="https://www.who.int/data/gho" target="_blank" style="font-size: 16px; font-family: 'Arial'; color: #2196F3; text-decoration: none;">
                🌐 Explorer plus de données sur le site de l'OMS
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )


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
