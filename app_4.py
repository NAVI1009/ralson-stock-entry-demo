import streamlit as st
import pandas as pd
import time

from google_sheets import client
from config import SHEET_ID, USERS_SHEET

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Ralson Stock Management",
    page_icon="🏭",
    layout="wide"
)

# Hide Streamlit navigation/sidebar
st.markdown("""
<style>
[data-testid="stSidebarNav"]{
display:none;
}

[data-testid="stSidebar"]{
display:none;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# SESSION VARIABLES
# ==========================================

if "page" not in st.session_state:
    st.session_state.page = "login"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = {}

if "reset_user" not in st.session_state:
    st.session_state.reset_user = ""

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

users = load_users()
# ==========================================
# LOGIN PAGE
# ==========================================

st.markdown(
    """
    <div style="
    text-align:center;
    padding:20px;
    ">

    <h1 style="color:#005BAC;">
    🏭 RALSON STOCK MANAGEMENT
    </h1>

    <h4>
    Production Planning & Control
    </h4>

    </div>
    """,
    unsafe_allow_html=True
)

# ==========================================
# LOGIN
# ==========================================

if st.session_state.page == "login":

    st.subheader("Login")

    userid = st.text_input(
        "User ID"
    ).strip().upper()

    password = st.text_input(
        "Password",
        type="password"
    )

    remember = st.checkbox(
        "Remember Me"
    )

    col1, col2 = st.columns(2)

    # ==========================
    # LOGIN BUTTON
    # ==========================

    with col1:

        if st.button(
            "Login",
            use_container_width=True
        ):

            user = users[
                users["UserId"]
                .astype(str)
                .str.upper()
                ==
                userid
            ]

            if user.empty:

                st.error(
                    "❌ User ID not found."
                )

            else:

                user = user.iloc[0]

                if password != str(user["Password"]):

                    st.error(
                        "❌ Incorrect Password."
                    )

                else:

                    st.session_state.logged_in = True

                    st.session_state.user = {

                        "userid": user["UserId"],

                        "name": user["Name"],

                        "department": user["Department"],

                        "role": user["Role"]

                    }

                    st.success(
                        f"Welcome {user['Name']}!"
                    )

                    time.sleep(1)

                    st.switch_page(
                        "pages/Dashboard.py"
                    )

    # ==========================
    # REGISTER BUTTON
    # ==========================

    with col2:

        if st.button(
            "Register",
            use_container_width=True
        ):

            st.session_state.page = "register"

            st.rerun()

    st.divider()

    if st.button(
        "Forgot Password?",
        use_container_width=True
    ):

        st.session_state.page = "forgot"

        st.rerun()
        # ==========================================
# REGISTER PAGE
# ==========================================

elif st.session_state.page == "register":

    st.subheader("👤 New User Registration")

    userid = st.text_input(
        "User ID"
    ).strip().upper()

    name = st.text_input(
        "Full Name"
    ).strip()

    department = st.text_input(
        "Department"
    ).strip()

    role = st.selectbox(
        "Role",
        [
            "Operator",
            "Supervisor",
            "Manager"
        ]
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    confirm = st.text_input(
        "Confirm Password",
        type="password"
    )

    col1, col2 = st.columns(2)

    # ==========================================
    # CREATE ACCOUNT
    # ==========================================

    with col1:

        if st.button(
            "Create Account",
            use_container_width=True
        ):

            users = load_users()

            existing = users[
                users["UserId"]
                .astype(str)
                .str.upper()
                ==
                userid
            ]

            if userid == "":

                st.error("Enter User ID")

            elif name == "":

                st.error("Enter Name")

            elif department == "":

                st.error("Enter Department")

            elif password == "":

                st.error("Enter Password")

            elif not existing.empty:

                st.error(
                    "User ID already exists."
                )

            elif password != confirm:

                st.error(
                    "Passwords do not match."
                )

            else:

                users_ws.append_row(

                    [
                        userid,
                        name,
                        department,
                        role,
                        password
                    ],

                    value_input_option="USER_ENTERED"

                )

                load_users.clear()

                st.success(
                    "✅ Account Created Successfully"
                )

                time.sleep(2)

                st.session_state.page = "login"

                st.rerun()

    # ==========================================
    # BACK
    # ==========================================

    with col2:

        if st.button(
            "Back to Login",
            use_container_width=True
        ):

            st.session_state.page = "login"

            st.rerun()
    # ==========================================
# FORGOT PASSWORD
# ==========================================

elif st.session_state.page == "forgot":

    st.subheader("🔑 Forgot Password")

    userid = st.text_input(
        "User ID"
    ).strip().upper()

    name = st.text_input(
        "Full Name"
    ).strip()

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "Continue",
            use_container_width=True
        ):

            users = load_users()

            row = users[
                (
                    users["UserId"]
                    .astype(str)
                    .str.upper()
                    ==
                    userid
                )
                &
                (
                    users["Name"]
                    .astype(str)
                    .str.lower()
                    ==
                    name.lower()
                )
            ]

            if row.empty:

                st.error(
                    "User ID or Name is incorrect."
                )

            else:

                st.session_state.reset_user = userid

                st.session_state.page = "reset"

                st.rerun()

    with col2:

        if st.button(
            "Back",
            use_container_width=True
        ):

            st.session_state.page = "login"

            st.rerun()

# ==========================================
# RESET PASSWORD
# ==========================================

elif st.session_state.page == "reset":

    st.subheader("🔒 Reset Password")

    pwd1 = st.text_input(
        "New Password",
        type="password"
    )

    pwd2 = st.text_input(
        "Confirm Password",
        type="password"
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "Save Password",
            use_container_width=True
        ):

            if pwd1 == "":

                st.error(
                    "Password cannot be empty."
                )

            elif pwd1 != pwd2:

                st.error(
                    "Passwords do not match."
                )

            else:

                users = load_users()

                idx = users[
                    users["UserId"]
                    .astype(str)
                    .str.upper()
                    ==
                    st.session_state.reset_user
                ].index[0]

                users.loc[
                    idx,
                    "Password"
                ] = pwd1

                users_ws.clear()

                users_ws.update(
                    [users.columns.tolist()]
                    +
                    users.values.tolist()
                )

                load_users.clear()

                st.success(
                    "✅ Password Updated Successfully"
                )

                time.sleep(2)

                st.session_state.page = "login"

                st.session_state.reset_user = ""

                st.rerun()

    with col2:

        if st.button(
            "Cancel",
            use_container_width=True
        ):

            st.session_state.page = "login"

            st.rerun()
    
