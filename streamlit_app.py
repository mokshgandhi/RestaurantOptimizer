# streamlit_app.py

import streamlit as st
import pandas as pd

from data_simulation import generate_data
from demand_model import train_model, predict_demand
from fuzzy_engine import build_fuzzy_system
from recipe_engine import substitute_ingredients, apply_fuzzy_adjustment
from aco_optimizer import ACORecipeOptimizer
from config import RECIPES, INGREDIENTS

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="Restaurant AI System", layout="wide")

st.title("🍽️ AI-Powered Restaurant Optimization Dashboard")
st.markdown("Hybrid System: ML + Fuzzy Logic + ACO Optimization")

# ---------------------------
# SIDEBAR INPUTS
# ---------------------------
st.sidebar.header("📊 Inputs")

day = st.sidebar.slider("Day (0=Mon, 6=Sun)", 0, 6, 5)
weather = st.sidebar.selectbox("Weather", ["hot", "moderate", "rainy"])

freshness = st.sidebar.slider("Freshness (Days left)", 0, 10, 3)

st.sidebar.subheader("Inventory")
cheese = st.sidebar.slider("Cheese Stock", 0, 500, 150)
tomato = st.sidebar.slider("Tomato Stock", 0, 500, 200)
paneer = st.sidebar.slider("Paneer Stock", 0, 500, 80)

stock = {
    "cheese": cheese,
    "tomato": tomato,
    "paneer": paneer
}

recipe_name = st.sidebar.selectbox("Select Recipe", list(RECIPES.keys()))

# ---------------------------
# LOAD MODELS (CACHED)
# ---------------------------
@st.cache_resource
def load_model():
    df = generate_data()
    return train_model(df)

model = load_model()

@st.cache_resource
def load_fuzzy():
    return build_fuzzy_system()

# ---------------------------
# MAIN COMPUTE BUTTON
# ---------------------------
if st.button("🚀 Run Optimization"):

    fuzzy = load_fuzzy()

    # Step 1: Demand Prediction
    demand = predict_demand(model, day, weather)

    # Step 2: Fuzzy Logic
    fuzzy.input['demand'] = demand
    fuzzy.input['stock'] = sum(stock.values())
    fuzzy.input['freshness'] = freshness
    fuzzy.compute()

    reorder = fuzzy.output['reorder']
    adjustment = fuzzy.output['adjustment']

    # Step 3: Recipe Processing
    base_recipe = RECIPES[recipe_name]

    substituted_recipe = substitute_ingredients(base_recipe, stock)
    adjusted_recipe = apply_fuzzy_adjustment(substituted_recipe, adjustment)

    # Step 4: ACO Optimization
    cost_map = {k: INGREDIENTS[k]['cost'] for k in INGREDIENTS}
    aco = ACORecipeOptimizer(list(adjusted_recipe.keys()), cost_map)

    optimized_recipe, score = aco.optimize(adjusted_recipe, stock)

    # ---------------------------
    # DISPLAY RESULTS
    # ---------------------------

    st.subheader("📈 Demand Prediction")
    st.metric("Predicted Orders", round(demand, 2))

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📦 Inventory Decision")
        st.metric("Reorder Quantity", round(reorder, 2))

    with col2:
        st.subheader("🍳 Recipe Adjustment")
        st.metric("Adjustment Factor", round(adjustment, 2))

    # ---------------------------
    # RECIPE COMPARISON
    # ---------------------------
    st.subheader("🍽️ Recipe Evolution")

    df_recipe = pd.DataFrame({
        "Ingredient": list(base_recipe.keys()),
        "Original": list(base_recipe.values()),
        "After Fuzzy": [adjusted_recipe[i] for i in base_recipe],
        "After ACO": [optimized_recipe.get(i, 0) for i in base_recipe]
    })

    st.dataframe(df_recipe, use_container_width=True)

    # ---------------------------
    # COST ANALYSIS
    # ---------------------------
    st.subheader("💰 Cost Analysis")

    def calc_cost(recipe):
        return sum(recipe[i] * INGREDIENTS[i]['cost'] for i in recipe)

    original_cost = calc_cost(base_recipe)
    optimized_cost = calc_cost(optimized_recipe)

    col3, col4 = st.columns(2)

    with col3:
        st.metric("Original Cost", original_cost)

    with col4:
        st.metric("Optimized Cost", optimized_cost)

    # ---------------------------
    # VISUALIZATION
    # ---------------------------
    st.subheader("📊 Ingredient Usage Comparison")

    chart_df = df_recipe.set_index("Ingredient")
    st.bar_chart(chart_df)

    # ---------------------------
    # INSIGHTS
    # ---------------------------
    st.subheader("🧠 AI Insights")

    if adjustment > 0.7:
        st.warning("High adjustment due to low stock or spoilage risk")

    if reorder > 300:
        st.error("Urgent restocking required!")

    if optimized_cost < original_cost:
        st.success("ACO successfully reduced cost 🎯")
