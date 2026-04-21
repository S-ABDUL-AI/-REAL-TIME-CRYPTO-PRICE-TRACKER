import datetime
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd
import requests
import streamlit as st

# -----------------------------
# APP CONFIG
# -----------------------------
st.set_page_config(
    page_title="Real-time crypto price tracker",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# CUSTOM CSS
# -----------------------------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: #f8fafc;
        font-family: "Segoe UI", system-ui, sans-serif;
    }
    h1, h2, h3, h4 { color: #FFD700 !important; }
    section[data-testid="stSidebar"] { background-color: #0f172a; color: #f8fafc; }
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] div { color: #e2e8f0 !important; }
    .alert {
        padding: 10px 14px;
        border-radius: 8px;
        font-size: 15px;
        font-weight: 600;
        text-align: center;
        margin-bottom: 12px;
    }
    .alert-success { background-color: #14532d; color: #86efac; border: 2px solid #22c55e; }
    .alert-danger { background-color: #7f1d1d; color: #fecaca; border: 2px solid #ef4444; }
    .alert-info { background-color: #1e3a8a; color: #bfdbfe; border: 2px solid #60a5fa; }
    .ticker {
        background: #020617;
        padding: 12px 14px;
        border-radius: 8px;
        color: #fde047;
        font-weight: 600;
        border: 1px solid #334155;
        margin-bottom: 14px;
    }
    .kpi-card {
        background: #1e293b;
        padding: 14px;
        border-radius: 10px;
        text-align: center;
        font-size: 17px;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 0.5rem;
        border: 1px solid #334155;
    }
    .muted { color: #94a3b8; font-size: 0.85rem; }
    /* KPI / metrics — force light text on dark gradient (Streamlit defaults are dark-on-light). */
    [data-testid="stMetric"] {
        background: rgba(15, 23, 42, 0.65) !important;
        padding: 12px 14px !important;
        border-radius: 10px !important;
        border: 1px solid #334155 !important;
    }
    [data-testid="stMetric"] label,
    [data-testid="stMetric"] p,
    [data-testid="stMetric"] span,
    [data-testid="stMetric"] div {
        color: #f8fafc !important;
    }
    [data-testid="stMetricValue"] {
        color: #ffffff !important;
    }
    [data-testid="stMetricValue"] * {
        color: #ffffff !important;
    }
    [data-testid="stMetricLabel"] {
        color: #e2e8f0 !important;
    }
    [data-testid="stMetricLabel"] * {
        color: #e2e8f0 !important;
    }
    [data-testid="stMetricDelta"] {
        color: #f1f5f9 !important;
    }
    [data-testid="stMetricDelta"] * {
        color: inherit !important;
    }
    [data-testid="stMetricDelta"] svg {
        fill: currentColor !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# -----------------------------
# HEADER
# -----------------------------
st.title("Real-time crypto price tracker")

st.markdown(
    """
<div style="
    background-color: rgba(255, 255, 255, 0.08);
    padding: 18px 20px;
    border-radius: 12px;
    color: #f1f5f9;
    font-size: 15px;
    border: 1px solid rgba(255,255,255,0.12);
">
<p style="margin:0 0 8px 0;color:#FFD700;font-weight:700;">How to use this app</p>
<p style="margin:0;">
Pick coins and a <b>refresh interval</b> in the sidebar. This panel calls the <b>CoinGecko</b> public API, keeps a short
<b>local history</b> for charts, and compares the <b>oldest vs newest</b> point in the last <b>5 minutes</b> to label
<b>spike / drop / stable</b> (±2% rule from the README).
</p>
</div>
""",
    unsafe_allow_html=True,
)

# -----------------------------
# COINS CONFIG
# -----------------------------
COINS = {
    "₿ Bitcoin (BTC)": "bitcoin",
    "Ξ Ethereum (ETH)": "ethereum",
    "🟡 Binance Coin (BNB)": "binancecoin",
    "🔷 Cardano (ADA)": "cardano",
    "◎ Solana (SOL)": "solana",
}

selected_coins = st.sidebar.multiselect(
    "Coins to track",
    list(COINS.keys()),
    default=["₿ Bitcoin (BTC)", "Ξ Ethereum (ETH)", "🟡 Binance Coin (BNB)"],
)
refresh_rate = st.sidebar.slider("Refresh interval (seconds)", 5, 60, 10)
auto_refresh = st.sidebar.toggle("Auto refresh", value=True)
refresh_now = st.sidebar.button("Refresh now", use_container_width=True)

st.sidebar.divider()
st.sidebar.markdown(
    """
**Developer**  
Sherriff Abdul-Hamid · AI / data / economics  
📧 [Email](mailto:Sherriffhamid001@gmail.com)  
🌐 [GitHub](https://github.com/S-ABDUL-AI) · [Repo](https://github.com/S-ABDUL-AI/-REAL-TIME-CRYPTO-PRICE-TRACKER) · [LinkedIn](https://www.linkedin.com/in/abdul-hamid-sherriff-08583354/)
"""
)

if refresh_now:
    st.rerun()

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; RealTimeCryptoTracker/1.1; "
        "+https://github.com/S-ABDUL-AI/-REAL-TIME-CRYPTO-PRICE-TRACKER)"
    ),
    "Accept": "application/json",
}


def get_prices(coin_ids: List[str]) -> Tuple[Dict[str, Dict[str, Optional[float]]], Optional[str]]:
    """Return per-coin usd + 24h change, and optional error message for the UI."""
    if not coin_ids:
        return {}, None
    ids = ",".join(coin_ids)
    url = (
        "https://api.coingecko.com/api/v3/simple/price"
        f"?ids={ids}&vs_currencies=usd&include_24hr_change=true"
    )
    try:
        response = requests.get(url, headers=_HEADERS, timeout=20)
        if response.status_code == 429:
            return {cid: {"usd": None, "chg24": None} for cid in coin_ids}, (
                "CoinGecko rate limit (429). Wait a minute or raise the refresh interval."
            )
        response.raise_for_status()
        data: Dict[str, Any] = response.json()
        out: Dict[str, Dict[str, Optional[float]]] = {}
        for coin_id in coin_ids:
            blob = data.get(coin_id) or {}
            usd = blob.get("usd")
            chg = blob.get("usd_24h_change")
            out[coin_id] = {
                "usd": float(usd) if usd is not None else None,
                "chg24": float(chg) if chg is not None else None,
            }
        return out, None
    except requests.RequestException as exc:
        return {cid: {"usd": None, "chg24": None} for cid in coin_ids}, f"Price request failed: {exc}"


if not selected_coins:
    st.warning("Select at least one coin from the sidebar.")
    st.stop()

if "history" not in st.session_state:
    st.session_state.history = {}

_run_every = datetime.timedelta(seconds=int(refresh_rate)) if auto_refresh else None


@st.fragment(run_every=_run_every)
def _live_dashboard() -> None:
    """Periodic refresh lives here so the UI is not blocked by ``time.sleep`` on every run."""
    ticker_ph = st.empty()
    coin_ids = [COINS[name] for name in selected_coins]
    rows, err_msg = get_prices(coin_ids)
    ts = datetime.datetime.now()

    if err_msg:
        st.error(err_msg)

    spike_drop_messages: List[str] = []
    lookback_minutes = 5

    cols = st.columns(len(selected_coins))

    for i, coin_name in enumerate(selected_coins):
        coin_id = COINS[coin_name]
        blob = rows.get(coin_id) or {}
        price = blob.get("usd")
        chg24 = blob.get("chg24")

        with cols[i]:
            st.subheader(coin_name)

            if price is None:
                st.error("Could not load this price (network, rate limit, or API error).")
                continue

            hist = st.session_state.history.setdefault(coin_id, [])
            hist.append({"time": ts, "price": float(price)})
            if len(hist) > 200:
                del hist[:-200]

            df = pd.DataFrame(hist)
            cutoff_time = ts - datetime.timedelta(minutes=lookback_minutes)
            df_recent = df[df["time"] >= cutoff_time]

            alert_message = ""
            alert_class = "alert-info"

            if len(df_recent) > 1:
                old_price = float(df_recent.iloc[0]["price"])
                new_price = float(df_recent.iloc[-1]["price"])
                if old_price == 0:
                    change_pct = 0.0
                else:
                    change_pct = (new_price - old_price) / old_price * 100.0

                if change_pct >= 2:
                    alert_message = f"🚀 Spike +{change_pct:.2f}% vs start of last {lookback_minutes} min window"
                    alert_class = "alert-success"
                    spike_drop_messages.append(f"{coin_name.split('(')[0].strip()}: +{change_pct:.1f}%")
                elif change_pct <= -2:
                    alert_message = f"📉 Drop {change_pct:.2f}% vs start of last {lookback_minutes} min window"
                    alert_class = "alert-danger"
                    spike_drop_messages.append(f"{coin_name.split('(')[0].strip()}: {change_pct:.1f}%")
                else:
                    alert_message = f"ℹ️ Stable ({change_pct:+.2f}% over last {lookback_minutes} min in this session)"
                    alert_class = "alert-info"
            else:
                alert_message = "⏳ Collecting points — need two samples in the 5‑minute window for a move label"
                alert_class = "alert-info"

            st.markdown(f'<div class="alert {alert_class}">{alert_message}</div>', unsafe_allow_html=True)

            delta_txt = None
            if chg24 is not None:
                delta_txt = f"{chg24:+.2f}% vs 24h"
            st.metric("Spot (USD)", f"${float(price):,.2f}", delta=delta_txt)

            chart_df = df.set_index("time")[["price"]].rename(columns={"price": "USD"})
            st.caption("Session history (this browser tab)")
            st.line_chart(chart_df, height=220)

            tail = df.tail(5).copy()
            tail["time"] = tail["time"].dt.strftime("%H:%M:%S")
            st.dataframe(tail.set_index("time"), use_container_width=True, height=160)

    if spike_drop_messages:
        banner = " · ".join(spike_drop_messages)
        ticker_ph.markdown(
            f'<div class="ticker">🔔 <b>Live moves (±2% / {lookback_minutes} min)</b> — {banner}</div>',
            unsafe_allow_html=True,
        )
    else:
        ticker_ph.markdown(
            f'<div class="ticker">🔔 No ±2% moves in the last {lookback_minutes} minutes of this session '
            f"— prices still update on your interval. Last pull: {ts.strftime('%H:%M:%S')}</div>",
            unsafe_allow_html=True,
        )


_live_dashboard()

# Note: ``time.sleep`` + ``st.rerun()`` was removed — it delayed the entire page on every refresh.
# Auto-refresh is handled by ``@st.fragment(run_every=...)`` (Streamlit ≥ 1.33).
