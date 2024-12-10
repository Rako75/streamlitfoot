import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import base64
import os

# Charger le dataset
data = pd.read_csv('understat.com.csv')

# Fonction pour convertir une image en base64
def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return "data:image/png;base64," + base64.b64encode(img_file.read()).decode()

# Ajouter le chemin des logos
LOGO_FOLDER = "Premier League"

# Ajouter une colonne avec les URLs des logos en base64
def get_logo_path(team_name):
    team_logo = f"{team_name.replace(' ', '_')}.png"
    logo_path = os.path.join(LOGO_FOLDER, team_logo)
    if os.path.exists(logo_path):
        return image_to_base64(logo_path)
    else:
        return None  # Si le logo n'existe pas

data['logo_url'] = data['team'].apply(get_logo_path)

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
    if row['logo_url']:  # Vérifier que l'image est disponible
        fig_animation.add_layout_image(
            dict(
                source=row['logo_url'],  # URL en base64
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
