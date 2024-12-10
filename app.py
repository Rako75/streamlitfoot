import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Charger les données
data = pd.read_csv('df_Big5.csv')

# Interface Streamlit : Choisir la catégorie à visualiser
category_choice = st.selectbox('Choisissez une catégorie', ['Position', 'League'])

# Calculer la répartition des catégories choisies
category_counts = data[category_choice].value_counts()

# Créer un graphique circulaire
plt.figure(figsize=(8, 8))
category_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90, cmap='Set3')

# Ajouter un titre
plt.title(f'Repartition des joueurs par {category_choice}', fontsize=16)

# Afficher le graphique dans Streamlit
st.pyplot(plt)
