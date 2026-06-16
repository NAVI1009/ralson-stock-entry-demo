import streamlit as st
import pandas as pd

USERS_FILE = "users.xlsx"

# ==========================
# LOGIN CHECK
# ==========================

if not st.session_state.get("logged_in", False):
    st.switch_page("app_4.py")

# ==========================
# PAGE CONFIG
# ==========================

st.set_page_config(
    page_title="Profile",
    page_icon="👤",
    layout="wide"
)

# ==========================
# HIDE DEFAULT NAVIGATION
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

    # ADMIN SIDEBAR
    if st.session_state.user["userid"] == "ADMIN001":

        if st.button(
            "⚙️ Admin",
            use_container_width=True
        ):
            st.switch_page(
                "pages/Admin.py"
            )

        if st.button(
            "📜 History",
            use_container_width=True
        ):
            st.switch_page(
                "pages/History.py"
            )

        if st.button(
            "👤 Profile",
            use_container_width=True
        ):
            st.rerun()

    # EMPLOYEE SIDEBAR
    else:

        if st.button(
            "📦 Dashboard",
            use_container_width=True
        ):
            st.switch_page(
                "pages/Dashboard.py"
            )

        if st.button(
            "📜 History",
            use_container_width=True
        ):
            st.switch_page(
                "pages/History.py"
            )

        if st.button(
            "👤 Profile",
            use_container_width=True
        ):
            st.rerun()

    st.divider()

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False
        st.session_state.user = {}

        st.switch_page(
            "app_4.py"
        )
# ==========================
# PROFILE
# ==========================

st.title("👤 My Profile")

col1, col2 = st.columns(2)

with col1:

    st.info(
        f"User ID: {st.session_state.user['userid']}"
    )

    st.info(
        f"Name: {st.session_state.user['name']}"
    )

with col2:

    st.success(
        f"Department: {st.session_state.user['department']}"
    )

# ==========================
# CHANGE PASSWORD
# ==========================

st.divider()

st.subheader("🔒 Change Password")

old_password = st.text_input(
    "Current Password",
    type="password"
)

new_password = st.text_input(
    "New Password",
    type="password"
)

confirm_password = st.text_input(
    "Confirm New Password",
    type="password"
)

if st.button(
    "Update Password",
    use_container_width=True
):

    users = pd.read_excel(
        USERS_FILE,
        dtype=str
    ).fillna("")

    row = users[
        users["userid"]
        ==
        st.session_state.user["userid"]
    ]

    if row.empty:

        st.error("User not found")

    elif old_password != row.iloc[0]["password"]:

        st.error("Current password is incorrect")

    elif new_password != confirm_password:

        st.error("Passwords do not match")

    else:

        idx = row.index[0]

        users.loc[
            idx,
            "password"
        ] = new_password

        users.to_excel(
            USERS_FILE,
            index=False
        )

        st.success(
            "✅ Password Updated Successfully"
        )