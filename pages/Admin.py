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
        len(users)
    )

with c2:

    st.metric(
        "Materials",
        len(master)
    )

with c3:

    st.metric(
        "Stock Updates",
        len(logs)
    )

st.divider()

# ==========================
# USER SEARCH
# ==========================

st.subheader("👥 User Management")

search_user = st.text_input(
    "Search User ID"
)

filtered_users = users.copy()

if search_user:

    filtered_users = users[
        users["userid"]
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
    users["userid"]
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

        users = users[
            users["userid"]
            !=
            user_to_delete
        ]

        users.to_excel(
            USERS_FILE,
            index=False
        )

        st.success(
            "User Deleted"
        )

        st.rerun()

# ==========================
# RESET PASSWORD
# ==========================

st.divider()

st.subheader("🔒 Reset Password")

reset_user = st.selectbox(
    "Select User For Password Reset",
    users["userid"]
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

    idx = users[
        users["userid"]
        ==
        reset_user
    ].index[0]

    users.loc[
        idx,
        "password"
    ] = new_password

    users.to_excel(
        USERS_FILE,
        index=False
    )

    st.success(
        "Password Reset Successfully"
    )

# ==========================
# DOWNLOAD FILES
# ==========================

st.divider()

st.subheader("📥 Downloads")

col1, col2, col3 = st.columns(3)

with col1:

    with open(
        USERS_FILE,
        "rb"
    ) as f:

        st.download_button(
            "Download Users",
            f,
            file_name="users.xlsx"
        )

with col2:

    with open(
        MASTER_FILE,
        "rb"
    ) as f:

        st.download_button(
            "Download Stock",
            f,
            file_name="master.xlsx"
        )

with col3:

    with open(
        LOG_FILE,
        "rb"
    ) as f:

        st.download_button(
            "Download Logs",
            f,
            file_name="logs.xlsx"
        )
        st.divider()

st.subheader("⚙️ Column Configuration")

master_ws = sheet.worksheet("Master")

master_df = pd.DataFrame(
    master_ws.get_all_records()
)

columns = master_df.columns.tolist()

material_column = st.selectbox(
    "Material Column",
    columns
)

code_column = st.selectbox(
    "Code Column",
    columns
)

stock_column = st.selectbox(
    "Stock Column",
    columns
)

if st.button(
    "💾 Save Configuration",
    use_container_width=True
):

    config_ws = sheet.worksheet(
        "Config"
    )

    config_ws.clear()

    config_ws.update(
        "A1:C2",
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
        "Configuration Saved"
    )
