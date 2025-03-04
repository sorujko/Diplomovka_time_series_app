import streamlit as st
import os
import pandas as pd
import json
st.set_page_config(page_title="Data_exploration", page_icon="🕵️‍♂️", layout="wide")
# Page Title
st.title("🕵 Data Exploration")

st.write("Explore data by selecting a country and an indicator (and model type). Use the tabs to view specific data categories.")

with st.sidebar.expander("ℹ️ Important Notes"):
    st.write("Indicator **GDP (USD)** has it's values **billions USD** in Value column (Ukazovateľ GDP (USD) ma v stĺpci Value hodnoty v miliardách USC)")

col1, col2, col3, col4 , col5  = st.columns(5)
with col1:
    st.page_link("pages/🖼️Graph_gallery.py", label="**Graph Gallery**", icon="🖼️")

with col2:
    st.page_link("pages/⚔️Data_Wars.py", label="**Data Wars**", icon="⚔️")

with col3:
        st.page_link("Home_page.py", label="**Home**")

with col4:
        st.empty()  # Placeholder for spacing
with col5:
        st.empty()  # Placeholder for spacing


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
                df.loc[df["Indicator"].isin(["GDP (USD)"]), "RMSE"] /= 1_000_000_000
                if countries_selected:
                    df = df[df['Country'].isin(countries_selected)]
                if indicators_selected:
                    df = df[df['Indicator'].isin(indicators_selected)]
                if models_selected:
                    df = df[df['Model'].isin(models_selected)]

            # Center the DataFrame using the custom CSS class (full width)
            
            with st.container():
                #st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
                st.dataframe(df)
                #st.markdown('</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error loading CSV file: {e}")

    else:
        st.error(f"Selected folder '{folder_selection}' does not exist.")
    
    with st.sidebar.expander("About Final Data"):
        st.write("""
        In this tab, you can explore and filter the **final data** stored in different subfolders. Here's what you can do:
        
        - **Folders:** 
        - `country_rankings`: View rankings by country. Filter by countries and models.
        - `indicator_rankings`: View rankings by indicator. Filter by indicators and models.
        - `log_files`: Explore log data. Filter by countries, indicators, and models.
        - `overall_rankings`: View overall rankings without additional filters.
        
        - **File Selection:** The most recent CSV file from the selected folder is chosen by default, but you can select any other file available.

        - **Filters:** 
        - Depending on the folder, you can filter the data by **Countries**, **Indicators**, or **Models**.
        - For `country_rankings` and `indicator_rankings`, applicable filters are shown automatically.
        
        - **Output:** 
        - A filtered table is displayed based on your selections.
        - If no filters are applied, the full dataset is shown.

        Explore the available data and customize the view with the options provided!
        """)

# Tab 2 - Train Model Data
with tab2:

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
            df.loc[df["Indicator"].isin(["GDP (USD)"]), "RMSE"] /= 1_000_000_000

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
    
    with st.sidebar.expander("About Model Result Data"):
        st.write("""
        This tab allows you to explore **model training data** from folders containing '_train' in their name. Here's what you can do:
        
        - **Folder Selection:**
        - Automatically detects subfolders within the `data` directory that are related to model training (folders with '_train' in their name).
        - Select the desired training folder from the dropdown.

        - **File Selection:**
        - Lists all CSV files within the selected folder, sorted for convenience.
        - The most recent CSV file is selected by default, but you can choose any file from the dropdown.

        - **Filters:**
        - Filter the training data by **Countries** or **Indicators** using the multi-select dropdowns. 
        - Leave filters empty to view the entire dataset.

        - **Output:**
        - Displays the filtered dataset in a tabular format.
        - Automatically removes unnecessary columns like 'Rank', if present, for cleaner data visualization.

        Use this tab to inspect, filter, and analyze the training data for your models!
        """)

