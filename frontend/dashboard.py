import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import time
import os
import requests
from datetime import datetime

from login import check_login
def neon_bar(df, y, title):

    colors = [
        "#7c3aed",
        "#6366f1",
        "#3b82f6",
        "#06b6d4",
        "#22d3ee",
        "#38bdf8",
        "#818cf8",
        "#a78bfa",
    ]

    fig = px.bar(
        df,
        x="strategy",
        y=y,
        title=title,
    )

    fig.update_traces(
        marker_color=colors,
        marker_line_width=0,
    )

    fig.update_layout(

        paper_bgcolor="#0f172a",
        plot_bgcolor="#0f172a",

        font=dict(color="white"),

        xaxis=dict(
            showgrid=True,
            gridcolor="#1f2937"
        ),

        yaxis=dict(
            showgrid=True,
            gridcolor="#1f2937"
        ),

        title_font_size=16,

        margin=dict(l=10, r=10, t=40, b=10),

    )

    return fig

def fancy_bar(df, y):

    fig = px.bar(
        df,
        x="strategy",
        y=y,
        color="strategy",
        template="plotly_dark"
    )

    fig.update_traces(
        marker=dict(
            line=dict(width=0),
        ),
        opacity=0.9
    )

    fig.update_layout(

        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(color="white"),

        title_font_size=18,

        margin=dict(l=10, r=10, t=40, b=10),

        bargap=0.3,

    )

    return fig

FILE = "logs/results.csv"

DEFAULT_COLUMNS = [
    "strategy",
    "reward",
    "cost",
    "latency",
    "energy",
    "sla",
    "carbon",
    "servers",
    "resources",
    "memory",
    "max_servers",
    "cloud_resource_capacity",
    "cloud_memory_capacity",
    "users",
]


def _get_api_url():

    if "API_URL" in st.secrets:
        return str(st.secrets["API_URL"]).rstrip("/")

    api_url = os.getenv("API_URL", "").strip()
    if not api_url:
        return None

    return api_url.rstrip("/")


def _get_api_key():

    if "API_KEY" in st.secrets:
        return str(st.secrets["API_KEY"])

    return os.getenv("API_KEY", "")


def _with_required_columns(df: pd.DataFrame) -> pd.DataFrame:

    for col in DEFAULT_COLUMNS:
        if col not in df.columns:
            df[col] = 0 if col != "strategy" else "UNKNOWN"

    return df


def _run_local_simulation() -> pd.DataFrame:

    try:
        from main import run_all
        results = run_all()
        return _with_required_columns(pd.DataFrame(results))
    except Exception:
        return pd.DataFrame(columns=DEFAULT_COLUMNS)


@st.cache_data(ttl=5, show_spinner=False)
def load_results():

    api_url = _get_api_url()
    api_key = _get_api_key()

    headers = {}
    if api_key:
        headers["x-api-key"] = api_key

    if api_url:
        try:
            response = requests.get(f"{api_url}/simulate", headers=headers, timeout=6)
            response.raise_for_status()
            payload = response.json()
            api_results = payload.get("results", [])

            df = pd.DataFrame(api_results)
            if not df.empty:
                return _with_required_columns(df)
        except Exception:
            pass

    # Free/no-backend mode: compute simulation inside Streamlit app.
    df_local = _run_local_simulation()
    if not df_local.empty:
        return df_local

    try:
        df = pd.read_csv(FILE)
        return _with_required_columns(df)
    except Exception:
        return pd.DataFrame(columns=DEFAULT_COLUMNS)

st.set_page_config(
    page_title="AI Cloud Optimizer",
    layout="wide"
)

if not check_login():
    st.stop()

df = load_results()

if "detail" not in st.session_state:
    st.session_state.detail = None


def show_no_data_message():

    st.warning("No data is available yet.")
    st.info("Set API_URL for backend mode, or use standalone mode to run simulations directly in Streamlit.")


# ---------- CSS ----------

