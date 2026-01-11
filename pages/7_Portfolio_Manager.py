import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Portfolio Manager", page_icon="🌍", layout="wide")

if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.error("Please log in first.")
    st.stop()

st.title("Portfolio Manager")
st.markdown("### 🏢 Manage Multiple Sites (The 'HQ' View)")
st.info("Edit the table below to plan multiple mini-grids at once (Up to 20 sites).")

# --- 1. CREATE THE PORTFOLIO DATA STRUCTURE ---
# We create a dataframe that looks like your 'Portfolio tab.csv'
# Rows = Metrics, Columns = Site Names
default_data = {
    "Metric": [
        "Capacity (kWp)",
        "Battery (kWh)",
        "Capex (Million ₦)",
        "Households",
        "Tariff (₦/kWh)"
    ],
    "Site 1 (Kano)": [50, 100, 22, 150, 250],
    "Site 2 (Lagos)": [100, 200, 45, 300, 240],
    "Site 3 (Abuja)": [30, 60, 15, 80, 260],
    "Site 4 (Ogun)": [0, 0, 0, 0, 0], # Placeholder
    "Site 5 (Kaduna)": [0, 0, 0, 0, 0], # Placeholder
}

df_portfolio = pd.DataFrame(default_data)

# --- 2. EDITABLE GRID ---
# This lets the user type directly into the "Excel" sheet on the web
edited_portfolio = st.data_editor(
    df_portfolio,
    use_container_width=True,
    num_rows="dynamic",
    key="portfolio_grid"
)

# --- 3. AGGREGATE CALCULATIONS ---
st.divider()
st.subheader("📊 Portfolio Summary")

# We need to flip the table (transpose) to do math on it easily
# Don't worry about the complex code here, it just reorganizes the data for the charts
try:
    # Drop the 'Metric' column and flip rows/columns
    math_df = edited_portfolio.set_index("Metric").T

    # Convert text to numbers (just in case)
    math_df = math_df.apply(pd.to_numeric, errors='coerce').fillna(0)

    # Calculate Totals
    total_capacity = math_df["Capacity (kWp)"].sum()
    total_capex = math_df["Capex (Million ₦)"].sum()
    total_connections = math_df["Households"].sum()
    avg_tariff = math_df[math_df["Tariff (₦/kWh)"] > 0]["Tariff (₦/kWh)"].mean()

    # Display Metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Capacity", f"{total_capacity:,.0f} kWp")
    m2.metric("Total Investment", f"₦{total_capex:,.1f} M")
    m3.metric("Total Connections", f"{total_connections:,.0f}")
    m4.metric("Avg. Portfolio Tariff", f"₦{avg_tariff:,.2f}/kWh")

    # --- 4. VISUALS ---
    c1, c2 = st.columns(2)

    with c1:
        st.caption("Investment per Site")
        st.bar_chart(math_df["Capex (Million ₦)"], color="#2E86C1")

    with c2:
        st.caption("Tariff Comparison (Cheapest vs Most Expensive)")
        # Filter out empty sites
        active_sites = math_df[math_df["Tariff (₦/kWh)"] > 0]
        st.bar_chart(active_sites["Tariff (₦/kWh)"], color="#28B463")

except Exception as e:
    st.warning("Enter data in the table above to see the charts!")

# --- 5. EXPORT ---
st.divider()
if st.button("📥 Download Portfolio Report"):
    csv = edited_portfolio.to_csv(index=False).encode('utf-8')
    st.download_button(
        "Click to Download CSV",
        csv,
        "portfolio_report.csv",
        "text/csv"
    )
