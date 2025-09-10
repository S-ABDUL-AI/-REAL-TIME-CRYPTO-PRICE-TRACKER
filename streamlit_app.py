import streamlit as st
import requests
import pandas as pd
import datetime
import time

# -----------------------------
# APP CONFIG
# -----------------------------
st.set_page_config(page_title="🚀 REAL-TIME CRYPTO PRICE TRACKER", layout="wide")

# -----------------------------
# CUSTOM CSS
# -----------------------------
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: white;
        font-family: 'Segoe UI', sans-serif;
    }
    h1, h2, h3, h4 { color: #FFD700 !important; }
    section[data-testid="stSidebar"] { background-color: #111; color: white; }
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] div { color: white !important; }
    .alert {
        padding: 10px;
        border-radius: 8px;
        font-size: 16px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 15px;
    }
    .alert-success { background-color: #14532d; color: #22c55e; border: 2px solid #22c55e; }
    .alert-danger { background-color: #7f1d1d; color: #ef4444; border: 2px solid #ef4444; }
    .alert-info { background-color: #1e3a8a; color: #60a5fa; border: 2px solid #60a5fa; }
    .ticker {
        background: #000;
        padding: 10px;
        border-radius: 8px;
        color: #FFD700;
        font-weight: bold;
        white-space: nowrap;
        overflow: hidden;
    }
    .ticker span {
        display: inline-block;
        padding-right: 50px;
        animation: ticker 20s linear infinite;
    }
    @keyframes ticker {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }
    .footer {
        margin-top: 50px;
        text-align: center;
        font-size: 14px;
        color: #aaa;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.title("🚀 Multi-Coin Real-Time Crypto Tracker")

st.markdown("""
<div style="
    background-color: rgba(255, 255, 255, 0.1); 
    padding: 20px; 
    border-radius: 12px; 
    color: white; 
    font-size: 16px;
">
<h3 style="color: #FFD700;">👋 Welcome!</h3>
<p>
This dashboard shows <b>live prices</b> for multiple cryptocurrencies.
</p>

✅ Each coin has:  
- Live price updates  
- Smart alerts (🚀 spike / 📉 drop / ℹ️ stable over 5 minutes)  
- Charts of recent price movements  
- Mini tables of recent values  

👉 The goal is to look and feel like a <b>trading assistant panel</b>.  

</div>
""", unsafe_allow_html=True)

# -----------------------------
# COINS CONFIG
# -----------------------------
COINS = {
    "₿ Bitcoin (BTC)": "bitcoin",
    "♦ Ethereum (ETH)": "ethereum",
    "🟡 Binance Coin (BNB)": "binancecoin",
    "🔷 Cardano (ADA)": "cardano",
    "🌞 Solana (SOL)": "solana",
}

selected_coins = st.sidebar.multiselect(
    "Select Cryptocurrencies to Track",
    list(COINS.keys()),
    default=["₿ Bitcoin (BTC)", "♦ Ethereum (ETH)", "🟡 Binance Coin (BNB)"]
)
refresh_rate = st.sidebar.slider("Refresh rate (seconds)", 5, 60, 10)

# Sidebar developer details (moved here instead of inside main page)
st.sidebar.markdown("---")
st.sidebar.markdown("""
**👨‍💻 Developer**  
Sherriff Abdul-Hamid
AI Engineer | Data Scientist | Economist  
📧 [Sherriffhamid001@gmail.com](mailto:Sherriffhamid001@gmail.com)  
🌐 [GitHub: S-ABDUL-AI](https://github.com/S-ABDUL-AI) | 
🔗 [LinkedIn](https://www.linkedin.com/in/abdul-hamid-sherriff-08583354/)
""")

# -----------------------------
# FETCH PRICE FUNCTION
# -----------------------------
def get_price(coin_id: str):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        return data[coin_id]["usd"]
    except Exception:
        return None

# -----------------------------
# GLOBAL ALERT TICKER
# -----------------------------
global_alerts = []

# -----------------------------
# TRACK + DISPLAY PER COIN
# -----------------------------
cols = st.columns(len(selected_coins))  # one column per coin

for i, coin_name in enumerate(selected_coins):
    coin_id = COINS[coin_name]
    price = get_price(coin_id)

    with cols[i]:
        st.subheader(coin_name)

        if price is not None:
            # Save history per coin
            if "history" not in st.session_state:
                st.session_state.history = {}
            if coin_id not in st.session_state.history:
                st.session_state.history[coin_id] = []

            st.session_state.history[coin_id].append({"time": datetime.datetime.now(), "price": price})

            # Keep last 200 records
            if len(st.session_state.history[coin_id]) > 200:
                st.session_state.history[coin_id] = st.session_state.history[coin_id][-200:]

            df = pd.DataFrame(st.session_state.history[coin_id])

            # Alerts
            lookback_minutes = 5
            cutoff_time = datetime.datetime.now() - datetime.timedelta(minutes=lookback_minutes)
            df_recent = df[df["time"] >= cutoff_time]

            alert_message = ""
            alert_class = "alert-info"

            if len(df_recent) > 1:
                old_price = df_recent.iloc[0]["price"]
                new_price = df_recent.iloc[-1]["price"]
                change_pct = ((new_price - old_price) / old_price) * 100

                if change_pct >= 2:
                    alert_message = f"🚀 {coin_name} spiked +{change_pct:.2f}% in last {lookback_minutes} min!"
                    alert_class = "alert-success"
                    global_alerts.append(alert_message)
                elif change_pct <= -2:
                    alert_message = f"📉 {coin_name} dropped {change_pct:.2f}% in last {lookback_minutes} min!"
                    alert_class = "alert-danger"
                    global_alerts.append(alert_message)
                else:
                    alert_message = f"ℹ️ Stable ({change_pct:.2f}% in {lookback_minutes} min)"
                    alert_class = "alert-info"
            else:
                alert_message = "⏳ Not enough data yet"
                alert_class = "alert-info"

            st.markdown(f'<div class="alert {alert_class}">{alert_message}</div>', unsafe_allow_html=True)

            # ✅ Custom Metric with White Font
            st.markdown(f"""
                <div style="
                    background: #1e293b;
                    padding: 15px;
                    border-radius: 10px;
                    text-align: center;
                    font-size: 20px;
                    font-weight: bold;
                    color: white;
                ">
                    💰 Price: ${price:,.2f}
                </div>
            """, unsafe_allow_html=True)

            # Chart
            st.line_chart(df.set_index("time")["price"], height=200)

            # Table
            st.dataframe(df.tail(5).set_index("time"))
        else:
            st.error("❌ Could not fetch price")

# -----------------------------
# SHOW GLOBAL ALERTS BAR (on top of page)
# -----------------------------
if global_alerts:
    alerts_text = " | ".join(global_alerts)
    st.markdown(f'<div class="ticker"><span>{alerts_text}</span></div>', unsafe_allow_html=True)

# -----------------------------
# AUTO REFRESH
# -----------------------------
time.sleep(refresh_rate)
st.rerun()
