import streamlit as st
import os
import pandas as pd
import json
import glob
import numpy as np

st.set_page_config(page_title="Data_wars", page_icon="⚔️", layout="wide")
# Page Title
st.title("⚔️ Data Wars")

st.write("Small interactive games with data.")

with st.sidebar.expander("ℹ️ Important Notes"):
    st.write("Indicator **GDP (USD)** has it's values **billions USD** in Value column (Ukazovateľ GDP (USD) ma v stĺpci Value hodnoty v miliardách USC)")

col1, col2, col3, col4 , col5  = st.columns(5)
with col1:
    st.page_link("pages/🖼️Graph_gallery.py", label="**Graph Gallery**", icon="🖼️")

with col2:
    st.page_link("pages/🕵Data_exploration.py", label="**Data Exploration**", icon="🕵️")

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
tab1, tab2 = st.tabs(["🤺 1 vs 1", "🚀 Result_comparison"])

import streamlit as st
import pandas as pd
import glob
import os
import random

with st.sidebar.expander("About 1 vs 1"):
                st.write("""
    In this section, you can make a guess what model performs better for randomly chosen **country** and **indicator**.

    - **Press the button:**  
      - Press the button with model name you believe performed better for this country - indicator combination

    - **Result:**  
      - After you press button table will reveal it's content and you will see if you guessed correctly 

    - **Play again:**  
      - Press the Try again button to play again.

    """)

