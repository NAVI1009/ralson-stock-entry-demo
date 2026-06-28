import streamlit as st
import pandas as pd
import time

from google_sheets import client
from config import SHEET_ID, USERS_SHEET

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Ralson PPC Portal",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

/* ========================================= */
/* Hide Streamlit */
/* ========================================= */

#MainMenu{
visibility:hidden;
}

footer{
visibility:hidden;
}

header{
visibility:hidden;
}

[data-testid="stSidebar"]{
display:none;
}

[data-testid="stSidebarNav"]{
display:none;
}

/* ========================================= */
/* Background */
/* ========================================= */

.stApp{

background:#F5F7FA;

background-image:

linear-gradient(rgba(0,91,172,.04) 1px, transparent 1px),

linear-gradient(90deg, rgba(0,91,172,.04) 1px, transparent 1px);

background-size:45px 45px;

}

/* ========================================= */
/* Container */
/* ========================================= */

.block-container{

padding-top:2rem;
padding-bottom:1rem;
max-width:1450px;

}

/* ========================================= */
/* Inputs */
/* ========================================= */

.stTextInput input{

height:50px;

border-radius:10px;

border:1px solid #D7DCE5;

background:white;

font-size:16px;

}

/* ========================================= */
/* Buttons */
/* ========================================= */

.stButton button{

height:52px;

border-radius:10px;

font-size:17px;

font-weight:600;

}

/* ========================================= */
/* Divider */
/* ========================================= */

hr{

border:1px solid #E4E8EE;

}

/* ========================================= */
/* Headings */
/* ========================================= */

h1,h2,h3,h4{

font-family:Arial;

}

