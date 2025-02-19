import streamlit as st
import os
import json
# Page Configuration
st.set_page_config(
    page_title="Macroeconomic Forecasting: Master's Thesis",
    page_icon="📈",
    layout="centered",
    initial_sidebar_state="expanded"
)


# Main Page Content
def main():
    # Title and Introduction
    st.title("📊 Forecasting Macroeconomic Indicators")
    st.markdown("""
    ### **Master's Thesis**  
    Welcome to the interactive overview of my Master's Thesis project:  
    **"Forecasting Macroeconomic Indicators: Comparing Traditional Methods with Machine Learning Techniques."**
    """)
    
    # Links to other pages (side by side, grouped in columns 1 and 2)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.page_link("pages/🕵Data_exploration.py", label="**Data Exploration**", icon="🕵️")


    with col2:
        st.page_link("pages/🖼️Graph_gallery.py", label="**Graph Gallery**", icon="🖼️")
 
    with col3:
        st.empty()  # Placeholder for spacing

    with col4:
        st.empty()  # Placeholder for spacing
    
    col1, col2 = st.columns(2)
    countries_file = "countries.json"
    indicators_file = "indicators.json"
    # Loading and displaying countries.json in the first column
    with col1:
        if os.path.exists(countries_file):
            with open(countries_file, "r") as file:
                countries_data = json.load(file)
            with st.expander("### Countries", expanded=False):  # Collapsible section
                st.json(countries_data)  # Display the contents of countries.json
        else:
            st.error(f"{countries_file} not found.")

    # Loading and displaying indicators.json in the second column
    with col2:
        if os.path.exists(indicators_file):
            with open(indicators_file, "r") as file:
                indicators_data = json.load(file)
            with st.expander("### Indicators", expanded=False):  # Collapsible section
                st.json(indicators_data)  # Display the contents of indicators.json
        else:
            st.error(f"{indicators_file} not found.")
    
    st.markdown("""
    <small>Explore Country: https://data.worldbank.org/country/{country_code}</small>
""", unsafe_allow_html=True)
    st.markdown("""
    <small>Explore Indicator: https://data.worldbank.org/indicator/{indicator_code}</small>
""", unsafe_allow_html=True)
    st.markdown("""
    <small>Get data: https://api.worldbank.org/v2/country/{country_code}/indicator/{indicator_code}</small>
""", unsafe_allow_html=True)
    st.markdown("""
    <small>(You have to fill {} with correct values for actual results to be displayed , examples are JSON values)</small>
""", unsafe_allow_html=True)
    


    # Overview Section
    st.markdown("""
    ---
    ### **Project Overview**  
    The thesis explores and evaluates the performance of different forecasting methods for macroeconomic indicators using univariate time series analysis. The primary goal is to compare the accuracy and effectiveness of **traditional forecasting models** with **modern machine learning techniques**.
    
    #### **Key Objectives:**  
    - Analyze the behavior and predictability of macroeconomic indicators.  
    - Compare **traditional approaches**, such as:  
        - **ARIMA (AutoRegressive Integrated Moving Average)**.  
        - **Holt-Winters Exponential Smoothing**.  
    - Benchmark these methods against **machine learning models**, including:  
        - **Prophet**.  
        - **XGBoost**.  
        - **LSTM (Long Short-Term Memory Networks)**.  
    - Evaluate the models' predictive accuracy and identify the strengths and weaknesses of each approach.  
    """)

# Sidebar Content
def sidebar():
    st.sidebar.header("About Me")
    st.sidebar.markdown("""
    **Author:** Your Name  
    **University:** Your Institution  
    **Field of Study:** Data Science / Economics
    **CRZP:** [Your CRZP Link](#)  
    **Year:** 2025
    ____________
    GitHub (this app) : [click](https://github.com/sorujko/Diplomovka_time_series)  
    GitHub (models) : [click](https://github.com/sorujko/Diplomovka_time_series_app)  
    LinkedIn : [click](https://www.linkedin.com/in/juraj-hakos1/)
    """)

# Run the App
if __name__ == "__main__":
    sidebar()
    main()
