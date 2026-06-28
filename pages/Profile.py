import streamlit as st
import pandas as pd

from google_sheets import client
from config import SHEET_ID, USERS_SHEET

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Profile",
    page_icon="👤",
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

users_ws = sheet.worksheet(USERS_SHEET)

# ==========================================
# LOAD USERS
# ==========================================

@st.cache_data(ttl=30)
def load_users():

    df = pd.DataFrame(
        users_ws.get_all_records()
    )

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    return df

users_df = load_users()
# ==========================================
# CURRENT USER
# ==========================================

user = users_df[
    users_df["UserId"].astype(str)
    ==
    st.session_state.user["userid"]
]

if user.empty:

    st.error("User not found.")

    st.stop()

user = user.iloc[0]

# ==========================================
# PAGE TITLE
# ==========================================

st.title("👤 My Profile")

st.markdown("---")

# ==========================================
# USER INFORMATION
# ==========================================

col1, col2 = st.columns(2)

with col1:

    st.text_input(
        "User ID",
        value=user["UserId"],
        disabled=True
    )

    st.text_input(
        "Name",
        value=user["Name"],
        disabled=True
    )

with col2:

    st.text_input(
        "Department",
        value=user["Department"],
        disabled=True
    )

    st.text_input(
        "Role",
        value=user["Role"],
        disabled=True
    )

st.markdown("---")
with st.sidebar:

    st.markdown("# 🏭 Ralson")

    st.markdown("---")

    st.markdown(
        f"""
### 👤 {st.session_state.user["name"]}

**User ID:** {st.session_state.user["userid"]}

**Department:** {st.session_state.user["department"]}
"""
    )
    dashboard_color = "secondary"
history_color = "secondary"
profile_color = "primary"
admin_color = "secondary"


    if st.button("📦 Dashboard", use_container_width=True):
        st.switch_page("pages/Dashboard.py")

    if st.session_state.user["userid"] == "ADMIN001":
        if st.button("⚙️ Admin", use_container_width=True):
            st.switch_page("pages/Admin.py")

    if st.button("📜 History", use_container_width=True):
        st.switch_page("pages/History.py")

    if st.button("👤 Profile", use_container_width=True):
        st.rerun()

    st.divider()

    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user = {}
        st.switch_page("app_4.py")
# ==========================================
# CHANGE PASSWORD
# ==========================================

st.subheader("🔒 Change Password")

current_password = st.text_input(
    "Current Password",
    type="password"
)

new_password = st.text_input(
    "New Password",
    type="password"
)

confirm_password = st.text_input(
    "Confirm Password",
    type="password"
)
# ==========================================
# UPDATE PASSWORD
# ==========================================

if st.button(
    "💾 Update Password",
    use_container_width=True
):

    if current_password == "":

        st.error("Enter your current password.")

    elif current_password != str(user["Password"]):

        st.error("Current password is incorrect.")

    elif new_password == "":

        st.error("New password cannot be empty.")

    elif new_password != confirm_password:

        st.error("New passwords do not match.")

    elif new_password == current_password:

        st.warning("New password must be different from the current password.")

    else:

        try:

            # Reload latest users data
            users_df = load_users()

            row_index = users_df[
                users_df["UserId"].astype(str)
                ==
                st.session_state.user["userid"]
            ].index[0]

            users_df.loc[
                row_index,
                "Password"
            ] = new_password

            # Rewrite users sheet
            users_ws.clear()

            users_ws.update(
                [users_df.columns.tolist()]
                +
                users_df.values.tolist()
            )

            # Clear cache
            load_users.clear()

            st.success("✅ Password updated successfully.")

            st.info(
                "Please login again using your new password."
            )

            st.session_state.logged_in = False
            st.session_state.user = {}

            st.switch_page("app_4.py")

        except Exception as e:

            st.error(f"Error updating password: {e}")
