import streamlit as st
import pandas as pd
import time

from google_sheets import client
from config import SHEET_ID, USERS_SHEET

# ============================================
# PAGE CONFIG
# ============================================

st.set_page_config(
    page_title="Ralson PPC Portal",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.markdown("""
<style>

/* Hide Sidebar completely */

[data-testid="stSidebar"]{
    display:none;
}

/* Hide sidebar navigation */

[data-testid="stSidebarNav"]{
    display:none;
}

/* Hide collapsed sidebar button (☰ or >) */

[data-testid="collapsedControl"]{
    display:none;
}

/* Remove left padding created by sidebar */

section.main > div{
    padding-left:2rem !important;
}

</style>
""", unsafe_allow_html=True)
# ============================================
# DARK ERP CSS
# ============================================

st.markdown("""
<style>

/* Hide Streamlit */

#MainMenu,
footer,
header{
visibility:hidden;
}

[data-testid="stSidebarNav"]{
display:none;
}

/* Background */

.stApp{
background:#111827;
}

/* Page */

.block-container{
padding-top:20px;
max-width:1400px;
}

/* Text */

h1,h2,h3,h4,label,p{
color:white !important;
}

</style>
""", unsafe_allow_html=True)
# ============================================
# SESSION VARIABLES
# ============================================

if "page" not in st.session_state:
    st.session_state.page = "login"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = {}

if "reset_user" not in st.session_state:
    st.session_state.reset_user = ""

# ============================================
# GOOGLE SHEETS
# ============================================

sheet = client.open_by_key(SHEET_ID)

users_ws = sheet.worksheet(USERS_SHEET)

# ============================================
# LOAD USERS
# ============================================

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

# ============================================
# PAGE LAYOUT
# ============================================

left, right = st.columns(
    [1.35, 1],
    gap="large"
)

# ============================================
# LEFT PANEL
# ============================================

with left:

    st.image(
        "ralson_logo.png",
        width=360
    )

    st.markdown("""
# Welcome to

# <span style="color:#22C55E;">RALSON</span>

### PPC Stock Management Portal

Manage tyre inventory, stock updates,
trolley allocation and production planning
through one centralized cloud platform.
""",
    unsafe_allow_html=True)

    st.write("")
    st.write("")

    r1, r2 = st.columns(2)

    with r1:

        st.info("""
### 📦 Stock Updates

Real-time inventory
management.
""")

    with r2:

        st.info("""
### 📊 Live Reports

History, Logs,
Material Status.
""")

    st.write("")

    r3, r4 = st.columns(2)

    with r3:

        st.info("""
### 👥 Multi User

Operator

Supervisor

Admin
""")

    with r4:

        st.info("""
### 🔒 Secure

Google Sheets

Cloud Database
""")
# ============================================
# RIGHT PANEL
# ============================================

with right:
    st.markdown("""
    <h1 style="
        text-align:center;
        color:white;
        margin-bottom:5px;
    ">
    Sign In
    </h1>

    <p style="
        text-align:center;
        color:#94A3B8;
        margin-bottom:25px;
    ">
    Login to access the PPC Stock Portal
    </p>
    """, unsafe_allow_html=True)
    userid = st.text_input("👤 User ID")
    password = st.text_input(
    "🔒 Password",
    type="password"
    )
    remember = st.checkbox("Remember Me")
    c1, c2 = st.columns(2)
    with c1:
        login_btn = st.button(
        "Login",
        use_container_width=True
    )
    with c2:
        register_btn = st.button(
        "Register",
        use_container_width=True
    )
    forgot_btn = st.button(
    "Forgot Password?",
    use_container_width=True
    )
    if login_btn:

            user = users[
                users["UserId"]
                .astype(str)
                .str.upper()
                ==
                userid
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
                    elif st.session_state.page == "register":
                        st.markdown("""
        <h2 style='text-align:center;color:white;'>
        Create New Account
        </h2>

        <p style='text-align:center;color:#94A3B8;'>
        Register a new employee
        </p>
        """, unsafe_allow_html=True)
                        userid = st.text_input(
                            "👤 User ID"
                            ).strip().upper()
                        name = st.text_input(
                            "👨 Full Name"
                            )
                        department = st.text_input(
                            "🏭 Department"
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
                            "🔒 Password",
                            type="password"
                            )
                        confirm = st.text_input(
                            "✅ Confirm Password",
                            type="password"
                            )
            st.write("")
            c1, c2 = st.columns(2)
            with c1:
                create_btn = st.button(
                "✅ Create Account",
                use_container_width=True,
                type="primary"
                )
            with c2:
                back_btn = st.button(
                "⬅ Back",
                use_container_width=True
            )
                if create_btn:
                    users = load_users()

            existing = users[
                users["UserId"]
                .astype(str)
                .str.upper()
                ==
                userid
            ]

            if userid == "":

                st.error("Please enter User ID.")

            elif name == "":

                st.error("Please enter Name.")

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
                elif st.session_state.page == "forgot":
                    st.markdown("""
        <h2 style='text-align:center;color:white;'>
        Forgot Password
        </h2>

        <p style='text-align:center;color:#94A3B8;'>
        Verify your identity
        </p>
        """, unsafe_allow_html=True)
                    userid = st.text_input(
                        "👤 User ID"
                        ).strip().upper()
                    name = st.text_input(
                        "👨 Full Name"
                        )
                    st.write("")
                    c1, c2 = st.columns(2)
                    with c1:
                        verify_btn = st.button(
                "✅ Verify",
                use_container_width=True,
                type="primary"
                )
                        with c2:
                            back_btn = st.button(
                "⬅ Back",
                use_container_width=True
                )
                            if verify_btn:
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
                    "Invalid User ID or Name."
                )

            else:

                st.session_state.reset_user = userid

                st.session_state.page = "reset"

                st.rerun()
                if back_btn:
                    st.session_state.page = "login"
                    st.rerun()

    # ============================================
    # RESET PASSWORD
    # ============================================

                elif st.session_state.page == "reset":
                    st.markdown("""
        <h2 style='text-align:center;color:white;'>
        Reset Password
        </h2>

        <p style='text-align:center;color:#94A3B8;'>
        Create your new password
        </p>
        """, unsafe_allow_html=True)
                    pwd1 = st.text_input(
            "🔒 New Password",
            type="password"
            )
                    pwd2 = st.text_input(
            "✅ Confirm Password",
            type="password"
            )
                    st.write("")
                    c1, c2 = st.columns(2)
            with c1:
                save_btn = st.button(
                "💾 Save Password",
                use_container_width=True,
                type="primary"
            )

            with c2:
                cancel_btn = st.button(
                "❌ Cancel",
                use_container_width=True
            )

            if save_btn:

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
# ============================================
# FOOTER
# ============================================

st.write("")
st.write("")
st.write("")

st.markdown("""
<hr style="border:1px solid #334155;">
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([2,1,2])

with col1:

    st.markdown("""
<div style="color:#94A3B8;font-size:14px;">
🏭 <b>Ralson Tyres Ltd.</b><br>
Production Planning & Control
</div>
""", unsafe_allow_html=True)

with col2:

    st.markdown("""
<div style="text-align:center;color:#64748B;font-size:14px;">
Version 1.0
</div>
""", unsafe_allow_html=True)

with col3:

    st.markdown("""
<div style="text-align:right;color:#94A3B8;font-size:14px;">
Developed using Streamlit & Google Sheets
</div>
""", unsafe_allow_html=True)

st.write("")

st.markdown("""
<div style="
text-align:center;
color:#64748B;
font-size:13px;
padding-bottom:10px;
">
© 2026 Ralson Tyres Limited • All Rights Reserved
</div>
""", unsafe_allow_html=True)
