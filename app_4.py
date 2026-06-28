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

/* Background */

.stApp{

background:#F4F7FB;

background-image:
linear-gradient(rgba(0,91,172,.05) 1px, transparent 1px),
linear-gradient(90deg, rgba(0,91,172,.05) 1px, transparent 1px);

background-size:45px 45px;

}

/* Main */

.block-container{

padding-top:30px;

max-width:1450px;

}

/* Inputs */

.stTextInput input{

height:60px !important;

border-radius:18px !important;

border:2px solid #D1D5DB !important;

font-size:18px !important;

padding-left:18px !important;

background:white !important;

color:black !important;

box-shadow:0 4px 12px rgba(0,0,0,.08);

}
input[type="password"]{

height:60px !important;

border-radius:18px !important;

font-size:18px !important;

}

.stTextInput input:focus{

border:2px solid #005BAC;

}

/* Select */

.stSelectbox div{

border-radius:12px;

}

/* Buttons */

.stButton>button{

height:52px;

border-radius:14px;

font-size:17px;

font-weight:700;

border:none;

transition:.3s;

background:#D71920;

color:white;

}

.stButton>button:hover{

background:#B91218;

transform:translateY(-2px);

}

/* LOGIN BUTTON */

div[data-testid="column"]:nth-of-type(1) button{

background:#22C55E !important;

color:white !important;

border:none !important;

border-radius:18px !important;

height:58px !important;

font-size:20px !important;

font-weight:700 !important;

}

/* REGISTER BUTTON */

div[data-testid="column"]:nth-of-type(2) button{

background:#3B82F6 !important;

color:white !important;

border:none !important;

border-radius:18px !important;

height:58px !important;

font-size:20px !important;

font-weight:700 !important;

}
/* FORGOT PASSWORD */

button[kind="secondary"]{

background:#3B82F6 !important;

color:white !important;

border:none !important;

border-radius:18px !important;

height:58px !important;

font-size:20px !important;

font-weight:700 !important;

}
/* CHECKBOX */

.stCheckbox label{

color:black !important;

font-size:18px !important;

font-weight:600 !important;

}

/* Headings */

h1,h2,h3,h4{

font-family:Segoe UI;

}
div[data-testid="column"]:nth-of-type(1) .stButton>button{

background:#D71920;

color:white;

}

div[data-testid="column"]:nth-of-type(2) .stButton>button{

background:#111827;

color:white;

}
</style>
""", unsafe_allow_html=True)

# ==========================================================
# SESSION
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

@st.cache_data(ttl=20)

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

left, right = st.columns(
    [1.1,1],
    gap="large"
)
# ==========================================================
# LEFT PANEL
# ==========================================================

with left:

    st.image(
        "ralson_logo.png",
        width=420
    )

    st.markdown("""
    <h1 style="
    color:#005BAC;
    font-size:60px;
    font-weight:800;
    margin-bottom:0;
    ">
    Welcome to
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <h1 style="
    color:#D71920;
    font-size:72px;
    font-weight:900;
    margin-top:-25px;
    margin-bottom:0;
    ">
    RALSON
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <h2 style="
    color:#374151;
    font-size:44px;
    font-weight:700;
    margin-top:-10px;
    ">
    PPC Stock Management Portal
    </h2>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style="
    color:#6B7280;
    font-size:20px;
    line-height:1.8;
    max-width:700px;
    ">
    Manage tyre inventory, stock updates,
    trolley allocation and production planning
    through one centralized cloud platform.
    </p>
    """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    # ======================================================
    # FEATURE CARDS
    # ======================================================

    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:

        st.markdown("""
        <div style="
        background:white;
        border-radius:18px;
        padding:25px;
        box-shadow:0 10px 25px rgba(0,0,0,.08);
        min-height:170px;
        ">

        <h2 style="color:#005BAC;">
        📦 Stock Updates
        </h2>

        <p style="
        color:#555;
        font-size:18px;
        ">
        Instantly update inventory
        and stock records in
        real time.
        </p>

        </div>
        """, unsafe_allow_html=True)

    with row1_col2:

        st.markdown("""
        <div style="
        background:white;
        border-radius:18px;
        padding:25px;
        box-shadow:0 10px 25px rgba(0,0,0,.08);
        min-height:170px;
        ">

        <h2 style="color:#005BAC;">
        📊 Live Reports
        </h2>

        <p style="
        color:#555;
        font-size:18px;
        ">
        Track production,
        stock movement and
        update history.
        </p>

        </div>
        """, unsafe_allow_html=True)

    st.write("")

    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:

        st.markdown("""
        <div style="
        background:white;
        border-radius:18px;
        padding:25px;
        box-shadow:0 10px 25px rgba(0,0,0,.08);
        min-height:170px;
        ">

        <h2 style="color:#005BAC;">
        👥 Multi User
        </h2>

        <p style="
        color:#555;
        font-size:18px;
        ">
        Secure login for
        Operators,
        Supervisors
        and Admins.
        </p>

        </div>
        """, unsafe_allow_html=True)

    with row2_col2:

        st.markdown("""
        <div style="
        background:white;
        border-radius:18px;
        padding:25px;
        box-shadow:0 10px 25px rgba(0,0,0,.08);
        min-height:170px;
        ">

        <h2 style="color:#005BAC;">
        🔒 Secure Cloud
        </h2>

        <p style="
        color:#555;
        font-size:18px;
        ">
        Data stored safely
        using Google Sheets
        cloud integration.
        </p>

        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.caption("© 2026 Ralson Tyres Ltd. | Production Planning & Control")
