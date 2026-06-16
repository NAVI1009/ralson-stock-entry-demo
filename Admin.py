import streamlit as st
import pandas as pd
import os

USERS_FILE = "users.xlsx"
MASTER_FILE = "master.xlsx"
LOG_FILE = "logs.xlsx"
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

    if st.button("📜 History", use_container_width=True):
        st.switch_page("pages/History.py")

    if st.button("👤 Profile", use_container_width=True):
        st.switch_page("pages/Profile.py")

    if st.button("⚙️ Admin", use_container_width=True):
        st.rerun()

    st.divider()

    if st.button("🚪 Logout", use_container_width=True):

        st.session_state.logged_in = False
        st.session_state.user = {}

        st.switch_page("app_4.py")

# ==========================
# HEADER
# ==========================

st.title("⚙️ Admin Panel")

# ==========================
# LOAD DATA
# ==========================

users = pd.read_excel(
    USERS_FILE,
    dtype=str
).fillna("")

master = pd.read_excel(
    MASTER_FILE
)

logs = pd.read_excel(
    LOG_FILE
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

st.subheader("⚙️ Stock Database Configuration")

import os

excel_files = [
    f for f in os.listdir(".")
    if f.endswith(".xlsx")
    and f not in [
        "users.xlsx",
        "logs.xlsx",
        "config.xlsx"
    ]
]

config = pd.read_excel("config.xlsx")

current_file = config.loc[0, "excel_file"]
st.subheader("📤 Upload New Stock File")

uploaded_file = st.file_uploader(
    "Upload Excel File",
    type=["xlsx"]
)

if uploaded_file is not None:

    with open(
        uploaded_file.name,
        "wb"
    ) as f:

        f.write(
            uploaded_file.getbuffer()
        )

    st.success(
        f"{uploaded_file.name} uploaded successfully"
    )

    st.rerun()

selected_file = st.selectbox(
    "Select Stock Excel File",
    excel_files,
    index=excel_files.index(current_file)
    if current_file in excel_files
    else 0
)

temp_df = pd.read_excel(selected_file)

available_columns = [
    col for col in temp_df.columns
    if col not in [
        "Code",
        "Material Description"
    ]
]

current_column = config.loc[0, "stock_column"]

selected_column = st.selectbox(
    "Select Stock Column",
    available_columns,
    index=available_columns.index(current_column)
    if current_column in available_columns
    else 0
)

if st.button(
    "💾 Save Configuration",
    use_container_width=True
):

    config.loc[0, "excel_file"] = selected_file
    config.loc[0, "stock_column"] = selected_column

    config.to_excel(
        "config.xlsx",
        index=False
    )

    st.success(
        "Configuration Saved Successfully"
    )
# ==========================
# RECENT ACTIVITY
# ==========================

st.divider()

st.subheader("🕒 Recent Activity")

st.dataframe(
    logs.tail(20),
    use_container_width=True
)