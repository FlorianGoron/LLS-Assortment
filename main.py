import streamlit as st
import matplotlib.pyplot as plt
from pulp import LpMaximize, LpProblem, LpVariable, lpSum, value, PULP_CBC_CMD
import time

# Example data
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

def calculate_kpis(selected_articles, articles, orders, selected_stores=None):
    """
    Calculate the KPIs for a given list of selected articles and selected stores.

    Parameters:
    selected_articles (list): List of selected article codes.
    articles (list): Complete list of articles with their codes and sizes.
    orders (list): List of orders with associated articles and 'agabaritic' tag.
    selected_stores (list, optional): List of stores to include in the calculation. Takes all orders if None or empty.

    Returns:
    dict: A dictionary with KPI1, KPI2, and KPI3 values.
    """
    
    # If selected_stores is None or empty, take all orders
    if selected_stores is None or len(selected_stores) == 0:
        filtered_orders = orders
    else:
        # Filter orders based on selected stores
        filtered_orders = [order for order in orders if order['magasin'] in selected_stores]

    # Index articles by article code for quick access to their sizes
    articles_dict = {article['cod_art']: article for article in articles}

    # Pre-calculate total volumes per order
    order_volumes = {
        order['id']: sum(articles_dict[article_id]['size_art'] for article_id in order['articles'])
        for order in filtered_orders
    }

    # Initialize KPI counters
    kpi1_count = 0
    kpi2_count = 0
    kpi3_count = 0

    for order in filtered_orders:
        order_articles = order['articles']
        total_order_volume = order_volumes[order['id']]
        
        # Check if all articles in the order are in the list of selected articles (KPI1)
        if all(article_id in selected_articles for article_id in order_articles):
            kpi1_count += 1

            # Check if the order is agabaritic (KPI2)
            if order['tag_agabaritic_order'] == 1:
                kpi2_count += 1
        
        # Calculate the available volume for the order (KPI3)
        available_volume = sum(
            articles_dict[article_id]['size_art']
            for article_id in order_articles
            if article_id in selected_articles
        )

        # Check if the available volume is at least 50% of the total order volume
        if available_volume >= 0.5 * total_order_volume:
            kpi3_count += 1

    # Calculate KPI percentages
    total_orders = len(filtered_orders)
    total_agabaritic_orders = sum(order['tag_agabaritic_order'] for order in filtered_orders)

    kpi1_percentage = (kpi1_count / total_orders) * 100 if total_orders > 0 else 0
    kpi2_percentage = (kpi2_count / total_agabaritic_orders) * 100 if total_agabaritic_orders > 0 else 0
    kpi3_percentage = (kpi3_count / total_orders) * 100 if total_orders > 0 else 0

    return {
        'kpi1_count': kpi1_count,
        'kpi2_count': kpi2_count,
        'kpi3_count': kpi3_count,
        'kpi1_percentage': kpi1_percentage,
        'kpi2_percentage': kpi2_percentage,
        'kpi3_percentage': kpi3_percentage
    }


