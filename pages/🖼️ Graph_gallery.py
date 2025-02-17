import streamlit as st
import os
import json
from PIL import Image

# Page setup
st.set_page_config(page_title="🖼️ Graph Gallery", page_icon="🖼️", layout="wide")

# Load country and indicator data
with open("countries.json", "r") as country_file:
    countries = json.load(country_file)  # Expecting { "Austria": ..., "Czech Republic": ... }

with open("indicators.json", "r") as indicator_file:
    indicators = json.load(indicator_file)  # Expecting { "Exports of goods and services (% of GDP)": ... }

# Title for the page
st.title("🖼️ Graph Gallery")
st.write("Explore visualizations by selecting a country and an indicator (and model type). Use the tabs to view specific graph types.")

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Model Line Graphs", 
    "📊 Line Graphs", 
    "📉 Autocorrelation Plots", 
    "📦 Seasonal Decompose Plots"
])

# Helper function to generate and display image
def generate_and_display_image(folder, graph_type, country, indicator, model_type=None):
    # Format country and indicator for file naming

    formatted_country = country.replace(" ", "_")
    formatted_indicator = indicator.replace(" ", "_")

    # Add model type to the file name if it's for model_plot
    if folder == "model_plot" and model_type:
        file_name = f"{model_type}_{formatted_country}_{formatted_indicator}.png"
    else:
        file_name = f"{graph_type}_{formatted_country}_{formatted_indicator}.png"

    # Construct the path
    path = os.path.join("images", folder, "Countries", formatted_country, file_name)


    # Check if file exists and display
    if os.path.isfile(path):
        try:
            img = Image.open(path)
            st.image(img, caption=f"{graph_type} | {country} | {indicator}", use_container_width=True)
        except Exception as e:
            st.error(f"Error loading image: {e}")
    else:
        st.error("File not found. Please check the selected country, indicator, and model type.")

# Dropdowns for country and indicator selection
st.sidebar.header("Select Parameters")
selected_country = st.sidebar.selectbox("Choose a Country", list(countries.keys()))
selected_indicator = st.sidebar.selectbox("Choose an Indicator", list(indicators.keys()))

# Additional dropdown for model type (only for model_plot)
model_types = ["ARIMA", "Holt_Winters", "XGBoost", "LSTM", "Prophet", 'AllModels']
selected_model_type = st.sidebar.selectbox("Choose a Model Type (for Model Line Graphs)", model_types)

# Tab 1: Model Line Graphs
with tab1:
    st.header("📊 Model Line Graphs")
    generate_and_display_image("model_plot", "Model", selected_country, selected_indicator, selected_model_type)

# Tab 2: Line Graphs
with tab2:
    st.header("📊 Line Graphs")
    generate_and_display_image("plot", "Line", selected_country, selected_indicator)

# Tab 3: Autocorrelation Plots
with tab3:
    st.header("📉 Autocorrelation Plots")
    generate_and_display_image("autocor_plot", "Autocor", selected_country, selected_indicator)

# Tab 4: Seasonal Decompose Plots
with tab4:
    st.header("📦 Seasonal Decompose Plots")
    generate_and_display_image("season_decompose", "Seasonality", selected_country, selected_indicator)
