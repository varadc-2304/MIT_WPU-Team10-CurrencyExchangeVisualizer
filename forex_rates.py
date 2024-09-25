import streamlit as st
import pandas as pd
import re
import pymongo
from pymongo import MongoClient
import datetime

# MongoDB client setup
client = pymongo.MongoClient("mongodb+srv://vaidat:qwerty123@nt-hackathon.a7lhy.mongodb.net/")
db = client["currency_exchange"]

# Fetch currency list from MongoDB
get_currencies = db.rate_new.find({}, {"_id": 0})
currencies = pd.DataFrame(list(get_currencies))
currency_list = list(currencies.columns)[1:]

def main():
    st.title("Currency Table")
    container2 = st.container()
    container3 = st.container()

    with container2:
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            from_curr = st.selectbox("Base Currency", currency_list)
            # from_curr = re.search(r"\((.*?)\)", from_curr)
            # from_curr = from_curr.group(1)
        with col5:
            start_date = st.date_input("Date", min_value=datetime.date(2012, 1, 1))
        
        # Convert datetime.date to datetime.datetime for MongoDB query
        start_date = datetime.datetime.combine(start_date, datetime.datetime.min.time())
        
        # Fetch data from MongoDB within the specified date range
        data_of_date = db.rate_new.find({"Date": start_date}, {"_id": 0})

        data = [doc for doc in data_of_date]

        if not data:
            st.warning("No data retrieved for the given date.")
            return  # Early exit if no data

        # Create DataFrame from fetched data
        df = pd.DataFrame(data)

        if '_id' in df.columns:
            df = df.drop(columns=['_id'])

        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d', errors='coerce')
            df.set_index('Date', inplace=True)
            df.sort_index(inplace=True)
            
            
    print(df)
    
    data = {
        "Currency":list(df.columns)[1:],
        "Rate": df.iloc[0].values[1:]/df.get(from_curr).values[0]
    }

    # Creating a DataFrame
    df = pd.DataFrame(data)

    # Display the table using st.table
    st.table(df)

if __name__ == "__main__":
    main()
