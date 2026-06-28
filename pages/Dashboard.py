import streamlit as st
import pandas as pd
from datetime import datetime

from google_sheets import client
from config import SHEET_ID
from gspread_dataframe import set_with_dataframe

# ============================================
# PAGE CONFIG
# ============================================

st.set_page_config(
    page_title="Dashboard",
    page_icon="📦",
    layout="wide"
)

# ============================================
# HIDE DEFAULT NAVIGATION
# ============================================

st.markdown("""
<style>
[data-testid="stSidebarNav"]{
display:none;
}
</style>
""", unsafe_allow_html=True)

# ============================================
# LOGIN CHECK
# ============================================

if not st.session_state.get("logged_in", False):
    st.switch_page("app_4.py")

if "user" not in st.session_state:
    st.switch_page("app_4.py")

# ============================================
# CONNECT TO GOOGLE SHEETS
# ============================================

sheet = client.open_by_key(SHEET_ID)

master_ws = sheet.worksheet("Master")
users_ws = sheet.worksheet("users")
logs_ws = sheet.worksheet("logs")

# ============================================
# LOAD DATA
# ============================================

master_df = pd.DataFrame(
    master_ws.get_all_records()
)

users_df = pd.DataFrame(
    users_ws.get_all_records()
)

logs_df = pd.DataFrame(
    logs_ws.get_all_records()
)

master_df.columns = (
    master_df.columns
    .astype(str)
    .str.strip()
)

# ============================================
# COLUMN NAMES
# ============================================

CODE_COL = "Code"
MATERIAL_COL = "Material Description"
STOCK_COL = "13 GT"

# ============================================
# SIDEBAR
# ============================================

with st.sidebar:

    st.title("🏭 Ralson")

    st.write(
        f"**{st.session_state.user['name']}**"
    )

    st.caption(
        st.session_state.user["department"]
    )

    st.divider()

    if st.button(
        "📦 Dashboard",
        use_container_width=True
    ):
        st.rerun()

    if (
        st.session_state.user["userid"]
        ==
        "ADMIN001"
    ):

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
        st.switch_page(
            "pages/Profile.py"
        )

    st.divider()

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False
        st.session_state.user = {}

        st.switch_page("app_4.py")
    # ============================================
# HEADER
# ============================================

st.markdown(
    f"""
<div style="
background:linear-gradient(90deg,#005BAC,#0077D9);
padding:25px;
border-radius:15px;
color:white;
margin-bottom:25px;
">

<h2>🏭 Ralson PPC Stock Management</h2>

<h3>Welcome, {st.session_state.user["name"]}</h3>

<p><b>Department:</b> {st.session_state.user["department"]}</p>

</div>
""",
    unsafe_allow_html=True
)

# ============================================
# MATERIAL SEARCH
# ============================================

st.subheader("🔍 Search Material")

material_list = (
    master_df[MATERIAL_COL]
    .fillna("")
    .astype(str)
    .tolist()
)

selected_material = st.selectbox(
    "Material Description",
    material_list
)

# ============================================
# GET SELECTED MATERIAL
# ============================================

selected_row = master_df[
    master_df[MATERIAL_COL]
    ==
    selected_material
].iloc[0]

material_code = selected_row[CODE_COL]

current_stock = pd.to_numeric(
    selected_row[STOCK_COL],
    errors="coerce"
)

if pd.isna(current_stock):
    current_stock = 0

current_stock = int(current_stock)

# ============================================
# SHOW DETAILS
# ============================================

c1, c2 = st.columns(2)

with c1:

    st.info(
        f"""
### Material Code

**{material_code}**
"""
    )

with c2:

    st.success(
        f"""
### Current Stock

**{current_stock}**
"""
    )

# ============================================
# STOCK ENTRY
# ============================================

st.subheader("📦 Update Stock")

new_stock = st.number_input(
    "Enter Updated Stock",
    min_value=0,
    value=current_stock,
    step=1
)
# ============================================
# UPDATE STOCK
# ============================================

if st.button(
    "✅ Update Stock",
    use_container_width=True
    ):
    try:
        row_index = master_df[
            master_df[MATERIAL_COL] == selected_material
        ].index[0]

        old_stock = master_df.loc[
            row_index,
            STOCK_COL
        ]

        if pd.isna(old_stock):
            old_stock = 0

        old_stock = int(float(old_stock))

        # Update dataframe
        master_df.loc[
            row_index,
            STOCK_COL
        ] = int(new_stock)

        # Save Master Sheet
        master_ws.clear()

        master_ws.update(
            [master_df.columns.tolist()]
            +
            master_df.values.tolist()
        )

        # ============================================
        # SAVE LOG
        # ============================================

        log = [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            st.session_state.user["userid"],
            st.session_state.user["name"],
            st.session_state.user["department"],
            material_code,
            selected_material,
            old_stock,
            int(new_stock)
        ]

        logs_ws.append_row(
            log,
            value_input_option="USER_ENTERED"
        )
        st.success("Stock Updated Successfully")
        st.balloons()
        st.markdown(
    f"""
    ## ✅ Stock Updated
    **Material:** {selected_material}
    **Code:** {material_code}
    **Previous Stock:** {old_stock}
    **Updated Stock:** {new_stock}
    **Updated By:** {st.session_state.user["name"]}
    """
    )
        st.rerun()
    except Exception as e:
        st.error(f"❌ {e}")

# ============================================
# ADMIN - RECENT ACTIVITY
# ============================================

if st.session_state.user["userid"] == "ADMIN001":

    st.divider()

    st.subheader("🕒 Recent Activity")

    logs_df = pd.DataFrame(
        logs_ws.get_all_records()
    )

    if not logs_df.empty:

        st.dataframe(
            logs_df.tail(20),
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No activity available.")
