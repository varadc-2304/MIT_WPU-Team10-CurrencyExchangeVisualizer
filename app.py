import streamlit as st

# Importing your modules
import dashboard
import currency_bucket
import forex_rates
import exchange_rate

st.set_page_config(layout="wide")

# Display the project name as a branded title at the top
st.markdown(
    """
    <h1 style='text-align: center; color: #4CAF50;'>Exchangify</h1>
    <h5 style='text-align: center; color: #888;'>Navigate the World of Currency with Ease</h5>
    """,
    unsafe_allow_html=True
)

# Define a function to display content based on the selected tab
def display_page(tab):
    if tab == "Home":
        dashboard.main()
    elif tab == "Custom Currency Bucket":
        currency_bucket.main()
    elif tab == "Forex Rates":
        forex_rates.main()
    elif tab == "Exchange Rates":
        exchange_rate.main()

# Set up the top navigation using tabs
tabs = st.tabs(["Home", "Custom Currency Bucket", "Forex Rates", "Exchange Rates"])

# Display the selected tab
with tabs[0]:
    display_page("Home")
with tabs[1]:
    display_page("Custom Currency Bucket")
with tabs[2]:
    display_page("Forex Rates")
with tabs[3]:
    display_page("Exchange Rates")
