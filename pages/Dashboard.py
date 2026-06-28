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
    STOCK_COLUMN,
    TROLLEY_COLUMN
)

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Dashboard",
    page_icon="🏭",
    layout="wide"
)

# ==========================================================
# HIDE STREAMLIT PAGE NAVIGATION
# ==========================================================

st.markdown("""
<style>

[data-testid="stSidebarNav"]{
    display:none;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# LOGIN CHECK
# ==========================================================

if not st.session_state.get("logged_in", False):
    st.switch_page("app_4.py")

if "user" not in st.session_state:
    st.switch_page("app_4.py")

# ==========================================================
# GOOGLE SHEETS CONNECTION
# ==========================================================

sheet = client.open_by_key(SHEET_ID)

master_ws = sheet.worksheet(MASTER_SHEET)
users_ws = sheet.worksheet(USERS_SHEET)
logs_ws = sheet.worksheet(LOGS_SHEET)

# ==========================================================
# CACHE FUNCTIONS
# ==========================================================

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


# ==========================================================
# LOAD DATA
# ==========================================================

master_df = load_master()

users_df = load_users()

logs_df = load_logs()

# ==========================================================
# INITIAL SESSION VARIABLES
# ==========================================================

if "update_success" not in st.session_state:
    st.session_state.update_success = False

if "success_data" not in st.session_state:
    st.session_state.success_data = {}
# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.markdown("# 🏭 Ralson")

    st.markdown("---")

    st.markdown(
        f"""
### 👤 {st.session_state.user["name"]}

**User ID:** {st.session_state.user["userid"]}

**Department:** {st.session_state.user["department"]}
""")

    st.markdown("---")

    # ======================================================
    # NAVIGATION
    # ======================================================

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

    if (
        st.session_state.user["userid"]
        == "ADMIN001"
    ):

        if st.button(
            "⚙️ Admin Panel",
            use_container_width=True
        ):
            st.switch_page(
                "pages/Admin.py"
            )

    st.markdown("---")

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        # Clear cache
        st.cache_data.clear()

        # Clear session
        st.session_state.logged_in = False
        st.session_state.user = {}
        st.session_state.update_success = False
        st.session_state.success_data = {}

        st.switch_page("app_4.py")
    # ==========================================================
# DASHBOARD HEADER
# ==========================================================

st.markdown(
    f"""
<div style="
background:linear-gradient(90deg,#005BAC,#0077D9);
padding:30px;
border-radius:18px;
color:white;
margin-bottom:20px;
box-shadow:0px 4px 15px rgba(0,0,0,0.2);
">

<h1 style="margin-bottom:5px;">
🏭 Ralson PPC Stock Management
</h1>

<h3 style="margin-top:10px;">
Welcome, {st.session_state.user["name"]}
</h3>

<p style="font-size:18px;">
<b>Department:</b> {st.session_state.user["department"]}
</p>

</div>
""",
    unsafe_allow_html=True
)

# ==========================================================
# DASHBOARD STATISTICS
# ==========================================================

total_materials = len(master_df)

total_stock = pd.to_numeric(
    master_df[STOCK_COLUMN],
    errors="coerce"
).fillna(0).sum()

total_updates = len(logs_df)

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        label="📦 Total Materials",
        value=f"{total_materials:,}"
    )

with col2:

    st.metric(
        label="🏭 Total Stock",
        value=f"{int(total_stock):,}"
    )

with col3:

    st.metric(
        label="📜 Total Updates",
        value=f"{total_updates:,}"
    )

st.divider()

# ==========================================================
# MATERIAL SEARCH
# ==========================================================

st.subheader("🔍 Search Material")

material_list = sorted(

    master_df[MATERIAL_COLUMN]
    .fillna("")
    .astype(str)
    .tolist()

)
if "last_material" not in st.session_state:
    st.session_state.last_material = ""
selected_material = st.selectbox(

    "Material Description",

    material_list,

    index=0

)
# Hide success card when material changes
if st.session_state.last_material != selected_material:

    st.session_state.update_success = False
    st.session_state.success_data = {}

    st.session_state.last_material = selected_material

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

current_trolley = selected_row.get(
    TROLLEY_COLUMN,
    ""
)

if pd.isna(current_trolley):
    current_trolley = ""

st.divider()
# ==========================================================
# MATERIAL DETAILS
# ==========================================================

card1, card2, card3 = st.columns(3)

with card1:

    st.markdown(f"""
<div style="
background:#0F172A;
padding:20px;
border-radius:15px;
text-align:center;
border:1px solid #334155;
">

<h4 style="color:#60A5FA;">🏷 Material Code</h4>

<h2 style="color:white;">{material_code}</h2>

</div>
""", unsafe_allow_html=True)

with card2:

    st.markdown(f"""
<div style="
background:#0F172A;
padding:20px;
border-radius:15px;
text-align:center;
border:1px solid #334155;
">

<h4 style="color:#22C55E;">📦 Current Stock</h4>

<h2 style="color:white;">{current_stock}</h2>

</div>
""", unsafe_allow_html=True)

with card3:

    st.markdown(f"""
<div style="
background:#0F172A;
padding:20px;
border-radius:15px;
text-align:center;
border:1px solid #334155;
">

<h4 style="color:#FACC15;">🚚 Trolley No.</h4>

<h2 style="color:white;">{current_trolley}</h2>

</div>
""", unsafe_allow_html=True)

st.write("")

# ==========================================================
# UPDATE SECTION
# ==========================================================

st.subheader("📦 Update Stock")

left, right = st.columns(2)

with left:

    new_stock = st.number_input(
        "Updated Stock",
        min_value=0,
        value=current_stock,
        step=1
    )

with right:

    trolley_no = st.text_input(
        "Trolley Number",
        value=str(current_trolley)
    )

st.write("")

# ==========================================================
# UPDATE BUTTON
# ==========================================================

update_btn = st.button(
    "✅ Update Stock",
    use_container_width=True,
    type="primary"
)

st.write("")

# ==========================================================
# SUCCESS CARD
# ==========================================================

if st.session_state.update_success:

    data = st.session_state.success_data

    st.markdown(f"""
<div style="
background:#14532D;
padding:25px;
border-radius:15px;
border-left:8px solid #22C55E;
color:white;
margin-top:10px;
margin-bottom:20px;
">

<h2>✅ Stock Updated Successfully</h2>

<hr>

<b>Material :</b> {data['material']}<br><br>

<b>Code :</b> {data['code']}<br><br>

<b>Previous Stock :</b> {data['old_stock']}<br><br>

<b>Updated Stock :</b> {data['new_stock']}<br><br>

<b>Trolley No :</b> {data.get('trolley', '-') }<br><br>

<b>Updated By :</b> {data['user']}<br><br>

<b>Department :</b> {data['department']}<br><br>

<b>Date & Time :</b> {data['datetime']}

</div>
""", unsafe_allow_html=True)
# ==========================================================
# UPDATE STOCK
# ==========================================================

if update_btn:

    try:

        # --------------------------------------------
        # Find Selected Row
        # --------------------------------------------

        row_index = master_df[
            master_df[MATERIAL_COLUMN] == selected_material
        ].index[0]

        old_stock = pd.to_numeric(
            master_df.loc[row_index, STOCK_COLUMN],
            errors="coerce"
        )

        if pd.isna(old_stock):
            old_stock = 0

        old_stock = int(old_stock)

        # --------------------------------------------
        # Update DataFrame
        # --------------------------------------------

        master_df.loc[
            row_index,
            STOCK_COLUMN
        ] = int(new_stock)

        master_df.loc[
            row_index,
            TROLLEY_COLUMN
        ] = trolley_no

        # --------------------------------------------
        # Update Google Sheet
        # --------------------------------------------

        master_ws.update(
            "A1",
            [
                master_df.columns.tolist()
            ] + master_df.values.tolist()
        )

        # --------------------------------------------
        # Save Log
        # --------------------------------------------

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

        # --------------------------------------------
        # Clear Cache
        # --------------------------------------------

        load_master.clear()
        load_logs.clear()

        # --------------------------------------------
        # Success Card Data
        # --------------------------------------------

        st.session_state.success_data = {

            "material": selected_material,

            "code": material_code,

            "old_stock": old_stock,

            "new_stock": int(new_stock),

            "trolley": trolley_no,

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
    # ==========================================================
# ADMIN RECENT ACTIVITY
# ==========================================================

if st.session_state.user["userid"] == "ADMIN001":

    st.divider()

    st.subheader("🕒 Recent Activity")

    latest_logs = load_logs()

    if not latest_logs.empty:

        if "datetime" in latest_logs.columns:

            latest_logs = latest_logs.sort_values(
                by="datetime",
                ascending=False
            )

        st.dataframe(
            latest_logs.head(20),
            use_container_width=True,
            hide_index=True,
            height=450
        )

    else:

        st.info("No activity available.")

# ==========================================================
# LOW STOCK ALERT
# ==========================================================

st.divider()

st.subheader("⚠ Low Stock Alert")

low_stock_df = master_df.copy()

low_stock_df[STOCK_COLUMN] = pd.to_numeric(
    low_stock_df[STOCK_COLUMN],
    errors="coerce"
).fillna(0)

low_stock_df = low_stock_df[
    low_stock_df[STOCK_COLUMN] <= 10
]

if low_stock_df.empty:

    st.success("✅ No Low Stock Materials")

else:

    st.warning(
        f"{len(low_stock_df)} material(s) have stock less than or equal to 10."
    )

    st.dataframe(

        low_stock_df[
            [
                CODE_COLUMN,
                MATERIAL_COLUMN,
                STOCK_COLUMN,
                TROLLEY_COLUMN
            ]
        ],

        use_container_width=True,
        hide_index=True

    )

# ==========================================================
# DASHBOARD SUMMARY
# ==========================================================

st.divider()

c1, c2, c3 = st.columns(3)

with c1:

    st.metric(
        "Materials",
        len(master_df)
    )

with c2:

    st.metric(
        "Users",
        len(users_df)
    )

with c3:

    st.metric(
        "Updates",
        len(load_logs())
    )

# ==========================================================
# FOOTER
# ==========================================================

st.markdown("---")

st.caption(
    f"""
🏭 **Ralson PPC Stock Management System**

Logged in as **{st.session_state.user["name"]}**

Department: **{st.session_state.user["department"]}**
"""
)
