
import streamlit as st
import pandas as pd
import time

st.markdown("""
<style>
[data-testid="stSidebarNav"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
[data-testid="stSidebar"] {
    display:none;
}
</style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="Ralson Stock Management",
    page_icon="🏭",
    layout="wide"
)

USERS_FILE = "users.xlsx"

# ======================
# SESSION VARIABLES
# ======================

if "page" not in st.session_state:
    st.session_state.page = "login"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = {}

if "reset_user" not in st.session_state:
    st.session_state.reset_user = ""

# ======================
# LOAD USERS
# ======================

users = pd.read_excel(
    USERS_FILE,
    dtype=str
).fillna("")

# ======================
# LOGIN PAGE
# ======================

st.markdown(
    """
    <h1 style='text-align:center;color:#005BAC;'>
    🏭 RALSON STOCK MANAGEMENT
    </h1>
    """,
    unsafe_allow_html=True
)

# LOGIN SCREEN

if st.session_state.page == "login":

    userid = st.text_input("User ID")

    password = st.text_input(
        "Password",
        type="password"
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "Login",
            use_container_width=True
        ):

            row = users[
                users["userid"]
                .str.upper()
                ==
                userid.upper()
            ]

            if row.empty:

                st.error(
                    "User Not Found"
                )

            elif password == row.iloc[0]["password"]:
                st.session_state.logged_in = True
                st.session_state.user = {
                    "userid": row.iloc[0]["userid"],
                    "name": row.iloc[0]["name"],
                    "department": row.iloc[0]["department"]
                }
                st.switch_page("pages/Dashboard.py")

            else:

                st.error(
                    "Wrong Password"
                )

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

# ======================
# REGISTER PAGE
# ======================

elif st.session_state.page == "register":

    st.subheader(
        "👤 New User Registration"
    )

    userid = st.text_input(
        "User ID"
    )

    name = st.text_input(
        "Name"
    )

    department = st.text_input(
        "Department"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    confirm = st.text_input(
        "Confirm Password",
        type="password"
    )

    if st.button(
        "Create Account"
    ):

        existing = users[
            users["userid"]
            .str.upper()
            ==
            userid.upper()
        ]

        if not existing.empty:

            st.error(
                "User Already Exists"
            )

        elif password != confirm:

            st.error(
                "Passwords Do Not Match"
            )

        else:

            users.loc[
                len(users)
            ] = [

                userid.upper(),
                name,
                department,
                password
            ]

            users.to_excel(
                USERS_FILE,
                index=False
            )

            st.success(
                "Account Created Successfully"
            )

            time.sleep(2)

            st.session_state.page = "login"

            st.rerun()

    if st.button(
        "Back To Login"
    ):

        st.session_state.page = "login"

        st.rerun()

# ======================
# FORGOT PASSWORD PAGE
# ======================

elif st.session_state.page == "forgot":

    st.subheader(
        "🔑 Forgot Password"
    )

    userid = st.text_input(
        "User ID"
    )

    name = st.text_input(
        "Name"
    )

    if st.button(
        "Continue"
    ):

        row = users[
            (users["userid"]
             .str.upper()
             ==
             userid.upper())
            &
            (users["name"]
             .str.lower()
             ==
             name.lower())
        ]

        if row.empty:

            st.error(
                "Invalid User ID or Name"
            )

        else:

            st.session_state.reset_user = userid

            st.session_state.page = "reset"

            st.rerun()

    if st.button(
        "Back"
    ):

        st.session_state.page = "login"

        st.rerun()

# ======================
# RESET PASSWORD PAGE
# ======================

elif st.session_state.page == "reset":

    st.subheader(
        "🔒 Reset Password"
    )

    pwd1 = st.text_input(
        "New Password",
        type="password"
    )

    pwd2 = st.text_input(
        "Confirm Password",
        type="password"
    )

    if st.button(
        "Save Password"
    ):

        if pwd1 != pwd2:

            st.error(
                "Passwords Do Not Match"
            )

        else:

            idx = users[
                users["userid"]
                .str.upper()
                ==
                st.session_state.reset_user.upper()
            ].index[0]

            users.loc[
                idx,
                "password"
            ] = pwd1

            users.to_excel(
                USERS_FILE,
                index=False
            )

            st.success(
                "Password Updated Successfully"
            )

            time.sleep(2)

            st.session_state.page = "login"

            st.rerun()