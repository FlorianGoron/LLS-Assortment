import streamlit as st
import pandas as pd

def display_orders_page():
    # Exemple de données de commandes
    commandes = [
        {'id': 1, 'articles': [4, 9, 3], "tag_agabaritic_order": 1, 'magasin': 'Store 1'},
        {'id': 2, 'articles': [10, 4], "tag_agabaritic_order": 1, 'magasin': 'Store 1'},
        {'id': 3, 'articles': [3, 4], "tag_agabaritic_order": 1, 'magasin': 'Store 1'},
        {'id': 4, 'articles': [5], "tag_agabaritic_order": 1, 'magasin': 'Store 1'},
        {'id': 5, 'articles': [8, 5, 7, 10], "tag_agabaritic_order": 1, 'magasin': 'Store 1'},
        {'id': 6, 'articles': [7, 5], "tag_agabaritic_order": 1, 'magasin': 'Store 1'},
        {'id': 7, 'articles': [10], "tag_agabaritic_order": 1, 'magasin': 'Store 1'},
        {'id': 8, 'articles': [4, 1, 3], "tag_agabaritic_order": 1, 'magasin': 'Store 1'},
        {'id': 9, 'articles': [6, 5], "tag_agabaritic_order": 1, 'magasin': 'Store 1'},
        {'id': 10, 'articles': [2, 5, 1, 8], "tag_agabaritic_order": 1, 'magasin': 'Store 1'},
        {'id': 11, 'articles': [7, 3], "tag_agabaritic_order": 1, 'magasin': 'Store 2'},
        {'id': 12, 'articles': [4, 10, 6], "tag_agabaritic_order": 1, 'magasin': 'Store 2'},
        {'id': 13, 'articles': [3, 6], "tag_agabaritic_order": 1, 'magasin': 'Store 2'},
        {'id': 14, 'articles': [9, 1, 4], "tag_agabaritic_order": 0, 'magasin': 'Store 2'},
        {'id': 15, 'articles': [7, 1, 6, 10, 2], "tag_agabaritic_order": 1, 'magasin': 'Store 2'},
        {'id': 16, 'articles': [2, 4], "tag_agabaritic_order": 0, 'magasin': 'Store 2'},
        {'id': 17, 'articles': [6], "tag_agabaritic_order": 0, 'magasin': 'Store 2'},
        {'id': 18, 'articles': [2], "tag_agabaritic_order": 0, 'magasin': 'Store 2'},
        {'id': 19, 'articles': [1], "tag_agabaritic_order": 0, 'magasin': 'Store 2'},
        {'id': 20, 'articles': [3, 7, 6], "tag_agabaritic_order": 1, 'magasin': 'Store 2'},
        {'id': 21, 'articles': [14], "tag_agabaritic_order": 0, 'magasin': 'Store 3'},
        {'id': 22, 'articles': [12, 14, 10, 11], "tag_agabaritic_order": 1, 'magasin': 'Store 3'},
        {'id': 23, 'articles': [15, 13, 14], "tag_agabaritic_order": 1, 'magasin': 'Store 3'},
        {'id': 24, 'articles': [11, 13], "tag_agabaritic_order": 1, 'magasin': 'Store 3'},
        {'id': 25, 'articles': [12, 14, 13], "tag_agabaritic_order": 1, 'magasin': 'Store 3'},
        {'id': 26, 'articles': [13, 14, 10], "tag_agabaritic_order": 1, 'magasin': 'Store 3'},
        {'id': 27, 'articles': [14, 15, 11], "tag_agabaritic_order": 1, 'magasin': 'Store 3'},
        {'id': 28, 'articles': [12, 15, 13], "tag_agabaritic_order": 1, 'magasin': 'Store 3'},
        {'id': 29, 'articles': [10, 15], "tag_agabaritic_order": 1, 'magasin': 'Store 3'},
        {'id': 30, 'articles': [14, 11], "tag_agabaritic_order": 0, 'magasin': 'Store 3'}
    ]

    # Convertir les données en DataFrame pour une meilleure visualisation
    df_commandes = pd.DataFrame(commandes)

    st.title("Orders visualization")
    st.dataframe(df_commandes, height=600, width=1200)