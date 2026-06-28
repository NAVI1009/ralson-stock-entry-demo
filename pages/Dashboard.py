import streamlit as st
import pandas as pd
from datetime import datetime

from google_sheets import client
from config import (
    SHEET_ID,
    MASTER_SHEET,
    USERS_SHEET,
    LOGS_SHEET,
    CODE_COLUMN,
    MATERIAL_COLUMN,
    STOCK_COLUMN
)

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="Dashboard",
    page_icon="🏭",
    layout="wide"
)

# ======================================================
# HIDE STREAMLIT NAVIGATION
# ======================================================

st.markdown("""
<style>
[data-testid="stSidebarNav"]{
display:none;
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# LOGIN CHECK
# ======================================================

if not st.session_state.get("logged_in", False):
    st.switch_page("app_4.py")

if "user" not in st.session_state:
    st.switch_page("app_4.py")

# ======================================================
# GOOGLE SHEETS
# ======================================================

sheet = client.open_by_key(SHEET_ID)

master_ws = sheet.worksheet(MASTER_SHEET)
users_ws = sheet.worksheet(USERS_SHEET)
logs_ws = sheet.worksheet(LOGS_SHEET)

# ======================================================
# CACHE FUNCTIONS
# ======================================================

@st.cache_data(ttl=30)
def load_master():

    df = pd.DataFrame(
        master_ws.get_all_records()
    )

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    return df


@st.cache_data(ttl=30)
def load_logs():

    df = pd.DataFrame(
        logs_ws.get_all_records()
    )

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    return df


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

# ======================================================
# LOAD DATA
# ======================================================

master_df = load_master()

users_df = load_users()

logs_df = load_logs()
# ======================================================
# SIDEBAR
# ======================================================

with st.sidebar:

    st.markdown("# 🏭 Ralson")

    st.markdown("---")

    st.markdown(
        f"""
### 👤 {st.session_state.user["name"]}

**User ID:** {st.session_state.user["userid"]}

**Department:** {st.session_state.user["department"]}

**Role:** {st.session_state.user["role"]}
"""
    )

    st.markdown("---")

    # ===============================
    # Navigation
    # ===============================

    if st.button(
        "📦 Dashboard",
        use_container_width=True,
        type="primary"
    ):
        st.rerun()

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

    if st.session_state.user["userid"] == "ADMIN001":

        if st.button(
            "⚙️ Admin Panel",
            use_container_width=True
        ):
            st.switch_page("pages/Admin.py")

    st.markdown("---")

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.cache_data.clear()

        st.session_state.logged_in = False
        st.session_state.user = {}

        st.switch_page("app_4.py")
    # ======================================================
# DASHBOARD HEADER
# ======================================================

st.markdown(
    f"""
    <div style="
    background:linear-gradient(90deg,#005BAC,#0077D9);
    padding:30px;
    border-radius:20px;
    color:white;
    margin-bottom:25px;
    ">
    <h1>🏭 Ralson PPC Stock Management</h1>
    <h3>Welcome, {st.session_state.user["name"]}</h3>
    <p>
    <b>Department:</b> {st.session_state.user["department"]}
    </p>
    </div>
    """,
    unsafe_allow_html=True
)
# ======================================================
# DASHBOARD STATISTICS
# ======================================================

total_materials = len(master_df)

total_stock = pd.to_numeric(
    master_df[STOCK_COLUMN],
    errors="coerce"
).fillna(0).sum()

total_updates = len(logs_df)

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "📦 Materials",
        f"{total_materials:,}"
    )

with col2:

    st.metric(
        "🏭 Total Stock",
        f"{int(total_stock):,}"
    )

with col3:

    st.metric(
        "📜 Total Updates",
        f"{total_updates:,}"
    )

st.divider()
# ======================================================
# MATERIAL SEARCH
# ======================================================

st.subheader("🔍 Material Search")

material_list = sorted(
    master_df[MATERIAL_COLUMN]
    .fillna("")
    .astype(str)
    .tolist()
)

selected_material = st.selectbox(
    "Select Material",
    material_list
)

selected_row = master_df[
    master_df[MATERIAL_COLUMN]
    ==
    selected_material
].iloc[0]

material_code = selected_row[CODE_COLUMN]

current_stock = pd.to_numeric(
    selected_row[STOCK_COLUMN],
    errors="coerce"
)

if pd.isna(current_stock):
    current_stock = 0

current_stock = int(current_stock)

trolley = selected_row.get(
    "Trolley No.",
    "-"
)

# ======================================================
# MATERIAL DETAILS
# ======================================================

c1, c2, c3 = st.columns(3)

with c1:

    st.info(f"""

### 🏷 Material Code

## {material_code}

""")

with c2:

    st.success(f"""

### 📦 Current Stock

## {current_stock}

""")

with c3:

    st.warning(f"""

### 🚚 Trolley No.

## {trolley}

""")

st.divider()

# ======================================================
# UPDATE STOCK
# ======================================================

st.subheader("📦 Update Stock")

new_stock = st.number_input(

    "Updated Stock",

    min_value=0,

    value=current_stock,

    step=1

)

# ======================================================
# SUCCESS CARD
# ======================================================

if "update_success" not in st.session_state:

    st.session_state.update_success = False

if st.session_state.update_success:

    data = st.session_state.success_data

    st.markdown(f"""
<div style="
background:#0F5132;
padding:20px;
border-radius:15px;
color:white;
border-left:8px solid #22C55E;
margin-bottom:25px;
">

<h2>✅ Stock Updated Successfully</h2>

<hr>

<b>Material :</b> {data['material']}<br><br>

<b>Code :</b> {data['code']}<br><br>

<b>Previous Stock :</b> {data['old_stock']}<br><br>

<b>Updated Stock :</b> {data['new_stock']}<br><br>

<b>Updated By :</b> {data['user']}<br><br>

<b>Department :</b> {data['department']}<br><br>

<b>Date & Time :</b> {data['datetime']}

</div>
""",
    unsafe_allow_html=True
)
    # ======================================================
# UPDATE BUTTON
# ======================================================

if st.button(
    "✅ Update Stock",
    use_container_width=True
):

    try:

        # Find selected row
        row_index = master_df[
            master_df[MATERIAL_COLUMN]
            ==
            selected_material
        ].index[0]

        old_stock = pd.to_numeric(
            master_df.loc[row_index, STOCK_COLUMN],
            errors="coerce"
        )
        if pd.isna(old_stock):
            old_stock = 0
            old_stock = int(old_stock)

        # -----------------------------------
        # Update dataframe
        # -----------------------------------

        master_df.loc[
            row_index,
            STOCK_COLUMN
        ] = int(new_stock)

        # -----------------------------------
        # Rewrite Master Sheet
        # -----------------------------------

        master_ws.update(
            [
                master_df.columns.tolist()
            ]
            +
            master_df.values.tolist(),
            "A1"
        )

        # -----------------------------------
        # Save Log
        # -----------------------------------

        log = [

            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

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

        # -----------------------------------
        # Clear cache
        # -----------------------------------

        load_master.clear()

        load_logs.clear()

        # -----------------------------------
        # Success Card Data
        # -----------------------------------

        st.session_state.success_data = {

            "material": selected_material,

            "code": material_code,

            "old_stock": old_stock,

            "new_stock": int(new_stock),

            "user": st.session_state.user["name"],

            "department": st.session_state.user["department"],

            "datetime": datetime.now().strftime(
                "%d-%m-%Y %H:%M:%S"
            )

        }

        st.session_state.update_success = True

        st.balloons()

        st.rerun()

    except Exception as e:

        st.error(
            f"❌ {e}"
        )
    # ======================================================
# ADMIN DASHBOARD
# ======================================================

if st.session_state.user["userid"] == "ADMIN001":

    st.divider()

    st.subheader("🕒 Recent Activity")

    logs_df = load_logs()

    if not logs_df.empty:

        if "datetime" in logs_df.columns:

            logs_df = logs_df.sort_values(
                "datetime",
                ascending=False
            )

        st.dataframe(
            logs_df.head(20),
            use_container_width=True,
            hide_index=True,
            height=400
        )

    else:

        st.info("No recent activity available.")

# ======================================================
# LOW STOCK ALERT
# ======================================================

st.divider()

st.subheader("⚠️ Low Stock Materials")

stock_data = master_df.copy()

stock_data[STOCK_COLUMN] = pd.to_numeric(
    stock_data[STOCK_COLUMN],
    errors="coerce"
).fillna(0)

low_stock = stock_data[
    stock_data[STOCK_COLUMN] <= 10
]

if low_stock.empty:

    st.success("✅ No Low Stock Materials")

else:

    st.warning(
        f"{len(low_stock)} material(s) have stock less than or equal to 10."
    )

    st.dataframe(
        low_stock[
            [
                CODE_COLUMN,
                MATERIAL_COLUMN,
                STOCK_COLUMN,
                "Trolley No."
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

# ======================================================
# DASHBOARD FOOTER
# ======================================================

st.divider()

st.caption(
    f"""
Ralson PPC Stock Management System

Logged in as:
{st.session_state.user["name"]}

Department:
{st.session_state.user["department"]}
"""
)
