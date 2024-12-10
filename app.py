import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Charger les données
data = pd.read_csv('df_Big5.csv')

# Interface Streamlit : Sélectionner plusieurs joueurs
players_choice = st.multiselect('Choisissez des joueurs à comparer', data['Player'].unique())

# Vérifier si des joueurs ont été choisis
if len(players_choice) > 0:
    # Filtrer les données selon les joueurs choisis
    filtered_data = data[data['Player'].isin(players_choice)]

    # Interface Streamlit : Choisir la statistique à comparer
    stat_choice = st.selectbox('Choisissez une statistique à comparer', 
                               ['Playing Time Min', 'Take-Ons Succ', 'Carries TotDist', 'Goals', 'Passes'])

    # Créer un graphique en barres pour comparer les joueurs sur la statistique choisie
    plt.figure(figsize=(10, 6))
    sns.barplot(data=filtered_data, x='Player', y=stat_choice, palette="viridis")

    # Ajouter des détails au graphique
    plt.title(f'Comparaison des joueurs sur la statistique: {stat_choice}', fontsize=16)
    plt.xlabel('Joueur', fontsize=12)
    plt.ylabel(stat_choice, fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Afficher le graphique dans Streamlit
    st.pyplot(plt)

else:
    st.write("Veuillez sélectionner au moins un joueur pour effectuer la comparaison.")
