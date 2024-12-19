import os
import streamlit as st
import google.generativeai as genai
import pandas as pd

# Définir la clé API Gemini
os.environ["GEMINI_API_KEY"] = "votre_clé_API_GEMINI"  # Remplacez par votre clé API Gemini

# Configurer l'API Gemini
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

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

# Charger la base de données des statistiques des joueurs
df = pd.read_csv('df_Big5.csv')

# Fonction pour générer une réponse avec Gemini
def generate_response(prompt):
    """Utilise Gemini pour générer des réponses basées sur un prompt."""
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(prompt)
    return response.text

# Fonction pour obtenir les statistiques d'un joueur
def get_player_stats(player_name):
    player_data = df[df['Player'].str.contains(player_name, case=False)]
    
    if player_data.empty:
        return f"Aucun joueur trouvé avec le nom {player_name}."
    
    player_stats = player_data[['Player', 'Performance Gls', 'Performance Ast', 'Performance G+A', 'Performance G-PK', 'League', 'Age', 'Position']]
    return player_stats.to_string(index=False)

# Fonction pour obtenir les meilleurs buteurs d'une ligue
def get_top_scorers(league_name):
    league_data = df[df['League'].str.contains(league_name, case=False)]
    
    # Trier les joueurs par nombre de buts marqués
    top_scorers = league_data[['Player', 'Performance Gls']].sort_values(by='Performance Gls', ascending=False).head(5)
    return top_scorers.to_string(index=False)

# Fonction pour comparer deux joueurs
def compare_players(player_name1, player_name2):
    player_data1 = df[df['Player'].str.contains(player_name1, case=False)]
    player_data2 = df[df['Player'].str.contains(player_name2, case=False)]
    
    if player_data1.empty or player_data2.empty:
        return "Un ou les deux joueurs n'ont pas été trouvés."
    
    stats1 = player_data1[['Player', 'Performance Gls', 'Performance Ast', 'Performance G+A', 'Performance G-PK']].iloc[0]
    stats2 = player_data2[['Player', 'Performance Gls', 'Performance Ast', 'Performance G+A', 'Performance G-PK']].iloc[0]
    
    comparison = f"Comparaison entre {stats1['Player']} et {stats2['Player']}:\n"
    comparison += f"Buts: {stats1['Performance Gls']} vs {stats2['Performance Gls']}\n"
    comparison += f"Passes décisives: {stats1['Performance Ast']} vs {stats2['Performance Ast']}\n"
    comparison += f"Buts + Passes décisives: {stats1['Performance G+A']} vs {stats2['Performance G+A']}\n"
    comparison += f"Buts marqués (sans penaltys): {stats1['Performance G-PK']} vs {stats2['Performance G-PK']}"
    
    return comparison

# Interface Streamlit
st.title("Assistant Football avec Gemini")
st.markdown("Posez vos questions sur le football et obtenez des réponses intelligentes grâce à Gemini !")

# Choisir l'action souhaitée (statistiques, meilleurs buteurs, comparer)
action = st.radio("Que souhaitez-vous savoir ?", ("Statistiques de joueur", "Meilleurs buteurs", "Comparer deux joueurs", "Question générale"))

if action == "Statistiques de joueur":
    player_name = st.text_input("Entrez le nom du joueur :")
    if st.button("Obtenir les statistiques"):
        if player_name:
            stats = get_player_stats(player_name)
            st.text_area("Statistiques du joueur", stats, height=300)
        else:
            st.error("Veuillez entrer le nom d'un joueur.")

elif action == "Meilleurs buteurs":
    league_name = st.text_input("Entrez le nom de la ligue :")
    if st.button("Obtenir les meilleurs buteurs"):
        if league_name:
            top_scorers = get_top_scorers(league_name)
            st.text_area("Meilleurs buteurs", top_scorers, height=300)
        else:
            st.error("Veuillez entrer le nom d'une ligue.")

elif action == "Comparer deux joueurs":
    player1 = st.text_input("Entrez le premier joueur :")
    player2 = st.text_input("Entrez le deuxième joueur :")
    if st.button("Comparer les joueurs"):
        if player1 and player2:
            comparison = compare_players(player1, player2)
            st.text_area("Comparaison des joueurs", comparison, height=300)
        else:
            st.error("Veuillez entrer les noms de deux joueurs.")

elif action == "Question générale":
    prompt = st.text_area("Posez votre question :", placeholder="Exemple : Qui a remporté le Ballon d'Or 2023 ?")
    if st.button("Obtenir une réponse avec Gemini"):
        if prompt:
            answer = generate_response(prompt)
            st.text_area("Réponse avec Gemini", answer, height=300)
        else:
            st.error("Veuillez entrer une question avant de cliquer sur le bouton.")

