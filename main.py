import streamlit as st

# Main page title
st.set_page_config(page_title="Main Page", page_icon="🌟", layout="centered")

# Title and description
st.title("Welcome to the Main Page! 🌟")
st.write(
    """
    This is the main page of your Streamlit app. You can use this space to display 
    information, collect inputs, or show visualizations.
    """
)

# Example inputs
st.header("Interactive Section")
name = st.text_input("Enter your name:", "")
if name:
    st.write(f"Hello, {name}! 👋")

# Example button
if st.button("Click Me!"):
    st.success("Button clicked! 🚀")

# Example sidebar
st.sidebar.title("Navigation")
st.sidebar.write("Use the sidebar to navigate to other sections.")

# Footer
st.markdown("---")
st.markdown("💡 *Powered by Streamlit*")
