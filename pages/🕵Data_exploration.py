import streamlit as st
import os
import pandas as pd
import json
st.set_page_config(page_title="🕵 Data_exploration", page_icon="🕵", layout="wide")
# Page Title
st.title("🕵 Data Exploration")

st.write("Explore data by selecting a country and an indicator (and model type). Use the tabs to view specific data categories.")


# Custom CSS to make dataframes full width and align the filters horizontally
st.markdown("""
    <style>
        .dataframe-container {
            width: 100%;  /* Make the dataframe container take up full width */
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .filter-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        .stDataFrame {
            width: 100% !important;  /* Ensure dataframes take full width */
        }
    </style>
""", unsafe_allow_html=True)

# Define model types
model_types = ["ARIMA", "Holt-Winters", "XGBoost", "LSTM", "Prophet"]

# Define paths to JSON files
indicators_file = 'indicators.json'  # Adjust path if necessary
countries_file = 'countries.json'  # Adjust path if necessary

# Load JSON files for indicators and countries
with open(indicators_file, 'r') as f:
    indicators = json.load(f)

with open(countries_file, 'r') as f:
    countries = json.load(f)

# Create tabs
tab1, tab2, tab3 = st.tabs(["🏁 Final_data", "🎯 Model_result_data", "🛠️ Model_best_params"])

