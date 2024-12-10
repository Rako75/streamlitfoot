import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Charger les données
data = pd.read_csv('df_Big5.csv')

# Interface Streamlit : Sélectionner les joueurs
players_choice = st.multiselect('Choisissez des joueurs à comparer', data['Player'].unique())

# Interface Streamlit : Sélectionner les statistiques à comparer
stats_choice = st.multiselect(
    'Choisissez les statistiques à comparer', 
    ['Performance Gls', 'Performance Ast', 'Expected xG', 'Expected xAG', 
     'Progression PrgC', 'Progression PrgP', 'Standard SoT', 'Total Cmp%', 
     'Take-Ons Succ', 'Performance Recov'],
    default=['Performance Gls', 'Performance Ast', 'Expected xG']
)

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
    for player in radar_data_normalized.index:
        fig.add_trace(go.Scatterpolar(
            r=radar_data_normalized.loc[player].values,
            theta=stats_choice,
            fill='toself',
            name=player
        ))

    # Configurer le graphique
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1])
        ),
        showlegend=True,
        title="Comparaison des joueurs (Radar Chart)"
    )

    # Afficher le radar chart
    st.plotly_chart(fig)

else:
    st.write("Veuillez sélectionner au moins un joueur et une statistique pour afficher le radar chart.")
