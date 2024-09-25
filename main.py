import streamlit as st
import streamlit_option_menu
from streamlit_option_menu import option_menu

# Définir la configuration de la page en premier
st.set_page_config(page_title="LLS - Assortment, KPI values", layout="centered")

# Import des autres pages
from articles_page import display_articles_page
from orders_page import display_orders_page
from optimum_page import display_optimum_page
from lls_assortment_page import display_lls_assortment_page

# Définir les options de la barre latérale
with st.sidebar:
    page = option_menu(
    menu_title = "Menu",
    options = ["Home", "Find the optimum assortment", "LLS assortment visualization", "Articles visualization", "Orders visualization"],
    icons = ["house","activity","list-ul","basket-fill", "basket-fill"], 
    menu_icon = "cast",
    default_index = 0,
    #orientation = "horizontal",
)

#page = st.sidebar.radio("Aller à", ("Home", "Find the optimum assortment", "Articles visualization", "Orders visualization"))

# Afficher la page en fonction de la sélection
if page == "Home":
    st.title("LLS - Assortment, KPI values")
    st.markdown(r"""         
    We aim to find the list of articles that maximizes the following sum:
            
    $$
    \text{Maximize} \quad \lambda_1 \cdot \text{KPI}_1 + \lambda_2 \cdot \text{KPI}_2 + \lambda_3 \cdot \text{KPI}_3
    $$

    Under the constraint of the maximum number of articles that the LLS can hold
                
    Where: 
    - **KPI 1**: The number of orders completed by the LLS (1)
    - **KPI 2**: The number of AGABARITIC orders prepared by the LLS (2)
    - **KPI 3**: The number of orders prepared by the LLS (3)
                
    And: 
    - **λ1** represents the weight given to KPI 1
    - **λ2** represents the weight given to KPI 2
    - **λ3** represents the weight given to KPI 3

                
    **Notes** :
                
    (1) An order is complete if all the products that make up the order are sourced in the LLS  
    (2) An order is considered AGABARITIC if it exceeds a certain volume or one of its products exceeds a certain dimension  
    (3) An order is said to be prepared by the LLS if the volume of products sourced in the LLS represents at least 50% of the total order volume
    """)

if page == "Find the optimum assortment":
    display_optimum_page()

if page == "LLS assortment visualization":
    display_lls_assortment_page() 

elif page == "Articles visualization":
    display_articles_page()

elif page == "Orders visualization":
    display_orders_page()