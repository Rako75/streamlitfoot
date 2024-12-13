# -*- coding: utf-8 -*-
"""Chatbot_API_Football.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1P1eRKkMWfyyYl0xQP3CKQGEJGbFRr6u3
"""

!pip install openai streamlit requests

import streamlit as st
import openai
import requests

# Configurer les clés API
OPENAI_API_KEY = "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"
FOOTBALL_API_KEY = "f50308e571124a3393a11df1307c789e"
FOOTBALL_BASE_URL = "https://api.football-data.org/v4"

# Configurer OpenAI
openai.api_key = OPENAI_API_KEY

# Fonction pour appeler l'API de football
def get_football_data(endpoint):
    headers = {"X-Auth-Token": FOOTBALL_API_KEY}
    response = requests.get(f"{FOOTBALL_BASE_URL}/{endpoint}", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Impossible de récupérer les données."}

# Fonction pour générer une réponse avec GPT
def generate_response(prompt):
    try:
        completion = openai.Completion.create(
            engine="text-davinci-003",  # Vous pouvez ajuster avec GPT-4 si disponible
            prompt=prompt,
            max_tokens=150,
            temperature=0.7,
        )
        return completion.choices[0].text.strip()
    except Exception as e:
        return f"Erreur lors de l'appel au modèle GPT : {Str(e)}"

# Interface Streamlit
st.title("Chatbot Football ⚽")
st.write("Posez une question sur le football, comme : 'Quel est le classement de la Ligue 1 ?' ou 'Prochains matchs de PSG ?'")

# Champ de saisie utilisateur
user_question = st.text_input("Votre question :")

if user_question:
    # Analyse de la question
    if "classement" in user_question.lower():
        st.write("🔄 Recherche des informations...")
        # Exemple pour la Premier League
        league_code = "FL1"  # Code pour la Ligue 1, à adapter dynamiquement
        data = get_football_data(f"competitions/{league_code}/standings")
        if "error" not in data:
            standings = data.get("standings", [])[0].get("table", [])
            response = "\n".join(
                [f"{team['position']}. {team['team']['name']} - {team['points']} pts" for team in standings]
            )
        else:
            response = data["error"]

    elif "match" in user_question.lower():
        st.write("🔄 Recherche des informations sur les matchs...")
        # Exemple pour le PSG
        team_name = "Paris Saint-Germain"
        team_data = get_football_data("teams/524/matches")  # ID PSG : 524 (API Football Data)
        if "error" not in team_data:
            matches = team_data.get("matches", [])
            response = "\n".join(
                [f"{match['homeTeam']['name']} vs {match['awayTeam']['name']} - {match['utcDate']}" for match in matches]
            )
        else:
            response = team_data["error"]

    else:
        # Envoi à GPT pour une réponse générale
        st.write("🤖 Génération de la réponse...")
        gpt_prompt = f"Tu es un assistant expert en football. Réponds à la question suivante : {user_question}"
        response = generate_response(gpt_prompt)

    # Afficher la réponse
    st.success(response)
