import streamlit as st
import pandas as pd

from google_sheets import client
from config import SHEET_ID

# ======================================
# LOGIN CHECK
# ======================================

if not st.session_state.get("logged_in", False):
    st.switch_page("app_4.py")

if st.session_state.user["userid"] != "ADMIN001":
    st.error("Unauthorized Access")
    st.stop()

# ======================================
# PAGE CONFIG
# ======================================

st.set_page_config(
    page_title="Admin",
    page_icon="⚙",
    layout="wide"
)

st.markdown("""
<style>
[data-testid="stSidebarNav"]{
display:none;
}
</style>
""", unsafe_allow_html=True)

# ======================================
# GOOGLE SHEETS
# ======================================

sheet = client.open_by_key(SHEET_ID)

master_ws = sheet.worksheet("Master")
users_ws = sheet.worksheet("users")
logs_ws = sheet.worksheet("logs")

master_df = pd.DataFrame(master_ws.get_all_records())
users_df = pd.DataFrame(users_ws.get_all_records())
logs_df = pd.DataFrame(logs_ws.get_all_records())
# ======================================
# SIDEBAR
# ======================================

with st.sidebar:

    st.image("ralson_logo.png", width=170)

    st.markdown("## 🏭 Ralson PPC")

    st.write(f"**👤 {st.session_state.user['name']}**")
    st.write(f"**ID :** {st.session_state.user['userid']}")
    st.write(f"**Department :** {st.session_state.user['department']}")
    st.write(f"**Role :** Admin")

    st.divider()

    if st.button(
        "📦 Dashboard",
        use_container_width=True
    ):
        st.switch_page("pages/Dashboard.py")

    if st.button(
        "📜 History",
        use_container_width=True
    ):
        st.switch_page("pages/History.py")

    if st.button(
        "👤 Profile",
        use_container_width=True
    ):
        st.switch_page("pages/Profile.py")

    st.button(
        "⚙ Admin",
        use_container_width=True,
        disabled=True
    )

    st.divider()

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False
        st.session_state.user = {}

        st.switch_page("app_4.py")

# ======================================
# PAGE HEADER
# ======================================

st.title("⚙ Admin Panel")

st.caption(
    "Manage users, master stock sheet and system activity."
)

st.divider()

# ======================================
# SUMMARY CARDS
# ======================================

c1, c2, c3 = st.columns(3)

with c1:

    st.metric(
        "👥 Total Users",
        len(users_df)
    )

with c2:

    st.metric(
        "📦 Materials",
        len(master_df)
    )

with c3:

    st.metric(
        "📜 Total Updates",
        len(logs_df)
    )

st.divider()
# ======================================
# MASTER SHEET MANAGEMENT
# ======================================

st.subheader("📂 Master Sheet")

col1, col2 = st.columns([2,1])

with col1:

    uploaded_file = st.file_uploader(
        "Upload New Master Excel File",
        type=["xlsx"]
    )

    if uploaded_file is not None:

        try:

            new_master = pd.read_excel(uploaded_file)

            if st.button(
                "✅ Replace Master Sheet",
                use_container_width=True
            ):

                master_ws.clear()

                master_ws.update(
                    [new_master.columns.tolist()]
                    +
                    new_master.values.tolist()
                )

                st.success(
                    "Master Sheet Updated Successfully."
                )

                st.balloons()

                st.rerun()

        except Exception as e:

            st.error(e)

with col2:

    st.info(
        f"""
### Current Data

📦 Materials

**{len(master_df)}**

"""
    )

st.divider()

# ======================================
# DOWNLOAD LOGS
# ======================================

st.subheader("📥 Download System Logs")

csv = logs_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(

    "📜 Download Logs",

    csv,

    file_name="ralson_logs.csv",

    mime="text/csv",

    use_container_width=True

)

st.divider()
# ======================================
# USER MANAGEMENT
# ======================================

st.subheader("👥 User Management")

if users_df.empty:

    st.warning("No users available.")

else:

    st.dataframe(
        users_df,
        use_container_width=True,
        hide_index=True
    )

st.write("")

# ======================================
# DELETE USER
# ======================================

st.subheader("🗑 Delete User")

user_list = users_df["UserId"].astype(str).tolist()

selected_user = st.selectbox(
    "Select User",
    user_list
)

c1, c2 = st.columns(2)

with c1:

    if st.button(
        "🗑 Delete User",
        use_container_width=True
    ):

        if selected_user == "ADMIN001":

            st.error(
                "Admin account cannot be deleted."
            )

        else:

            users_df = users_df[
                users_df["UserId"] != selected_user
            ]

            users_ws.clear()

            users_ws.update(
                [users_df.columns.tolist()]
                +
                users_df.values.tolist()
            )

            st.success(
                "User Deleted Successfully."
            )

            st.rerun()

with c2:

    if st.button(
        "🔄 Refresh Users",
        use_container_width=True
    ):

        st.rerun()

st.divider()

# ======================================
# SYSTEM INFORMATION
# ======================================

st.subheader("📊 System Information")

col1, col2 = st.columns(2)

with col1:

    st.info(f"""
### 📦 Master Sheet

Rows : **{len(master_df)}**

Columns : **{len(master_df.columns)}**
""")

with col2:

    st.info(f"""
### 👥 Users

Registered : **{len(users_df)}**

Logs : **{len(logs_df)}**
""")
# ======================================
# ADD NEW USER
# ======================================

st.divider()

st.subheader("➕ Add New User")

col1, col2 = st.columns(2)

with col1:

    new_userid = st.text_input(
        "User ID"
    ).strip().upper()

    new_name = st.text_input(
        "Employee Name"
    )

with col2:

    new_department = st.text_input(
        "Department"
    )

    new_role = st.selectbox(
        "Role",
        [
            "Operator",
            "Supervisor",
            "Manager",
            "Admin"
        ]
    )

new_password = st.text_input(
    "Password",
    type="password"
)

if st.button(
    "➕ Add User",
    use_container_width=True
):

    if (
        new_userid == ""
        or new_name == ""
        or new_department == ""
        or new_password == ""
    ):

        st.error("Please fill all fields.")

    elif new_userid in users_df["UserId"].astype(str).tolist():

        st.error("User ID already exists.")

    else:

        new_row = pd.DataFrame([{

            "UserId": new_userid,

            "Name": new_name,

            "Department": new_department,

            "Role": new_role,

            "Password": new_password

        }])

        users_df = pd.concat(
            [users_df, new_row],
            ignore_index=True
        )

        users_ws.clear()

        users_ws.update(
            [users_df.columns.tolist()]
            +
            users_df.values.tolist()
        )

        st.success("User Added Successfully.")

        st.balloons()

        st.rerun()
