import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Grid Arrival Risk", page_icon="⚡")

if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.error("Please log in first.")
    st.stop()

st.title("Step 6: Grid Arrival Impact")
st.progress(100)

# --- 1. GET DATA FROM PREVIOUS STEPS ---
# We need the Capex and Funding info to calculate what you lose
total_capex = st.session_state.get('total_capex', 22000000.0)
equity_pct = st.session_state.get('fin_equity', 30.0) / 100
debt_pct = st.session_state.get('fin_debt', 40.0) / 100

st.info("Based on NERC Regulations: What happens if the main grid connects to your site?")

# --- 2. GRID ARRIVAL INPUTS ---
col1, col2 = st.columns(2)
with col1:
    arrival_year = st.slider("Year of Grid Arrival", min_value=1, max_value=20, value=10,
                             help="In which year does the DisCo extend the grid to this community?")

with col2:
    scenario = st.selectbox("Compensation Scenario",
                            ["Option 1: Asset Handover (Compensation)",
                             "Option 2: Co-existence (Parallel Operation)",
                             "Option 3: Mini-Grid becomes Distributor"])

# --- 3. CALCULATION: STRANDED ASSET VALUE ---
# We calculate the "Book Value" of the assets at the time of arrival
# (Simple straight-line depreciation logic)

useful_life = 20 # years
annual_dep = total_capex / useful_life
accumulated_dep = annual_dep * arrival_year
remaining_book_value = max(0, total_capex - accumulated_dep)

# Debt Outstanding Calculation (Simplified amortization)
# Assuming 10 year loan
loan_tenor = st.session_state.get('fin_tenor', 10)
initial_debt = total_capex * debt_pct
if arrival_year < loan_tenor:
    pct_remaining = (loan_tenor - arrival_year) / loan_tenor
    debt_outstanding = initial_debt * pct_remaining
else:
    debt_outstanding = 0

# --- 4. OUTPUTS ---
st.divider()
st.subheader(f" impact in Year {arrival_year}")

c1, c2, c3 = st.columns(3)
c1.metric("📉 Remaining Asset Value", f"₦{remaining_book_value:,.0f}")
c2.metric("🏦 Debt Still Owed", f"₦{debt_outstanding:,.0f}")

# Logic for Compensation
if "Handover" in scenario:
    compensation = remaining_book_value # Regulated Book Value
    net_equity = compensation - debt_outstanding
    c3.metric("💰 Est. Compensation", f"₦{compensation:,.0f}")

    if net_equity > 0:
        st.success(f"✅ Safe Exit! After paying off debt, investors recover ₦{net_equity:,.0f}")
    else:
        st.error(f"⚠️ Risk! Compensation covers debt, but investors lose ₦{abs(net_equity):,.0f}")

elif "Co-existence" in scenario:
    st.warning("⚠️ In Co-existence, your revenue might drop by 40-60% due to competition.")
    c3.metric("Est. Revenue Drop", "-50%")

# --- 5. VISUALIZATION ---
# Show the "Value Cliff" chart
years = list(range(1, 21))
values = []
for y in years:
    dep = (total_capex / useful_life) * y
    val = max(0, total_capex - dep)
    values.append(val)

chart_data = pd.DataFrame({"Year": years, "Asset Value": values})
st.line_chart(chart_data, x="Year", y="Asset Value")

st.caption("The line shows the regulated value of your system dropping over time.")
