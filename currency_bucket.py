import streamlit as st
import requests
import matplotlib.pyplot as plt


# Function to fetch exchange rates
def fetch_exchange_rates(base_currency):
    url = f"https://v6.exchangerate-api.com/v6/67663e5c57d81adae0ce6789/latest/{base_currency}"
    response = requests.get(url)
    data = response.json()
    
    return data['conversion_rates']

# List of all currencies
CURRENCY_LIST = [
    "USD", "AED", "AFN", "ALL", "AMD", "ANG", "AOA", "ARS", "AUD",
    "AWG", "AZN", "BAM", "BBD", "BDT", "BGN", "BHD", "BIF", "BMD",
    "BND", "BOB", "BRL", "BSD", "BTN", "BWP", "BYN", "BZD", "CAD",
    "CDF", "CHF", "CLP", "CNY", "COP", "CRC", "CUP", "CVE", "CZK",
    "DJF", "DKK", "DOP", "DZD", "EGP", "ERN", "ETB", "EUR", "FJD",
    "FKP", "FOK", "GBP", "GEL", "GGP", "GHS", "GIP", "GMD", "GNF",
    "GTQ", "GYD", "HKD", "HNL", "HRK", "HTG", "HUF", "IDR", "ILS",
    "IMP", "INR", "IQD", "IRR", "ISK", "JEP", "JMD", "JOD", "JPY",
    "KES", "KGS", "KHR", "KID", "KMF", "KRW", "KWD", "KYD", "KZT",
    "LAK", "LBP", "LKR", "LRD", "LSL", "LYD", "MAD", "MDL", "MGA",
    "MKD", "MMK", "MNT", "MOP", "MRU", "MUR", "MVR", "MWK", "MXN",
    "MYR", "MZN", "NAD", "NGN", "NIO", "NOK", "NPR", "NZD", "OMR",
    "PAB", "PEN", "PGK", "PHP", "PKR", "PLN", "PYG", "QAR", "RON",
    "RSD", "RUB", "RWF", "SAR", "SBD", "SCR", "SDG", "SEK", "SGD",
    "SHP", "SLE", "SLL", "SOS", "SRD", "SSP", "STN", "SYP", "SZL",
    "THB", "TJS", "TMT", "TND", "TOP", "TRY", "TTD", "TVD", "TWD",
    "TZS", "UAH", "UGX", "UYU", "UZS", "VES", "VND", "VUV", "WST",
    "XAF", "XCD", "XDR", "XOF", "XPF", "YER", "ZAR", "ZMW", "ZWL"
] # Your currency list here



# Streamlit application
def main():
    st.title("Custom Currency Basket")

    # Input base currency and amount invested
    col1, col2 = st.columns(2)  # Create two columns for better layout
    with col1:
        base_currency = st.selectbox("Select your Base Currency", options=CURRENCY_LIST, index=CURRENCY_LIST.index("INR"))
    with col2:
        amount_invested = st.number_input(f"Enter the amount invested in {base_currency}", min_value=0.0, format="%.2f")

    st.write("---")  # Horizontal line for separation

    # Input currency distribution
    st.write("### Enter the distribution of your investment in different currencies:")
    currencies = st.multiselect("Select Currencies", options=CURRENCY_LIST, default=["USD"])
    weights = {}

    # User input for weights
    for currency in currencies:
        weight = st.number_input(f"Enter the weight for {currency} (%)", min_value=0.0, max_value=100.0, format="%.2f")
        weights[currency] = weight

    # Calculate total weight and validate
    total_weight = sum(weights.values())
    if total_weight > 100:
        st.error("Total weight exceeds 100%. Please adjust the weights.")
    elif total_weight < 100 and total_weight > 0:
        st.warning("Total weight is less than 100%. Adjust weights to distribute properly.")

    # Fetch exchange rates and calculate worth of investments in other currencies
    if st.button("Calculate Worth"):
        exchange_rates = fetch_exchange_rates(base_currency)
        worths = {}
        
        for currency, weight in weights.items():
            # Calculate worth of investment in each currency
            worth = (amount_invested * (weight / 100)) * exchange_rates[currency]
            worths[currency] = worth

        # Display the results
        st.write("### Worth of investments in different currencies:")
        for currency, worth in worths.items():
            st.write(f"{worth:.2f} {currency}")

        # Visualization: Line chart for percent distribution
        if worths:
            # Prepare data for plotting
            labels = list(worths.keys())
            sizes = [weight for weight in weights.values()]
            amounts = list(worths.values())
            percentage_distribution = [(weight / total_weight) * 100 for weight in sizes]

            plt.figure(figsize=(10, 6))
            plt.plot(labels, percentage_distribution, marker='o', linestyle='-', color='b', label='Percent Distribution')

            # Annotate the amounts on the line chart
            for i, amount in enumerate(amounts):
                plt.text(labels[i], percentage_distribution[i], f'{amount:.2f}', ha='center', va='bottom')

            plt.title('Investment Percent Distribution by Currency')
            plt.xlabel('Currency')
            plt.ylabel('Percentage (%)')
            plt.xticks(rotation=45)
            plt.ylim(0, max(percentage_distribution) + 10)  # Give some space above the highest point
            plt.grid()
            plt.axhline(0, color='black', linewidth=0.5, ls='--')
            plt.legend()
            st.pyplot(plt)  # Render the line chart in the Streamlit app
            plt.close()  # Close the plot to avoid display issues

