"""Player Ranking Tool for rating individual skills."""

import streamlit as st
import pandas as pd
from datetime import datetime

from utils.storage import load_roster, load_ratings, save_ratings
from utils.ranking_engine import calculate_all_ratings, recalculate_single_player
from utils.config import OFFENSE_SKILLS, DEFENSE_SKILLS, SKILL_MIN, SKILL_MAX

st.set_page_config(page_title="Player Ranking", page_icon="⭐", layout="wide")

st.title("⭐ Player Ranking Tool")
st.markdown("Rate players on individual skills (1-5 scale).")

# Load data
roster_df = load_roster()
ratings_df = load_ratings()

if 'ratings_df' not in st.session_state:
    st.session_state.ratings_df = ratings_df

# Select player
st.markdown("### Select Player to Rate")

player_names = roster_df['name'].tolist()
selected_player = st.selectbox("Player", player_names, key="player_select")

if not selected_player:
    st.info("Please select a player to rate.")
    st.stop()

# Get player's current ratings
player_ratings = st.session_state.ratings_df[st.session_state.ratings_df['name'] == selected_player]

if player_ratings.empty:
    st.error(f"No ratings found for {selected_player}")
    st.stop()

player_data = player_ratings.iloc[0].to_dict()

st.markdown("---")

# Skill rating form
st.markdown("### Rate Player Skills")

col1, col2 = st.columns(2)

# Offense skills
with col1:
    st.markdown("#### 🏈 Offense Skills")

    offense_values = {}
    for skill in OFFENSE_SKILLS:
        skill_key = f"offense_{skill}"
        current_value = player_data.get(skill_key, 3.0)

        offense_values[skill_key] = st.slider(
            skill.replace('_', ' ').title(),
            min_value=SKILL_MIN,
            max_value=SKILL_MAX,
            value=float(current_value),
            step=0.5,
            key=f"offense_{skill}_{selected_player}",
            help=f"Rate {skill.replace('_', ' ')} from 1 (limited) to 5 (advanced)"
        )

# Defense skills
with col2:
    st.markdown("#### 🛡️ Defense Skills")

    defense_values = {}
    for skill in DEFENSE_SKILLS:
        skill_key = f"defense_{skill}"
        current_value = player_data.get(skill_key, 3.0)

        defense_values[skill_key] = st.slider(
            skill.replace('_', ' ').title(),
            min_value=SKILL_MIN,
            max_value=SKILL_MAX,
            value=float(current_value),
            step=0.5,
            key=f"defense_{skill}_{selected_player}",
            help=f"Rate {skill.replace('_', ' ')} from 1 (limited) to 5 (advanced)"
        )

st.markdown("---")

# Save button
col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    if st.button("💾 Save Ratings", type="primary"):
        # Update ratings in dataframe
        player_idx = st.session_state.ratings_df[st.session_state.ratings_df['name'] == selected_player].index[0]

        for skill_key, value in {**offense_values, **defense_values}.items():
            st.session_state.ratings_df.at[player_idx, skill_key] = value

        # Recalculate scores and ratings for this player
        st.session_state.ratings_df = recalculate_single_player(selected_player, st.session_state.ratings_df)

        # Save to file
        save_ratings(st.session_state.ratings_df)

        # Mark lineups as stale
        st.session_state.lineup_is_stale = True

        st.success(f"✅ Ratings saved for {selected_player}!")
        st.rerun()

with col2:
    if st.button("🔄 Recalculate All"):
        st.session_state.ratings_df = calculate_all_ratings(st.session_state.ratings_df)
        save_ratings(st.session_state.ratings_df)
        st.success("✅ All ratings recalculated!")
        st.rerun()

st.markdown("---")

# Display current scores
st.markdown("### Current Ratings")

player_ratings = st.session_state.ratings_df[st.session_state.ratings_df['name'] == selected_player].iloc[0]

col1, col2, col3 = st.columns(3)

with col1:
    offense_score = player_ratings.get('offense_score', 0.0)
    offense_rating = player_ratings.get('offense_rating', 'C')
    st.metric("Offense Score", f"{offense_score:.2f}")
    st.markdown(f"**Rating:** {offense_rating}")

with col2:
    defense_score = player_ratings.get('defense_score', 0.0)
    defense_rating = player_ratings.get('defense_rating', 'C')
    st.metric("Defense Score", f"{defense_score:.2f}")
    st.markdown(f"**Rating:** {defense_rating}")

with col3:
    overall_score = player_ratings.get('overall_score', 0.0)
    overall_rating = player_ratings.get('overall_rating', 'C')
    st.metric("Overall Score", f"{overall_score:.2f}")
    st.markdown(f"**Rating:** {overall_rating}")

st.markdown("---")

# Quick reference
with st.expander("ℹ️ Rating Scale Reference"):
    st.markdown("""
    **Skill Rating Scale:**

    - **5 (Advanced):** Elite skill level, consistently excellent
    - **4 (Strong):** Above average, reliable performance
    - **3 (Average):** Adequate skill level, developing
    - **2 (Developing):** Below average, needs improvement
    - **1 (Limited):** Minimal skill level, just starting

    **Composite Score Ratings:**

    - **A:** 4.5 and above (Elite)
    - **B:** 3.5 to 4.49 (Strong)
    - **C:** 2.5 to 3.49 (Average)
    - **D:** 1.5 to 2.49 (Developing)
    - **F:** Below 1.5 (Limited)

    **Tips:**
    - Be honest and consistent with ratings
    - Consider game performance, not just practice
    - Review and adjust ratings throughout the season
    - Use half-point increments for precision
    """)
