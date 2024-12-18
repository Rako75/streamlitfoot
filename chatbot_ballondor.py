# -*- coding: utf-8 -*-
"""chatbot_ballondor.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1kZW8P3P-1ICdawztOa2j-dmuNrID-zLT
"""

import streamlit as st
import pandas as pd
from transformers import pipeline

# Charger les données filtrées depuis un fichier CSV
@st.cache_data
def load_data():
    data = pd.read_csv('Ballondor2024.csv')  # Remplacez par le chemin de votre fichier CSV
    return data

# Charger le modèle de langage
@st.cache_resource
def load_model():
    return pipeline("question-answering", model="deepset/roberta-base-squad2")  # Modèle QA

# Fonction pour trouver le joueur à partir de la question
def find_player_from_question(question, data):
    for player in data['player']:
        if player.lower() in question.lower():
            return player
    return None

# Récupérer les statistiques et la vidéo d'un joueur
def get_player_info(player_name, data):
    player_data = data[data['player'].str.contains(player_name, case=False, na=False)]
    if not player_data.empty:
        return player_data.iloc[0].to_dict()  # Retourne les infos du joueur sous forme de dictionnaire
    else:
        return None

# Charger les données et le modèle
data = load_data()
model = load_model()

# Interface Streamlit
st.title("🏆 Chatbot Ballon d'Or 2024")
st.write("Posez une question sur un joueur pour découvrir ses statistiques et ses moments forts.")

# Entrée utilisateur
question = st.text_input("Posez une question sur un joueur :")

if question:
    # Trouver le joueur mentionné dans la question
    player_name = find_player_from_question(question, data)

    if player_name:
        # Récupérer les informations du joueur
        player_info = get_player_info(player_name, data)

        if player_info:
            st.subheader(f"📋 Statistiques de {player_name}")
            st.write(f"**Équipe** : {player_info['team']}")
            st.write(f"**Ligue** : {player_info['league']}")
            st.write(f"**Nation** : {player_info['nation']}")
            st.write(f"**Buts** : {player_info['Performance-Gls']}")
            st.write(f"**Passes décisives** : {player_info['Performance-Ast']}")
            st.write(f"**xG attendu** : {player_info['Expected-xG']}")
            st.write(f"**Cartons jaunes** : {player_info['Performance-CrdY']}")
            st.write(f"**Cartons rouges** : {player_info['Performance-CrdR']}")

            # Affichage de la vidéo si disponible
            if pd.notna(player_info['URL']):
                st.video(player_info['URL'])
                st.write(f"🎥 Moments forts de **{player_name}** : [Lien direct]({player_info['URL']})")
            else:
                st.write("❌ Aucune vidéo disponible pour ce joueur.")
        else:
            st.write("❌ Impossible de récupérer les informations pour ce joueur.")
    else:
        st.write("❌ Aucun joueur mentionné dans votre question. Essayez de poser une question différente.")

# **Footer**
st.write("---")
st.write("⚡ Chatbot réalisé avec Streamlit et Hugging Face Transformers.")