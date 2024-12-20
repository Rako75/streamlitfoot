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

# Fonction pour charger un fichier CSV avec gestion des encodages
def load_csv_with_encoding(file_path):
    encodings = ['utf-8', 'iso-8859-1', 'latin1']  # Liste des encodages courants
    for encoding in encodings:
        try:
            return pd.read_csv(file_path, encoding=encoding)
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Impossible de lire le fichier {file_path} avec les encodages essayés.")

# Charger les sous-datasets (sans gardiens)
try:
    attaquants = load_csv_with_encoding('Attaquants_Big5.csv')
    milieux = load_csv_with_encoding('Milieux_Big5.csv')
    defenseurs = load_csv_with_encoding('Defenseurs_Big5.csv')
except ValueError as e:
    st.error(f"Erreur lors du chargement des fichiers : {e}")
    st.stop()

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

# Fonction pour afficher un histogramme
def plot_histogram(data, column, title):
    plt.figure(figsize=(10, 6))
    sns.histplot(data[column], kde=False, bins=15, color='blue')
    plt.title(title)
    plt.xlabel(column)
    plt.ylabel('Fréquence')
    st.pyplot(plt)

# Fonction pour obtenir les statistiques d'un joueur
def get_player_stats(player_name, position_data, position):
    player_data = position_data[position_data['Joueur'].str.contains(player_name, case=False)]
    
    if player_data.empty:
        return f"Aucun joueur trouvé avec le nom {player_name}."
    
    player_stats = player_data.iloc[0]
    if position == "Attaquants":
        return f"{player_name} a marqué {player_stats['Buts']} buts et réalisé {player_stats['Passes decisives']} passes décisives."
    elif position == "Milieux":
        return f"{player_name} a enregistré {player_stats['Passes decisives']} passes décisives et contribué à {player_stats['Buts']} buts."
    elif position == "Défenseurs":
        return f"{player_name} a réalisé {player_stats['Tacles reussis']} tacles et {player_stats['Interceptions ']} interceptions."

# Fonction pour obtenir les meilleurs buteurs d'une ligue
def get_top_scorers(league_name, position_data):
    league_data = position_data[position_data['Ligue'].str.contains(league_name, case=False)]
    top_scorers = league_data[['Joueur', 'Buts']].sort_values(by='Buts', ascending=False).head(5)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Buts', y='Joueur', data=top_scorers, palette='viridis')
    plt.title(f"Top 5 buteurs de la {league_name}")
    plt.xlabel("Nombre de buts")
    plt.ylabel("Joueur")
    st.pyplot(plt)

    return top_scorers

# Interface Streamlit
st.title("Assistant Football avec Gemini")
st.markdown("Posez vos questions sur le football et obtenez des réponses intelligentes grâce à Gemini !")

# Choisir l'action souhaitée
action = st.radio("Que souhaitez-vous savoir ?", ("Statistiques de joueur", "Meilleurs buteurs", "Comparer deux joueurs", "Question générale"))

if action == "Statistiques de joueur":
    position = st.radio("Sélectionnez la position du joueur", ("Attaquants", "Milieux", "Défenseurs"))
    player_name = st.text_input("Entrez le nom du joueur :")
    data = attaquants if position == "Attaquants" else milieux if position == "Milieux" else defenseurs

    if st.button("Obtenir les statistiques"):
        if player_name:
            stats = get_player_stats(player_name, data, position)
            st.text_area("Statistiques du joueur", stats, height=200)

            # Graphique de répartition
            st.markdown("### Graphique : Répartition des statistiques")
            if position == "Attaquants":
                plot_histogram(data, 'Buts', "Répartition des buts - Attaquants")
            elif position == "Milieux":
                plot_histogram(data, 'Passes decisives', "Répartition des passes décisives - Milieux")
            elif position == "Défenseurs":
                plot_histogram(data, 'Interceptions ', "Répartition des interceptions - Défenseurs")
        else:
            st.error("Veuillez entrer le nom d'un joueur.")

elif action == "Meilleurs buteurs":
    league_name = st.text_input("Entrez le nom de la ligue :")
    position = st.radio("Sélectionnez la position des joueurs", ("Attaquants", "Milieux", "Défenseurs"))
    data = attaquants if position == "Attaquants" else milieux if position == "Milieux" else defenseurs

    if st.button("Obtenir les meilleurs buteurs"):
        if league_name:
            get_top_scorers(league_name, data)
        else:
            st.error("Veuillez entrer le nom d'une ligue.")

elif action == "Comparer deux joueurs":
    position = st.radio("Sélectionnez la position des joueurs", ("Attaquants", "Milieux", "Défenseurs"))
    player1 = st.text_input("Entrez le premier joueur :")
    player2 = st.text_input("Entrez le deuxième joueur :")
    data = attaquants if position == "Attaquants" else milieux if position == "Milieux" else defenseurs

    if st.button("Comparer les joueurs"):
        if player1 and player2:
            # Comparaison visuelle et textuelle non implémentée dans cette version
            st.markdown("Comparaison à venir")
        else:
            st.error("Veuillez entrer les noms des deux joueurs.")

elif action == "Question générale":
    prompt = st.text_area("Posez votre question :")
    if st.button("Obtenir une réponse"):
        if prompt:
            answer = generate_response(f"Répondre uniquement sur le football : {prompt}")
            st.markdown(f"**Réponse :** {answer}")
        else:
            st.error("Veuillez entrer une question.")
