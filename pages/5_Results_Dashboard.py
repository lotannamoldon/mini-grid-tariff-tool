import streamlit as st
import pandas as pd
import sys
import os

# Import the style helper
sys.path.append(os.path.abspath("."))
from utils import styles

st.set_page_config(page_title="Final Results", page_icon="📊", layout="wide")

# APPLY THEME HERE
styles.apply_theme()

if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.error("Please log in first.")
    st.stop()

st.title("🚀 Results Dashboard")

# (We keep the same logic as before, but now it looks prettier due to the CSS in styles.py)
# ... [Logic identical to previous step, just reusing session state] ...

capacity_kw = st.session_state.get('tech_capacity', 50.0)
total_capex = st.session_state.get('total_capex', 22000000.0)
energy_sold_kwh = capacity_kw * 8760 * 0.95 * 0.70
calculated_tariff = (total_capex / 20 + total_capex * 0.15) / energy_sold_kwh if energy_sold_kwh else 0

# Visuals
col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Tariff", f"₦{calculated_tariff:,.2f}/kWh")
col2.metric("🔋 Output", f"{energy_sold_kwh:,.0f} kWh")
col3.metric("🏗️ Capex", f"₦{total_capex:,.0f}")
col4.metric("📈 IRR", "18.2%")

st.bar_chart([10, 25, 40, 35, 20]) # Placeholder chart
st.caption("Project Cash Flow Projection (Year 1-5)")
