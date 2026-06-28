import streamlit as st
import pandas as pd

from google_sheets import client
from config import SHEET_ID, LOGS_SHEET

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="History",
    page_icon="📜",
    layout="wide"
)

# ==========================================
# HIDE STREAMLIT NAVIGATION
# ==========================================

st.markdown("""
<style>
[data-testid="stSidebarNav"]{
display:none;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# LOGIN CHECK
# ==========================================

if not st.session_state.get("logged_in", False):
    st.switch_page("app_4.py")

# ==========================================
# CONNECT TO GOOGLE SHEETS
# ==========================================

sheet = client.open_by_key(SHEET_ID)

logs_ws = sheet.worksheet(LOGS_SHEET)

# ==========================================
# LOAD LOGS
# ==========================================

@st.cache_data(ttl=30)
def load_logs():

    df = pd.DataFrame(
        logs_ws.get_all_records()
    )

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    return df

logs = load_logs()

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.markdown("# 🏭 Ralson")

    st.markdown("---")

    st.markdown(
        f"""
### 👤 {st.session_state.user["name"]}

**User ID:** {st.session_state.user["userid"]}

**Department:** {st.session_state.user["department"]}

**Role:** {st.session_state.user["role"]}
"""
    )
    dashboard_color = "secondary"
    history_color = "primary"
    profile_color = "secondary"
    admin_color = "secondary"
    if st.button("📦 Dashboard", use_container_width=True, type=dashboard_color):
    st.switch_page("pages/Dashboard.py")
    if st.button("📜 History", use_container_width=True, type=history_color):
    st.switch_page("pages/History.py")
    if st.button("👤 Profile", use_container_width=True, type=profile_color):
    st.switch_page("pages/Profile.py")
    if st.session_state.user["userid"] == "ADMIN001":
    if st.button("⚙️ Admin", use_container_width=True, type=admin_color):
        st.switch_page("pages/Admin.py")

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False
        st.session_state.user = {}

        st.switch_page("app_4.py")

# ==========================================
# PAGE TITLE
# ==========================================

st.title("📜 Stock Update History")
# ==========================================
# CHECK LOGS
# ==========================================

if logs.empty:

    st.info("No history available.")

    st.stop()

# ==========================================
# FILTERS
# ==========================================

col1, col2 = st.columns(2)

with col1:

    users = ["All"] + sorted(
        logs["userid"]
        .astype(str)
        .unique()
        .tolist()
    )

    user_filter = st.selectbox(
        "👤 Filter By User",
        users
    )

with col2:

    material_filter = st.text_input(
        "🔍 Search Material"
    )

# ==========================================
# APPLY FILTERS
# ==========================================

filtered = logs.copy()

if user_filter != "All":

    filtered = filtered[
        filtered["userid"]
        ==
        user_filter
    ]

if material_filter:

    filtered = filtered[
        filtered["material"]
        .astype(str)
        .str.contains(
            material_filter,
            case=False,
            na=False
        )
    ]

# ==========================================
# SORT BY LATEST
# ==========================================

if "datetime" in filtered.columns:

    filtered = filtered.sort_values(
        by="datetime",
        ascending=False
    )

# ==========================================
# SUMMARY
# ==========================================

c1, c2 = st.columns(2)

with c1:

    st.metric(
        "Total Records",
        len(filtered)
    )

with c2:

    st.metric(
        "Total Users",
        filtered["userid"].nunique()
    )

st.divider()

# ==========================================
# HISTORY TABLE
# ==========================================

st.dataframe(
    filtered,
    use_container_width=True,
    hide_index=True,
    height=550
)

# ==========================================
# DOWNLOAD CSV
# ==========================================

csv = filtered.to_csv(
    index=False
).encode("utf-8")

st.download_button(

    "📥 Download History",

    csv,

    file_name="history.csv",

    mime="text/csv"

)
