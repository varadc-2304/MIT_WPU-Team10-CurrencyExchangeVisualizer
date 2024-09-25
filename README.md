# Exchangify

## Abstract

Exchangify is an innovative Streamlit application designed to simplify the management and visualization of currency exchange rates. The application provides users with the ability to track and analyze the worth of investments across various currencies in real time. By leveraging a custom currency bucket feature, users can enter their base currency, distribution preferences, and investment amounts, making informed decisions easier than ever. Whether for personal finance or professional trading, Exchangify is the go-to solution for anyone navigating the complex world of currency exchange.

## Technologies Used

- **Streamlit**: For building the interactive web application.
- **Python**: The primary programming language used for developing the application logic.
- **MongoDB**: For storing and managing exchange rate data efficiently.
- **Exchange Rate API**: To fetch real-time exchange rates for currency comparisons and conversions.

## Features

- **Dashboard**: A central interface for users to select currencies, set time periods, and analyze exchange rate trends with detailed statistics and visualizations.
- **Custom Currency Bucket**: Users can create personalized baskets of currencies and analyze their investments.
- **Forex Rates**: Provides real-time foreign exchange rates against a selected base currency.
- **Exchange Rates**: Allows users to view exchange rates for all currencies supported by the application.

## Modules

### Dashboard

The Dashboard Module of Exchangify enables users to analyze currency trends through a straightforward and intuitive interface. Users start by selecting a primary and secondary currency, then specify the duration and enter the start and end dates for analysis. Based on this input, the module generates a comprehensive line graph illustrating the rates of the secondary currency compared to the primary currency. In addition to visualizing trends, it displays critical data points, including the maximum rate, minimum rate, average rate, and percentage increase. A standout feature of this module is its ability to convert the entered primary currency into the secondary currency, enhancing both user experience and functionality. The module also includes a risk factor analysis, which is based on the Standard Deviation of the exchange rates. The graph visually represents the risk level using a color-coded line: red for high fluctuation, orange for medium, and green for low fluctuation.

**Key Features:**

- **Currency Selection**: Choose primary and secondary currencies from a user-friendly dropdown menu.
- **Duration Specification**: Define the analysis period with start and end dates for tailored insights.
- **Line Graph Generation**: Visualize the exchange rate trends between selected currencies through a line graph.
- **Statistical Display**: View maximum, minimum, average rates, and percentage increase directly on the graph.
- **Risk Factor Analysis**: Color-coded lines (red, orange, green) show fluctuations based on Standard Deviation, along with a color box displaying volatility.
- **Currency Conversion**: Seamlessly convert the entered primary currency to the secondary currency.

### Custom Currency Basket

The Custom Currency Basket Module of Exchangify empowers users to manage and visualize their investments across multiple currencies seamlessly. Users begin by selecting a base currency and specifying the amount invested. Following this, they can choose from various currencies to create a distribution of their investment. The module allows users to input the weight of each currency, ensuring that the total weight is accurately maintained at 100%. Upon calculation, the module fetches the latest exchange rates and computes the worth of the investments in different currencies. A visually engaging line chart displays the percentage distribution of the investments, along with individual worths, enhancing the user’s understanding of their currency allocations.

**Key Features:**

- **Base Currency Selection**: Users can select their primary base currency and specify the amount invested.
- **Investment Distribution**: Choose from a list of currencies and define the investment distribution using weights.
- **Weight Validation**: The module validates that the total weight does not exceed or fall short of 100%.
- **Worth Calculation**: Fetches current exchange rates to calculate and display the worth of investments in selected currencies.
- **Visualization**: Displays a line chart showing the percentage distribution of investments across different currencies.

### Forex Rates

The Forex Rates Module in Exchangify provides a detailed snapshot of currency exchange rates relative to a selected base currency. Users input the base currency and the desired date, after which the module fetches the latest exchange rates for all other currencies. The exchange rates are presented in a tabular format, allowing users to easily compare the value of various currencies against their chosen base currency.

**Key Features:**

- **Base Currency Input**: Users can select their base currency for comparison.
- **Date Selection**: Choose the date for which the exchange rates should be retrieved.
- **Comprehensive Comparison**: Displays all other currency exchange rates in a table compared to the base currency.

