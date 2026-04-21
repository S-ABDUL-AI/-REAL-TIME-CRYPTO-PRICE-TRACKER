# 🚀 Real-Time Multi-Coin Crypto Tracker  

**Live app (Streamlit Cloud):** [https://55kx7euqkmqnbchpmb8aq9.streamlit.app/](https://55kx7euqkmqnbchpmb8aq9.streamlit.app/)  
**Repository:** [github.com/S-ABDUL-AI/-REAL-TIME-CRYPTO-PRICE-TRACKER](https://github.com/S-ABDUL-AI/-REAL-TIME-CRYPTO-PRICE-TRACKER)

Auto-refresh uses Streamlit **`@st.fragment(run_every=…)`** so the page is not blocked by a long `time.sleep` on every update; the CoinGecko call includes **24h % change** next to spot price.

### 📌 Background  
Cryptocurrency markets operate 24/7 with **high volatility**, creating both opportunities and risks.  
Traders and enthusiasts need **real-time tools** that provide price updates, trend monitoring, and alerts in an **easy-to-use dashboard**.  


### ❓ Problem  
- ⚡ Prices change rapidly (sometimes **5% in minutes**) but most dashboards **lag**.  
- 🚨 No simple way to get **alerts** for sudden price moves.  
- 🖥️ Existing dashboards often lack an **intuitive, all-in-one assistant view**.  


### 💡 Solution – Multi-Coin Crypto Tracker  
This dashboard solves the problem by:  
✅ Real-time crypto prices (via **CoinGecko API**)  
✅ Track **multiple coins side by side**  
✅ **Smart alerts** (🚀 spike / 📉 drop / ℹ️ stable)  
✅ Interactive **charts & mini tables**  
✅ **Beautiful UI** with dark theme and white fonts  


### 🖼️ Features  
- 🎨 Modern **dark UI** with crypto logos  
- 📊 **Price history charts** (auto-updating)  
- 📋 **Mini tables** of recent values  
- 🛎️ **Smart alerts** (always visible at the top)  
- ⚡ **Auto-refresh** every 5–60 seconds (non-blocking fragment timer)  
- 📱 Fully responsive → works on **desktop & mobile**  

### 🛠️ Tech Stack  
- **Python 3.9+**  
- **Streamlit**  
- **Pandas**  
- **Requests**  
- **CoinGecko API**  

### 📥 Installation  

```bash
# Clone the repo
git clone https://github.com/S-ABDUL-AI/-REAL-TIME-CRYPTO-PRICE-TRACKER.git
cd -REAL-TIME-CRYPTO-PRICE-TRACKER

# Create a virtual environment
python -m venv .venv

# Activate it
source .venv/bin/activate    # Mac/Linux
.venv\Scripts\activate       # Windows

# Install dependencies
pip install -r requirements.txt

# Run locally (Community Cloud uses app.py as entry)
streamlit run app.py
```

### 🌐 Streamlit Community Cloud

Deploy this repo from [Streamlit Community Cloud](https://share.streamlit.io/). Set **Main file path** to `app.py`.

**If visitors see “You do not have access to this app or it does not exist”** (or are redirected to a Streamlit sign-in page), the deployment is **private**. Fix it while signed into the same GitHub account used to deploy:

1. Open [share.streamlit.io](https://share.streamlit.io/) → your app → **⚙️ Settings** (or use **Share** in the app header).
2. Under **Sharing** / **Who can view this app**, choose **Public** (e.g. “This app is public” / “Make this app public”).
3. Save, wait for the app to restart, then share the `.streamlit.app` URL show in the dashboard (update any old links on your website if the subdomain changed).

Private apps only work for you and explicitly invited viewers; public apps work for everyone without signing in.

📊 Demo Preview

🔹 Full Dashboard
🔹 Real-Time Alerts
🔹 Sidebar with Developer Info
🔹 (Insert GIF/Screenshot here)

🔔 Alerts Explained

🚀 Spike → Price ↑ more than +2% in last 5 minutes

📉 Drop → Price ↓ more than -2% in last 5 minutes

ℹ️ Stable → Price within ±2% in last 5 minutes

👨‍💻 Developer

Sherriff Abdul-Hamid
AI Engineer | Data Scientist | Economist

📧 Sherriffhamid001@gmail.com

🌐 GitHub: S-ABDUL-AI

🔗 LinkedIn

📌 Future Enhancements

🤖 AI-powered price prediction

🔌 WebSocket streaming for ultra-fast updates

💼 Portfolio tracking (profit/loss calculator)

📲 Push alerts to Telegram/Slack

📜 License

This project is licensed under the MIT License – feel free to use, modify, and share with attribution.

