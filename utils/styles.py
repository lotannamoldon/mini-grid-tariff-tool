
import streamlit as st

def apply_theme():
    # 1. ADD LOGO
    # Replace this URL with your own company logo later!
    logo_url = "https://cdn-icons-png.flaticon.com/512/3106/3106807.png"
    st.sidebar.image(logo_url, width=150)

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔋 Mini-Grid Portal")
    st.sidebar.caption("v2.0 | Pan-Atlantic University")

    # 2. CUSTOM CSS (The "Make it Pretty" Code)
    # This hides the default "Streamlit" menu and adds shadows to boxes
    st.markdown("""
        <style>
        /* Main Background Color (Optional - currently using default white) */

        /* Box Styling (Metrics) */
        [data-testid="stMetricValue"] {
            font-size: 2rem;
            color: #2E86C1; /* Professional Blue */
        }

        /* Buttons */
        .stButton button {
            background-color: #2E86C1;
            color: white;
            border-radius: 10px;
            font-weight: bold;
        }
        .stButton button:hover {
            background-color: #1B4F72;
            color: white;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #F4F6F6;
        }

        /* Headers */
        h1, h2, h3 {
            color: #17202A;
        }
        </style>
    """, unsafe_allow_html=True)