### Exchange Rates

This module provides a real-time view of currency exchange rates using USD as the default base currency. It allows users to search and filter exchange rates by selecting a currency code from a dropdown menu. Upon selection, the module retrieves the exchange rate of the chosen currency against USD and displays it in a tabular format. If no specific currency is selected, the module presents the exchange rates of all available currencies compared to USD.

**Key Features:**

- **Live Data Fetching**: Retrieves up-to-date exchange rates using an external API.
- **Base Currency (USD)**: USD is set as the default base currency for rate comparison.
- **Searchable Dropdown**: Allows users to search and filter exchange rates by selecting a specific currency from the dropdown.
- **Dynamic Table**: Displays exchange rates in an easy-to-read table that adjusts to the screen width, enhancing user experience.

## Conclusion

Exchangify is a user-friendly platform for managing foreign exchange rates. It features custom currency baskets, real-time Forex data, and detailed trend analysis, enabling users to gain valuable insights into currency performance. Utilizing Streamlit, Python, MongoDB, and APIs, Exchangify offers an efficient solution for monitoring global currency fluctuations and enhancing financial decision-making.

## Installation

To run Exchangify locally, follow these steps:

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/MIT_WPU-Team10-Exchangify.git
   ```
2. Navigate to the project directory:
   ```sh
   cd MIT_WPU-Team10-Exchangify
   ```
3. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Run the application:
   ```sh
   streamlit run app.py
   ```

## Dataset

- **Source**: The CSV file can be downloaded from [here](https://github.com/varadc-2304/MIT_WPU-Team10-Exchangify/blob/main/NEW4_Exchange_Rate_Report_2012_2024.csv).

  For the data between 2022 and 2024, the dataset was generated from [here](https://www.imf.org/external/np/fin/ert/GUI/Pages/ReportOptions.aspx).

- **Pre-processing**: The preprocessed concatenated dataset in the CSV file was ingested in MongoDB. The schema for the MongoDB documents is provided in [schema.txt](https://github.com/varadc-2304/MIT_WPU-Team10-Exchangify/blob/main/schema.txt).

Preprocessing Steps:

1] Loading the Data:CSV files from 2012 to 2022 were loaded. The files have varying structures:
   i.2012 to 2018: 1 date column and 52 countries' exchange rates against USD.
   ii.2019 to 2021: 1 date column and 38 countries.
   iii.2022 : 1 date column and 37 countries.
   
2] Handling Missing Values:
   i.Interpolation:Used the "time" method of interpolation to fill missing values. This method considers the time index for smoothing the missing data across          consecutive dates.
   ii.Forward Fill (ffill):For any remaining missing values after interpolation, forward fill was applied to propagate the last available valid value forward.
   iii.Concatenating CSV Files:After handling the missing values, all CSV files from 2012 to 2022 were concatenated into one dataset to ensure consistency for 
    further processing.

3] Generating Data for 2023 and 2024:
   i.Created datasets for 2023 and 2024 with the same structure (date and 37 countries) as the 2022 file.
   ii.Filling Values:Used interpolation followed by forward fill to populate the values for the 2023 and 2024 data.
   
4] Adding Missing Dates:
   i.Checked for and added any missing dates within the timeline from 2012 to 2024 to ensure a continuous, complete date sequence.
   ii.Once missing dates were added, interpolation and forward fill were re-applied to fill in any new gaps in the data.
   
5] Handling Null Columns (2019-2024):
   i.For any remaining null values from 2019 to 2024:
   ii.Online Research: Checked the historical currency exchange rate graph online for the specific country from 2019 to the present date.
   iii.Identified key points:
         a)Exchange rate in 2019.
         b)Exchange rate at present.
         c)If a peak or maxima occurred during this period, noted that value.
   iv.Numpy Linspace: Used numpy.linspace() to generate evenly spaced values between 2019 and the present, ensuring a gradual and realistic progression of       
       exchange rates. Applied this to interpolate data, including the maxima when applicable.
       
6] Rounding Values:After completing the data filling, all exchange rate values were rounded to match the precision of the original dataset provided for the 
   earlier years.


