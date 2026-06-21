import streamlit as st
import pandas as pd
import os
from google_sheets import client
from config import SHEET_ID
sheet = client.open_by_key(SHEET_ID)
config_ws = sheet.worksheet("Config")

users_ws = sheet.worksheet("users")
users_df = pd.DataFrame(
    users_ws.get_all_records()
)

logs_ws = sheet.worksheet("logs")
logs_df = pd.DataFrame(
    logs_ws.get_all_records()
)

config_df = pd.DataFrame(
    config_ws.get_all_records()
)

master_ws = sheet.worksheet("Master")

master_df = pd.DataFrame(
    master_ws.get_all_records()
)

if (
    st.session_state.user["userid"]
    !=
    "ADMIN001"
):

    st.error(
        "⛔ Access Denied"
    )

    st.stop()
# ==========================
# LOGIN CHECK
# ==========================

if not st.session_state.get("logged_in", False):
    st.switch_page("app_4.py")

# ==========================
# ADMIN CHECK
# ==========================

if st.session_state.user["userid"] != "ADMIN001":

    st.error("⛔ Access Denied")

    st.stop()

# ==========================
# PAGE CONFIG
# ==========================

st.set_page_config(
    page_title="Admin Panel",
    page_icon="⚙️",
    layout="wide"
)

# ==========================
# HIDE STREAMLIT NAV
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
    
with st.sidebar:

    st.markdown("## 🏭 Ralson")

    st.markdown(
        f"""
        👤 **{st.session_state.user['name']}**

        🏢 {st.session_state.user['department']}
        """
    )

    st.divider()

    if st.button("📦 Dashboard", use_container_width=True):
        st.switch_page("pages/Dashboard.py")


    if st.button("⚙️ Admin", use_container_width=True):
            st.switch_page("pages/Admin.py")

    if st.button("📜 History", use_container_width=True):
        st.switch_page("pages/History.py")

    if st.button("👤 Profile", use_container_width=True):
        st.switch_page("pages/Profile.py")

    st.divider()

    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user = {}
        st.switch_page("app_4.py")

# ==========================
# HEADER
# ==========================

st.title("⚙️ Admin Panel")
st.subheader("📊 Dashboard Overview")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "📦 Materials",
        len(master_df)
    )

with c2:
    st.metric(
        "👥 Users",
        len(users_df)
    )

with c3:
    st.metric(
        "📜 Updates",
        len(logs_df)
    )

with c4:
    admin_count = len(
        users_df[
            users_df["Department"]
            .str.upper()
            ==
            "ADMIN"
        ]
    )


# ==========================
# LOAD DATA
# ==========================

# ==========================
# LOAD DATA FROM GOOGLE SHEETS
# ==========================

master_ws = sheet.worksheet("Master")
master_df = pd.DataFrame(
    master_ws.get_all_records()
)

users_ws = sheet.worksheet("users")
users_df = pd.DataFrame(
    users_ws.get_all_records()
)

logs_ws = sheet.worksheet("logs")
logs_df = pd.DataFrame(
    logs_ws.get_all_records()
)

config_ws = sheet.worksheet("Config")
config_df = pd.DataFrame(
    config_ws.get_all_records()
)

# ==========================
# DASHBOARD STATS
# ==========================

st.subheader("📊 Summary")

c1, c2, c3 = st.columns(3)

with c1:

    st.metric(
        "Users",
        len(users_df)
    )

with c2:

    st.metric(
        "Materials",
        len(master_df)
    )

with c3:

    st.metric(
        "Stock Updates",
        len(logs_df)
    )

st.divider()

# ==========================
# USER SEARCH
# ==========================

st.subheader("👥 User Management")

search_user = st.text_input(
    "Search User ID"
)

filtered_users = users_df.copy()

if search_user:

    filtered_users = users_df[
        users_df["userid"]
        .str.contains(
            search_user,
            case=False,
            na=False
        )
    ]

st.dataframe(
    filtered_users,
    use_container_width=True
)

# ==========================
# DELETE USER
# ==========================

st.divider()

st.subheader("🗑️ Delete User")

user_to_delete = st.selectbox(
    "Select User",
    users_df["UserID"]
    .tolist()
)

if st.button(
    "Delete User",
    use_container_width=True
):

    if user_to_delete == "ADMIN001":

        st.error(
            "Admin cannot be deleted"
        )

    else:
        users_df = users_df[
        users_df["userid"] != user_to_delete
        ]

    users_ws.clear()

    users_ws.update(
        [users_df.columns.values.tolist()]
        +
        users_df.values.tolist()
    )

    st.success("User Deleted")

    st.rerun()

# ==========================
# RESET PASSWORD
# ==========================

st.divider()

st.subheader("🔒 Reset Password")

reset_user = st.selectbox(
    "Select User For Password Reset",
    users_df["UserID"]
    .tolist(),
    key="reset"
)

new_password = st.text_input(
    "New Password",
    type="password"
)

if st.button(
    "Reset Password",
    use_container_width=True
):

    idx = users_df[
        users_df["UserID"]
        ==
        reset_user
    ].index[0]

    users_df.loc[
        idx,
        "password"
    ] = new_password

    users_ws.clear()

users_ws.update(
    [users_df.columns.tolist()]
    +
    users_df.values.tolist()
)
st.success(
        "Password Reset Successfully"
    )

# ==========================
# DOWNLOAD FILES
# ==========================
st.divider()

st.subheader("⚙️ Column Configuration")

master_ws = sheet.worksheet("Master")

master_df = pd.DataFrame(
    master_ws.get_all_records()
)

columns = master_df.columns.tolist()

config_ws = sheet.worksheet("Config")

config_df = pd.DataFrame(
    config_ws.get_all_records()
)

current_material = (
    config_df.loc[0, "material_column"]
    if "material_column" in config_df.columns
    else columns[0]
)

current_code = (
    config_df.loc[0, "code_column"]
    if "code_column" in config_df.columns
    else columns[0]
)

current_stock = (
    config_df.loc[0, "stock_column"]
    if "stock_column" in config_df.columns
    else columns[0]
)

material_column = st.selectbox(
    "Material Description Column",
    columns,
    index=columns.index(current_material)
    if current_material in columns
    else 0
)

code_column = st.selectbox(
    "Code Column",
    columns,
    index=columns.index(current_code)
    if current_code in columns
    else 0
)

stock_column = st.selectbox(
    "Stock Column",
    columns,
    index=columns.index(current_stock)
    if current_stock in columns
    else 0
)

if st.button(
    "💾 Save Configuration",
    use_container_width=True
):

    config_ws.clear()

    config_ws.update(
        [
            [
                "material_column",
                "code_column",
                "stock_column"
            ],
            [
                material_column,
                code_column,
                stock_column
            ]
        ]
    )

    st.success(
        "Configuration Saved Successfully"
    )

    st.rerun()
