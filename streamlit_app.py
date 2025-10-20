import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import timedelta

from trading_insights.config import DataConfig, TrainConfig
from trading_insights.ingest import fetch_stock, fetch_vix
from trading_insights.earnings import parse_earnings_text
from trading_insights.backtest import build_dataset, train_and_backtest

# ---------- Page setup / style ----------
st.set_page_config(page_title="Trading Insights – Earnings Event Study", page_icon="📈", layout="wide")
st.markdown("""
<style>
.big-number {font-size: 38px; font-weight: 700; line-height: 1.1;}
.subtle {color: #666;}
.card {padding: 18px 20px; border-radius: 14px; border: 1px solid #eee; background: #fafafa;}
.kpi {padding: 14px 16px; border-radius: 12px; border: 1px solid #eee;}
</style>
""", unsafe_allow_html=True)

st.title("📈 Trading Insights: Earnings Event Study (EPS + VIX → OLS)")
st.caption("Modular backtesting pipeline with prediction for the **next earnings** (uses sample data by default).")

# ---------- Controls ----------
with st.sidebar:
    st.header("Settings")
    use_sample = st.checkbox("Use sample data (offline-friendly)", value=True, help="Uncheck to fetch live data via Yahoo Finance.")
    ticker = st.text_input("Ticker", "AAPL")
    neutral_band = st.slider("Neutral band (±%)", 0.0, 2.0, 0.5, 0.1,
                             help="If predicted change is within this band, we call it 'Neutral'.")
    st.markdown("---")
    st.caption("Tip: Keep sample mode on for demos; turn it off to fetch latest market data.")

# Load default example earnings for the text area
with open("assets/sample_earnings.txt", "r") as f:
    default_earnings_text = f.read()

earnings_text = st.text_area("Paste earnings (YYYY-MM-DD, EPS)", height=180, value=default_earnings_text)

run = st.button("Run analysis")

if run:
    try:
        # ----- Load data (sample or live) -----
        if use_sample:
            stock = pd.read_csv("assets/sample_stock_AAPL.csv", parse_dates=["Date"])
            vix = pd.read_csv("assets/sample_vix.csv", parse_dates=["Date"])
        else:
            dcfg = DataConfig(ticker=ticker)
            stock = fetch_stock(dcfg.ticker, dcfg.start, dcfg.end)
            vix = fetch_vix(dcfg.vix_symbol, dcfg.start, dcfg.end)

        earnings = parse_earnings_text(earnings_text)
        data = build_dataset(stock, earnings, vix).dropna()

        if data.empty:
            st.warning("No rows in dataset after feature construction. Try different dates or toggle sample mode.")
            st.stop()

        # ----- Train / metrics -----
        model, metrics = train_and_backtest(data, TrainConfig())

        # ----- Latest prediction -----
        last_earnings_date = earnings["Earnings Date"].max()
        est_next_earnings = last_earnings_date + timedelta(days=90)  # simple estimate for demo
        # features for prediction: last EPS, last VIX on/<= last earnings date
        latest_eps = earnings.loc[earnings["Earnings Date"] == last_earnings_date, "EPS"].iloc[0]
        latest_vix = vix[vix["Date"] <= last_earnings_date]["VIX_Close"].iloc[-1]
        X_pred = pd.DataFrame({"eps":[latest_eps], "vix_level":[latest_vix]})
        pred_pct = float(model.predict(X_pred)[0])

        # ----- Recommendation logic -----
        rec, tone, emoji = "", "info", "⚖️"
        if pred_pct > neutral_band:
            rec, tone, emoji = "Consider BUY before earnings", "success", "📈"
        elif pred_pct < -neutral_band:
            rec, tone, emoji = "Caution / AVOID buying pre-earnings", "error", "⚠️"
        else:
            rec, tone, emoji = "Neutral / HOLD", "warning", "⚖️"

        # ----- Top summary cards -----
        colA, colB = st.columns([1.4, 1])
        with colA:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(f"**Predicted move after next earnings ({est_next_earnings.date()} est.)**")
            st.markdown(f'<div class="big-number">{pred_pct:+.2f}%</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="subtle">Inputs → EPS: {latest_eps:.2f} • VIX: {latest_vix:.1f}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with colB:
            if tone == "success":
                st.success(f"{emoji} **Recommendation:** {rec}")
            elif tone == "error":
                st.error(f"{emoji} **Recommendation:** {rec}")
            else:
                st.warning(f"{emoji} **Recommendation:** {rec}")

        st.markdown("")

        # ----- KPIs -----
        k1, k2, k3 = st.columns(3)
        k1.markdown(f'<div class="kpi">**Train R²**<br><span class="big-number">{metrics.get("train_r2", float("nan")):.2f}</span></div>', unsafe_allow_html=True)
        k2.markdown(f'<div class="kpi">**Test R²**<br><span class="big-number">{(metrics.get("test_r2") or 0):.2f}</span></div>', unsafe_allow_html=True)
        k3.markdown(f'<div class="kpi">**Samples**<br><span class="big-number">{len(data)}</span></div>', unsafe_allow_html=True)

        st.markdown("---")

        # ----- Charts (Altair) -----
        st.subheader("Historical post-earnings moves")
        chart_df = data.copy()
        chart_df["Sign"] = np.where(chart_df["price_change_pct"] >= 0, "Up", "Down")
        bar = alt.Chart(chart_df).mark_bar().encode(
            x=alt.X("yearmonthdate(Earnings Date):T", title="Earnings Date"),
            y=alt.Y("price_change_pct:Q", title="Price Change (%)"),
            color=alt.Color("Sign:N", scale=alt.Scale(domain=["Up","Down"], range=["#2e7d32","#c62828"])),
            tooltip=["Earnings Date","price_change_pct","eps","vix_level"]
        ).properties(height=260)
        st.altair_chart(bar, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("EPS vs. post-earnings move")
            c1 = alt.Chart(chart_df).mark_circle(size=90).encode(
                x=alt.X("eps:Q", title="EPS"),
                y=alt.Y("price_change_pct:Q", title="Price Change (%)"),
                tooltip=["Earnings Date","eps","price_change_pct"]
            ).properties(height=260)
            st.altair_chart(c1, use_container_width=True)
        with col2:
            st.subheader("VIX vs. post-earnings move")
            c2 = alt.Chart(chart_df).mark_circle(size=90).encode(
                x=alt.X("vix_level:Q", title="VIX level"),
                y=alt.Y("price_change_pct:Q", title="Price Change (%)"),
                tooltip=["Earnings Date","vix_level","price_change_pct"]
            ).properties(height=260)
            st.altair_chart(c2, use_container_width=True)

        st.markdown("---")
        st.subheader("Backtest dataset")
        st.dataframe(data)

        st.caption("Note: Next earnings date shown is an estimate (+90 days from last). This demo uses an OLS model and simple features for clarity.")
    except Exception as e:
        st.error(f"Error: {e}")