def optimize_warehouse(articles, orders, max_articles=15, selected_stores=['Store 1', 'Store 2', 'Store 3'], lambda_1=1/3, lambda_2=1/3, lambda_3=1/3):
    """
    Optimize the storage of articles in the warehouse to maximize KPIs.

    Parameters:
    articles (list): List of articles with their codes and sizes.
    orders (list): List of orders with associated articles and the 'agabaritic' tag.
    max_articles (int, optional): Maximum number of articles the warehouse can hold. If None, no constraint on the number of articles.
    selected_stores (list, optional): List of stores selected by the user. If None, all stores are considered.
    lambda_1 (float, optional): Weight coefficient for KPI_1. Default is 1/3.
    lambda_2 (float, optional): Weight coefficient for KPI_2. Default is 1/3.
    lambda_3 (float, optional): Weight coefficient for KPI_3. Default is 1/3.

    Returns:
    dict: Optimal results including articles to store, KPIs, and used volume.
    """
    # Start execution
    start_time = time.time()
    
    # Create the problem model
    model = LpProblem(name="stock-optimization", sense=LpMaximize)

    # Decision variables for articles
    x = {article['cod_art']: LpVariable(name=f"x_{article['cod_art']}", cat='Binary') for article in articles}

    # Decision variables for KPI_1 (if all articles in the order are in the warehouse)
    y = {order['id']: LpVariable(name=f"y_{order['id']}", cat='Binary') for order in orders}

    # Decision variables for KPI_2 (if more than 50% of the volume of the AGABARITIC order is covered by the warehouse)
    z_agabaritic = {order['id']: LpVariable(name=f"z_agabaritic_{order['id']}", cat='Binary') for order in orders}

    # Decision variables for KPI_3 (if more than 50% of the volume of the order is covered by the warehouse)
    z = {order['id']: LpVariable(name=f"z_{order['id']}", cat='Binary') for order in orders}

    # Constraint for KPI_1: y_i can only be 1 if all articles in order i are in the warehouse
    for order in orders:
        for article_id in order['articles']:
            model += (y[order['id']] <= x[article_id], f"constr_y_{order['id']}_{article_id}")

    # Constraints for KPI_2 and KPI_3
    for order in orders:
        total_volume = sum(next(article['size_art'] for article in articles if article['cod_art'] == article_id) for article_id in order['articles'])
        warehouse_volume = lpSum(x[article_id] * next(article['size_art'] for article in articles if article['cod_art'] == article_id) for article_id in order['articles'])
        
        # Constraint for KPI_2: The order must be AGABARITIC and the warehouse volume must cover at least 50% of the total order volume
        if order['tag_agabaritic_order'] == 1:
            model += (warehouse_volume >= 0.5 * total_volume * z_agabaritic[order['id']], f"constr_z_agabaritic_{order['id']}")
            
        # Constraint for KPI_3: Check if more than 50% of the order volume is covered by the warehouse (all orders)
        model += (warehouse_volume >= 0.5 * total_volume * z[order['id']], f"constr_z_{order['id']}")

    # Objective function: Maximizing KPI_1, KPI_2, and KPI_3 with specified weights
    # Total number of orders
    total_orders = len(orders)

    # Total number of AGABARITIC orders
    total_agabaritic_orders = sum(order['tag_agabaritic_order'] for order in orders)

    # KPI_1: Total number of orders where all articles come from the warehouse (LLS)
    KPI_1 = lpSum(y[order['id']] for order in orders)

    # KPI_2: Total number of "AGABARITIC" orders where the volume of articles from the warehouse represents more than 50% of the total volume
    KPI_2 = lpSum(z_agabaritic[order['id']] for order in orders if order['tag_agabaritic_order'] == 1)

    # KPI_3: Total number of orders where the volume of articles from the warehouse represents more than 50% of the total order volume
    KPI_3 = lpSum(z[order['id']] for order in orders)

    # Add the objective function with weighting
    model += lambda_1 * KPI_1 + lambda_2 * KPI_2 + lambda_3 * KPI_3

    # Constraint: Total number of articles in the warehouse must not exceed max_articles
    model += lpSum(x[article['cod_art']] for article in articles) <= max_articles

    # Solve the problem
    model.solve(PULP_CBC_CMD(msg=False))

    # Calculate KPIs in percentage
    kpi1_count = value(KPI_1)
    kpi2_count = value(KPI_2)
    kpi3_count = value(KPI_3)
    kpi1_percentage = (kpi1_count / total_orders) * 100 if total_orders > 0 else 0
    kpi2_percentage = (kpi2_count / total_agabaritic_orders) * 100 if total_agabaritic_orders > 0 else 0

    # Optimal articles to store
    optimal_articles = [article['cod_art'] for article in articles if value(x[article['cod_art']]) == 1]

    # Total used volume
    used_volume = lpSum(x[article['cod_art']].varValue * article['size_art'] for article in articles).value()

    # Total volume of shipped orders
    shipped_orders_volume = sum(
        sum(article['size_art'] for article_id in order['articles'] for article in articles if article['cod_art'] == article_id)
        for order in orders if value(z[order['id']]) == 1
    )

    # End execution
    end_time = time.time()
        
    # Execution duration
    execution_time = end_time - start_time
    print(f"Algorithm execution time: {execution_time:.4f} seconds")
    
    # Results
    return {
        'optimal_articles': optimal_articles,
        'kpi1_count': kpi1_count,
        'kpi2_count': kpi2_count,
        'kpi3_count': kpi3_count,
        'kpi1_percentage': kpi1_percentage,
        'kpi2_percentage': kpi2_percentage,
        'used_volume': used_volume, 
        'shipped_orders_volume': shipped_orders_volume,
        'lambda_1': lambda_1, 
        'lambda_2': lambda_2,
        'lambda_3': lambda_3,
        'selected_stores': selected_stores,
        'number_of_articles': max_articles,
    }

########################################

# Page configuration
st.set_page_config(page_title="LLS - Assortment, KPI values", layout="centered")

# Application title
st.title("LLS - Assortment, KPI values")

