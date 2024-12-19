import os
import pandas as pd
import streamlit as st
import google.generativeai as genai

# Définir la clé API Gemini
os.environ["GEMINI_API_KEY"] = "AIzaSyCqozHPzc1NRb-Xf4t6DEYTDIutFcOe_bU"

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

# Fonction pour générer une réponse avec Gemini
def generate_response(prompt):
    """Utilise Gemini pour générer des réponses basées sur un prompt."""
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(prompt)
    return response.text

# Chargement des datasets
attaquants = pd.read_csv('Attaquants_Big5.csv')
milieux = pd.read_csv('Milieux_Big5.csv')
defenseurs = pd.read_csv('Defenseurs_Big5.csv')

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

# Interface Streamlit
st.title("Assistant Foot avec Gemini")
st.markdown("Posez vos questions générales sur le football ou demandez des statistiques spécifiques sur les joueurs !")

# Entrée de question
prompt = st.text_area(
    "Posez votre question :",
    placeholder="Exemple : Qui sont les meilleurs attaquants de la saison ? Quelles sont les statistiques de Lionel Messi cette saison ?",
)

# Actions
if st.button("Obtenir une réponse"):
    if prompt:
        # Si la question est générale, utiliser Gemini pour générer une réponse
        if "meilleurs" in prompt or "statistiques" in prompt:
            answer = generate_response(prompt)
            st.markdown(f"**Réponse générale :** {answer}")
        # Si la question est spécifique à un joueur
        else:
            player_name = prompt
            # Déterminer la position du joueur et récupérer les données correspondantes
            if player_name in attaquants['Player'].values:
                answer = get_player_stats(player_name, attaquants)
            elif player_name in milieux['Player'].values:
                answer = get_player_stats(player_name, milieux)
            elif player_name in defenseurs['Player'].values:
                answer = get_player_stats(player_name, defenseurs)
            else:
                answer = f"Le joueur {player_name} n'a pas été trouvé dans la base de données."
            st.markdown(f"**Réponse spécifique :** {answer}")
    else:
        st.error("Veuillez entrer une question avant de cliquer sur le bouton.")
