import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="IPL Data Analysis Dashboard",
    page_icon="🏏",
    layout="wide"
)

st.title("🏏 IPL Data Analysis Dashboard")
st.markdown("**Interactive analysis of Indian Premier League matches (2008–2023)**")
st.markdown("---")

# ─── Load Data ────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    # Using IPL dataset from GitHub (public dataset)
    matches_url = "https://raw.githubusercontent.com/dsrscientist/dataset1/master/IPL_matches.csv"
    try:
        df = pd.read_csv(matches_url)
    except Exception:
        # Fallback: generate synthetic data for demo
        np.random.seed(42)
        teams = ["MI", "CSK", "RCB", "KKR", "SRH", "DC", "PBKS", "RR"]
        seasons = list(range(2008, 2024))
        n = 800
        df = pd.DataFrame({
            "season": np.random.choice(seasons, n),
            "team1": np.random.choice(teams, n),
            "team2": np.random.choice(teams, n),
            "winner": np.random.choice(teams, n),
            "win_by_runs": np.random.randint(0, 100, n),
            "win_by_wickets": np.random.randint(0, 10, n),
            "toss_winner": np.random.choice(teams, n),
            "toss_decision": np.random.choice(["bat", "field"], n),
            "city": np.random.choice(["Mumbai", "Chennai", "Kolkata", "Delhi", "Bangalore"], n),
        })
    return df

df = load_data()

# ─── Sidebar Filters ─────────────────────────────────────────────────────────
with st.sidebar:
    st.header("🔧 Filters")
    if "season" in df.columns:
        seasons = sorted(df["season"].unique())
        selected_seasons = st.multiselect(
            "Select Seasons",
            options=seasons,
            default=seasons[-5:]
        )
        filtered_df = df[df["season"].isin(selected_seasons)]
    else:
        filtered_df = df

    st.markdown("---")
    st.markdown("**Dataset Info**")
    st.metric("Total Matches", len(filtered_df))
    st.metric("Seasons", filtered_df["season"].nunique() if "season" in filtered_df.columns else "N/A")

# ─── KPI Row ─────────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("🏟️ Total Matches", len(filtered_df))
with col2:
    st.metric("🏆 Seasons Covered", filtered_df["season"].nunique() if "season" in filtered_df.columns else "-")
with col3:
    if "winner" in filtered_df.columns:
        top_team = filtered_df["winner"].value_counts().index[0]
        st.metric("👑 Most Wins", top_team)
with col4:
    if "toss_decision" in filtered_df.columns:
        top_decision = filtered_df["toss_decision"].value_counts().index[0]
        st.metric("🎯 Fav Toss Decision", top_decision.capitalize())

st.markdown("---")

# ─── Charts Row 1 ────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 Top 8 Teams by Wins")
    if "winner" in filtered_df.columns:
        wins = filtered_df["winner"].value_counts().head(8)
        fig, ax = plt.subplots(figsize=(7, 4))
        colors = sns.color_palette("husl", len(wins))
        bars = ax.barh(wins.index, wins.values, color=colors)
        ax.set_xlabel("Number of Wins")
        ax.bar_label(bars, padding=3, fontsize=9)
        ax.invert_yaxis()
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

with col2:
    st.subheader("🎯 Toss Decision Analysis")
    if "toss_decision" in filtered_df.columns:
        toss = filtered_df["toss_decision"].value_counts()
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.pie(toss.values, labels=[t.capitalize() for t in toss.index],
               autopct='%1.1f%%', colors=["#FF6B6B", "#4ECDC4"],
               startangle=90, textprops={'fontsize': 12})
        ax.set_title("Bat vs Field after Toss")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

# ─── Charts Row 2 ────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("📅 Matches Per Season")
    if "season" in filtered_df.columns:
        matches_per_season = filtered_df.groupby("season").size().reset_index(name="matches")
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.plot(matches_per_season["season"], matches_per_season["matches"],
                marker='o', color="#FF6B6B", linewidth=2, markersize=6)
        ax.fill_between(matches_per_season["season"], matches_per_season["matches"],
                        alpha=0.2, color="#FF6B6B")
        ax.set_xlabel("Season")
        ax.set_ylabel("Number of Matches")
        ax.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

with col2:
    st.subheader("🌆 Top Match Venues")
    if "city" in filtered_df.columns:
        venues = filtered_df["city"].value_counts().head(7)
        fig, ax = plt.subplots(figsize=(7, 4))
        sns.barplot(x=venues.values, y=venues.index, palette="viridis", ax=ax)
        ax.set_xlabel("Number of Matches")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

# ─── Raw Data ─────────────────────────────────────────────────────────────────
st.markdown("---")
with st.expander("📋 View Raw Data"):
    st.dataframe(filtered_df.head(50), use_container_width=True)

st.markdown("---")
st.markdown("*Built by **Jatin Chauhan** | Engineer @ Samsung R&D | [LinkedIn](https://www.linkedin.com/in/jatin-chauhan-a07153171/)*")
