import streamlit as st
import pandas as pd
import plotly.graph_objects as go
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
st.title("Évolution des Logos des Équipes")

# Filtrer les données par ligue
leagues = data['league'].unique()  # Suppose que cette colonne contient les noms des ligues
selected_league = st.selectbox("Sélectionnez une ligue :", options=leagues)

# Filtrer les données en fonction de la ligue sélectionnée
filtered_data = data[data['league'] == selected_league]

# Créer un graphique sans points, juste avec les logos
fig = go.Figure()

# Créer une liste pour les frames (année)
frames = []

# Ajouter les logos au graphique pour chaque année
for year in sorted(filtered_data['year'].unique()):
    # Filtrer les données pour l'année actuelle
    year_data = filtered_data[filtered_data['year'] == year]

    # Créer un scatter avec des logos comme images
    frame_data = go.Scatter(
        x=year_data['position'],
        y=year_data['pts'],
        mode="markers",
        marker=dict(size=0),  # Pas de points visibles, uniquement les logos
        hoverinfo="text",
        text=year_data['team']
    )
    
    # Ajouter les logos pour chaque équipe dans cette frame
    frame_images = []
    for i, row in year_data.iterrows():
        if row['logo_url']:  # Vérifier que l'image est disponible
            frame_images.append(
                go.layout.Image(
                    source=row['logo_url'],  # URL en base64
                    x=row['position'],
                    y=row['pts'],
                    xref="x",
                    yref="y",
                    sizex=0.1,  # Ajuster la taille des logos
                    sizey=0.1,  # Ajuster la taille des logos
                    xanchor="center",
                    yanchor="middle"
                )
            )

    # Ajouter les images de logos dans la frame
    frames.append(go.Frame(data=[frame_data], layout=dict(images=frame_images), name=str(year)))

# Ajouter les frames pour l'animation
fig.frames = frames

# Mettre à jour le layout pour l'animation
fig.update_layout(
    title=f"Évolution des Logos en {selected_league}",
    xaxis_title="Position (Classement)",
    yaxis_title="Points",
    template="plotly_dark",
    updatemenus=[dict(
        type="buttons",
        showactive=False,
        buttons=[dict(
            label="Play",
            method="animate",
            args=[None, dict(frame=dict(duration=500, redraw=True), fromcurrent=True)]
        )]
    )]
)

# Afficher le graphique dans Streamlit
st.plotly_chart(fig)
