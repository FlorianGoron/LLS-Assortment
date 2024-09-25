import streamlit as st
import pandas as pd

def display_lls_assortment_page():
    # Exemple de données d'articles (liste actuelle)
    articles = [
        {'cod_art': 1, 'size_art': 10},
        {'cod_art': 5, 'size_art': 25},
        {'cod_art': 7, 'size_art': 15},
        {'cod_art': 8, 'size_art': 20},
        {'cod_art': 9, 'size_art': 5},
        {'cod_art': 10, 'size_art': 25},
        {'cod_art': 11, 'size_art': 10},
        {'cod_art': 12, 'size_art': 15},
        {'cod_art': 13, 'size_art': 20},
    ]

    # Vérifier si les articles optimaux sont déjà calculés
    if 'optimal_articles' in st.session_state:
        optimal_articles = st.session_state['optimal_articles']
    else:
        st.warning("Veuillez d'abord exécuter la simulation pour obtenir la liste optimale d'articles.")
        return

    # Convertir les données en DataFrame
    df_articles = pd.DataFrame(articles)
    df_optimal_articles = pd.DataFrame(optimal_articles)

    # Convertir les colonnes 'cod_art' en type str pour les deux DataFrames
    df_articles['cod_art'] = df_articles['cod_art'].astype(str)
    df_optimal_articles['cod_art'] = df_optimal_articles['cod_art'].astype(str)

    # Fusionner les deux DataFrames pour identifier les articles communs, etc.
    merged_df = pd.merge(df_articles, df_optimal_articles, on='cod_art', how='outer', suffixes=('_current', '_optimal'))
    merged_df['size_art (m3)'] = merged_df['size_art_current'].combine_first(merged_df['size_art_optimal']).round(2).astype(str)
    merged_df['status'] = merged_df.apply(lambda row: 'Common' if pd.notna(row['size_art_current']) and pd.notna(row['size_art_optimal'])
                                          else ('Only in current' if pd.notna(row['size_art_current']) else 'Only in optimal'), axis=1)

    display_df = merged_df[['cod_art', 'size_art (m3)', 'status']].sort_values(by='status', ascending=True)

    def color_rows(row):
        if row['status'] == 'Common':
            return ['background-color: lightgreen']*len(row)
        elif row['status'] == 'Only in current':
            return ['background-color: lightcoral']*len(row)
        elif row['status'] == 'Only in optimal':
            return ['background-color: lightblue']*len(row)

    st.title("Comparison of current and optimal assortments")
    st.dataframe(display_df.style.apply(color_rows, axis=1), height=600, width=1200)
