import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Charger les données
data = pd.read_csv('df_Big5.csv')

# Filtrer les colonnes numériques uniquement
numeric_columns = data.select_dtypes(include='number').columns.tolist()

# Interface Streamlit : Sélectionner les joueurs
players_choice = st.multiselect('Choisissez des joueurs à comparer', data['Player'].unique())

# Interface Streamlit : Sélectionner les statistiques parmi toutes les colonnes numériques
stats_choice = st.multiselect('Choisissez les statistiques à comparer', numeric_columns, default=numeric_columns[:6])

if len(players_choice) > 0 and len(stats_choice) > 0:
    # Filtrer les données pour les joueurs sélectionnés
    filtered_data = data[data['Player'].isin(players_choice)]

    # Préparer les données pour le radar chart
    radar_data = filtered_data[['Player'] + stats_choice].set_index('Player')

    # Normaliser les données pour un affichage uniforme
    radar_data_normalized = radar_data.copy()
    for col in stats_choice:
        radar_data_normalized[col] = (radar_data[col] - radar_data[col].min()) / (radar_data[col].max() - radar_data[col].min())

    # Créer le radar chart avec Plotly
    fig = go.Figure()

    for idx, player in enumerate(radar_data_normalized.index):
        fig.add_trace(go.Scatterpolar(
            r=radar_data_normalized.loc[player].values,
            theta=stats_choice,
            fill='toself',
            name=player,
            marker=dict(color=px.colors.qualitative.Plotly[idx % len(px.colors.qualitative.Plotly)]),  # Couleurs distinctes
        ))

    # Ajouter des annotations pour chaque point
    for player in radar_data_normalized.index:
        for i, stat in enumerate(stats_choice):
            value = radar_data.loc[player, stat]
            angle = 360 / len(stats_choice) * i
            fig.add_annotation(
                x=0.5,
                y=0.5,
                text=f"{value:.2f}",
                showarrow=False,
                font=dict(size=10),
                xanchor="center",
                yanchor="middle",
                xshift=80 * i * 0.5,  # Ajuster pour éviter la collision
                yshift=80 * i * 0.5,
            )

    # Configurer le graphique
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1], tickvals=[0, 0.5, 1], ticktext=["0", "0.5", "1"])
        ),
        showlegend=True,
        title="Comparaison des joueurs (Radar Chart avec Annotations)",
    )

    # Afficher le radar chart
    st.plotly_chart(fig, use_container_width=True)

else:
    st.write("Veuillez sélectionner au moins un joueur et une statistique pour afficher le radar chart.")
