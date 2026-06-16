import streamlit as st
import pandas as pd
from datetime import datetime
import os

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

MASTER_FILE = "master.xlsx"
LOG_FILE = "logs.xlsx"

df = pd.read_excel(MASTER_FILE)

try:
    logs_df = pd.read_excel(LOG_FILE)
except:
    logs_df = pd.DataFrame()

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

    if st.button("📜 History", use_container_width=True):
        st.switch_page("pages/History.py")

    if st.button("👤 Profile", use_container_width=True):
        st.switch_page("pages/Profile.py")
    if st.session_state.user["userid"] == "ADMIN001":
        if st.button(
         "⚙️ Admin",
           use_container_width=True
        ):
            st.switch_page(
                "pages/Admin.py"
                )
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
# LOGIN CHECK
# ==========================

if not st.session_state.get("logged_in", False):
    st.switch_page("app_4.py")

# ==========================
# PAGE CONFIG
# ==========================

st.set_page_config(
    page_title="Dashboard",
    page_icon="📦",
    layout="wide"
)

# ==========================
# CREATE LOG FILE IF MISSING
# ==========================

if not os.path.exists(LOG_FILE):

    pd.DataFrame(
        columns=[
            "datetime",
            "userid",
            "name",
            "department",
            "code",
            "material",
            "old_stock",
            "new_stock"
        ]
    ).to_excel(
        LOG_FILE,
        index=False
    )

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

df = pd.read_excel(MASTER_FILE)
users_df = pd.read_excel(
    "users.xlsx",
    dtype=str
).fillna("")

logs_df = pd.read_excel(
    LOG_FILE
)

config = pd.read_excel("config(1).xlsx")

MASTER_FILE = str(
    config.loc[0, "excel_file"]
).strip()

STOCK_COLUMN = str(
    config.loc[0, "stock_column"]
).strip()

df = pd.read_excel(MASTER_FILE)
df.columns = (
    df.columns
    .astype(str)
    .str.strip()
)

# ==========================
# SEARCH MATERIAL
# ==========================


selected = st.selectbox(
    "🔍 Search and Select Material",
    df["Material Description"]
    .astype(str)
    .tolist(),
    key="material_search"
)

# ==========================
# SHOW DETAILS
# ==========================

if selected:

    row = df[
        df["Material Description"]
        ==
        selected
    ].iloc[0]

    code = row["Code"]

    current_stock = row[STOCK_COLUMN]

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
    # ==========================

    new_stock = st.number_input(
        "📦 Enter Updated Stock",
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
            df["Code"]
            ==
            code
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

        df.to_excel(
            MASTER_FILE,
            index=False
        )

        logs = pd.read_excel(
            LOG_FILE
        )

        logs.loc[
            len(logs)
        ] = [

            datetime.now(),

            st.session_state.user[
                "userid"
            ],

            st.session_state.user[
                "name"
            ],

            st.session_state.user[
                "department"
            ],

            code,

            selected,

            old_stock,

            new_stock
        ]

        logs.to_excel(
            LOG_FILE,
            index=False
        )

        # ==========================
        # SUCCESS CARD
        # ==========================

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
