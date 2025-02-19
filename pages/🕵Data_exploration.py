import streamlit as st
import os
import pandas as pd
import json
st.set_page_config(page_title="🕵 Data_exploration", page_icon="🕵", layout="wide")
# Page Title
st.title("🕵 Data Exploration")
st.write("Explore data by selecting a country and an indicator (and model type). Use the tabs to view specific data categories.")
col1, col2, col3, col4 , col5  = st.columns(5)
with col1:
        if st.button("🖼️**Graph Gallery**", key=378):
            st.markdown('<meta http-equiv="refresh" content="0; URL=/Graph_gallery" />', unsafe_allow_html=True)

with col2:
        if st.button(" **Home**", key=25555):
            st.markdown('<meta http-equiv="refresh" content="0; URL=/" />', unsafe_allow_html=True)
 
with col3:
        st.empty()  # Placeholder for spacing

with col4:
        st.empty()  # Placeholder for spacing
with col5:
        st.empty()  # Placeholder for spacing

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
tab1, tab2, tab3, tab4 = st.tabs(["🏁 Final_data", "🎯 Model_result_data", "🛠️ Model_best_params", "📝 Input_data"])

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

# Tab 4 - Input Data
with tab4:
    st.subheader("Input Data")

    # Base path for input data
    base_path = "data/base"

    # Paths for JSON files
    countries_file = "countries.json"
    indicators_file = "indicators.json"

    # Check if required files and directories exist
    if not os.path.isdir(base_path):
        st.error(f"The directory '{base_path}' does not exist.")
    elif not os.path.isfile(countries_file):
        st.error(f"The file '{countries_file}' does not exist.")
    elif not os.path.isfile(indicators_file):
        st.error(f"The file '{indicators_file}' does not exist.")
    else:
        try:
            # Load country names and indicator names from JSON files (as keys)
            with open(countries_file, 'r') as f:
                countries = list(json.load(f).keys())

            with open(indicators_file, 'r') as f:
                indicators = list(json.load(f).keys())

            # Add "All_Countries" and "All_Indicators" options
            countries.insert(0, "All_Countries")
            indicators.insert(0, "All_Indicators")

            # Check if lists are populated
            if not countries:
                st.error("No countries found in 'countries.json'.")
            elif not indicators:
                st.error("No indicators found in 'indicators.json'.")
            else:
                # Dropdown for country selection
                selected_country = st.selectbox("Select Country", countries)

                # Dropdown for indicator selection
                selected_indicator = st.selectbox("Select Indicator", indicators)

                # Handle the cases for "All_Countries" and "All_Indicators"
                if selected_country == "All_Countries":
                    selected_country = None  # This will signify all countries selected
                if selected_indicator == "All_Indicators":
                    selected_indicator = None  # This will signify all indicators selected

                # Construct the filename based on the selected options
                if selected_country and selected_indicator:
                    selected_file = f"{selected_country.replace(' ', '_')}_{selected_indicator.replace(' ', '_')}.parquet"
                    selected_file_path = os.path.join(base_path, selected_file)
                else:
                    selected_file_path = None

                # Handle case when "All Indicators + Any Country" is selected
                if selected_country and selected_indicator is None:
                    try:
                        # Load and aggregate data for all indicators for the selected country
                        all_dfs = []
                        for indicator in indicators[1:]:  # Skip "All_Indicators"
                            file_name = f"{selected_country.replace(' ', '_')}_{indicator.replace(' ', '_')}.parquet"
                            file_path = os.path.join(base_path, file_name)
                            if os.path.isfile(file_path):
                                df = pd.read_parquet(file_path)
                                df = df.dropna()
                                df['Country'] = selected_country
                                df['Indicator'] = indicator
                                all_dfs.append(df)

                        if all_dfs:
                            combined_df = pd.concat(all_dfs, ignore_index=True)
                            st.write(f"Displaying data for **{selected_country}** with all indicators:")
                            st.dataframe(combined_df)
                        else:
                            st.error(f"No data found for {selected_country} with all indicators.")
                    except Exception as e:
                        st.error(f"Error loading data: {e}")

                # Handle case when "Any Country + All Indicators" is selected
                elif selected_country is None and selected_indicator:
                    try:
                        # Load and aggregate data for all countries for the selected indicator
                        all_dfs = []
                        for country in countries[1:]:  # Skip "All_Countries"
                            file_name = f"{country.replace(' ', '_')}_{selected_indicator.replace(' ', '_')}.parquet"
                            file_path = os.path.join(base_path, file_name)
                            if os.path.isfile(file_path):
                                df = pd.read_parquet(file_path)
                                df = df.dropna()
                                df['Country'] = country
                                df['Indicator'] = selected_indicator
                                all_dfs.append(df)

                        if all_dfs:
                            combined_df = pd.concat(all_dfs, ignore_index=True)
                            st.write(f"Displaying data for all countries with **{selected_indicator}**:")
                            st.dataframe(combined_df)
                        else:
                            st.error(f"No data found for {selected_indicator} with all countries.")
                    except Exception as e:
                        st.error(f"Error loading data: {e}")

                # Handle case when "All_Countries" and "All_Indicators" are selected
                elif selected_country is None and selected_indicator is None:
                    try:
                        # Aggregate data for all countries and all indicators
                        all_dfs = []  # List to store all DataFrames for all countries and indicators
                        for country in countries[1:]:  # Skip "All_Countries"
                            for indicator in indicators[1:]:  # Skip "All_Indicators"
                                file_name = f"{country.replace(' ', '_')}_{indicator.replace(' ', '_')}.parquet"
                                file_path = os.path.join(base_path, file_name)
                                if os.path.isfile(file_path):
                                    df = pd.read_parquet(file_path)
                                    df = df.dropna()
                                    df['Country'] = country
                                    df['Indicator'] = indicator
                                    all_dfs.append(df)

                        if all_dfs:
                            combined_df = pd.concat(all_dfs, ignore_index=True)
                            st.write("Displaying aggregated data for all countries and indicators:")
                            st.dataframe(combined_df)
                        else:
                            st.error("No data found for the selected countries and indicators.")
                    except Exception as e:
                        st.error(f"Error loading aggregated data: {e}")

                else:
                    # Case: Specific country and indicator selected
                    if os.path.isfile(selected_file_path):
                        try:
                            df = pd.read_parquet(selected_file_path)
                            df = df.dropna()

                            # Fix year format by removing commas in the 'year' column (if it's in the dataset)
                            if 'Year' in df.columns:
                                df['Year'] = df['Year'].astype(str).apply(lambda x: x.replace(',', ''))  # Remove commas

                            # Display the cleaned DataFrame
                            st.write(f"Displaying cleaned data for **{selected_country} - {selected_indicator}**:")
                            st.dataframe(df)

                        except Exception as e:
                            st.error(f"Error loading the file: {e}")
                    else:
                        st.error(f"The file '{selected_file}' does not exist.")

        except Exception as e:
            st.error(f"Error loading JSON files: {e}")



