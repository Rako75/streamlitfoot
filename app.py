import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# Charger le dataset
data = pd.read_csv('understat.com.csv')

# Ajouter l'URL de base pour les logos
GITHUB_BASE_URL = "https://raw.githubusercontent.com/Rako75/streamlitfoot/main/Premier%20League/"
DEFAULT_LOGO = f"{GITHUB_BASE_URL}default.png"

# Vérification des URLs
def is_valid_logo_url(url):
    try:
        response = requests.head(url)
        return response.status_code == 200
    except:
        return False

# Ajouter une colonne avec les URLs des logos
data['logo_url'] = data['team'].apply(lambda x: f"{GITHUB_BASE_URL}{x.replace(' ', '_')}.png")
data['logo_url'] = data['logo_url'].apply(lambda url: url if is_valid_logo_url(url) else DEFAULT_LOGO)

# Titre de l'application
st.title("Évolution des Points des Équipes par Ligue avec Logos")

# Filtrer les données par ligue
leagues = data['league'].unique()  # Suppose que cette colonne contient les noms des ligues
selected_league = st.selectbox("Sélectionnez une ligue :", options=leagues)

# Filtrer les données en fonction de la ligue sélectionnée
filtered_data = data[data['league'] == selected_league]

# Animation des points par année avec logos
st.subheader(f"Évolution des Points pour {selected_league}")

# Créer un graphique interactif avec animation
fig_animation = px.scatter(
    filtered_data,
    x="position",
    y="pts",
    animation_frame="year",
    size="pts",
    color="team",
    hover_name="team",
    title=f"Évolution des Points en {selected_league}",
    labels={
        "year": "Année",
        "pts": "Points",
        "position": "Position (Classement)"
    },
    template="plotly_dark"
)

# Ajouter les logos au graphique
for i, row in filtered_data.iterrows():
    fig_animation.add_layout_image(
        dict(
            source=row['logo_url'],
            x=row['position'],
            y=row['pts'],
            xref="x",
            yref="y",
            sizex=2,
            sizey=2,
            xanchor="center",
            yanchor="middle"
        )
    )

# Afficher le graphique dans Streamlit
st.plotly_chart(fig_animation)
