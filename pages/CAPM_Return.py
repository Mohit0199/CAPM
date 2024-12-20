import streamlit as st
import pandas as pd
import datetime
import yfinance as yf
import pandas_datareader.data as web
import pages.utils.capm_functions as capm_functions


st.set_page_config(
    page_title="CAPM",
    page_icon="chart_with_upwards_trend",
    layout="wide"
)

st.title("Capital Asset Pricing Model")

df = pd.read_excel("Yahoo Ticker Symbols.xlsx", sheet_name="Stock", header=3)
stock_tickers = df[df['Exchange'] == 'NSI']['Ticker'].to_list()

#Getting Input from User
col1, col2 = st.columns([1,1])
with col1:
    stocks_list = st.multiselect("Choose 4 Stocks", stock_tickers, ['TATAMOTORS.NS'], max_selections=4)
with col2:
    year = st.number_input("Number of Years", 1, 10)


#Downloading data
try:
    end = datetime.date.today()
    start = datetime.date(datetime.date.today().year-year, datetime.date.today().month, datetime.date.today().day)
    nifty50 = yf.download("^NSEI", start=start, end=end)['Close']
    nifty50.columns = ['NSE']

    stocks_df = pd.DataFrame()

    for stock in stocks_list:
        data = yf.download(stock, start=start, end=end)
        stocks_df[f'{stock}'] = data['Close']

    stocks_df.reset_index(inplace=True)
    nifty50.reset_index(inplace=True)
    nifty50.columns = ['Date', 'Nifty50']
    stocks_df['Date'] = stocks_df['Date'].astype('datetime64[ns]')
    stocks_df['Date'] = pd.to_datetime(stocks_df['Date'])
    stocks_df = pd.merge(stocks_df, nifty50, on='Date', how='inner')


    col1, col2 = st.columns([1,1])
    with col1:
        st.markdown("### Dataframe Head")
        st.dataframe(stocks_df.head(), use_container_width=True)
    with col2:
        st.markdown("### Dataframe Tail")
        st.dataframe(stocks_df.tail(), use_container_width=True)


    col1, col2 = st.columns([1,1])
    with col1:
        st.markdown("### Price of all the Stocks")
        st.plotly_chart(capm_functions.interactive_plot(stocks_df))
    with col2:
        st.markdown("### Price of all the Stocks (After Normalizing)")
        st.plotly_chart(capm_functions.interactive_plot(capm_functions.normalize(stocks_df)))


    stocks_daily_return = capm_functions.daily_return(stocks_df)

    beta = {}
    alpha = {}

    for i in stocks_daily_return.columns:
        if i != 'Date' and i != 'Nifty50':
            b, a = capm_functions.calculate_beta(stocks_daily_return, i)

            beta[i] = b
            alpha[i] = a

    beta_df = pd.DataFrame(columns=['Stock', 'Beta Value'])
    beta_df['Stock'] = beta.keys()
    beta_df['Beta Value'] = [str(round(i, 2)) for i in beta.values()]


    with col1:
        st.markdown('### Calculated Beta Value')
        st.dataframe(beta_df, use_container_width=True)


    rf = 7.365  # Risk-free rate (7.365% as per the government bond yield)
    rm = stocks_daily_return['Nifty50'].mean()*252  # Annualized market return using Nifty 50 daily returns

    return_df = pd.DataFrame()
    return_value = []

    for stock, value in beta.items():
        return_value.append(str(round(rf+(value*(rm-rf)),2)))

    return_df['Stock'] = stocks_list
    return_df['Return Value'] = return_value

    with col2:
        st.markdown('### Calculated Return using CAPM')
        st.dataframe(return_df, use_container_width=True)

except:
    st.write("Please select valid inputs")