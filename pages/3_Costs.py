import streamlit as st
import pandas as pd

st.set_page_config(page_title="Project Costs", page_icon="💰")

if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.error("Please log in first.")
    st.stop()

st.title("Step 3: Project Costs (CAPEX & OPEX)")
st.progress(60)

# --- SECTION 1: CAPITAL EXPENDITURE (CAPEX) ---
st.header("1. Capital Costs (Capex)")
st.info("Edit the table below. Enter costs in NGN (Naira).")

# We create a default "Template" just like the Excel rows
capex_data = {
    "Item": [
        "Solar PV Modules",
        "Inverters",
        "Batteries (Storage)",
        "Distribution Network (Poles/Cables)",
        "Smart Meters",
        "Civil Works (Land/Fence)",
        "Logistics & Installation"
    ],
    "Cost (NGN)": [5000000, 2500000, 7000000, 3000000, 1500000, 1000000, 2000000],
    "Useful Life (Years)": [25, 10, 10, 20, 15, 25, 25]
}
df_capex = pd.DataFrame(capex_data)

# st.data_editor allows the user to click and type inside the table!
edited_capex = st.data_editor(
    df_capex,
    num_rows="dynamic", # Users can add new rows if they want
    use_container_width=True,
    key="capex_table"
)

# Calculate Total instantly
total_capex = edited_capex["Cost (NGN)"].sum()
st.metric("Total Initial Investment (CAPEX)", f"₦{total_capex:,.2f}")


# --- SECTION 2: OPERATING EXPENSES (OPEX) ---
st.divider()
st.header("2. Operating Expenses (OPEX)")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Annual Maintenance")
    fixed_opex = st.number_input("Fixed Annual O&M (Staff, Security)", value=1500000, step=50000)
    variable_opex = st.number_input("Variable O&M (per kWh)", value=5.0, step=0.5)

with col2:
    st.subheader("Working Capital")
    # This is that CRITICAL Cell C133 we talked about!
    st.markdown("**Cash Buffer (Cell C133)**")
    working_cap_days = st.number_input("Days of Working Capital Required", value=90, help="How many days of cash do you need in the bank?")

    # Calculate the Working Capital Value immediately
    daily_opex = fixed_opex / 365
    required_cash = daily_opex * working_cap_days
    st.caption(f"You need to hold **₦{required_cash:,.0f}** in the bank.")

# --- NAVIGATION ---
st.divider()
if st.button("Save & Continue to Finance >", type="primary"):
    st.session_state['total_capex'] = total_capex
    st.success("Costs Saved! Ready for Financial Structure.")
