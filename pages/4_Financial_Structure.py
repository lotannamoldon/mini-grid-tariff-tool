import streamlit as st

st.set_page_config(page_title="Financial Structure", page_icon="🏦")

if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.error("Please log in first.")
    st.stop()

st.title("Step 4: Financial Structure")
st.progress(80)

# --- SECTION 1: FUNDING SOURCES (Excel Section 1.5) ---
st.header("1. Funding Sources")
st.info("How is this project being paid for? (Must sum to 100%)")

col1, col2, col3 = st.columns(3)
with col1:
    # Key: fin_equity
    equity_pct = st.number_input("Equity (%)", min_value=0, max_value=100, value=30, key="fin_equity")
with col2:
    # Key: fin_debt
    debt_pct = st.number_input("Debt (%)", min_value=0, max_value=100, value=40, key="fin_debt")
with col3:
    # Key: fin_grants
    grant_pct = st.number_input("Grants / Subsidies (%)", min_value=0, max_value=100, value=30, key="fin_grants")

# Validation Check: Ensure it equals 100%
total_funding = equity_pct + debt_pct + grant_pct
if total_funding != 100:
    st.error(f"⚠️ Total funding is {total_funding}%. It must equal 100%.")
else:
    st.success("✅ Funding structure is valid.")

# --- SECTION 2: COST OF CAPITAL (Excel Section 1.7) ---
st.divider()
st.header("2. Cost of Capital (WACC Inputs)")

c1, c2 = st.columns(2)
with c1:
    st.subheader("Debt Parameters")
    # Key: fin_interest
    interest_rate = st.number_input("Interest Rate on Debt (%)", value=18.0, step=0.5, key="fin_interest")
    tenor = st.number_input("Loan Tenor (Years)", value=10, step=1, key="fin_tenor")

with c2:
    st.subheader("Equity & Taxes")
    # Key: fin_roe
    roe = st.number_input("Target Return on Equity (ROE %)", value=25.0, key="fin_roe", help="Profit margin investors demand")
    tax_rate = st.number_input("Corporate Tax Rate (%)", value=30.0, key="fin_tax")

# --- SAVE & CONTINUE ---
st.divider()
if st.button("Save & View Final Dashboard >", type="primary"):
    st.success("Financial Parameters Saved! Ready for Calculation.")
