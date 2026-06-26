import streamlit as st
from datetime import datetime
import os
from gspread_dataframe import get_as_dataframe
from google_sheets import client
from config import SHEET_ID
import pandas as pd


st.set_page_config(
    page_title="Dashboard",
    page_icon="📦",
    layout="wide"
)


sheet = client.open_by_key(SHEET_ID)

st.write(
    sheet.title
)
st.markdown("""
<style>
[data-testid="stSidebarNav"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)


if "logged_in" not in st.session_state:
    st.switch_page("app_4.py")

if not st.session_state.logged_in:
    st.switch_page("app_4.py")

if "user" not in st.session_state:
    st.switch_page("app_4.py")

sheet = client.open_by_key(SHEET_ID)

stock_ws = sheet.worksheet("Master")

records = stock_ws.get_all_records()

df = pd.DataFrame(records)

with st.sidebar:

    st.markdown("## 🏭 Ralson")

    st.markdown(
    f"""
    👤 **{st.session_state.user['name']}**

    🏢 {st.session_state.user['department']}
    """
)

    st.divider()

    if st.button("📦 Dashboard", use_container_width=True):
        st.switch_page("pages/Dashboard.py")
    if st.session_state.user["userid"] == "ADMIN001":
        if st.button("⚙️ Admin", use_container_width=True):
            st.switch_page("pages/Admin.py")

    if st.button("📜 History", use_container_width=True):
        st.switch_page("pages/History.py")

    if st.button("👤 Profile", use_container_width=True):
        st.switch_page("pages/Profile.py")
    st.divider()
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user = {}
        st.switch_page("app_4.py")
# ==========================
# LOGIN CHECK
# ==========================

if not st.session_state.get("logged_in", False):
    st.switch_page("app_4.py")

# ==========================
# PAGE CONFIG
# ==========================


# ==========================
# CREATE LOG FILE IF MISSING
# ==========================
config_df = get_as_dataframe(
    sheet.worksheet("Config")
).dropna(how="all")

MATERIAL_COLUMN = "Material description"
CODE_COLUMN = "Code"
STOCK_COLUMN = "13 GT"

# ==========================
# HEADER CARD
# ==========================

st.markdown(
    f"""
    <div style="
    background:#005BAC;
    padding:20px;
    border-radius:15px;
    color:white;
    text-align:center;
    margin-bottom:20px;
    ">
        <h2>🏭 Ralson Stock Management</h2>
        <p>
        Logged in as:
        {st.session_state.user['name']}
        ({st.session_state.get('user', {}).get('department', '')})
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# ==========================
# LOAD MASTER FILE
# ==========================

sheet = client.open_by_key(SHEET_ID)

master_ws = sheet.worksheet("Master")

df = pd.DataFrame(
    master_ws.get_all_records()
)
users_ws = sheet.worksheet("users")

users_df = pd.DataFrame(
    users_ws.get_all_records()
)

logs_ws = sheet.worksheet("logs")

logs_df = pd.DataFrame(
    logs_ws.get_all_records()
)

config_ws = sheet.worksheet("Config")

config_df = pd.DataFrame(
    config_ws.get_all_records()
)
st.write("Columns Found:")
st.write(df.columns.tolist())
MATERIAL_COLUMN = "Material Description"
CODE_COLUMN = "Code"
STOCK_COLUMN = "13 GT"
df.columns = (
    df.columns
    .astype(str)
    .str.strip()
)


selected = st.selectbox(
    "🔍 Search and Select Material",
    df[MATERIAL_COLUMN]
    .astype(str)
    .tolist(),
    key="material_search"
)

# ==========================
# SHOW DETAILS
# ==========================

if selected:

    row = df[
        df[MATERIAL_COLUMN]
        ==
        selected
    ].iloc[0]

    code = row[CODE_COLUMN]
current_stock = row[STOCK_COLUMN]
current_stock = pd.to_numeric(
	current_stock,
	errors="coerce"
)
new_stock = st.number_input(
    "Enter Stock",
    value=current_stock,
    min_value=0
)
if pd.isna(current_stock):
	current_stock = 0
	col1, col2 = st.columns(2)
with col1:
	st.markdown(
            f"""
            <div style="
            background:#112B45;
            color:white;;
            padding:20px;
            border-radius:15px;
            text-align:center;
            box-shadow:0px 2px 8px rgba(0,0,0,0.1);
            ">
                <h4>Material Code</h4>
                <h2>{code}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )
with col2:
	st.markdown(
		f"""
		<div style="
		background:#0F172A;
		border:1px solid #334155;
		padding:20px;
		border-radius:15px;
		text-align:center;
		">
        <h4 style="color:#22C55E;">
        Current Stock
        </h4>
        <h2 style="color:white;">
        {current_stock}
        </h2>
        </div>
        """,
		unsafe_allow_html=True
	)
	st.write("")

    # ==========================
    # STOCK ENTRY
    # ========================= 
    
    new_stock = st.number_input("📦 Enter Updated Stock",
		min_value=0,
		value=int(current_stock),
		step=1,
		key="stock_input"
	)

    # ==========================
    # UPDATE BUTTON
    # ==========================

if st.button(
    "✅ Update Stock",
    use_container_width=True
):

    idx = df[
        df[CODE_COLUMN] == code
    ].index[0]

    old_stock = df.loc[
        idx,
        STOCK_COLUMN
    ]

    if pd.isna(old_stock):
        old_stock = 0

    df.loc[
        idx,
        STOCK_COLUMN
    ] = new_stock

    from gspread_dataframe import set_with_dataframe

    set_with_dataframe(
        master_ws,
        df
    )

    logs_df = pd.DataFrame(
        logs_ws.get_all_records()
    )

    new_log = pd.DataFrame([
        {
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "userid": st.session_state.user["userid"],
            "name": st.session_state.user["name"],
            "department": st.session_state.user["department"],
            "code": code,
            "material": selected,
            "old_stock": old_stock,
            "new_stock": new_stock
        }
    ])

    logs_df = pd.concat(
        [logs_df, new_log],
        ignore_index=True
    )

    set_with_dataframe(
        logs_ws,
        logs_df
    )

    st.success("Stock Updated Successfully")

    st.rerun() 
    
    st.markdown(f"""
                    <div style="
                    background:#1E293B;
                    padding:20px;
                    border-radius:15px;
                    border-left:6px solid #22C55E;
                    margin-top:20px;
                    color:white;
                    ">

                    <h3 style="color:#22C55E;">
                    ✅ Stock Updated Successfully
                    </h3>

                    <hr style="border:1px solid #334155;">

                    <p><b>Material:</b> {selected}</p>
                    <p><b>Code:</b> {code}</p>
                    <p><b>Previous Stock:</b> {old_stock}</p>
                    <p><b>Updated Stock:</b> {new_stock}</p>
                    <p><b>Updated By:</b> {st.session_state.user['name']}</p>
                    <p><b>Department:</b> {st.session_state.user['department']}</p>
                    <p><b>Date & Time:</b> {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}</p>

                    </div>
                    """,
                    unsafe_allow_html=True
                )
if (
    st.session_state.user["userid"]
    ==
    "ADMIN001"
):

    st.divider()

    st.subheader(
        "🕒 Recent Activity"
    )

    logs_df = pd.DataFrame(
        logs_ws.get_all_records()
    )

    st.dataframe(
        logs_df.tail(20),
        use_container_width=True
    )