# Final Data Tab (Tab 1)
with tab1:
    st.subheader("Final Data")

    # Create a sub-tab for selecting the subfolder
    folder_selection = st.selectbox(
        "Select a Folder",
        ["country_rankings", "indicator_rankings", "log_files", "overall_rankings"]
    )

    # Path to the base directory where the subfolders are located
    base_directory = "data/final"

    # Get the path to the selected folder
    selected_folder_path = os.path.join(base_directory, folder_selection)

    # List the CSV files in the selected folder and sort them
    if os.path.isdir(selected_folder_path):
        csv_files = [f for f in os.listdir(selected_folder_path) if f.endswith(".csv")]
        csv_files.sort()  # Sort the files (you can modify this for another sorting criterion)

        # Select the last file by default
        selected_file = csv_files[-1] if csv_files else None

        # Display the file selection dropdown with the last file selected by default
        selected_file = st.selectbox("Select a CSV File", csv_files, index=len(csv_files)-1 if csv_files else 0)

        # Path to the selected CSV file
        selected_file_path = os.path.join(selected_folder_path, selected_file)

        # Create a horizontal layout for the filter options
        with st.container():
            col1, col2, col3 = st.columns([2, 2, 2])  # Create three columns
            with col1:
                if folder_selection == "country_rankings" or folder_selection == "log_files":
                    # Allow country selection but default to empty (nothing selected)
                    countries_selected = st.multiselect("Select Countries", list(countries.keys()))
            
            with col2:
                if folder_selection == "indicator_rankings" or folder_selection == "log_files":
                    # Allow indicator selection but default to empty (nothing selected)
                    indicators_selected = st.multiselect("Select Indicators", list(indicators.keys()))
            
            with col3:
                # Model selection for all folder types, but default to empty (nothing selected)
                models_selected = st.multiselect("Select Models", model_types)

        # Load and filter the CSV file based on the selections
        try:
            df = pd.read_csv(selected_file_path)

            # Apply filters based on selected options, only if any selection is made
            if folder_selection == "country_rankings" and (countries_selected or models_selected):
                if countries_selected:
                    df = df[df['Country'].isin(countries_selected)]
                if models_selected:
                    df = df[df['Model'].isin(models_selected)]
            if folder_selection == "indicator_rankings" and (indicators_selected or models_selected):
                if indicators_selected:
                    df = df[df['Indicator'].isin(indicators_selected)]
                if models_selected:
                    df = df[df['Model'].isin(models_selected)] 
            if folder_selection == "log_files":
                if countries_selected:
                    df = df[df['Country'].isin(countries_selected)]
                if indicators_selected:
                    df = df[df['Indicator'].isin(indicators_selected)]
                if models_selected:
                    df = df[df['Model'].isin(models_selected)]

            # Center the DataFrame using the custom CSS class (full width)
            with st.container():
                st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
                st.dataframe(df)
                st.markdown('</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error loading CSV file: {e}")

    else:
        st.error(f"Selected folder '{folder_selection}' does not exist.")

# Tab 2 - Train Model Data
with tab2:
    st.subheader("Train Model Data")

    # Path to the base directory where the subfolders are located
    base_directory = "data"

    # Get all subfolders with '_train' in their name
    train_subfolders = [f for f in os.listdir(base_directory) if os.path.isdir(os.path.join(base_directory, f)) and '_train' in f]

    # Select the subfolder from those that contain '_train'
    folder_selection = st.selectbox(
        "Select a Model Training Folder",
        train_subfolders
    )

    # Get the path to the selected folder
    selected_folder_path = os.path.join(base_directory, folder_selection)

    # List the CSV files in the selected folder and sort them
    if os.path.isdir(selected_folder_path):
        csv_files = [f for f in os.listdir(selected_folder_path) if f.endswith(".csv")]
        csv_files.sort()  # Sort the files (you can modify this for another sorting criterion)

        # Select the last file by default
        selected_file = csv_files[-1] if csv_files else None

        # Display the file selection dropdown with the last file selected by default
        selected_file = st.selectbox("Select a CSV File", csv_files, index=len(csv_files)-1 if csv_files else 0)

        # Path to the selected CSV file
        selected_file_path = os.path.join(selected_folder_path, selected_file)

        # Create a horizontal layout for the filter options
        with st.container():
            col1, col2 = st.columns([2, 2])  # Create two columns (since model selector is removed)
            with col1:
                # Country selection filter (if relevant to the data)
                countries_selected = st.multiselect("Select Countries", list(countries.keys()), default=[], key="country_selector")
            
            with col2:
                # Indicator selection filter (if relevant to the data)
                indicators_selected = st.multiselect("Select Indicators", list(indicators.keys()), default=[], key="indicator_selector")

        # Load and filter the CSV file based on the selections
        try:
            df = pd.read_csv(selected_file_path)

            # Drop the 'Rank' column if it exists
            if 'Rank' in df.columns:
                df = df.drop(columns=['Rank'])

            # Apply filters based on selected options, only if any selection is made
            if countries_selected:
                df = df[df['Country'].isin(countries_selected)]
            if indicators_selected:
                df = df[df['Indicator'].isin(indicators_selected)]

            # Center the DataFrame using the custom CSS class (full width)
            with st.container():
                st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
                st.dataframe(df)
                st.markdown('</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error loading CSV file: {e}")

    else:
        st.error(f"Selected folder '{folder_selection}' does not exist.")

model_types = ["ARIMA", "Holt_Winters", "XGBoost", "LSTM", "Prophet"]
# Tab 3 - Best Parameters
with tab3:
    st.subheader("Best Parameters")

    # Path to best_params base directory
    best_params_base_path = "best_params"

    # Indicator, Model, and Country selection
    indicator_options = list(indicators.keys()) + ["All Indicators"]
    indicator_selected = st.selectbox("Select Indicator", indicator_options)

    model_selected = st.selectbox("Select Model", model_types)

    # Add "All Countries" option
    country_options = list(countries.keys()) + ["All Countries"]
    country_selected = st.selectbox("Select Country", country_options)

    # Handle "All Countries" selection
    if country_selected == "All Countries":
        selected_countries = list(countries.keys())
    else:
        selected_countries = [country_selected]

    # Handle "All Indicators" selection
    if indicator_selected == "All Indicators":
        selected_indicators = list(indicators.keys())
    else:
        selected_indicators = [indicator_selected]

    # Container for results
    results_container = []

    # Iterate through all selected indicators and countries
    for country in selected_countries:
        for indicator in selected_indicators:
            # Build the path to the corresponding JSON file
            json_file_path = os.path.join(best_params_base_path, indicator, f"{model_selected}_{country}.json")

            # Try to read and process the JSON file
            if os.path.exists(json_file_path):
                try:
                    # Read the JSON data
                    with open(json_file_path, 'r') as file:
                        json_data = json.load(file)
                    
                    # Convert JSON data into a DataFrame
                    df = pd.json_normalize(json_data)

                    # Add metadata columns
                    df.insert(0, 'Country', country)
                    df.insert(0, 'Model', model_selected)
                    df.insert(0, 'Indicator', indicator)

                    # Handle XGBoost-specific SelectedFeatures files
                    if model_selected == "XGBoost":
                        features_file_path = os.path.join(best_params_base_path, indicator, f"SelectedFeatures_{country}.json")
                        if os.path.exists(features_file_path):
                            with open(features_file_path, 'r') as feature_file:
                                feature_data = json.load(feature_file)
                            
                            # Add features as additional columns
                            for i, feature in enumerate(feature_data):
                                df[f"Feature_{i+1}"] = feature

                    # Append the DataFrame to the results container
                    results_container.append(df)

                except json.JSONDecodeError:
                    st.error(f"Error decoding JSON from: {json_file_path}")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
            else:
                st.warning(f"No data for {model_selected} in {country} under {indicator}")

    # Display results
    if not results_container:
        st.warning("No data available for the selected parameters.")
    else:
        # Concatenate all dataframes from the list and display
        final_df = pd.concat(results_container, ignore_index=True)
        st.dataframe(final_df)
