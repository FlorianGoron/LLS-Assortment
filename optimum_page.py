import streamlit as st
import matplotlib.pyplot as plt
#from pulp import LpMaximize, LpProblem, LpVariable, lpSum, value, PULP_CBC_CMD
from ortools.linear_solver import pywraplp
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

def calculate_kpis_lmpl(selected_articles, articles, orders, selected_stores=None):
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

def calculate_kpis_obes(selected_articles, articles, orders, selected_stores=None, lambda_1=1/3, lambda_2=1/3, lambda_3=1/3):
    """
    Calculate the KPIs for a given list of selected articles and selected stores, and return the objective function value.

    Parameters:
    selected_articles (list): List of selected article codes.
    articles (list): Complete list of articles with their codes and sizes.
    orders (list): List of orders with associated articles and 'agabaritic' tag.
    selected_stores (list, optional): List of stores to include in the calculation. Takes all orders if None or empty.
    lambda_1 (float): Weight for KPI1 in the objective function.
    lambda_2 (float): Weight for KPI2 in the objective function.
    lambda_3 (float): Weight for KPI3 in the objective function.

    Returns:
    dict: A dictionary with KPI1, KPI2, KPI3 values and the value of the objective function.
    """
    
    # If selected_stores is None or empty, take all orders
    if selected_stores is None or len(selected_stores) == 0:
        filtered_orders = orders
    else:
        # Filter orders based on selected stores
        filtered_orders = [order for order in orders if order['magasin'] in selected_stores]

    # Index articles by article code for quick access to their sizes
    articles_dict = {article['cod_art']: article for article in articles}

    # Initialize KPI counters
    kpi1_count = 0
    kpi2_count = 0
    kpi3_count = 0

    for order in filtered_orders:
        order_articles = order['articles']
        
        # Check if all articles in the order are in the list of selected articles (KPI1)
        if all(article_id in selected_articles for article_id in order_articles):
            kpi1_count += 1

        # Check if at least one article of the order is in the selected articles (KPI2 and KPI3)
        if any(article_id in selected_articles for article_id in order_articles):
            # For KPI 2: Check if the order is agabaritic and has at least one article in the warehouse
            if order['tag_agabaritic_order'] == 1:
                kpi2_count += 1

            # For KPI 3: At least one article of any order is sourced in the warehouse
            kpi3_count += 1

    # Calculate KPI percentages
    total_orders = len(filtered_orders)
    total_agabaritic_orders = sum(order['tag_agabaritic_order'] for order in filtered_orders)

    kpi1_percentage = (kpi1_count / total_orders) * 100 if total_orders > 0 else 0
    kpi2_percentage = (kpi2_count / total_agabaritic_orders) * 100 if total_agabaritic_orders > 0 else 0
    kpi3_percentage = (kpi3_count / total_orders) * 100 if total_orders > 0 else 0

    # Calculate the objective function value (normalized between 0 and 100)
    objective_value = (lambda_1 * kpi1_percentage + lambda_2 * kpi2_percentage + lambda_3 * kpi3_percentage)

    return {
        'kpi1_count': kpi1_count,
        'kpi2_count': kpi2_count,
        'kpi3_count': kpi3_count,
        'kpi1_percentage': kpi1_percentage,
        'kpi2_percentage': kpi2_percentage,
        'kpi3_percentage': kpi3_percentage,
        'objective_value': objective_value  # Add the objective function value to the output
    }


