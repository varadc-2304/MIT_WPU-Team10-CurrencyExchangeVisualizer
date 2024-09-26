import streamlit as st
import datetime
from datetime import datetime, timedelta
import pymongo
import re
import pandas as pd
import requests
import matplotlib.pyplot as plt

# MongoDB client setup
client = pymongo.MongoClient("mongodb+srv://vansh:qwerty123@nt-hackathon.a7lhy.mongodb.net/")
db = client["currency_exchange"]

# Fetch currency list from MongoDB
get_currencies = db.rate_new.find({}, {"_id": 0})
currencies = pd.DataFrame(list(get_currencies))
currency_list = list(currencies.columns)[1:]

def fetch_exchange_rates(from_curr, to_curr):
    url = f"https://v6.exchangerate-api.com/v6/67663e5c57d81adae0ce6789/latest/{from_curr}"
    response = requests.get(url)
    data = response.json()
    return data.get('conversion_rates', {}).get(to_curr, None)

def main():
    st.title("Currency Exchange")

    container2 = st.container()
    with container2:
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            from_curr = st.selectbox("From", currency_list, index=currency_list.index("US Dollar (USD)"))
        with col2:
            to_curr = st.selectbox("To", currency_list)
        with col5:
            duration = st.selectbox("Duration", ["Duration", "Week", "Month", "Quarter", "Year"])
            end_date = datetime.now().date()
            if duration == "Week":
                start_date = end_date - timedelta(days=7)
            elif duration == "Month":
                start_date = end_date - timedelta(days=30)
            elif duration == "Quarter":
                start_date = end_date - timedelta(days=90)
            elif duration == "Year":
                start_date = end_date - timedelta(days=365)
            else:
                start_date = datetime(2012, 1, 1)

        with col3:
            start_date = st.date_input("Start Date", value=start_date, min_value=datetime(2012, 1, 1), max_value=end_date)
        with col4:
            end_date = st.date_input("End Date", value=end_date, min_value=start_date, max_value=end_date)

    start_date = pd.to_datetime(start_date, format='%Y-%m-%d', errors='coerce')
    end_date = pd.to_datetime(end_date, format='%Y-%m-%d', errors='coerce')

    # Fetch data from MongoDB within the specified date range
    data_between_dates = db.rate_new.find({
        "Date": {"$gte": start_date, "$lte": end_date}
    })

    data = [doc for doc in data_between_dates]

    if not data:
        st.warning("No data retrieved for the given date range.")
        return  # Early exit if no data

    # Create DataFrame from fetched data
    df = pd.DataFrame(data)

    if '_id' in df.columns:
        df = df.drop(columns=['_id'])

    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d', errors='coerce')
        df.set_index('Date', inplace=True)
        df.sort_index(inplace=True)

    # Filter based on the selected currencies and date range
    if from_curr in currency_list and to_curr in currency_list:
        filtered_data = df[[from_curr, to_curr]].loc[start_date:end_date].reset_index()

        if filtered_data.empty:
            st.warning("No data available for the selected currencies and date range.")
            return  # Early exit if filtered data is empty

        # Calculate exchange rate
        if to_curr != from_curr:  # Check if currencies are different
            filtered_data["rate"] = filtered_data[to_curr] / filtered_data[from_curr]
        else:
            filtered_data["rate"] = 1  # Same currency case

        # Create a plot
        plt.figure(figsize=(10, 5))

        # Calculate standard deviation
        rate_std = filtered_data["rate"].std()

        # Choose color based on the standard deviation and set the label for the legend
        if rate_std > 2:
            color = 'red'  # High Risk
            risk_label = 'High Risk'
        elif 1 <= rate_std <= 2:
            color = 'orange'  # Moderate Risk
            risk_label = 'Moderate Risk'
        else:
            color = 'green'  # Safe
            risk_label = 'Safe'
        # Plot the rate
        ax = plt.gca()

        # Plot the line
        ax.plot(filtered_data['Date'], filtered_data['rate'], color=color, linewidth=2, label=risk_label)

        # Customize the color gradient
        gradient = ax.fill_between(filtered_data['Date'], filtered_data['rate'], color=color, alpha=0.2, label=risk_label,)
        # Plot the rate
        #plt.plot(filtered_data['Date'], filtered_data['rate'], color=color, label=risk_label)
        plt.title(f"Exchange Rate from {from_curr} to {to_curr} ({start_date.date()} to {end_date.date()})")
        plt.xlabel("Date")
        plt.ylabel("Exchange Rate")
        plt.grid()

        # Add the legend
        plt.legend(title="Risk Level", loc='upper left', fontsize='medium', bbox_to_anchor=(1, 1))

        # Display the plot in Streamlit
        st.pyplot(plt)

        # Display statistics
        max_rate_index = filtered_data["rate"].idxmax()
        max_rate = filtered_data["rate"].iloc[max_rate_index]
        max_rate_date = filtered_data.loc[max_rate_index, "Date"]

        min_rate_index = filtered_data["rate"].idxmin()
        min_rate = filtered_data["rate"].iloc[min_rate_index]
        min_rate_date = filtered_data.loc[min_rate_index, "Date"]

        avg_rate = filtered_data["rate"].mean()
        start_rate = filtered_data.iloc[0]["rate"] if not filtered_data.empty else None
        end_rate = filtered_data.iloc[-1]["rate"] if not filtered_data.empty else None
        pct_change = ((end_rate - start_rate) / start_rate * 100) if start_rate and end_rate else None

        col8, col9 = st.columns(2)
        with col9:
            st.header("Statistics")
            st.write(f"Max Rate: {max_rate:.2f} On Date: {max_rate_date}")
            st.write(f"Min Rate: {min_rate:.2f} On Date: {min_rate_date}")
            st.write(f"Average Rate: {avg_rate:.2f}")
            st.write(f"Percentage Change: {pct_change:.2f}%" if pct_change is not None else "N/A")

    else:
        st.warning(f"The selected currencies ({from_curr}, {to_curr}) are not available in the dataset.")

    # Currency Calculator
    # Currency Calculator
    with col8:
        st.header("Currency Calculator")
        
        # Extracting currency codes without the extra details
        from_curr_code = re.search(r"\((.*?)\)", from_curr).group(1)
        to_curr_code = re.search(r"\((.*?)\)", to_curr).group(1)

        rate = fetch_exchange_rates(from_curr_code, to_curr_code)

        if rate is not None:
            from_val = st.number_input(from_curr_code, 0)
            result = from_val * rate
            st.subheader(f"{from_val} X {rate} = {result:.2f} {to_curr_code}")
        else:
            st.warning(f"Exchange rate from {from_curr_code} to {to_curr_code} is not available.")




if __name__ == "__main__":
    main()
