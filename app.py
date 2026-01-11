import streamlit as st
import sys
import os

# Ensure we can import from utils
sys.path.append(os.path.abspath("."))
from utils import styles

# 1. Page Config
st.set_page_config(page_title="Solar Tariff Portal", page_icon="☀️", layout="wide")

# 2. APPLY THEME (Logo + Colors)
styles.apply_theme()

# 3. Session State for Login
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# 4. Login Screen Logic
if not st.session_state['logged_in']:
    col1, col2 = st.columns([1, 2])

    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/4258/4258299.png", width=200)

    with col2:
        st.title("☀️ Solar Tariff Portal")
        st.subheader("Secure Login")
        st.info("Welcome to the Mini-Grid Financial Modelling Tool.")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("🔐 Access Portal"):
            if username: # Accepts any username for now
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("Please enter a username.")

else:
    # --- DASHBOARD HOME ---
    st.title("👋 Welcome Back, Developer")
    st.markdown("### Project Overview")

    # Create 3 nice "Cards" for quick stats
    c1, c2, c3 = st.columns(3)
    c1.metric("Active Projects", "3", "Kano, Lagos, Abuja")
    c2.metric("Pending Approvals", "1", "Grid Connection")
    c3.metric("Global IRR", "18.5%", "+2.4% vs Target")

    st.divider()

    col_nav1, col_nav2 = st.columns(2)
    with col_nav1:
        st.info("👈 **Start Here:** Click '1 Basic Info' in the sidebar to create a new site.")
    with col_nav2:
        st.success("📊 **Quick View:** Click '7 Portfolio' to see all your sites.")

    if st.button("Log Out"):
        st.session_state['logged_in'] = False
        st.rerun()