</style>
""", unsafe_allow_html=True)

# ============================================================
# SESSION VARIABLES
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "login"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = {}

if "reset_user" not in st.session_state:
    st.session_state.reset_user = ""

# ============================================================
# GOOGLE SHEETS
# ============================================================

sheet = client.open_by_key(SHEET_ID)

users_ws = sheet.worksheet(USERS_SHEET)

# ============================================================
# LOAD USERS
# ============================================================

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
# ============================================================
# ERP LAYOUT
# ============================================================

left, right = st.columns([1.25, 1])

# ============================================================
# LEFT PANEL
# ============================================================

with left:

    st.image(
        "ralson_logo.png",
        width=350
    )

    st.markdown("""
    <div style="margin-top:10px;">

    <h1 style="
    color:#005BAC;
    font-size:48px;
    font-weight:800;
    margin-bottom:0px;
    ">
    Welcome to
    </h1>

    <h1 style="
    color:#D71920;
    font-size:58px;
    font-weight:900;
    margin-top:-10px;
    ">
    RALSON
    </h1>

    <h2 style="
    color:#444;
    margin-top:-10px;
    ">
    PPC Stock Management Portal
    </h2>

    <p style="
    color:#666;
    font-size:18px;
    width:90%;
    ">

    Manage tyre inventory, stock updates,
    trolley allocation and production planning
    through one centralized system.

    </p>

    </div>

    """,
    unsafe_allow_html=True)

    st.write("")

    # =======================================
    # FEATURE CARDS
    # =======================================

    c1, c2 = st.columns(2)

    with c1:

        st.markdown("""
        <div style="
        background:white;
        padding:20px;
        border-radius:15px;
        box-shadow:0px 4px 12px rgba(0,0,0,.08);
        height:140px;
        ">

        <h3>📦 Stock Updates</h3>

        Update inventory instantly
        across the PPC department.

        </div>
        """,
        unsafe_allow_html=True)

    with c2:

        st.markdown("""
        <div style="
        background:white;
        padding:20px;
        border-radius:15px;
        box-shadow:0px 4px 12px rgba(0,0,0,.08);
        height:140px;
        ">

        <h3>📊 Live Reports</h3>

        View stock history,
        material status and logs.

        </div>
        """,
        unsafe_allow_html=True)

    st.write("")

    c3, c4 = st.columns(2)

    with c3:

        st.markdown("""
        <div style="
        background:white;
        padding:20px;
        border-radius:15px;
        box-shadow:0px 4px 12px rgba(0,0,0,.08);
        height:140px;
        ">

        <h3>👥 Multi User</h3>

        Secure access for
        Admins, Supervisors
        and Operators.

        </div>
        """,
        unsafe_allow_html=True)

    with c4:

        st.markdown("""
        <div style="
        background:white;
        padding:20px;
        border-radius:15px;
        box-shadow:0px 4px 12px rgba(0,0,0,.08);
        height:140px;
        ">

        <h3>🔒 Secure</h3>

        Powered by
        Google Sheets
        Cloud Database.

        </div>
        """,
        unsafe_allow_html=True)
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

# ============================================================
# RIGHT PANEL
# ============================================================

with right:

    st.markdown("""
    <div style="
        background:white;
        padding:35px;
        border-radius:22px;
        box-shadow:0px 12px 35px rgba(0,0,0,.12);
        margin-top:30px;
        margin-left:20px;
        margin-right:20px;
    ">
    """, unsafe_allow_html=True)

    st.markdown("""
    <h2 style="
        text-align:center;
        color:#005BAC;
        font-weight:700;
        margin-bottom:5px;
    ">
        Sign In
    </h2>

    <p style="
        text-align:center;
        color:#777;
        margin-bottom:30px;
    ">
        Login to access the PPC Stock Portal
    </p>
    """, unsafe_allow_html=True)

    # ======================================================
    # LOGIN PAGE
    # ======================================================

    if st.session_state.page == "login":

        userid = st.text_input(
            "👤 User ID",
            placeholder="Enter your User ID"
        ).strip().upper()

        password = st.text_input(
            "🔒 Password",
            type="password",
            placeholder="Enter your Password"
        )

        remember = st.checkbox(
            "Remember Me"
        )

        st.write("")

        col1, col2 = st.columns(2)

        with col1:

            login_btn = st.button(
                "🔑 Login",
                use_container_width=True,
                type="primary"
            )

        with col2:

            register_btn = st.button(
                "📝 Register",
                use_container_width=True
            )

        if st.button(
            "Forgot Password?",
            use_container_width=True
        ):
            st.session_state.page = "forgot"
            st.rerun()

        # ==========================================
        # LOGIN LOGIC
        # ==========================================

        if login_btn:

            user = users[
                users["UserId"]
                .astype(str)
                .str.upper()
                ==
                userid
            ]

            if user.empty():

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

        if register_btn:

            st.session_state.page = "register"

            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
    # ============================================================
# REGISTER PAGE
# ============================================================

    elif st.session_state.page == "register":

        st.markdown("""
        <h2 style="
        text-align:center;
        color:#005BAC;
        ">
        👤 Create Account
        </h2>

        <p style="
        text-align:center;
        color:gray;
        ">
        Register a new employee
        </p>
        """, unsafe_allow_html=True)

        userid = st.text_input(
            "👤 User ID"
        ).strip().upper()

        name = st.text_input(
            "📝 Full Name"
        )

        department = st.text_input(
            "🏭 Department"
        )

        role = st.selectbox(

            "Role",

            [

                "Operator",

                "Supervisor",

                "Manager"

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

        # =====================================
        # CREATE ACCOUNT
        # =====================================

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

                st.error(
                    "Enter User ID"
                )

            elif name == "":

                st.error(
                    "Enter Name"
                )

            elif department == "":

                st.error(
                    "Enter Department"
                )

            elif password == "":

                st.error(
                    "Enter Password"
                )

            elif password != confirm:

                st.error(
                    "Passwords do not match."
                )

            elif not existing.empty:

                st.error(
                    "User already exists."
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

                time.sleep(1.5)

                st.session_state.page = "login"

                st.rerun()

        if back_btn:

            st.session_state.page = "login"

            st.rerun()
        # ============================================================
# FORGOT PASSWORD
# ============================================================

    elif st.session_state.page == "forgot":

        st.markdown("""
        <h2 style="
        text-align:center;
        color:#005BAC;
        ">
        🔑 Forgot Password
        </h2>

        <p style="
        text-align:center;
        color:#777;
        ">
        Verify your identity to reset your password
        </p>
        """, unsafe_allow_html=True)

        userid = st.text_input(
            "👤 User ID"
        ).strip().upper()

        name = st.text_input(
            "📝 Full Name"
        ).strip()

        st.write("")

        c1, c2 = st.columns(2)

        with c1:

            continue_btn = st.button(
                "➡ Continue",
                use_container_width=True,
                type="primary"
            )

        with c2:

            back_btn = st.button(
                "⬅ Back",
                use_container_width=True
            )

        # ==========================================
        # VERIFY USER
        # ==========================================

        if continue_btn:

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
                    "❌ User ID or Name is incorrect."
                )

            else:

                st.success(
                    "Identity Verified Successfully."
                )

                time.sleep(1)

                st.session_state.reset_user = userid

                st.session_state.page = "reset"

                st.rerun()

        if back_btn:

            st.session_state.page = "login"

            st.rerun()
        # ============================================================
# RESET PASSWORD
# ============================================================

    elif st.session_state.page == "reset":

        st.markdown("""
        <h2 style="
        text-align:center;
        color:#005BAC;
        ">
        🔒 Reset Password
        </h2>

        <p style="
        text-align:center;
        color:#777;
        ">
        Create a new secure password
        </p>
        """, unsafe_allow_html=True)

        pwd1 = st.text_input(
            "🔑 New Password",
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
                    "✅ Password Updated Successfully"
                )

                time.sleep(1.5)

                st.session_state.page = "login"

                st.session_state.reset_user = ""

                st.rerun()

        if cancel_btn:

            st.session_state.page = "login"

            st.rerun()

    # ============================================================
    # CLOSE LOGIN CARD
    # ============================================================

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

# ============================================================
# FOOTER
# ============================================================

st.write("")
st.write("")
st.write("")

st.markdown("""
<div style="
text-align:center;
color:#666;
font-size:15px;
padding:20px;
">

<hr>

<b>Ralson Tyres Limited</b><br>

Production Planning & Control Portal<br><br>

Version 1.0 • © 2026

</div>
""",
unsafe_allow_html=True)
