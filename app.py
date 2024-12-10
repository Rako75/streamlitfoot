import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Charger les données
data = pd.read_csv('df_Big5.csv')

# Interface Streamlit : Choisir la ligue
league_choice = st.selectbox('Choisissez une ligue', data['League'].unique())

# Filtrer les données selon la ligue choisie
filtered_data = data[data['League'] == league_choice]

# Créer la boîte à moustaches pour la répartition des âges
plt.figure(figsize=(10, 6))
sns.boxplot(data=filtered_data, x='League', y='Age', palette="Set2")
plt.title(f'Répartition des âges des joueurs en {league_choice}', fontsize=16)
plt.xlabel('Ligue', fontsize=12)
plt.ylabel('Âge', fontsize=12)
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Afficher le graphique dans Streamlit
st.pyplot(plt)