st.subheader("Objective")
# Description of the objective
st.markdown("""
            
We aim to find the list of articles that maximizes the following sum:
          
>              Maximize λ1⋅KPI 1 + λ2⋅KPI 2 + λ3⋅KPI 3 

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

# Input for lambdas with a constraint so that the sum equals 100
st.sidebar.header("choice of parameters")

st.sidebar.markdown("<h4 style='font-size:16px;'>Weight of KPIs</h4>", unsafe_allow_html=True)

# Start by defining lambda1
lambda1 = st.sidebar.slider("λ1 (%)", min_value=0.0, max_value=100.0, value=33.0, step=0.1)

# The other two are calculated proportionally so that their sum with lambda1 is 100
if lambda1 < 100.0:
    lambda2 = st.sidebar.slider("λ2 (%)", min_value=0.0, max_value=100.0 - lambda1, value=(100.0 - lambda1) / 2, step=0.1)
    lambda3 = 100.0 - lambda1 - lambda2
else:
    lambda2 = 0.0
    lambda3 = 0.0

# Display the calculated lambda values
st.sidebar.write(f"λ3 is automatically calculated so that the sum is 100: λ3 = {lambda3:.2f}%")

# Input for the number of articles
number_of_articles = st.sidebar.number_input(label="Number of articles", min_value=1, max_value=15, value=5, step=1)

# List of stores to check
st.sidebar.subheader("Number of linked stores")
store1 = st.sidebar.checkbox("Store 1")
store2 = st.sidebar.checkbox("Store 2")
store3 = st.sidebar.checkbox("Store 3")

# Initialize the list of simulations in the session state if it does not already exist
if 'simulations' not in st.session_state:
    st.session_state.simulations = []

# Button to start the optimization calculation
if st.sidebar.button("Run optimization"):
    selected_stores = [f"Store {i+1}" for i, selected in enumerate([store1, store2, store3]) if selected]

    # If no checkbox is checked, select all stores by default
    if not selected_stores:
        selected_stores = ["Store 1", "Store 2", "Store 3"]
    
    # Call the optimize_warehouse function with the selected parameters
    results = optimize_warehouse(
        articles=articles,
        orders=commandes,
        selected_stores=selected_stores,
        max_articles=number_of_articles,
        lambda_1=lambda1 / 100,
        lambda_2=lambda2 / 100,
        lambda_3=lambda3 / 100
    )

    # Add the results to the list of simulations in the session state
    st.session_state.simulations.append(results)

# Display all simulation results
st.subheader("Simulation Results")

for i, sim in enumerate(st.session_state.simulations):
    st.write(f"**Simulation {i+1} :** λ1={sim['lambda_1']:.2f}, λ2={sim['lambda_2']:.2f}, λ3={sim['lambda_3']:.2f}, "
             f"Number of articles = {sim['number_of_articles']}, Linked stores = {', '.join(sim['selected_stores'])}")
    st.write(f"The articles to be stored in the LLS to optimize the KPIs are: {sim['optimal_articles']}")
    st.write(f"{sim['kpi1_count']:.0f} orders sourced from the LLS are complete, approximately "
             f"{sim['kpi1_percentage']:.0f}% of total orders")
    st.write(f"{sim['kpi2_count']:.0f} agabaritic orders are shipped from the LLS, approximately "
             f"{sim['kpi2_percentage']:.0f}% of agabaritic orders")
    st.write(f"{sim['kpi3_count']:.0f} orders have been prepared on the LLS")
    st.write(f"Total volume used in the LLS: {sim['used_volume']} m3")
    st.write(f"Total volume shipped from the LLS: {sim['shipped_orders_volume']} m3")

    # Example of a graph to display for each simulation
    optimal_articles = sim['optimal_articles']
    kpi1_percentage = []
    selected_articles = []
    for article in optimal_articles:
        selected_articles.append(article)
        results = calculate_kpis(selected_articles, articles, commandes, selected_stores=sim['selected_stores'])
        kpi1_percentage.append(results['kpi1_percentage'])

    cumulative_articles = list(range(1, len(optimal_articles) + 1))

    plt.figure(figsize=(10, 6))
    plt.plot(cumulative_articles, kpi1_percentage, marker='o', linestyle='-', color='b', label='KPI 1')
    plt.title("Evolution of KPI 1 based on the number of stored articles")
    plt.xlabel("Number of stored articles")
    plt.ylabel("KPI 1 (%)")
    plt.grid(True)
    plt.legend()

    st.pyplot(plt)

