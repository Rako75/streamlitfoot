import os
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

# Interface Streamlit
st.title("Assistant Ballon d'Or avec Gemini")
st.markdown("Posez vos questions sur le Ballon d'Or et obtenez des réponses intelligentes grâce à Gemini !")

# Entrée de question
prompt = st.text_area(
    "Posez votre question :",
    placeholder="Exemple : Qui sont les nominés pour le Ballon d'Or 2023 ? Quelles sont les statistiques de Lionel Messi cette saison ?",
)

# Actions
if st.button("Obtenir une réponse"):
    if prompt:
        # Génération de réponse avec Gemini
        answer = generate_response(prompt)

        # Affichage de la réponse
        st.markdown(f"**Réponse :** {answer}")
    else:
        st.error("Veuillez entrer une question avant de cliquer sur le bouton.")
