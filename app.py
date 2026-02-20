import streamlit as st
import yfinance as yf
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="SmartTradeNet",
    layout="wide",
    page_icon="📊"
)

# ---------------- PREMIUM STYLING ----------------
st.markdown("""
<style>
body {
    background-color: #0E1117;
}
.main {
    background-color: #0E1117;
}
.stButton>button {
    background: linear-gradient(90deg,#00C6FF,#0072FF);
    color: white;
    font-size: 18px;
    height: 3em;
    border-radius: 8px;
    border: none;
}
.stButton>button:hover {
    background: linear-gradient(90deg,#0072FF,#00C6FF);
}
.footer {
    text-align: center;
    color: grey;
    font-size: 14px;
    margin-top: 50px;
}
a {
    text-decoration: none;
    color: #00C6FF;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("# 📊 SmartTradeNet")
st.markdown("### AI-Powered Stock Insights for Smart Investors")
st.markdown("---")

# ---------------- STOCK LIST ----------------
NIFTY_50 = {
    "Reliance Industries": "RELIANCE.NS",
    "TCS": "TCS.NS",
    "HDFC Bank": "HDFCBANK.NS",
    "Infosys": "INFY.NS",
    "ICICI Bank": "ICICIBANK.NS",
    "Larsen & Toubro": "LT.NS",
    "SBI": "SBIN.NS",
    "Axis Bank": "AXISBANK.NS",
    "ITC": "ITC.NS",
    "Maruti Suzuki": "MARUTI.NS",
    "ONGC": "ONGC.NS",
    "Silver ETF": "SILVERBEES.NS"
}

col1, col2 = st.columns([3,1])

with col1:
    company_name = st.selectbox(
        "Search & Select Company",
        options=list(NIFTY_50.keys())
    )

with col2:
    analyze = st.button("🚀 Analyze")

stock = NIFTY_50[company_name]

st.markdown("---")

# ---------------- ANALYSIS ----------------
if analyze:

    with st.spinner("Fetching live market data..."):
        data = yf.download(stock, period="6mo")

    if data.empty:
        st.error("Unable to fetch stock data.")
    else:

        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        data["20_MA"] = data["Close"].rolling(window=20).mean()

        current_price = data["Close"].iloc[-1]
        moving_avg = data["20_MA"].iloc[-1]

        change_percent = ((current_price - data["Close"].iloc[-20]) / data["Close"].iloc[-20]) * 100

        m1, m2, m3 = st.columns(3)

        with m1:
            st.metric("Current Price", f"₹ {round(current_price,2)}")

        with m2:
            st.metric("20-Day Average", f"₹ {round(moving_avg,2)}")

        with m3:
            st.metric("20-Day Change", f"{round(change_percent,2)} %")

        st.markdown("---")
        st.subheader("📈 Price Trend")
        st.line_chart(data[["Close", "20_MA"]])

        st.markdown("---")
        st.subheader("🧠 Smart Signal")

        if current_price > moving_avg:
            st.success("🟢 BUY SIGNAL — Positive Momentum")
        elif current_price < moving_avg:
            st.error("🔴 SELL SIGNAL — Downward Trend")
        else:
            st.warning("🟡 HOLD — Market Consolidation")

# ---------------- ABOUT SECTION ----------------
st.markdown("---")
st.subheader("ℹ️ About SmartTradeNet")

st.write("""
SmartTradeNet is a beginner-friendly stock analysis platform that uses 
real-time market data to generate simple Buy, Hold, or Sell signals 
based on trend analysis.

It is designed to make financial insights easy to understand 
without complex trading jargon.
""")

# ---------------- FOOTER ----------------
st.markdown("""
<div class="footer">
Built by <b>Kona sai tharun</b> | SmartTradeNet 2026 <br>
<a href="https://github.com/KONASAITHARUN/smarttradenet" target="_blank">
View Source Code on GitHub
</a>
</div>
""", unsafe_allow_html=True)
