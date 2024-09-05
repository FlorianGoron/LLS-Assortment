import streamlit as st
import pandas as pd

def display_articles_page():
    # Exemple de données d'articles
    articles = [
        {'cod_art': 1, 'size_art': 10},
        {'cod_art': 2, 'size_art': 15},
        {'cod_art': 3, 'size_art': 20},
        {'cod_art': 4, 'size_art': 5},
        {'cod_art': 5, 'size_art': 25},
        {'cod_art': 6, 'size_art': 10},
        {'cod_art': 7, 'size_art': 15},
        {'cod_art': 8, 'size_art': 20},
        {'cod_art': 9, 'size_art': 5},
        {'cod_art': 10, 'size_art': 25},
        {'cod_art': 11, 'size_art': 10},
        {'cod_art': 12, 'size_art': 15},
        {'cod_art': 13, 'size_art': 20},
        {'cod_art': 14, 'size_art': 5},
        {'cod_art': 15, 'size_art': 25},
    ]

    # Convertir les données en DataFrame pour une meilleure visualisation
    df_articles = pd.DataFrame(articles)

    st.title("Articles visualization")
    st.dataframe(df_articles, height=600, width=1200)