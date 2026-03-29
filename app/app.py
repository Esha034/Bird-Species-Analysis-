import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Bird Intelligence Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    return pd.read_csv("data/processed/merged_data.csv")

df = load_data()

# ---------------- HELPER ----------------
def top_value(series):
    return series.value_counts().idxmax() if not series.empty else "No Data"

# ---------------- CUSTOM UI ----------------
st.markdown("""
<style>
.main-title {
    font-size: 42px;
    font-weight: 700;
    text-align: center;
    background: linear-gradient(90deg, #00C9FF, #92FE9D);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.glass {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0px 4px 25px rgba(0,0,0,0.3);
}
.metric-card {
    background: linear-gradient(135deg, #667eea, #764ba2);
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    color: white;
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown('<div class="main-title">🦜 Bird Intelligence Dashboard</div>', unsafe_allow_html=True)
st.caption("Explore bird biodiversity, seasonal patterns & environmental insights")

# ---------------- SIDEBAR ----------------
st.sidebar.title("⚙️ Smart Filters")

habitat = st.sidebar.multiselect("🌿 Habitat", df['habitat'].unique(), default=df['habitat'].unique())
season = st.sidebar.multiselect("☀️ Season", df['season'].unique(), default=df['season'].unique())
species = st.sidebar.multiselect("🦜 Species", df['common_name'].dropna().unique())
observer = st.sidebar.multiselect("👤 Observer", df['observer'].dropna().unique())

# ---------------- FILTERING ----------------
filtered = df[
    (df['habitat'].isin(habitat)) &
    (df['season'].isin(season))
]

if species:
    filtered = filtered[filtered['common_name'].isin(species)]

if observer:
    filtered = filtered[filtered['observer'].isin(observer)]

# ---------------- KPI SECTION ----------------
st.markdown("### Dashboard Summary")

c1, c2, c3, c4 = st.columns(4)

c1.markdown(f'<div class="metric-card">📌<br>Total Records<br><b>{len(filtered)}</b></div>', unsafe_allow_html=True)
c2.markdown(f'<div class="metric-card">🦜<br>Species Count<br><b>{filtered["scientific_name"].nunique()}</b></div>', unsafe_allow_html=True)
c3.markdown(f'<div class="metric-card">📍<br>Locations<br><b>{filtered["plot_name"].nunique()}</b></div>', unsafe_allow_html=True)
c4.markdown(f'<div class="metric-card">🌡️<br>Avg Temp<br><b>{filtered["temperature"].mean():.1f}°C</b></div>', unsafe_allow_html=True)

# ---------------- INSIGHTS ----------------
top_hab = top_value(filtered['habitat'])
top_sea = top_value(filtered['season'])
top_sp = top_value(filtered['common_name'])

st.markdown("### Smart Insights")

st.markdown(f"""
<div class="glass">
<ul>
<li><b>{top_hab}</b> habitat dominates bird observations</li>
<li>Peak activity occurs in <b>{top_sea}</b> season</li>
<li>Most observed species: <b>{top_sp}</b></li>
<li>High biodiversity zones detected across selected plots</li>
</ul>
</div>
""", unsafe_allow_html=True)

# ---------------- TABS ----------------
tab1, tab2, tab3 = st.tabs(["📊 Overview", "🦜 Species Intelligence", "🌍 Environmental Analysis"])

# ================= TAB 1 =================
with tab1:
    st.markdown("### Habitat & Seasonal Trends")

    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots()
        filtered['habitat'].value_counts().plot(kind='bar', ax=ax)
        st.pyplot(fig)

    with col2:
        fig, ax = plt.subplots()
        filtered['season'].value_counts().plot(kind='bar', ax=ax)
        st.pyplot(fig)

    st.markdown("### 📈 Monthly Activity Pattern")

    fig, ax = plt.subplots()
    filtered['month'].value_counts().sort_index().plot(marker='o', ax=ax)
    st.pyplot(fig)

# ================= TAB 2 =================
with tab2:
    st.markdown("### 🦜 Species Distribution")

    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots()
        filtered['common_name'].value_counts().head(10).plot(kind='bar', ax=ax)
        st.pyplot(fig)

    with col2:
        hotspots = filtered.groupby('plot_name')['scientific_name'].nunique().sort_values(ascending=False).head(10)
        fig, ax = plt.subplots()
        hotspots.plot(kind='bar', ax=ax)
        st.pyplot(fig)

    st.markdown("### 👤 Observer Contribution")

    fig, ax = plt.subplots()
    filtered['observer'].value_counts().head(10).plot(kind='bar', ax=ax)
    st.pyplot(fig)

# ================= TAB 3 =================
with tab3:
    st.markdown("### 🌡️ Environmental Impact")

    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots()
        ax.scatter(filtered['temperature'], filtered['humidity'])
        ax.set_xlabel("Temperature")
        ax.set_ylabel("Humidity")
        st.pyplot(fig)

    with col2:
        fig, ax = plt.subplots()
        filtered['distance'].value_counts().plot(kind='bar', ax=ax)
        st.pyplot(fig)

    st.markdown("### 🛰️ Observation Conditions")

    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots()
        filtered['flyover_observed'].value_counts().plot(kind='bar', ax=ax)
        st.pyplot(fig)

    with col2:
        fig, ax = plt.subplots()
        filtered['pif_watchlist_status'].value_counts().plot(kind='bar', ax=ax)
        st.pyplot(fig)

# ---------------- DOWNLOAD ----------------
st.markdown("---")

st.download_button(
    "📥 Export Filtered Dataset",
    filtered.to_csv(index=False),
    file_name="bird_filtered_data.csv"
)