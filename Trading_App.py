import streamlit as st

st.set_page_config(
    page_title="Trading App",
    page_icon="chart_with_upwards_trend",
    layout="wide"
)

st.title("Trading Guide App 📊")
st.header("Your Premier Platform for Informed Stock Investment Decisions")

st.image("app.jpg")

st.markdown("## Our Comprehensive Services:")

st.markdown("### :one: **Stock Analysis**")
st.write("Gain in-depth insights into individual stock performance, with detailed data on historical trends, market behavior, and other key metrics. This tool is designed to help you assess potential investment opportunities and make informed decisions.")

st.markdown("### :two: **Stock Prediction**")
st.write("Leverage advanced forecasting models to predict stock closing prices for the next 30 days. Our prediction tool uses historical data and sophisticated algorithms to provide accurate market trends, helping you anticipate price movements and optimize your investment strategy.")

st.markdown("### :three: **CAPM Return Calculation**")
st.write("The Capital Asset Pricing Model (CAPM) is a powerful tool used to calculate the expected return on a stock based on its risk and the overall market performance. This feature enables you to assess the risk-reward tradeoff of various stocks and make data-driven decisions.")