st.markdown("""
<style>

/* ---------- background ---------- */

.stApp {

    background:
        radial-gradient(circle at 15% 20%, rgba(14,165,233,0.15) 0%, transparent 45%),
        radial-gradient(circle at 85% 25%, rgba(124,58,237,0.15) 0%, transparent 45%),
        radial-gradient(circle at 50% 85%, rgba(6,182,212,0.12) 0%, transparent 45%),
        #020617;

}
/* ---------- sidebar ---------- */

section[data-testid="stSidebar"] {

    background: linear-gradient(
        180deg,
        #101631,
        #0f1836
    );

    border-right:1px solid rgba(255,255,255,0.06);
    padding:12px;
}


/* ---------- sidebar text ---------- */

.sidebar-title {
    font-size:20px;
    font-weight:700;
    color:#f8fafc;
    margin-bottom:18px;
}

.sidebar-section {
    color:#e879f9;
    font-size:12px;
    margin-top:12px;
    margin-bottom:8px;
    font-weight:700;
    letter-spacing:0.06em;
    text-transform:uppercase;
}


/* ---------- sidebar nav (CRM style) ---------- */

section[data-testid="stSidebar"] div[data-testid="stRadio"] {
    width: 100%;
}

section[data-testid="stSidebar"] div[data-testid="stRadio"] > div {
    gap: 0;
}

section[data-testid="stSidebar"] label[data-baseweb="radio"] {
    width: 100%;
    margin: 0 0 6px 0;
    border-radius: 0;
    min-height: 42px;
    padding: 9px 12px;
    background: transparent;
    border: 1px solid transparent;
    color: #c084fc;
    position: relative;
    transition: background 0.2s ease, color 0.2s ease;
}

section[data-testid="stSidebar"] label[data-baseweb="radio"] > div:first-child {
    display: none;
}

section[data-testid="stSidebar"] label[data-baseweb="radio"] > div:last-child {
    width: 100%;
}

section[data-testid="stSidebar"] label[data-baseweb="radio"] p {
    font-size: 16px;
    font-weight: 600;
    margin: 0;
    color: #c084fc;
}

section[data-testid="stSidebar"] label[data-baseweb="radio"]:hover {
    background: rgba(168, 85, 247, 0.18);
    color: #e9d5ff;
}

section[data-testid="stSidebar"] label[data-baseweb="radio"]:hover p {
    color: #e9d5ff;
}

section[data-testid="stSidebar"] label[data-baseweb="radio"]:has(input:checked) {
    background: linear-gradient(90deg, rgba(168,85,247,0.55), rgba(168,85,247,0.35));
    color: #f5d0fe;
    box-shadow: 0 0 16px rgba(168,85,247,0.35);
}

section[data-testid="stSidebar"] label[data-baseweb="radio"]:has(input:checked) p {
    color: #f5d0fe;
}

section[data-testid="stSidebar"] label[data-baseweb="radio"]:has(input:checked)::before {
    content: "";
    position: absolute;
    left: -12px;
    top: 50%;
    transform: translateY(-50%);
    width: 0;
    height: 0;
    border-top: 10px solid transparent;
    border-bottom: 10px solid transparent;
    border-left: 10px solid #a855f7;
}

/* Hide empty radio label text line rendered by Streamlit */
section[data-testid="stSidebar"] div[data-testid="stRadio"] > label {
    display: none;
}

/* Remove top/bottom spacing around nav block */
section[data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] {
    gap: 0;
}


/* ---------- NAVBAR ---------- */

.navbar {

    font-size:34px;
    font-weight:800;
    text-align:center;
    padding:12px;
    margin-bottom:15px;

    border-radius:12px;

    background:linear-gradient(
        90deg,
        #06b6d4,
        #3b82f6,
        #7c3aed
    );

    color:white;

    box-shadow:
        0 0 15px #0ea5e9,
        0 0 30px #7c3aed inset;

}
/* ===== ACTIVE SIDEBAR ITEM ===== */

.nav-item {

    padding: 10px;

    border-radius: 8px;

    margin-bottom: 6px;

    color: #c084fc;

    font-weight: 600;

}


.nav-active {

    background: linear-gradient(
        90deg,
        #7c3aed,
        #a855f7
    );

    color: white;

    box-shadow:
        0 0 10px #a855f7;

}

/* ---------- GLASS CARD ---------- */

.card {

    background: rgba(15, 23, 42, 0.85);

    border-radius: 18px;

    padding: 22px;

    border: 1px solid rgba(56,189,248,0.6);

    backdrop-filter: blur(12px);

    box-shadow:
        0 0 8px #0ea5e9,
        0 0 20px rgba(14,165,233,0.5),
        inset 0 0 10px rgba(56,189,248,0.3);

    transition: 0.25s ease;
}


/* hover glow */

.card:hover {

    box-shadow:
        0 0 12px #22d3ee,
        0 0 35px rgba(34,211,238,0.6),
        inset 0 0 12px rgba(34,211,238,0.4);

    transform: translateY(-3px);
}



.card::before {

    content: "";

    display: block;

    height: 3px;

    border-radius: 10px;

    background: linear-gradient(
        90deg,
        #22d3ee,
        #6366f1,
        #a855f7
    );

    margin-bottom: 10px;

}
            .glass-card {

    height: 150px;

    border-radius: 16px;

    padding: 14px;

    background: rgba(15,23,42,0.85);

    border: 1px solid rgba(56,189,248,0.7);

    backdrop-filter: blur(12px);

    box-shadow:
        0 0 10px #0ea5e9,
        inset 0 0 12px rgba(56,189,248,0.3);

    transition: 0.25s;
}

.glass-card:hover {

    transform: translateY(-5px);

    box-shadow:
        0 0 20px #22d3ee,
        0 0 40px rgba(34,211,238,0.5);

}

.card-title {

    font-size:14px;
    color:#94a3b8;
}

.card-strategy {

    font-size:28px;
    font-weight:700;
    color:white;
    margin-top:4px;
}

.card-value {

    font-size:14px;
    margin-top:6px;
    font-weight:600;
}

/* ---------- DATAFRAME ---------- */

[data-testid="stDataFrame"] {

    background:#020617;

    border-radius:12px;

    border:1px solid #0ea5e9;
}


/* ---------- TITLES ---------- */

h1, h2, h3 {
    color:#38bdf8;
}


/* ========================= */
/* FIX TABS STYLE */
/* ========================= */

/* remove glow block */

[data-baseweb="tab-highlight"] {
    display:none !important;
}


/* tab container line */

.stTabs [role="tablist"] {

    border-bottom:2px solid #0ea5e9 !important;

    box-shadow:
        0 0 8px #0ea5e9,
        0 0 18px #0284c7 !important;
}


/* tab text */

.stTabs [role="tab"] {

    background:transparent !important;

    border-radius:0 !important;

    font-size:18px !important;

    font-weight:600 !important;

    color:#cbd5f5 !important;

    padding:10px 20px !important;
}


/* active tab */

.stTabs [aria-selected="true"] {

    color:#22d3ee !important;

    border-bottom:3px solid #22d3ee !important;
}


/* hover */

.stTabs [role="tab"]:hover {

    color:#38bdf8 !important;
}
/* ===== REMOVE BLOCK STYLE ===== */

[data-baseweb="tab-highlight"] {
    display: none !important;
}

.stTabs div[data-baseweb="tab-border"] {
    display: none !important;
}


/* ===== FULL WIDTH GLOW LINE ===== */

.stTabs [role="tablist"] {

    border-bottom: 2px solid #22d3ee !important;

    box-shadow:
        0 0 10px #22d3ee,
        0 0 25px #06b6d4 !important;

}


/* ===== TAB TEXT ===== */

.stTabs [role="tab"] {

    background: transparent !important;

    border-radius: 0 !important;

    font-size: 18px !important;

    padding: 10px 18px !important;

}


/* ===== ACTIVE TAB ===== */

.stTabs [aria-selected="true"] {

    color: #22d3ee !important;

    border-bottom: 3px solid #22d3ee !important;

}
            /* remove tab glow block */

[data-baseweb="tab-highlight"] {
    display: none !important;
}

.stTabs [data-baseweb="tab-panel"] {
    box-shadow: none !important;
    border: none !important;
    background: transparent !important;
}


/* full line glow only */

.stTabs [role="tablist"] {

    border-bottom: 2px solid #22d3ee !important;

    box-shadow:
        0 0 10px #22d3ee,
        0 0 25px #06b6d4 !important;

}
</style>
""", unsafe_allow_html=True)
# ---------- NAVBAR ----------