with tab1:
    model_types = ["ARIMA", "Holt-Winters", "XGBoost", "LSTM", "Prophet"]
    indicators_opt = list(indicators.keys())
    countries_opt = list(countries.keys())
    if "random_model_1" not in st.session_state:

        random_model_1 = random.choice(model_types)
        random_model_2 = random.choice(model_types)
        random_country_index = random.randint(1, len(countries_opt) - 1)
        random_indicator_index = random.randint(1, len(indicators_opt) - 1)

        while random_model_2 == random_model_1:
            random_model_2 = random.choice(model_types)

        # Store the random selections in session state
        st.session_state.random_model_1 = random_model_1
        st.session_state.random_model_2 = random_model_2
        st.session_state.random_country_index = random_country_index
        st.session_state.random_indicator_index = random_indicator_index
    else:
        # Use previously stored selections
        random_model_1 = st.session_state.random_model_1
        random_model_2 = st.session_state.random_model_2
        random_country_index = st.session_state.random_country_index
        random_indicator_index = st.session_state.random_indicator_index


    # Stylish table-like display with headers for Indicator and Country
    st.markdown(f"""
    <div style="width:600px; margin: 0 auto; text-align: center; padding: 20px 0;">
        <table style="width: 600px; border: 1px solid #ccc; border-collapse: collapse; table-layout: fixed;">
            <thead>
                <tr style="background-color:rgb(54, 56, 58); color: white; font-size: 18px; font-weight: bold;">
                    <th style="padding: 5px; width: 50%;">Indicator</th>
                    <th style="padding: 5px; width: 50%;">Country</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="padding: 5px; font-size: 16px; color: #0073e6; text-align: center;">{indicators_opt[random_indicator_index]}</td>
                    <td style="padding: 5px; font-size: 16px; color: #28a745; text-align: center;">{countries_opt[random_country_index]}</td>
                </tr>
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)


    # Get the most recent file
    folder_path = "data/final/log_files"
    files = sorted(glob.glob(os.path.join(folder_path, "model_error_log_*.csv")), reverse=True)

    if files:
        latest_file = files[0]  # Most recent file
    else:
        st.error("No log files found in the directory.")
        st.stop()

    # Load data
    df = pd.read_csv(latest_file)
    df = df.loc[(df['Country'] == countries_opt[random_country_index]) & (df['Indicator'] == indicators_opt[random_indicator_index])]

    if random_model_1 and random_model_2 and random_model_1 != random_model_2:

        # Create 7 columns with specific relative widths
        col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 1, 1, 3, 1])
        
        # Track if either button has been clicked
        if 'button_pressed' not in st.session_state:
            st.session_state['button_pressed'] = False
        else:
            st.session_state['button_pressed'] = True

        with col2:
            # Disable both buttons if any of them has been pressed
            disable_buttons = st.session_state['button_pressed']
            
            if st.button('Try again'):
                # Reset all session state variables and enable buttons again
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
        # Custom CSS for wider buttons
        
        with col3:
            chosen_1 = st.button(f"{random_model_1}", disabled=disable_buttons)
            if chosen_1 and st.session_state['button_pressed'] == False :
                st.session_state['button_pressed'] = True  # Disable both buttons after first click
        st.markdown("""
            <style>
                .stButton > button {
                    width: 110px;
                }
            </style>
        """, unsafe_allow_html=True)

        with col4:
            chosen_2 = st.button(f"{random_model_2}", key=113, disabled=disable_buttons)
            if chosen_2 and st.session_state['button_pressed'] == False:
                st.session_state['button_pressed'] = True  # Disable both buttons after first click
        
        

        model_1_df = df.loc[df['Model'] == random_model_1, ['Model', 'RMSE']].rename(columns={'Model': 'Model_1', 'RMSE': 'RMSE_1'})
        model_2_df = df.loc[df['Model'] == random_model_2, ['RMSE', 'Model']].rename(columns={'Model': 'Model_2', 'RMSE': 'RMSE_2'})
        if indicators_opt[random_indicator_index] == "GDP (USD)":

            model_1_df['RMSE_1'] = model_1_df['RMSE_1'] / 1_000_000_000  # Divide by 1 billion
            model_2_df['RMSE_2'] = model_2_df['RMSE_2'] / 1_000_000_000  # Divide by 1 billion
        # Concatenate the dataframes horizontally
        merged_df = pd.concat([model_1_df.reset_index(drop=True), model_2_df.reset_index(drop=True)], axis=1)

        # Add RMSE comparison column
        if not merged_df.empty:
            merged_df["Comparison"] = merged_df.apply(lambda row: "<" if row["RMSE_1"] < row["RMSE_2"] else ">", axis=1)

            # Initialize variable for the answer check
            spravna_odpoved = False

            for index, row in merged_df.iterrows():
                rmse_1 = row["RMSE_1"]
                rmse_2 = row["RMSE_2"]
                
                
                

        # Add the dummy table HTML structure
        table_html_2 = """
            <style>
            .center-table-2 { 
                margin: auto; 
                width: 600px; /* Set a fixed width */
                border-collapse: collapse;
                text-align: center;
                font-family: Arial, sans-serif;
                table-layout: fixed; /* Ensures fixed column widths */
            }
            .center-table-2 th, .center-table-2 td {
                border: 1px solid black;
                padding: 10px;
                width: 120px; /* Set fixed column width */
                word-wrap: break-word; /* Prevents overflow */
            }
            .center-table-2 th {
                background-color: #333;
                color: white;
            }
        </style>
        <table class="center-table-2">
            <tr>
                <th>Model 1</th>
                <th>RMSE 1</th>
                <th>Comparison</th>
                <th>RMSE 2</th>
                <th>Model 2</th>
            </tr>
        """

        # Add rows with "?" for RMSE and comparison but correct Model values
        for _, row in merged_df.iterrows():
            table_html_2 += f"""<tr>
                <td>{row["Model_1"]}</td>
                <td>?</td>
                <td>?</td>
                <td>?</td>
                <td>{row["Model_2"]}</td>
            </tr>"""

        table_html_2 += "</table>"

        if not chosen_1 and not chosen_2:
            # Display the dummy table first with "?" placeholders
            st.markdown(table_html_2, unsafe_allow_html=True)

        # Now display the real table with RMSE values
        table_html ="""
            <style>
            .center-table { 
                margin: auto; 
                width: 600px; 
                border-collapse: collapse;
                text-align: center;
                font-family: Arial, sans-serif;
                table-layout: fixed; /* Ensures fixed column widths */
            }
            .center-table th, .center-table td {
                border: 1px solid black;
                padding: 10px;
                width: 120px; /* Set fixed column width */
                word-wrap: break-word; /* Prevents overflow */
            }
            .center-table th {
                background-color: #333;
                color: white;
            }
            .better {
                font-weight: bold;
                color: green;
            }
            .worse {
                font-weight: bold;
                color: red;
            }
        </style>
        <table class="center-table">
            <tr>
                <th>Model 1</th>
                <th>RMSE 1</th>
                <th>Comparison</th>
                <th>RMSE 2</th>
                <th>Model 2</th>
            </tr>
        """

        for _, row in merged_df.iterrows():
            rmse_1_style = 'better' if row["RMSE_1"] < row["RMSE_2"] else 'worse'
            rmse_2_style = 'better' if row["RMSE_2"] < row["RMSE_1"] else 'worse'

            table_html += f"""<tr>
                <td>{row["Model_1"]}</td>
                <td class="{rmse_1_style}">{row["RMSE_1"]:.4f}</td>
                <td>{row["Comparison"]}</td>
                <td class="{rmse_2_style}">{row["RMSE_2"]:.4f}</td>
                <td>{row["Model_2"]}</td>
            </tr>
            """

        table_html += "</table>"

        if chosen_1 or chosen_2:
            
            # Check if RMSE values and guesses are correct
            if rmse_1 < rmse_2 and chosen_1:
                spravna_odpoved = True
            elif rmse_1 > rmse_2 and chosen_2:
                spravna_odpoved = True
            else:
                spravna_odpoved = False
    # Display the real table with RMSE values and comparison
            st.markdown(table_html, unsafe_allow_html=True)
            
            # Define the style for the messages
            if spravna_odpoved:
                message = "Good guess"
                message_style = """
                <style>
                .good-guess {
                    color: gold;
                    font-weight: bold;
                    text-align: center;
                }
                </style>
                """
            else:
                message = "Nice try, maybe next time"
                message_style = """
                <style>
                .bad-guess {
                    color: silver;
                    font-weight: bold;
                    text-align: center;
                }
                </style>
                """
            
            # Apply the styles and display the message
            st.markdown(message_style, unsafe_allow_html=True)
            st.markdown(f'<p class="{ "good-guess" if spravna_odpoved else "bad-guess" }">{message}</p>', unsafe_allow_html=True)

            



with tab2:
    model_types = ["ARIMA", "Holt_Winters", "XGBoost", "LSTM", "Prophet"]
    base_path = "data/base"

    pd.set_option('display.float_format', '{:.2f}'.format)
    col1, col2, col3 = st.columns(3)

    with col1:
        country_selected = st.multiselect("Select Country", options=list(countries.keys()), default=[], key=6556327)
    with col2:
        indicator_selected = st.multiselect("Select Indicator", options=list(indicators.keys()), default=[], key=998741)
    with col3:
        model_selected = st.selectbox("Select Model", options=model_types, key=7412)

    # If nothing is selected, include all options
    selected_countries = country_selected if country_selected else countries.keys()
    selected_indicators = indicator_selected if indicator_selected else indicators.keys()
    folder_path = f"data/{model_selected}_train"

    files = sorted(glob.glob(os.path.join(folder_path, f"{model_selected}_error_log_*.csv")), reverse=True)

    # Ensure there are at least two files
    if len(files) < 2:
        raise ValueError("Not enough files found in the directory.")

    # Extract timestamps from filenames
    file_labels = [f.split("log_")[1].replace(".csv", "") for f in files]

    # File selectors
    x = st.selectbox("Select first file", options=files, format_func=lambda f: f.split("log_")[1].replace(".csv", ""), index=0, key = 877)
    y = st.selectbox("Select second file", options=[f for f in files if f != x], format_func=lambda f: f.split("log_")[1].replace(".csv", ""), index=1, key = 876)

    # Load the CSV files
    x_df = pd.read_csv(x)
    y_df = pd.read_csv(y)

    # Merge and process
    z = x_df.merge(y_df, how='inner', on=['Country', 'Indicator', 'Model']).drop(['Rank_x', 'Rank_y'], axis=1)

    if selected_countries:
        z = z.loc[z['Country'].isin(selected_countries)]

    if selected_indicators:
        z = z.loc[z['Indicator'].isin(selected_indicators)]

    # Rename X and Y to time_x and time_y
    time_x = x.split("log_")[1].replace(".csv", "")
    time_y = y.split("log_")[1].replace(".csv", "")

    z.rename(columns={'RMSE_x': f'RMSE_{time_x}', 'RMSE_y': f'RMSE_{time_y}'}, inplace=True)

    # Mask for rounding and GDP division
    mask_gdp = z['Indicator'] == "GDP (USD)"
    mask_other = ~mask_gdp

    # Divide by billion if GDP (USD)
    z.loc[mask_gdp, [f'RMSE_{time_x}', f'RMSE_{time_y}']] /= 1_000_000_000

    # Round to 2 decimals if not GDP (USD)
    z.loc[mask_other, [f'RMSE_{time_x}', f'RMSE_{time_y}']] = z.loc[mask_other, [f'RMSE_{time_x}', f'RMSE_{time_y}']].round(2)

    # Calculate difference and determine winner
    z['Rozdiel'] = abs(z[f'RMSE_{time_x}'] - z[f'RMSE_{time_y}'])

    conditions = [z[f'RMSE_{time_x}'] < z[f'RMSE_{time_y}'], z[f'RMSE_{time_x}'] > z[f'RMSE_{time_y}']]
    choices = [time_x, time_y]
    z['Winner'] = np.select(conditions, choices, default='Remíza')
    z = z.drop('Model', axis=1)
    st.dataframe(z)

with st.sidebar.expander("About Model Comparison"):
        st.write("""
    In this section, you can compare RMSE values of different forecasting models for selected **countries** and **indicators**. Here's how it works:

    - **Filters:**  
      - Select one  **country**.  
      - Choose one **indicator** (e.g., GDP, inflation).  
      - Pick a **forecasting model** from available options (ARIMA, Holt-Winters, XGBoost, LSTM, Prophet).  

    - **File Selection:**  
      - You can select two different error log files containing RMSE values from different training runs.  
      - The most recent file is pre-selected, but you can choose any available logs.  

    - **Output:**  
      - A table displaying RMSE values for both selected files.  
      - RMSE difference between the two files.  
      - The **better-performing model** for each country and indicator based on RMSE comparison.  

    Use the filters and selectors to analyze forecasting performance across different models and datasets!
    """)
    