def optimize_warehouse_ortools_obes(articles, orders, max_articles=15, fixed_articles=[], selected_stores=['Store 1', 'Store 2', 'Store 3'], lambda_1=1/3, lambda_2=1/3, lambda_3=1/3):
    """
    Optimize the storage of articles in the warehouse to maximize KPIs using OR-Tools.

    Parameters:
    articles (list): List of articles with their codes and sizes.
    orders (list): List of orders with associated articles and the 'agabaritic' tag.
    max_articles (int, optional): Maximum number of articles the warehouse can hold. If None, no constraint on the number of articles.
    fixed_articles (list): List of fixed articles that are already in the warehouse and cannot be removed.
    selected_stores (list, optional): List of stores selected by the user. If None, all stores are considered.
    lambda_1 (float, optional): Weight coefficient for KPI_1. Default is 1/3.
    lambda_2 (float, optional): Weight coefficient for KPI_2. Default is 1/3.
    lambda_3 (float, optional): Weight coefficient for KPI_3. Default is 1/3.

    Returns:
    dict: Optimal results including articles to store, KPIs, and used volume.
    """
    # Start execution
    start_time = time.time()

    # If selected_stores is None or empty, take all orders
    if selected_stores is None or len(selected_stores) == 0:
        orders = orders
    else:
        # Filter orders based on selected stores
        orders = [order for order in orders if order['magasin'] in selected_stores]
    
    # Create the solver
    solver = pywraplp.Solver.CreateSolver('CBC')
    
    if not solver:
        return None

    # Decision variables for articles (only for those not in fixed_articles)
    x = {article['cod_art']: solver.BoolVar(f"x_{article['cod_art']}") for article in articles if article['cod_art'] not in fixed_articles}

    # Decision variables for KPI_1 (if all articles in the order are in the warehouse)
    y = {order['id']: solver.BoolVar(f"y_{order['id']}") for order in orders}

    # New decision variables for KPI_2 and KPI_3 (if at least one article in the order is in the warehouse)
    z_agabaritic = {order['id']: solver.BoolVar(f"z_agabaritic_{order['id']}") for order in orders}
    z = {order['id']: solver.BoolVar(f"z_{order['id']}") for order in orders}

    # Constraint for KPI_1: y_i can only be 1 if all articles in order i are in the warehouse
    for order in orders:
        for article_id in order['articles']:
            if article_id in fixed_articles:
                solver.Add(y[order['id']] <= 1)  # Fixed article, always available
            else:
                solver.Add(y[order['id']] <= x[article_id])

    # New constraints for KPI_2 and KPI_3
    for order in orders:
        # At least one product must be sourced in the warehouse for both KPIs
        order_articles_in_warehouse = solver.Sum((x[article_id] if article_id not in fixed_articles else 1) for article_id in order['articles'])
        
        # For KPI_2: The order must be agabaritic and at least one article must be sourced in the warehouse
        if order['tag_agabaritic_order'] == 1:
            solver.Add(order_articles_in_warehouse >= 1 * z_agabaritic[order['id']])
        
        # For KPI_3: At least one article must be sourced in the warehouse for all orders
        solver.Add(order_articles_in_warehouse >= 1 * z[order['id']])

    # Objective function: Maximizing normalized KPI_1, KPI_2, and KPI_3
    total_orders = len(orders)
    total_agabaritic_orders = sum(order['tag_agabaritic_order'] for order in orders)

    # Normalize each KPI
    KPI_1 = solver.Sum(y[order['id']] for order in orders) / total_orders  # Normalized KPI_1
    KPI_2 = solver.Sum(z_agabaritic[order['id']] for order in orders if order['tag_agabaritic_order'] == 1) / total_agabaritic_orders  # Normalized KPI_2
    KPI_3 = solver.Sum(z[order['id']] for order in orders) / total_orders  # Normalized KPI_3

    # Objective: Maximize the weighted sum of normalized KPIs, scaled to 100
    solver.Maximize(lambda_1 * KPI_1 + lambda_2 * KPI_2 + lambda_3 * KPI_3)

    # Constraint: Total number of articles in the warehouse must not exceed max_articles (including fixed_articles)
    solver.Add(solver.Sum(x[article['cod_art']] for article in articles if article['cod_art'] not in fixed_articles) + len(fixed_articles) <= max_articles)

    # Solve the problem
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        # Optimal articles to store: selected articles (excluding fixed articles)
        selected_articles = [article['cod_art'] for article in articles if article['cod_art'] not in fixed_articles and x[article['cod_art']].solution_value() == 1]
        optimal_articles = fixed_articles + selected_articles  # Combine fixed and selected

        # Adjust list if it exceeds max_articles
        if len(optimal_articles) > max_articles:
            optimal_articles = fixed_articles + selected_articles[:max_articles - len(fixed_articles)]

        res = calculate_kpis_obes(selected_articles=optimal_articles, 
                                  articles=articles, 
                                  orders=orders, 
                                  selected_stores=selected_stores, 
                                  lambda_1=lambda_1, 
                                  lambda_2=lambda_2, 
                                  lambda_3=lambda_3)
        kpi1_count = res['kpi1_count']
        kpi2_count = res['kpi2_count']
        kpi3_count = res['kpi3_count']
        kpi1_percentage = res['kpi1_percentage']
        kpi2_percentage = res['kpi2_percentage']
        kpi3_percentage = res['kpi3_percentage']

        # Calculate used volume
        used_volume = sum(article['size_art'] for article in articles if article['cod_art'] in optimal_articles)
        
        # Calculate shipped_orders_volume
        shipped_orders_volume = sum(
            sum(article['size_art'] for article_id in order['articles'] for article in articles if article['cod_art'] == article_id)
            for order in orders if y[order['id']].solution_value() == 1
        )

        # End execution
        end_time = time.time()
        
        # Execution duration
        execution_time = end_time - start_time
        print(f"Algorithm execution time: {execution_time:.4f} seconds")

        return {
            'optimal_articles': optimal_articles,
            'kpi1_count': kpi1_count,
            'kpi2_count': kpi2_count,
            'kpi3_count': kpi3_count,
            'kpi1_percentage': kpi1_percentage,
            'kpi2_percentage': kpi2_percentage,
            'kpi3_percentage': kpi3_percentage,
            'used_volume': used_volume, 
            'shipped_orders_volume': shipped_orders_volume,  # Include the new value
            'lambda_1': lambda_1, 
            'lambda_2': lambda_2,
            'lambda_3': lambda_3,
            'selected_stores': selected_stores,
            'number_of_articles': max_articles,
        }

    else:
        print("The problem does not have an optimal solution.")
        return None