st.markdown(
    '<div class="navbar">☁ AI CLOUD OPTIMIZER CONSOLE</div>',
    unsafe_allow_html=True
)


# ---------- SIDEBAR ----------

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

page = st.session_state.page

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">Navigation</div>',
        unsafe_allow_html=True
    )

    nav_items = ["Dashboard", "Comparison", "Strategies", "Live Monitor"]
    selected_page = st.radio(
        "",
        nav_items,
        index=nav_items.index(st.session_state.page) if st.session_state.page in nav_items else 0,
        key="sidebar_page_selector",
    )
    st.session_state.page = selected_page

page = st.session_state.page
# ================= DASHBOARD =================
if "info" not in st.session_state:
    st.session_state.info = ""
if page == "Dashboard":

    if df.empty:
        show_no_data_message()
        st.stop()

    st.markdown('<div class="panel">', unsafe_allow_html=True)

    st.header("Overview")

    cloud_max_servers = int(df["max_servers"].iloc[0]) if not df.empty else 0
    cloud_resource_capacity = int(df["cloud_resource_capacity"].iloc[0]) if not df.empty else 0
    cloud_memory_capacity = int(df["cloud_memory_capacity"].iloc[0]) if not df.empty else 0

    if cloud_max_servers == 0 and not df.empty:
        cloud_max_servers = int(df["servers"].max())
    if cloud_resource_capacity == 0 and not df.empty:
        cloud_resource_capacity = int(df["resources"].max())
    if cloud_memory_capacity == 0 and not df.empty:
        cloud_memory_capacity = int(df["memory"].max())

    tc1, tc2, tc3 = st.columns(3)
    tc1.metric("Cloud Capacity Servers", cloud_max_servers)
    tc2.metric("Cloud Capacity Resources", cloud_resource_capacity)
    tc3.metric("Cloud Capacity Memory (GB)", cloud_memory_capacity)

    best_row = df.loc[df["reward"].idxmax()]
    worst_row = df.loc[df["reward"].idxmin()]

    low_cost = df.loc[df["cost"].idxmin()]
    low_latency = df.loc[df["latency"].idxmin()]
    low_energy = df.loc[df["energy"].idxmin()]
    low_carbon = df.loc[df["carbon"].idxmin()]
    best_sla = df.loc[df["sla"].idxmax()]
    max_users = df.loc[df["users"].idxmax()]

    def card(title, strategy, value):

        color = "#22c55e" if value >= 0 else "#ef4444"

        st.markdown(f"""
    <div class="glass-card">

    <div class="card-title">
    {title}
    </div>

    <div class="card-strategy">
    {strategy}
    </div>

    <div class="card-value" style="color:{color};">
    {value}
    </div>

    </div>
    """, unsafe_allow_html=True)
            
    # ---------- row 1 ----------

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        card(
            "Best Strategy",
            best_row["strategy"],
            round(best_row["reward"], 2)
        )

    with c2:
        card(
            "Worst Strategy",
            worst_row["strategy"],
            round(worst_row["reward"], 2)
        )

    with c3:
        card(
            "Lowest Cost",
            low_cost['strategy'],
            round(low_cost['cost'], 2)
        )

    with c4:
        card(
            "Lowest Latency",
            low_latency["strategy"],
            round(low_latency["latency"], 4)
        )


    c5, c6, c7, c8 = st.columns(4)

    with c5:
        card(
            "Lowest Energy",
            low_energy["strategy"],
            round(low_energy["energy"], 2)
        )

    with c6:
        card(
            "Lowest Carbon",
            low_carbon["strategy"],
            round(low_carbon["carbon"], 2)
        )

    with c7:
        card(
            "Best SLA",
            best_sla["strategy"],
            round(best_sla["sla"], 2)
        )

    with c8:
        card(
            "Max Users",
            max_users["strategy"],
            int(max_users["users"])
        )
    # ---------- RANK PANEL ----------

    st.markdown(
        '<div class="rank-panel">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="rank-title">Strategy Ranking</div>',
        unsafe_allow_html=True
    )
    rank_df = df.copy()

    # sort by reward
    rank_df = rank_df.sort_values(
        by="reward",
        ascending=False
    )

    rank_df["Rank"] = range(1, len(rank_df) + 1)

    rank_df = rank_df[
        [
            "Rank",
            "strategy",
            "reward",
            "cost",
            "latency",
            "energy",
            "carbon",
            "sla",
            "servers",
            "resources",
            "memory",
            "max_servers",
            "cloud_resource_capacity",
            "cloud_memory_capacity",
            "users",
        ]
    ]

    st.dataframe(
        rank_df,
        use_container_width=True,
        height=300
    )

