import pandas as pd
import streamlit as st
import plotly.express as px

df_attaquants = pd.read_csv('Attaquants_Big5.csv')

# Identifier le meilleur attaquant de chaque club (par exemple, selon G+A)
meilleurs_att = df_attaquants.loc[df_attaquants.groupby('Squad')['Performance G+A'].idxmax()]

# Streamlit UI
st.title("Comparaison des meilleurs attaquants par club")

# Choix de métriques pour comparer
metric = st.selectbox("Sélectionnez une métrique pour la comparaison :", 
                      ['Performance G+A', 'Expected xG', 'Playing Time Min'])

# Visualisation interactive
fig = px.bar(meilleurs_att, x='Player', y=metric, color='Squad', 
             title=f"Meilleurs attaquants par club - Comparaison selon {metric}",
             text=metric)
st.plotly_chart(fig)

# Détails des attaquants
st.subheader("Détails des meilleurs attaquants")
st.dataframe(meilleurs_att)