model_types = ["ARIMA", "Holt_Winters", "XGBoost", "LSTM", "Prophet"]
# Tab 3 - Best Parameters
with tab3:
    best_params_base_path = "best_params"

    # Arrange selection boxes in a row
    col1, col2, col3 = st.columns(3)
    with col1:
        country_selected = st.multiselect("Select Country", options=list(countries.keys()), default=[])
    with col2:
        indicator_selected = st.multiselect("Select Indicator", options=list(indicators.keys()), default=[])
    with col3:
        model_selected = st.selectbox("Select Model", model_types)

    # If nothing is selected, include all options
    selected_countries = country_selected if country_selected else list(countries.keys())
    selected_indicators = indicator_selected if indicator_selected else list(indicators.keys())

    results_container = []

    for country in selected_countries:
        for indicator in selected_indicators:
            json_file_path = os.path.join(best_params_base_path, indicator, f"{model_selected}_{country}.json")

            if os.path.exists(json_file_path):
                try:
                    with open(json_file_path, 'r') as file:
                        json_data = json.load(file)

                    df = pd.json_normalize(json_data)
                    df.insert(0, 'Country', country)
                    df.insert(0, 'Model', model_selected)
                    df.insert(0, 'Indicator', indicator)

                    if model_selected == "XGBoost":
                        features_file_path = os.path.join(best_params_base_path, indicator, f"SelectedFeatures_{country}.json")
                        if os.path.exists(features_file_path):
                            with open(features_file_path, 'r') as feature_file:
                                feature_data = json.load(feature_file)
                            for i, feature in enumerate(feature_data):
                                df[f"Feature_{i+1}"] = feature

                    results_container.append(df)
                except json.JSONDecodeError:
                    st.error(f"Error decoding JSON from: {json_file_path}")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
            else:
                st.warning(f"No data for {model_selected} in {country} under {indicator}")

    if not results_container:
        st.warning("No data available for the selected parameters.")
    else:
        final_df = pd.concat(results_container, ignore_index=True)
        st.dataframe(final_df)

    # Updated sidebar explanation
    with st.sidebar.expander("About Model Best Params"):
        st.write("""
        This tab allows you to explore the **best model parameters** stored in JSON files for different country, indicator, and model combinations.

        - **Country & Indicator Selection:**  
          - Use the multi-select dropdowns to choose specific countries and indicators.  
          - If left empty, all countries and indicators are included by default.

        - **Model Selection:**  
          - Choose a model type (e.g., XGBoost, Random Forest).

        - **Processing:**  
          - The system loads JSON files based on selections and displays the extracted parameters.  
          - If XGBoost is selected, it also loads the `SelectedFeatures` JSON file, if available.

        - **Results:**  
          - The extracted data is shown in a table.  
          - If no matching data is found, a warning is displayed.

        Use this tab to analyze model parameters efficiently!
        """)



# Tab 4 - Input Data
with tab4:
    base_path = "data/base"

    # Check if required files and directories exist
    if not os.path.isdir(base_path):
        st.error(f"The directory '{base_path}' does not exist.")
    elif not os.path.isfile(countries_file):
        st.error(f"The file '{countries_file}' does not exist.")
    elif not os.path.isfile(indicators_file):
        st.error(f"The file '{indicators_file}' does not exist.")
    else:
        try:
            # Load country and indicator names from JSON files
            with open(countries_file, 'r') as f:
                countries = list(json.load(f).keys())
            with open(indicators_file, 'r') as f:
                indicators = list(json.load(f).keys())


            if not countries or not indicators:
                st.error("No valid country or indicator data found.")
            else:
                # Arrange selection boxes in a row
                col1, col2 = st.columns(2)
                with col1:
                    country_selected = st.multiselect("Select Country", options=countries, default=[],key = 11154)
                with col2:
                    indicator_selected = st.multiselect("Select Indicator", options=indicators, default=[], key = 15468787)

                # If nothing is selected, include all options
                selected_countries = country_selected if country_selected else countries[1:]
                selected_indicators = indicator_selected if indicator_selected else indicators[1:]

                def load_and_combine_data(countries, indicators):
                    """Helper function to load and aggregate data."""
                    all_dfs = []
                    for country in countries:
                        for indicator in indicators:
                            file_name = f"{country.replace(' ', '_')}_{indicator.replace(' ', '_')}.parquet"
                            file_path = os.path.join(base_path, file_name)
                            if os.path.isfile(file_path):
                                df = pd.read_parquet(file_path).dropna()
                                df['Country'] = country
                                df['Indicator'] = indicator
                                all_dfs.append(df)
                    return pd.concat(all_dfs, ignore_index=True) if all_dfs else None

                # Load and combine data based on selections
                if selected_countries and selected_indicators:
                    combined_df = load_and_combine_data(selected_countries, selected_indicators)
                    combined_df.loc[combined_df["Indicator"].isin(["GDP (USD)"]), "Value"] /= 1_000_000_000
                    combined_df["Year"] = combined_df["Year"].astype(str)
                    if combined_df is not None:

                        st.dataframe(combined_df, width=600, height=500)
                    else:
                        st.error("No data found for the selected criteria.")
                else:
                    st.warning("Please select at least one country and one indicator.")

        except Exception as e:
            st.error(f"Error loading JSON files: {e}")

    # Updated sidebar explanation
    with st.sidebar.expander("About Input Data"):
        st.write("""
        This tab allows you to explore and analyze data from multiple countries and indicators.

        - **Country & Indicator Selection:**  
          - Use the multi-select dropdowns to choose specific countries and indicators.  
          - If no specific country or indicator is selected, all options are included by default.

        - **Data Handling:**  
          - The system dynamically loads `.parquet` files based on the selected country and indicator.  
          - If "All Countries" or "All Indicators" is selected, data is aggregated across the chosen countries/indicators.

        - **Results:**  
          - The extracted data is displayed in a table.  
          - If no matching data is found, a warning is displayed.

        Use this tab to explore data across different countries and indicators efficiently!
        """)




