import os
import pandas as pd
import google.generativeai as genai
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from math import pi

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

# Fonction pour créer un radar chart
def create_radar_chart(player1_stats, player2_stats, stats_labels, title):
    # Nombre de critères
    categories = stats_labels
    N = len(categories)

    # Valeurs pour les deux joueurs
    player1_values = [player1_stats[label] for label in categories]
    player2_values = [player2_stats[label] for label in categories]

    # Calculer l'angle entre chaque axe
    angles = [n / float(N) * 2 * pi for n in range(N)]
    player1_values += player1_values[:1]
    player2_values += player2_values[:1]
    angles += angles[:1]

    # Créer le graphique radar
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)

    # Tracer les lignes pour les deux joueurs
    ax.plot(angles, player1_values, color='b', linewidth=2, linestyle='solid', label="Joueur 1")
    ax.plot(angles, player2_values, color='r', linewidth=2, linestyle='solid', label="Joueur 2")

    # Remplir les zones sous les courbes
    ax.fill(angles, player1_values, color='b', alpha=0.4)
    ax.fill(angles, player2_values, color='r', alpha=0.4)

    # Ajouter des labels
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)

    # Ajouter le titre
    plt.title(title, size=20, color='black', y=1.1)

    # Ajouter une légende
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

    # Afficher le graphique
    st.pyplot(fig)

# Interface Streamlit
st.title("Assistant Football avec Gemini")
st.markdown("Posez vos questions sur le football et obtenez des réponses intelligentes grâce à Gemini !")

# Choisir l'action souhaitée
action = st.radio("Que souhaitez-vous savoir ?", ("Statistiques de joueur", "Meilleurs buteurs", "Comparer deux joueurs", "Question générale"))

if action == "Comparer deux joueurs":
    position = st.radio("Sélectionnez la position des joueurs", ("Attaquants", "Milieux", "Défenseurs"))
    player1 = st.text_input("Entrez le premier joueur :")
    player2 = st.text_input("Entrez le deuxième joueur :")
    data = attaquants if position == "Attaquants" else milieux if position == "Milieux" else defenseurs

    if st.button("Comparer les joueurs"):
        if player1 and player2:
            player1_data = data[data['Joueur'].str.contains(player1, case=False)]
            player2_data = data[data['Joueur'].str.contains(player2, case=False)]

            if not player1_data.empty and not player2_data.empty:
                player1_stats = player1_data.iloc[0]
                player2_stats = player2_data.iloc[0]

                # Choisir les critères de comparaison
                if position == "Attaquants":
                    stats_labels = ['Buts', 'Passes decisives', 'Buts + Passes décisives', 'Buts par 90 minutes', 'Tirs']
                elif position == "Milieux":
                    stats_labels = ['Passes decisives', 'Buts + Passes décisives', 'Passes progressives', 'Courses progressives', 'Passes vers le dernier tiers']
                elif position == "Défenseurs":
                    stats_labels = ['Tacles reussis', 'Interceptions ', 'Duels aeriens gagnes', 'Actions menant a un tir', 'Passes reussies totales']
                
                create_radar_chart(player1_stats, player2_stats, stats_labels, f"Comparaison entre {player1} et {player2}")
            else:
                st.error("Un ou les deux joueurs n'ont pas été trouvés.")
        else:
            st.error("Veuillez entrer les noms des deux joueurs.")

elif action == "Statistiques de joueur":
    position = st.radio("Sélectionnez la position du joueur", ("Attaquants", "Milieux", "Défenseurs"))
    player_name = st.text_input("Entrez le nom du joueur :")
    data = attaquants if position == "Attaquants" else milieux if position == "Milieux" else defenseurs

    if st.button("Obtenir les statistiques"):
        if player_name:
            stats = get_player_stats(player_name, data, position)
            st.text_area("Statistiques du joueur", stats, height=200)

elif action == "Meilleurs buteurs":
    league_name = st.text_input("Entrez le nom de la ligue :")
    position = st.radio("Sélectionnez la position des joueurs", ("Attaquants", "Milieux", "Défenseurs"))
    data = attaquants if position == "Attaquants" else milieux if position == "Milieux" else defenseurs

    if st.button("Obtenir les meilleurs buteurs"):
        if league_name:
            get_top_scorers(league_name, data)
        else:
            st.error("Veuillez entrer le nom d'une ligue.")

elif action == "Question générale":
    prompt = st.text_area("Posez votre question :")
    if st.button("Obtenir une réponse"):
        if prompt:
            answer = generate_response(f"Répondre uniquement sur le football : {prompt}")
            st.markdown(f"**Réponse :** {answer}")
        else:
            st.error("Veuillez entrer une question.")