# ==========================================================
# RIGHT PANEL
# ==========================================================

with right:

    st.write("")
    st.write("")

    login_container = st.container(border=True)

    with login_container:

        st.markdown("""
        <h1 style="
        text-align:center;
        color:#005BAC;
        font-size:46px;
        font-weight:800;
        margin-bottom:5px;
        ">
        Sign In
        </h1>
        """, unsafe_allow_html=True)

        st.markdown("""
        <p style="
        text-align:center;
        color:#6B7280;
        font-size:18px;
        margin-bottom:25px;
        ">
        Login to access the PPC Stock Portal
        </p>
        """, unsafe_allow_html=True)

        # =====================================
        # LOGIN PAGE
        # =====================================

        if st.session_state.page == "login":

            userid = st.text_input(
                "👤 User ID",
                placeholder="Enter User ID"
            ).strip().upper()

            password = st.text_input(
                "🔒 Password",
                type="password",
                placeholder="Enter Password"
            )

            remember = st.checkbox(
                "Remember Me"
            )

            st.write("")

            left_space, c1, c2, right_space = st.columns([0.15, 1, 1, 0.15])

            with c1:
                login_btn = st.button(
                    "🔑 Login",
                    use_container_width=True,
                    type="primary"
                )
            with c2:
                register_btn = st.button(
                    "📝 Register",
                    use_container_width=True
                )
                forgot_btn = st.button(
                    "Forgot Password?",
                    use_container_width=True
                )

            # =====================================
            # LOGIN
            # =====================================

            if login_btn:

                user = users[
                    users["UserId"]
                    .astype(str)
                    .str.upper()
                    ==
                    userid
                ]

                if user.empty:

                    st.error(
                        "User ID not found."
                    )

                else:

                    user = user.iloc[0]

                    if password != str(user["Password"]):

                        st.error(
                            "Incorrect Password."
                        )

                    else:

                        st.success(
                            f"Welcome {user['Name']}"
                        )

                        st.session_state.logged_in = True

                        st.session_state.user = {

                            "userid": user["UserId"],

                            "name": user["Name"],

                            "department": user["Department"],

                            "role": user["Role"]

                        }

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
        # =====================================================
        # REGISTER PAGE
        # =====================================================

        elif st.session_state.page == "register":

            st.markdown("""
            <h1 style="
            text-align:center;
            color:#005BAC;
            font-size:42px;
            font-weight:800;
            ">
            Create Account
            </h1>

            <p style="
            text-align:center;
            color:#666;
            ">
            Register a new employee
            </p>
            """, unsafe_allow_html=True)

            userid = st.text_input(
                "👤 User ID"
            ).strip().upper()

            name = st.text_input(
                "👤 Full Name"
            )

            department = st.text_input(
                "🏢 Department"
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

            # ==========================================
            # CREATE ACCOUNT
            # ==========================================

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
                        "Please enter User ID."
                    )

                elif name == "":

                    st.error(
                        "Please enter Name."
                    )

                elif department == "":

                    st.error(
                        "Please enter Department."
                    )

                elif password == "":

                    st.error(
                        "Please enter Password."
                    )

                elif password != confirm:

                    st.error(
                        "Passwords do not match."
                    )

                elif not existing.empty:

                    st.error(
                        "User ID already exists."
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
                        "Account Created Successfully."
                    )

                    time.sleep(1)

                    st.session_state.page = "login"

                    st.rerun()

            if back_btn:

                st.session_state.page = "login"

                st.rerun()
                    # =====================================================
        # FORGOT PASSWORD
        # =====================================================

        elif st.session_state.page == "forgot":

            st.markdown("""
            <h1 style="
            text-align:center;
            color:#005BAC;
            font-size:42px;
            font-weight:800;
            ">
            Forgot Password
            </h1>

            <p style="
            text-align:center;
            color:#666;
            ">
            Verify your identity to reset your password
            </p>
            """, unsafe_allow_html=True)

            userid = st.text_input(
                "👤 User ID"
            ).strip().upper()

            name = st.text_input(
                "👤 Full Name"
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
                        "User ID or Name is incorrect."
                    )

                else:

                    st.session_state.reset_user = userid

                    st.session_state.page = "reset"

                    st.rerun()

            if back_btn:

                st.session_state.page = "login"

                st.rerun()

        # =====================================================
        # RESET PASSWORD
        # =====================================================

        elif st.session_state.page == "reset":

            st.markdown("""
            <h1 style="
            text-align:center;
            color:#005BAC;
            font-size:42px;
            font-weight:800;
            ">
            Reset Password
            </h1>

            <p style="
            text-align:center;
            color:#666;
            ">
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

                    st.session_state.page = "login"

                    st.session_state.reset_user = ""

                    st.rerun()

            if cancel_btn:

                st.session_state.page = "login"

                st.session_state.reset_user = ""

                st.rerun()
# ==========================================================
# SPACING
# ==========================================================

st.write("")
st.write("")
st.write("")

# ==========================================================
# FOOTER
# ==========================================================