# ---------- TABS ----------

    st.markdown('<div class="card">', unsafe_allow_html=True)

    tabs = st.tabs([
        "Reward",
        "Cost",
        "Latency",
        "Energy",
        "Servers",
        "Resources",
        "Memory",
        "Users",
        "Carbon",
        "SLA"
    ])

    # ---------- REWARD ----------
    with tabs[0]:

        df2 = df.copy()
        df2["reward_display"] = df2["reward"] * -1

        fig = neon_bar(df2, "reward_display", "Reward")
        fig.update_yaxes(title="reward (-ve values)")

        st.plotly_chart(fig, use_container_width=True)


    # ---------- COST ----------
    with tabs[1]:
        st.plotly_chart(
            neon_bar(df, "cost", "Cost"),
            use_container_width=True
        )


    # ---------- LATENCY ----------
    with tabs[2]:
        st.plotly_chart(
            neon_bar(df, "latency", "Latency"),
            use_container_width=True
        )


    # ---------- ENERGY ----------
    with tabs[3]:
        st.plotly_chart(
            neon_bar(df, "energy", "Energy"),
            use_container_width=True
        )


    # ---------- SERVERS ----------
    with tabs[4]:
        st.plotly_chart(
            neon_bar(df, "servers", "Servers"),
            use_container_width=True
        )


    # ---------- USERS ----------
    with tabs[5]:
        st.plotly_chart(
            neon_bar(df, "resources", "Resources"),
            use_container_width=True
        )


    # ---------- MEMORY ----------
    with tabs[6]:
        st.plotly_chart(
            neon_bar(df, "memory", "Memory (GB)"),
            use_container_width=True
        )


    # ---------- USERS ----------
    with tabs[7]:
        st.plotly_chart(
            neon_bar(df, "users", "Users"),
            use_container_width=True
        )


    # ---------- CARBON ----------
    with tabs[8]:
        st.plotly_chart(
            neon_bar(df, "carbon", "Carbon"),
            use_container_width=True
        )


    # ---------- SLA ----------
    with tabs[9]:
        st.plotly_chart(
            neon_bar(df, "sla", "SLA"),
            use_container_width=True
        )

    st.markdown('</div>', unsafe_allow_html=True)

