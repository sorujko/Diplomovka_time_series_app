import streamlit as st
import os
import json
from PIL import Image

# Page setup
st.set_page_config(page_title="Graph Gallery", page_icon="🖼️", layout="wide")

# Load country and indicator data
with open("countries.json", "r") as country_file:
    countries = json.load(country_file)  # Expecting { "Austria": ..., "Czech Republic": ... }

with open("indicators.json", "r") as indicator_file:
    indicators = json.load(indicator_file)  # Expecting { "Exports of goods and services (% of GDP)": ... }

# Title for the page
st.title("🖼️ Graph Gallery")
st.write("Explore visualizations by selecting a country and an indicator (and model type). Use the tabs to view specific graph types.")

col1, col2, col3, col4 , col5  = st.columns(5)
with col1:
    st.page_link("pages/🕵Data_exploration.py", label="**Data Exploration**", icon="🕵️")

with col2:
    st.page_link("pages/⚔️Data_Wars.py", label="**Data Wars**", icon="⚔️")
 
with col3:
        st.page_link("Home_page.py", label="**Home**")

with col4:
        st.empty()  # Placeholder for spacing
with col5:
        st.empty()  # Placeholder for spacing

# Create tabs
tab1, tab2, tab3 = st.tabs([
    "📊 Model Line Graphs", 
    "📊 Line Graphs", 
    "📉 Autocorrelation Plots", 
    #"📦 Seasonal Decompose Plots"
])

def generate_and_display_image(folder, graph_type, country, indicator, model_type=None):
    # Format country and indicator for file naming
    formatted_country = country.replace(" ", "_")
    formatted_indicator = indicator.replace(" ", "_")

    # Initialize path variable to avoid UnboundLocalError
    path = None

    if country == "All_Countries":
        if folder == "model_plot" and model_type == 'AllModels':
            # Special case for All_Countries with model_plot
            path = os.path.join(
                "images",
                folder,
                "Indicators",
                indicator,
                f"All_Countries_{formatted_indicator}.png"
            )
        elif folder == "model_plot" and model_type != 'AllModels':
            # Load all images matching the pattern
            import glob
            base_path = os.path.join("images", folder, "Indicators", indicator)
            pattern = os.path.join(base_path, f"{model_type}_*.png")
            matching_files = glob.glob(pattern)

            if matching_files:
                for file_path in matching_files:
                    try:
                        img = Image.open(file_path)
                        st.image(img, use_container_width=True)
                    except Exception as e:
                        st.error(f"Error loading image: {e}")
            else:
                st.error("No files found matching the selected criteria.")
            # Return early to prevent further processing for this special case
            return
        else:
            # Special case for All_Countries with other folders
            path = os.path.join(
                "images",
                folder,
                "Indicators",
                formatted_indicator,
                f"{graph_type}_All_Countries_{formatted_indicator}.png"
            )
    elif country != "All_Countries" and indicator == 'all_indicators' and folder == "model_plot":
        if folder == "model_plot" and model_type == 'AllModels':
            # Special case for All_Countries with model_plot
            path = os.path.join(
                "images",
                folder,
                "Countries",
                formatted_country,
                f"{formatted_country}_all_indicators.png"
            )
        elif folder == "model_plot" and model_type != 'AllModels':
            # Load all images matching the pattern
            import glob
            base_path = os.path.join("images", folder, "Countries", formatted_country)
            pattern = os.path.join(base_path, f"{model_type}_*.png")
            matching_files = glob.glob(pattern)

            if matching_files:
                for file_path in matching_files:
                    try:
                        img = Image.open(file_path)
                        st.image(img, use_container_width=True)
                    except Exception as e:
                        st.error(f"Error loading image: {e}")
            else:
                st.error("No files found matching the selected criteria.")
            # Return early to prevent further processing for this special case
            return
        else:
            # Special case for All_Countries with other folders
            path = os.path.join(
                "images",
                folder,
                "Indicators",
                formatted_indicator,
                f"{graph_type}_All_Countries_{formatted_indicator}.png"
            )

    else:
        # Regular case for specific countries
        if folder == "model_plot" and formatted_indicator == 'all_indicators':
            file_name = f"{formatted_country}_{formatted_indicator}.png"
        elif folder == "model_plot" and model_type:
            file_name = f"{model_type}_{formatted_country}_{formatted_indicator}.png"
        else:
            file_name = f"{graph_type}_{formatted_country}_{formatted_indicator}.png"
        path = os.path.join("images", folder, "Countries", formatted_country, file_name)

    # Check if path is set and if the file exists
    if path and os.path.isfile(path):
        try:
            img = Image.open(path)
            st.image(img, caption=f"{graph_type} | {country} | {indicator}", use_container_width=True)
        except Exception as e:
            st.error(f"Error loading image: {e}")
    elif path:
        st.error("File not found. Please check the selected country, indicator, and model type.")




# Dropdowns for country and indicator selection
x = list(indicators.keys())
x.append('all_indicators')

y = list(countries.keys())
y.append('All_Countries')

st.sidebar.header("Select Parameters")
selected_country = st.sidebar.selectbox("Choose a Country", y)
selected_indicator = st.sidebar.selectbox("Choose an Indicator", x)

# Additional dropdown for model type (only for model_plot)
model_types = ["ARIMA", "Holt_Winters", "XGBoost", "LSTM", "Prophet", 'AllModels']
selected_model_type = st.sidebar.selectbox("Choose a Model Type (for Model Line Graphs)", model_types)

# Tab 1: Model Line Graphs
with tab1:
    #st.header("📊 Model Line Graphs")
    generate_and_display_image("model_plot", "Model", selected_country, selected_indicator, selected_model_type)

# Tab 2: Line Graphs
with tab2:
    #st.header("📊 Line Graphs")
    generate_and_display_image("plot", "Line", selected_country, selected_indicator)

# Tab 3: Autocorrelation Plots

with tab3:
    #st.header("📉 Autocorrelation Plots")
    generate_and_display_image("autocor_plot", "Autocor", selected_country, selected_indicator)

# Tab 4: Seasonal Decompose Plots
# tab4:
    #st.header("📦 Seasonal Decompose Plots")
    #generate_and_display_image("season_decompose", "Seasonality", selected_country, selected_indicator)

with st.sidebar.expander("ℹ️ Important Notes"):
    st.write("1. Do not combine 'All_Countries' with 'all_indicators'. This combination is not supported and will not work.")