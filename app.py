from pymongo import MongoClient
from datetime import datetime
import requests
import streamlit as st

# MongoDB connection details
MONGO_URI = "mongodb+srv://varad:qwerty123@nt-hackathon.a7lhy.mongodb.net/"
DATABASE_NAME = "currency_exchange"
COLLECTION_NAME = "rate"

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

# Function to fetch exchange rates from the API
def fetch_exchange_rates(base_currency='USD'):
    url = f'https://v6.exchangerate-api.com/v6/67663e5c57d81adae0ce6789/latest/{base_currency}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error fetching exchange rate data.")
        return None

# Function to prepare data in the required structure
def prepare_data(data):
    cleaned_data = {
        'Date': datetime.now()  # Set the current date
    }

    # Populate the cleaned data with currency rates
    conversion_rates = data['conversion_rates']
    for currency_code, rate in conversion_rates.items():
        if currency_code in desired_currencies:
            currency_name = f"{data['conversion_rates'].get(currency_code, currency_code)} ({currency_code})"
            cleaned_data[currency_name] = rate

    return cleaned_data

# Function to insert data into MongoDB
def insert_data_into_mongodb(data):
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]

    # Check if today's date data already exists
    existing_entry = collection.find_one({
        'Date': {
            '$gte': datetime.combine(datetime.now().date(), datetime.min.time()),
            '$lt': datetime.combine(datetime.now().date(), datetime.max.time())
        }
    })

    # If the entry doesn't exist, insert it
    if existing_entry:
        st.info("Today's exchange rate data already exists in the database.")
    else:
        collection.insert_one(data)
        st.success("Data inserted successfully into MongoDB.")

# Fetch, prepare, and insert the data
def update_exchange_rate_data():
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
