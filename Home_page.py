import streamlit as st

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
        if st.button("🕵️ **Data Exploration**", key=156411677):
            st.markdown('<meta http-equiv="refresh" content="0; URL=/Data_exploration" />', unsafe_allow_html=True)

    with col2:
        if st.button("🖼️ **Graph Gallery**", key=15641165):
            st.markdown('<meta http-equiv="refresh" content="0; URL=/Graph_gallery" />', unsafe_allow_html=True)
 
    with col3:
        st.empty()  # Placeholder for spacing

    with col4:
        st.empty()  # Placeholder for spacing

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