# ================= COMPARISON =================

if page == "Comparison":

    if df.empty:
        show_no_data_message()
        st.stop()

    st.header("All Constraints Comparison")

    metrics = [
        "reward",
        "cost",
        "latency",
        "energy",
        "servers",
        "resources",
        "memory",
        "users",
        "carbon",
        "sla"
    ]

    for m in metrics:

        st.subheader(m)

        st.plotly_chart(
            neon_bar(df, m, m.upper()),
            use_container_width=True
        )


# ================= STRATEGIES =================

if page == "Strategies":

    if df.empty:
        show_no_data_message()
        st.stop()

    st.header("Strategy Analysis")

    choice = st.selectbox(
        "Select Strategy",
        df.strategy
    )

    row = df[df.strategy == choice].iloc[0]

    st.dataframe(row.to_frame())

    tabs = st.tabs(["Daily", "Monthly", "Scaling"])


    # ---------- DAILY ----------

    with tabs[0]:

        days = list(range(1, 20))
        users = np.random.randint(50, 300, 19)

        d = pd.DataFrame({
            "day": days,
            "users": users
        })

        fig = px.line(d, x="day", y="users")

        fig.update_layout(
            paper_bgcolor="#0f172a",
            plot_bgcolor="#0f172a",
            font=dict(color="white")
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # ---------- MONTHLY ----------

    with tabs[1]:

        months = list(range(1, 13))
        load = np.random.randint(100, 500, 12)

        d = pd.DataFrame({
            "month": months,
            "load": load
        })

        fig = px.bar(d, x="month", y="load")

        fig.update_layout(
            paper_bgcolor="#0f172a",
            plot_bgcolor="#0f172a",
            font=dict(color="white")
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # ---------- SCALING ----------

    with tabs[2]:

        steps = list(range(1, 20))
        servers = np.random.randint(1, 10, 19)

        d = pd.DataFrame({
            "step": steps,
            "servers": servers
        })

        fig = px.line(d, x="step", y="servers")

        fig.update_layout(
            paper_bgcolor="#0f172a",
            plot_bgcolor="#0f172a",
            font=dict(color="white")
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# ================= LIVE MONITOR =================

if page == "Live Monitor":

    st.header("Live Cloud Monitoring")

    df_live_source = load_results()

    if df_live_source.empty:
        st.warning("No live backend data found yet. Start the backend API service.")
        time.sleep(3)
        st.rerun()

    # All strategies now run on the same workload trace; users are shared.
    users = int(df_live_source["users"].iloc[0]) if not df_live_source.empty else 0
    cloud_max_servers = int(df_live_source["max_servers"].iloc[0]) if not df_live_source.empty else 0
    cloud_resource_capacity = int(df_live_source["cloud_resource_capacity"].iloc[0]) if not df_live_source.empty else 0
    cloud_memory_capacity = int(df_live_source["cloud_memory_capacity"].iloc[0]) if not df_live_source.empty else 0

    if cloud_max_servers == 0 and not df_live_source.empty:
        cloud_max_servers = int(df_live_source["servers"].max())
    if cloud_resource_capacity == 0 and not df_live_source.empty:
        cloud_resource_capacity = int(df_live_source["resources"].max())
    if cloud_memory_capacity == 0 and not df_live_source.empty:
        cloud_memory_capacity = int(df_live_source["memory"].max())

    strategy_options = df_live_source["strategy"].tolist()
    selected_strategy = st.selectbox("Select strategy for exact usage", strategy_options)
    selected_row = df_live_source[df_live_source["strategy"] == selected_strategy].iloc[0]

    servers = int(selected_row["servers"])
    resources = int(selected_row["resources"]) if "resources" in selected_row.index else 0
    memory = int(selected_row["memory"]) if "memory" in selected_row.index else 0
    latency = round(float(selected_row["latency"]), 3)

    if "history" not in st.session_state:
        st.session_state.history = []

    st.session_state.history.append(users)

    if len(st.session_state.history) > 20:
        st.session_state.history.pop(0)

    df_live = pd.DataFrame({
        "time": list(range(len(st.session_state.history))),
        "users": st.session_state.history
    })

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("Shared Users", users)
    c2.metric(f"Servers In Use ({selected_strategy})", f"{servers}/{cloud_max_servers}")
    c3.metric(f"Resources In Use ({selected_strategy})", f"{resources}/{cloud_resource_capacity}")
    c4.metric(f"Memory In Use (GB) ({selected_strategy})", f"{memory}/{cloud_memory_capacity}")
    c5.metric(f"Latency ({selected_strategy})", latency)

    if st.checkbox("Show strategy snapshots", value=True):
        st.dataframe(
            df_live_source[["strategy", "users", "servers", "resources", "memory", "latency", "cost", "energy"]],
            use_container_width=True,
            hide_index=True,
        )

    fig = px.line(df_live, x="time", y="users")

    fig.update_layout(
        paper_bgcolor="#0f172a",
        plot_bgcolor="#0f172a",
        font=dict(color="white")
    )

    st.plotly_chart(fig, use_container_width=True)

    time.sleep(3)
    st.rerun()