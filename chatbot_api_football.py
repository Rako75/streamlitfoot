import os
import pandas as pd
import google.generativeai as genai
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Définir la clé API Gemini
os.environ["GEMINI_API_KEY"] = "AIzaSyCqozHPzc1NRb-Xf4t6DEYTDIutFcOe_bU"

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

# Fonction pour afficher un histogramme des buts
def plot_histogram(data, column, title, xlabel):
    plt.figure(figsize=(10, 6))
    sns.histplot(data[column], kde=True, color="blue", bins=15)
    plt.title(title, fontsize=16)
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel("Fréquence", fontsize=12)
    st.pyplot(plt)

# Fonction pour obtenir les statistiques d'un joueur
def get_player_stats(player_name, position_data):
    player_data = position_data[position_data['Joueur'].str.contains(player_name, case=False)]
    
    if player_data.empty:
        return f"Aucun joueur trouvé avec le nom {player_name}."
    
    player_stats = player_data.iloc[0]
    
    if position_data is attaquants:
        response = (
            f"{player_name} :\n"
            f"- Buts : {player_stats['Buts']}\n"
            f"- Passes décisives : {player_stats['Passes décisives']}\n"
            f"- Minutes jouées : {player_stats['Minutes jouées']}\n"
        )
    elif position_data is milieux:
        response = (
            f"{player_name} :\n"
            f"- Passes décisives : {player_stats['Passes décisives']}\n"
            f"- Passes progressives : {player_stats['Passes progressives']}\n"
            f"- Courses progressives : {player_stats['Courses progressives']}\n"
        )
    elif position_data is defenseurs:
        response = (
            f"{player_name} :\n"
            f"- Tacles réussis : {player_stats['Tacles réussis']}\n"
            f"- Interceptions : {player_stats['Interceptions']}\n"
            f"- Minutes jouées : {player_stats['Minutes jouées']}\n"
        )
    
    return response

# Fonction pour obtenir les meilleurs buteurs d'une ligue
def get_top_scorers(league_name, position_data):
    league_data = position_data[position_data['Ligue'].str.contains(league_name, case=False)]
    top_scorers = league_data[['Joueur', 'Buts']].sort_values(by='Buts', ascending=False).head(5)
    
    response = f"Meilleurs buteurs de la {league_name} :\n"
    for index, row in top_scorers.iterrows():
        response += f"- {row['Joueur']} avec {row['Buts']} buts.\n"
    
    # Afficher un graphique des meilleurs buteurs
    plt.figure(figsize=(8, 5))
    sns.barplot(x='Buts', y='Joueur', data=top_scorers, palette='coolwarm')
    plt.title(f"Top 5 buteurs de la {league_name}", fontsize=16)
    plt.xlabel("Buts", fontsize=12)
    plt.ylabel("Joueur", fontsize=12)
    st.pyplot(plt)
    
    return response

# Fonction pour comparer deux joueurs
def compare_players(player_name1, player_name2, position_data):
    player_data1 = position_data[position_data['Joueur'].str.contains(player_name1, case=False)]
    player_data2 = position_data[position_data['Joueur'].str.contains(player_name2, case=False)]
    
    if player_data1.empty or player_data2.empty:
        return "Un ou les deux joueurs n'ont pas été trouvés."
    
    stats1 = player_data1.iloc[0]
    stats2 = player_data2.iloc[0]
    
    comparison = f"Comparaison entre {stats1['Joueur']} et {stats2['Joueur']} :\n"
    
    if position_data is attaquants:
        comparison += (
            f" - Buts : {stats1['Buts']} vs {stats2['Buts']}\n"
            f" - Passes décisives : {stats1['Passes décisives']} vs {stats2['Passes décisives']}\n"
        )
    elif position_data is milieux:
        comparison += (
            f" - Passes progressives : {stats1['Passes progressives']} vs {stats2['Passes progressives']}\n"
            f" - Courses progressives : {stats1['Courses progressives']} vs {stats2['Courses progressives']}\n"
        )
    elif position_data is defenseurs:
        comparison += (
            f" - Tacles réussis : {stats1['Tacles réussis']} vs {stats2['Tacles réussis']}\n"
            f" - Interceptions : {stats1['Interceptions']} vs {stats2['Interceptions']}\n"
        )
    
    # Graphique de comparaison
    metrics = ['Buts', 'Passes décisives'] if position_data is attaquants else (
              ['Passes progressives', 'Courses progressives'] if position_data is milieux else
              ['Tacles réussis', 'Interceptions'])
    values1 = [stats1[metric] for metric in metrics]
    values2 = [stats2[metric] for metric in metrics]
    
    plt.figure(figsize=(10, 5))
    x = range(len(metrics))
    plt.bar(x, values1, width=0.4, label=stats1['Joueur'], align='center')
    plt.bar([p + 0.4 for p in x], values2, width=0.4, label=stats2['Joueur'], align='center')
    plt.xticks([p + 0.2 for p in x], metrics)
    plt.title("Comparaison des joueurs", fontsize=16)
    plt.legend()
    st.pyplot(plt)
    
    return comparison

# Interface Streamlit
st.title("Assistant Football avec Gemini")
st.markdown("Posez vos questions sur le football et obtenez des réponses intelligentes grâce à Gemini !")

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

if action == "Question générale":
    st.markdown("Posez une question sur le football.")
    prompt = st.text_area("Votre question :")
    if st.button("Obtenir une réponse"):
        if prompt:
            answer = generate_response(f"Répondre uniquement sur le football : {prompt}")
            st.markdown(f"**Réponse :** {answer}")
        else:
            st.error("Veuillez entrer une question.")
