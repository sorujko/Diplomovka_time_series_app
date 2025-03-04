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
tab1, tab2, tab3 = st.tabs(["🤺 1 vs 1", "🚀 Result_comparison", "📝 Order_quesser"])

import streamlit as st
import pandas as pd
import glob
import os

with tab1:
    model_types = ["", "ARIMA", "Holt-Winters", "XGBoost", "LSTM", "Prophet"]
    indicators_opt = list(indicators.keys())
    countries_opt = list(countries.keys())

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        model_1 = st.selectbox("Select Model", options=model_types, key=74121)
    with col2:
        model_2 = st.selectbox("Select Model", options=model_types, key=74133)
    with col3:
        indicator_selected = st.selectbox("Select Indicator", options=indicators_opt, key=741299)
    with col4:
        country_selected = st.selectbox("Select Country", options=countries_opt, key=7412992)

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
    df = df.loc[(df['Country'] == country_selected) & (df['Indicator'] == indicator_selected)]

    

    if model_1 and model_2 and model_1 != model_2:

        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            st.empty()
        with col2:
            st.empty()
        with col3:
            show_real_table = st.button("Show Real Data")
        with col4:
            quess = st.selectbox("Make a quess", options=[model_1,model_2], key=7412996)
        with col5:
            st.empty()
        with col6:
            st.empty()
        

        model_1_df = df.loc[df['Model'] == model_1, ['Model', 'RMSE']].rename(columns={'Model': 'Model_1', 'RMSE': 'RMSE_1'})
        model_2_df = df.loc[df['Model'] == model_2, ['RMSE', 'Model']].rename(columns={'Model': 'Model_2', 'RMSE': 'RMSE_2'})
        if indicator_selected == "GDP (USD)":

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
                
                # Check if RMSE values and guesses are correct
                if rmse_1 < rmse_2 and quess == row["Model_1"]:
                    spravna_odpoved = True
                elif rmse_1 > rmse_2 and quess == row["Model_2"]:
                    spravna_odpoved = True
                else:
                    spravna_odpoved = False
                

        # Add the dummy table HTML structure
        table_html_2 ="""
            <style>
            .center-table-2 { 
                margin: auto; 
                width: 60%; 
                border-collapse: collapse;
                text-align: center;
                font-family: Arial, sans-serif;
            }
            .center-table-2 th, .center-table-2 td {
                border: 1px solid black;
                padding: 10px;
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

        if not show_real_table:
            # Display the dummy table first with "?" placeholders
            st.markdown(table_html_2, unsafe_allow_html=True)

        # Now display the real table with RMSE values
        table_html ="""
            <style>
            .center-table { 
                margin: auto; 
                width: 60%; 
                border-collapse: collapse;
                text-align: center;
                font-family: Arial, sans-serif;
            }
            .center-table th, .center-table td {
                border: 1px solid black;
                padding: 10px;
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

        if show_real_table:
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
    x = st.selectbox("Select first file", options=files, format_func=lambda f: f.split("log_")[1].replace(".csv", ""), index=0)
    y = st.selectbox("Select second file", options=files, format_func=lambda f: f.split("log_")[1].replace(".csv", ""), index=1)

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




    