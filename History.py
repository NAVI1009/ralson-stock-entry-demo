import streamlit as st
import pandas as pd

LOG_FILE = "logs.xlsx"

# ==========================
# LOGIN CHECK
# ==========================

if not st.session_state.get("logged_in", False):
    st.switch_page("app_4.py")

# ==========================
# PAGE CONFIG
# ==========================

st.set_page_config(
    page_title="History",
    page_icon="📜",
    layout="wide"
)

# ==========================
# HIDE DEFAULT NAVIGATION
# ==========================

st.markdown("""
<style>
[data-testid="stSidebarNav"] {
    display:none;
}
</style>
""", unsafe_allow_html=True)

# ==========================
# SIDEBAR
# ==========================

with st.sidebar:

    st.markdown("## 🏭 Ralson")

    st.markdown(
        f"""
        👤 **{st.session_state.user['name']}**

        🏢 {st.session_state.user['department']}
        """
    )

    st.divider()

    # ADMIN
    if st.session_state.user["userid"] == "ADMIN001":

        if st.button("⚙️ Admin", use_container_width=True):
            st.switch_page("pages/Admin.py")

        if st.button("📜 History", use_container_width=True):
            st.rerun()

        if st.button("👤 Profile", use_container_width=True):
            st.switch_page("pages/Profile.py")

    # EMPLOYEE
    else:

        if st.button("📦 Dashboard", use_container_width=True):
            st.switch_page("pages/Dashboard.py")

        if st.button("📜 History", use_container_width=True):
            st.rerun()

        if st.button("👤 Profile", use_container_width=True):
            st.switch_page("pages/Profile.py")

    st.divider()

    if st.button("🚪 Logout", use_container_width=True):

        st.session_state.logged_in = False
        st.session_state.user = {}

        st.switch_page("app_4.py")
# ==========================
# PAGE TITLE
# ==========================

st.title("📜 Stock Update History")

# ==========================
# LOAD LOGS
# ==========================

try:

    logs = pd.read_excel(LOG_FILE)

except:

    st.warning("No history available.")

    st.stop()

# ==========================
# FILTERS
# ==========================

col1, col2 = st.columns(2)

with col1:

    user_filter = st.selectbox(
        "Filter By User",
        ["All"] + sorted(
            logs["userid"]
            .astype(str)
            .unique()
            .tolist()
        )
    )

with col2:

    material_filter = st.text_input(
        "Search Material"
    )

# ==========================
# APPLY FILTERS
# ==========================

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

# ==========================
# SUMMARY
# ==========================

st.info(
    f"Total Records: {len(filtered)}"
)

# ==========================
# TABLE
# ==========================

st.dataframe(
    filtered,
    use_container_width=True,
    height=500
)

# ==========================
# DOWNLOAD
# ==========================

excel_data = filtered.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    "📥 Download History",
    excel_data,
    file_name="history.csv",
    mime="text/csv"
)