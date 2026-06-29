import streamlit as st
import pandas as pd
import time

from google_sheets import client
from config import SHEET_ID, USERS_SHEET

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Ralson PPC Portal",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================================
# CSS
# ==========================================================

st.markdown("""
<style>

/* Hide Streamlit */

#MainMenu{
visibility:hidden;
}

header{
visibility:hidden;
}

footer{
visibility:hidden;
}

[data-testid="stSidebar"]{
display:none;
}

[data-testid="collapsedControl"]{
display:none;
}

/* Background */

.stApp{
    background:white;
}

/* Main Container */

.block-container{
    padding-top:25px;
    max-width:1500px;
}

/* Headings */

h1,h2,h3,h4,h5,p,label{
    color:inherit !important;
}

/* Inputs */

.stTextInput input{
    border-radius:12px !important;
    height:48px;
    font-size:17px;
}

.stTextInput input:focus{
    border:1px solid #005BAC !important;
    box-shadow:none !important;
}

/* Buttons */

.stButton>button{
    height:48px;
    border-radius:10px;
    font-size:16px;
    font-weight:600;
}

/* Divider */

hr{
    border:1px solid #E5E7EB;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# SESSION STATE
# ==========================================================

if "page" not in st.session_state:
    st.session_state.page = "login"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = {}

if "reset_user" not in st.session_state:
    st.session_state.reset_user = ""

# ==========================================================
# GOOGLE SHEETS
# ==========================================================

sheet = client.open_by_key(SHEET_ID)

users_ws = sheet.worksheet(USERS_SHEET)

# ==========================================================
# LOAD USERS
# ==========================================================

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

# ==========================================================
# PAGE LAYOUT
# ==========================================================

left, middle, right = st.columns(
    [1.45, 0.12, 0.95],
    gap="large"
)

# ==========================================================
# LEFT PANEL
# ==========================================================

with left:

    st.image(
        "ralson_logo.png",
        width=260
    )

    st.markdown("""
# Welcome to

# <span style="color:#D71920;">RALSON TYRES</span>

### PPC Stock Management Portal
""", unsafe_allow_html=True)

    st.write("")

    st.markdown("""
This portal allows **Production Planning & Control** employees to update stock in real time.
""")

    st.write("")

    c1, c2 = st.columns(2)

    with c1:

        st.info("""
### 📦 Stock

Manage Inventory
""")

    with c2:

        st.info("""
### 📊 Reports

View Logs
""")

    c3, c4 = st.columns(2)

    with c3:

        st.info("""
### 👥 Multiple Users 
         Active

""")

    with c4:

        st.info("""
### 🔒 Secure

Google Sheets
""")
# ==========================================================
# RIGHT PANEL
# ==========================================================

with right:

    st.markdown("""
    <div style="
        background:#f8f9fa;
        padding:30px;
        border-radius:18px;
        box-shadow:0px 4px 18px rgba(0,0,0,0.10);
    ">
    """, unsafe_allow_html=True)

    st.markdown("""
    ## Sign In

    Login to continue
    """)

    # ==========================================================
    # LOGIN PAGE
    # ==========================================================

    if st.session_state.page == "login":

        userid = st.text_input(
            "👤 User ID"
        ).strip().upper()

        password = st.text_input(
            "🔒 Password",
            type="password"
        )

        remember = st.checkbox("Remember Me")

        st.write("")

        col1, col2 = st.columns(2)

        with col1:

            login_btn = st.button(
                "Login",
                use_container_width=True,
                type="primary"
            )

        with col2:

            register_btn = st.button(
                "Register",
                use_container_width=True
            )

        forgot_btn = st.button(
            "Forgot Password?",
            use_container_width=True
        )

        # ---------------- LOGIN ----------------

        if login_btn:

            user = users[
                users["UserId"]
                .astype(str)
                .str.upper()
                == userid
            ]

            if user.empty:

                st.error("User ID not found.")

            else:

                user = user.iloc[0]

                if password != str(user["Password"]):

                    st.error("Incorrect Password.")

                else:

                    st.session_state.logged_in = True

                    st.session_state.user = {

                        "userid": user["UserId"],

                        "name": user["Name"],

                        "department": user["Department"],

                        "role": user["Role"]

                    }

                    st.success(
                        f"Welcome {user['Name']}"
                    )

                    time.sleep(1)

                    st.switch_page(
                        "pages/Dashboard.py"
                    )

        if register_btn:

            st.session_state.page = "register"

            st.rerun()

        if forgot_btn:

            st.session_state.page = "forgot"

            st.rerun()
            # ==========================================================
    # REGISTER PAGE
    # ==========================================================

    elif st.session_state.page == "register":

        st.markdown("""
        ## 👤 Create New Account

        Register a new PPC Portal account.
        """)

        userid = st.text_input(
            "User ID"
        ).strip().upper()

        name = st.text_input(
            "Full Name"
        )

        department = st.text_input(
            "Department"
        )

        role = st.selectbox(
            "Role",
            [
                "Operator",
                "Supervisor",
                "Manager",
                "Admin"
            ]
        )

        password = st.text_input(
            "Password",
            type="password",
            key="reg_password"
        )

        confirm = st.text_input(
            "Confirm Password",
            type="password",
            key="reg_confirm"
        )

        st.write("")

        col1, col2 = st.columns(2)

        with col1:

            create_btn = st.button(
                "Create Account",
                use_container_width=True,
                type="primary"
            )

        with col2:

            back_btn = st.button(
                "Back",
                use_container_width=True
            )

        if create_btn:

            users = load_users()

            existing = users[
                users["UserId"]
                .astype(str)
                .str.upper()
                == userid
            ]

            if userid == "":

                st.error("Please enter User ID.")

            elif name == "":

                st.error("Please enter Full Name.")

            elif department == "":

                st.error("Please enter Department.")

            elif password == "":

                st.error("Please enter Password.")

            elif password != confirm:

                st.error("Passwords do not match.")

            elif not existing.empty:

                st.error("User already exists.")

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
                    "Account Created Successfully."
                )

                time.sleep(1)

                st.session_state.page = "login"

                st.rerun()

        if back_btn:

            st.session_state.page = "login"

            st.rerun()
            # ==========================================================
    # FORGOT PASSWORD
    # ==========================================================

    elif st.session_state.page == "forgot":

        st.markdown("""
        ## 🔑 Forgot Password

        Verify your identity to reset your password.
        """)

        userid = st.text_input(
            "User ID"
        ).strip().upper()

        name = st.text_input(
            "Full Name"
        )

        st.write("")

        col1, col2 = st.columns(2)

        with col1:

            verify_btn = st.button(
                "Verify",
                use_container_width=True,
                type="primary"
            )

        with col2:

            back_btn = st.button(
                "Back",
                use_container_width=True
            )

        if verify_btn:

            users = load_users()

            row = users[
                (
                    users["UserId"]
                    .astype(str)
                    .str.upper()
                    == userid
                )
                &
                (
                    users["Name"]
                    .astype(str)
                    .str.lower()
                    == name.lower()
                )
            ]

            if row.empty():

                st.error("Invalid User ID or Name.")

            else:

                st.session_state.reset_user = userid

                st.session_state.page = "reset"

                st.rerun()

        if back_btn:

            st.session_state.page = "login"

            st.rerun()

    # ==========================================================
    # RESET PASSWORD
    # ==========================================================

    elif st.session_state.page == "reset":

        st.markdown("""
        ## 🔒 Reset Password
        """)

        pwd1 = st.text_input(
            "New Password",
            type="password",
            key="new_password"
        )

        pwd2 = st.text_input(
            "Confirm Password",
            type="password",
            key="confirm_new_password"
        )

        st.write("")

        col1, col2 = st.columns(2)

        with col1:

            save_btn = st.button(
                "Save Password",
                use_container_width=True,
                type="primary"
            )

        with col2:

            cancel_btn = st.button(
                "Cancel",
                use_container_width=True
            )

        if save_btn:

            if pwd1 == "":

                st.error("Password cannot be empty.")

            elif pwd1 != pwd2:

                st.error("Passwords do not match.")

            else:

                users = load_users()

                idx = users[
                    users["UserId"]
                    .astype(str)
                    .str.upper()
                    ==
                    st.session_state.reset_user.upper()
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
                    "Password Updated Successfully."
                )

                time.sleep(1)

                st.session_state.reset_user = ""

                st.session_state.page = "login"

                st.rerun()

        if cancel_btn:

            st.session_state.reset_user = ""

            st.session_state.page = "login"

            st.rerun()

    # Close the card
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================================
# FOOTER
# ==========================================================

st.write("")
st.write("")
st.divider()

st.caption(
    "© 2026 Ralson Tyres Ltd. | PPC Stock Management Portal"
)
