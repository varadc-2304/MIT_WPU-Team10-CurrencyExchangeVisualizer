import streamlit as st
from pymongo import MongoClient
from datetime import datetime
import requests

# Importing your modules
import dashboard
import currency_bucket
import forex_rates
import exchange_rate

# MongoDB connection details
MONGO_URI = "mongodb+srv://varad:qwerty123@nt-hackathon.a7lhy.mongodb.net/"
DATABASE_NAME = "currency_exchange"
COLLECTION_NAME = "rate_new"

# List of currency codes you want to insert (filter from the fetched data)
desired_currencies = [
    "DZD", "AUD", "BHD", "VEF", "BWP", "BRL", "BND", "CAD", 
    "CLP", "CNY", "COP", "CZK", "DKK", "EUR", "HUF", "ISK", 
    "INR", "IDR", "IRR", "ILS", "JPY", "KZT", "KRW", "KWD", 
    "LYD", "MYR", "MUR", "MXN", "NPR", "NZD", "NOK", "OMR", 
    "PKR", "PEN", "PHP", "PLN", "QAR", "RUB", "SAR", "SGD", 
    "ZAR", "LKR", "SEK", "CHF", "THB", "TTD", "TND", "AED", 
    "GBP", "USD", "UYU", "VES"
]

# Set up page layout and branding
st.set_page_config(layout="wide")

st.markdown(
    """
    <h1 style='text-align: center; color: #4CAF50;'>Exchangify</h1>
    <h5 style='text-align: center; color: #888;'>Navigate the World of Currency with Ease</h5>
    """,
    unsafe_allow_html=True
)

# Function to check if today's data exists in MongoDB
def check_if_exists(db, collection, date):
    return collection.find_one({"Date": date}) is not None

# Function to fetch exchange rates from the API
def fetch_exchange_rates(base_currency='USD'):
    url = f'https://v6.exchangerate-api.com/v6/67663e5c57d81adae0ce6789/latest/{base_currency}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching exchange rate data.")
        return None

# Function to prepare data in the required structure
def prepare_data(data):
    cleaned_data = {
        'Date': datetime.now().strftime("%Y-%m-%d")  # Store as YYYY-MM-DD string
    }
    conversion_rates = data['conversion_rates']
    for currency_name, rate in conversion_rates.items():
        if currency_name in desired_currencies:
            cleaned_data[currency_name] = rate
    return cleaned_data

# Function to insert data into MongoDB
def insert_data_into_mongodb(data):
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]

    today_date = datetime.now().strftime("%Y-%m-%d")
    if check_if_exists(db, collection, today_date):
        print(f"Data for {today_date} already exists in the database.")
    else:
        if len(data) > 1:
            collection.insert_one(data)
            print(f"Data inserted successfully for {today_date} into MongoDB.")
        else:
            print("No desired currencies found to insert.")

# Wrapper function to check and insert today's rates when navigating to specific tabs
def check_and_update_rates():
    exchange_data = fetch_exchange_rates('USD')
    if exchange_data:
        prepared_data = prepare_data(exchange_data)
        insert_data_into_mongodb(prepared_data)

# Define a function to display content based on the selected tab
def display_page(tab):
    if tab == "Home":
        dashboard.main()
    elif tab == "Custom Currency Bucket":
        currency_bucket.main()
    elif tab == "Forex Rates":
        check_and_update_rates()  # Update exchange rates if needed
        forex_rates.main()
    elif tab == "Exchange Rates":
        check_and_update_rates()  # Update exchange rates if needed
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