########################################
def display_optimum_page():

    # Application title
    st.title("LLS - Assortment, KPI values")

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
        results = optimize_warehouse_ortools_obes(
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
    
        # Store optimal list in session for use on other pages
        st.session_state['optimal_articles'] = [
            {'cod_art': article['cod_art'], 'size_art': article['size_art']} 
            for article in articles if article['cod_art'] in results['optimal_articles']
        ]

    # Display all simulation results
    st.subheader("Simulation Results")

    for i, sim in enumerate(st.session_state.simulations):
        st.write(f"**Simulation {i+1} :** λ1={sim['lambda_1']:.2f}, λ2={sim['lambda_2']:.2f}, λ3={sim['lambda_3']:.2f}, "
                f"Number of articles = {sim['number_of_articles']}, Linked stores = {', '.join(sim['selected_stores'])}")
        st.write(f"The articles to be stored in the LLS to optimize the KPIs are: **{sim['optimal_articles']}**")
        st.write(f"**{sim['kpi1_count']:.0f} orders** sourced from the LLS are complete, approximately "
                f"**{sim['kpi1_percentage']:.0f}% of total orders**")
        st.write(f"**{sim['kpi2_count']:.0f} agabaritic orders** are shipped from the LLS, approximately "
                f"**{sim['kpi2_percentage']:.0f}% of agabaritic orders**")
        st.write(f"**{sim['kpi3_count']:.0f} orders** have been prepared on the LLS, approximately "
                f"**{sim['kpi3_percentage']:.0f}% of total orders**")
        st.write(f"Total volume used in the LLS: {sim['used_volume']} m3")
        st.write(f"Total volume shipped from the LLS: {sim['shipped_orders_volume']} m3")

        # Example of a graph to display for each simulation
        optimal_articles = sim['optimal_articles']
        kpi1_percentage = []
        kpi2_percentage = []
        kpi3_percentage = []
        objective_value = []
        selected_articles = []
        for article in optimal_articles:
            selected_articles.append(article)
            results = calculate_kpis_obes(selected_articles, 
                                          articles, 
                                          commandes, 
                                          selected_stores=sim['selected_stores'], 
                                          lambda_1=sim['lambda_1'], 
                                          lambda_2=sim['lambda_2'], 
                                          lambda_3=sim['lambda_3'])
            kpi1_percentage.append(results['kpi1_percentage'])
            kpi2_percentage.append(results['kpi2_percentage'])
            kpi3_percentage.append(results['kpi3_percentage'])
            objective_value.append(results['objective_value'])
            print(objective_value)

        cumulative_articles = list(range(1, len(optimal_articles) + 1))

        plt.figure(figsize=(10, 6))

        # Tracer KPI 1, KPI 2, KPI 3 sur l'axe de gauche
        line1, = plt.plot(cumulative_articles, kpi1_percentage, marker='o', linestyle='-', color='b', label='KPI 1')
        line2, = plt.plot(cumulative_articles, kpi2_percentage, marker='o', linestyle='-', color='g', label='KPI 2')
        line3, = plt.plot(cumulative_articles, kpi3_percentage, marker='o', linestyle='-', color='r', label='KPI 3')
        plt.xlabel("Value of objective function")
        plt.ylabel("KPI 1, KPI 2, KPI 3 (%)")

        # Tracer la fonction objective sur l'axe de droite
        ax2 = plt.gca().twinx()
        line4, = ax2.plot(cumulative_articles, objective_value, marker='s', linestyle='--', color='y', label='Objective')
        ax2.set_ylabel("Objective function") 

        plt.title("Evolution of KPIs based on the number of stored articles")
        plt.grid(True)

        # Définir les limites de l'axe y pour correspondre aux données combinées de KPI 1, KPI 2, KPI 3
        plt.ylim(min(min(kpi1_percentage), min(kpi2_percentage), min(kpi3_percentage)) - 5, max(max(kpi1_percentage), max(kpi2_percentage), max(kpi3_percentage)) + 5)

        # Combiner les lignes et les étiquettes des deux axes pour une seule légende
        lines = [line1, line2, line3, line4]
        labels = [line.get_label() for line in lines]
        plt.legend(lines, labels, loc='upper left')

        st.pyplot(plt)

