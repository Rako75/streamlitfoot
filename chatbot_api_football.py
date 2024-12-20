import os
import pandas as pd
import google.generativeai as genai
import streamlit as st

# Définir la clé API Gemini
os.environ["GEMINI_API_KEY"] = "AIzaSyCqozHPzc1NRb-Xf4t6DEYTDIutFcOe_bU"  # Remplacez par votre clé API

# Configurer l'API Gemini avec la clé API
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Charger les sous-datasets (sans gardiens)
attaquants = pd.read_csv('Attaquants_Big5.csv')
milieux = pd.read_csv('Milieux_Big5.csv')
defenseurs = pd.read_csv('Defenseurs_Big5.csv')

# Configuration du modèle de génération de texte Gemini
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
)

# Fonction pour générer une réponse avec Gemini
def generate_response(prompt):
    """Utilise Gemini pour générer des réponses basées sur un prompt."""
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(prompt)
    return response.text

# Fonction pour obtenir les statistiques d'un joueur
def get_player_stats(player_name, position_data):
    player_data = position_data[position_data['Player'].str.contains(player_name, case=False)]
    
    if player_data.empty:
        return f"Aucun joueur trouvé avec le nom {player_name}."
    
    # Extraire les statistiques pertinentes
    player_stats = player_data.iloc[0]
    
    # Formuler la réponse naturellement
    if position_data is attaquants:
        response = f"{player_name} a marqué {player_stats['Performance Gls']} buts et réalisé {player_stats['Performance Ast']} passes décisives cette saison."
    elif position_data is milieux:
        response = f"{player_name} a enregistré {player_stats['Performance Ast']} passes décisives et contribué à {player_stats['Performance G+A']} buts."
    elif position_data is defenseurs:
        response = f"{player_name} a réalisé {player_stats['Performance TklW']} tacles et {player_stats['Performance Blks']} blocs."
    
    return response

# Fonction pour obtenir les meilleurs buteurs d'une ligue
def get_top_scorers(league_name, position_data):
    league_data = position_data[position_data['League'].str.contains(league_name, case=False)]
    
    # Trier les joueurs par nombre de buts marqués
    top_scorers = league_data[['Player', 'Performance Gls']].sort_values(by='Performance Gls', ascending=False).head(5)
    
    response = f"Voici les meilleurs buteurs de la {league_name} :\n"
    for index, row in top_scorers.iterrows():
        response += f"{row['Player']} avec {row['Performance Gls']} buts.\n"
    
    return response

# Fonction pour comparer deux joueurs
def compare_players(player_name1, player_name2, position_data):
    player_data1 = position_data[position_data['Player'].str.contains(player_name1, case=False)]
    player_data2 = position_data[position_data['Player'].str.contains(player_name2, case=False)]
    
    if player_data1.empty or player_data2.empty:
        return "Un ou les deux joueurs n'ont pas été trouvés."
    
    stats1 = player_data1.iloc[0]
    stats2 = player_data2.iloc[0]
    
    comparison = f"Comparaison entre {stats1['Player']} et {stats2['Player']} :\n"
    
    if position_data is attaquants:
        comparison += f" - Buts : {stats1['Performance Gls']} vs {stats2['Performance Gls']}\n"
        comparison += f" - Passes décisives : {stats1['Performance Ast']} vs {stats2['Performance Ast']}\n"
    elif position_data is milieux:
        comparison += f" - Passes décisives : {stats1['Performance Ast']} vs {stats2['Performance Ast']}\n"
        comparison += f" - Contributions (Buts + Passes) : {stats1['Performance G+A']} vs {stats2['Performance G+A']}\n"
    elif position_data is defenseurs:
        comparison += f" - Tacles réalisés : {stats1['Performance TklW']} vs {stats2['Performance TklW']}\n"
        comparison += f" - Blocs réalisés : {stats1['Performance Blks']} vs {stats2['Performance Blks']}\n"
    
    return comparison

# Interface Streamlit
st.title("Assistant Football avec Gemini")
st.markdown("Posez vos questions sur le football et obtenez des réponses intelligentes grâce à Gemini !")

# Choisir l'action souhaitée (statistiques, meilleurs buteurs, comparer)
action = st.radio("Que souhaitez-vous savoir ?", ("Statistiques de joueur", "Meilleurs buteurs", "Comparer deux joueurs", "Question générale"))

if action == "Statistiques de joueur":
    position = st.radio("Sélectionnez la position du joueur", ("Attaquants", "Milieux", "Défenseurs"))
    player_name = st.text_input("Entrez le nom du joueur :")
    
    if position == "Attaquants":
        data = attaquants
    elif position == "Milieux":
        data = milieux
    elif position == "Défenseurs":
        data = defenseurs
    
    if st.button("Obtenir les statistiques"):
        if player_name:
            stats = get_player_stats(player_name, data)
            st.text_area("Statistiques du joueur", stats, height=200)
        else:
            st.error("Veuillez entrer le nom d'un joueur.")

elif action == "Meilleurs buteurs":
    league_name = st.text_input("Entrez le nom de la ligue :")
    position = st.radio("Sélectionnez la position des joueurs", ("Attaquants", "Milieux", "Défenseurs"))
    
    if position == "Attaquants":
        data = attaquants
    elif position == "Milieux":
        data = milieux
    elif position == "Défenseurs":
        data = defenseurs
    
    if st.button("Obtenir les meilleurs buteurs"):
        if league_name:
            top_scorers = get_top_scorers(league_name, data)
            st.text_area("Meilleurs buteurs", top_scorers, height=200)
        else:
            st.error("Veuillez entrer le nom d'une ligue.")

elif action == "Comparer deux joueurs":
    position = st.radio("Sélectionnez la position des joueurs", ("Attaquants", "Milieux", "Défenseurs"))
    player1 = st.text_input("Entrez le premier joueur :")
    player2 = st.text_input("Entrez le deuxième joueur :")
    
    if position == "Attaquants":
        data = attaquants
    elif position == "Milieux":
        data = milieux
    elif position == "Défenseurs":
        data = defenseurs
    
    if st.button("Comparer les joueurs"):
        if player1 and player2:
            comparison = compare_players(player1, player2, data)
            st.text_area("Comparaison des joueurs", comparison, height=200)
        else:
            st.error("Veuillez entrer les noms des deux joueurs.")

# Question générale avec Gemini
if action == "Question générale":
    st.markdown("**Note**: Veuillez poser uniquement des questions liées au football.")
    
    prompt = st.text_area(
        "Posez votre question :",
        placeholder="Exemple : Qui sont les nominés pour le Ballon d'Or 2023 ? Quelles sont les statistiques de Lionel Messi cette saison ?",
    )

    if st.button("Obtenir une réponse"):
        if prompt:
            # Génération de réponse avec Gemini
            answer = generate_response(f"Répondre uniquement sur le football : {prompt}")
            st.markdown(f"**Réponse :** {answer}")
        else:
            st.error("Veuillez entrer une question avant de cliquer sur le bouton.")
