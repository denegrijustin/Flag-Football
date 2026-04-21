"""Ratings and Eligibility page for viewing calculated ratings and setting positions."""

import streamlit as st
import pandas as pd

from utils.storage import load_roster, load_ratings, save_ratings
from utils.visualizer import color_rating, display_ratings_table
from utils.position_fit import generate_position_recommendations
from utils.config import ALL_POSITIONS, RATING_COLORS

st.set_page_config(page_title="Ratings & Eligibility", page_icon="📊", layout="wide")

st.title("📊 Ratings and Eligibility")
st.markdown("View calculated ratings and set position eligibility.")

# Load data
roster_df = load_roster()
ratings_df = load_ratings()

if 'ratings_df' not in st.session_state:
    st.session_state.ratings_df = ratings_df
else:
    ratings_df = st.session_state.ratings_df

st.markdown("### Player Ratings Overview")

# Display ratings table with color coding
display_df = ratings_df[[
    'name',
    'offense_rating', 'offense_score',
    'defense_rating', 'defense_score',
    'overall_rating', 'overall_score'
]].copy()

# Style the dataframe
def style_rating(val):
    if val in RATING_COLORS:
        color = RATING_COLORS[val]
        return f'background-color: {color}; color: white; font-weight: bold'
    return ''

styled_df = display_df.style.applymap(
    style_rating,
    subset=['offense_rating', 'defense_rating', 'overall_rating']
)

st.dataframe(styled_df, use_container_width=True)

st.markdown("---")

# Position recommendations
st.markdown("### Position Recommendations")

recommendations_df = generate_position_recommendations(ratings_df)

st.dataframe(recommendations_df, use_container_width=True)

st.markdown("---")

# Position eligibility editor
st.markdown("### Set Position Eligibility")

st.info("💡 Use position recommendations above to help set eligibility. Select all positions a player can play.")

selected_player = st.selectbox("Select Player", ratings_df['name'].tolist(), key="eligibility_player")

if selected_player:
    player_data = ratings_df[ratings_df['name'] == selected_player].iloc[0]

    # Get current eligibility
    current_eligibility = player_data.get('eligible_positions', '')
    if isinstance(current_eligibility, str):
        current_eligibility_list = [p.strip() for p in current_eligibility.split(',') if p.strip()]
    else:
        current_eligibility_list = []

    # Position selection
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Offense Positions")
        offense_positions = [
            "quarterback", "running back", "slot 1", "slot 2",
            "wide receiver 1", "wide receiver 2", "center"
        ]

        offense_eligible = []
        for pos in offense_positions:
            if st.checkbox(pos.title(), value=pos in current_eligibility_list, key=f"eli_{pos}"):
                offense_eligible.append(pos)

    with col2:
        st.markdown("#### Defense Positions")
        defense_positions = [
            "linebacker 1", "linebacker 2", "linebacker 3",
            "cornerback 1", "cornerback 2", "blitzer"
        ]

        defense_eligible = []
        for pos in defense_positions:
            if st.checkbox(pos.title(), value=pos in current_eligibility_list, key=f"eli_{pos}"):
                defense_eligible.append(pos)

    all_eligible = offense_eligible + defense_eligible

    # QB designation
    st.markdown("#### Quarterback Designation")

    col1, col2 = st.columns(2)

    with col1:
        is_first_half_qb = st.checkbox(
            "First Half QB",
            value=bool(player_data.get('is_first_half_qb', False)),
            key="first_half_qb"
        )

    with col2:
        is_second_half_qb = st.checkbox(
            "Second Half QB",
            value=bool(player_data.get('is_second_half_qb', False)),
            key="second_half_qb"
        )

    # Save button
    if st.button("💾 Save Eligibility", type="primary"):
        player_idx = ratings_df[ratings_df['name'] == selected_player].index[0]

        st.session_state.ratings_df.at[player_idx, 'eligible_positions'] = ', '.join(all_eligible)
        st.session_state.ratings_df.at[player_idx, 'is_first_half_qb'] = is_first_half_qb
        st.session_state.ratings_df.at[player_idx, 'is_second_half_qb'] = is_second_half_qb

        save_ratings(st.session_state.ratings_df)

        st.success(f"✅ Eligibility saved for {selected_player}!")
        st.rerun()

st.markdown("---")

# Rating distribution
st.markdown("### Rating Distribution")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Offense Ratings**")
    offense_counts = ratings_df['offense_rating'].value_counts().sort_index()
    for rating in ['A', 'B', 'C', 'D', 'F']:
        count = offense_counts.get(rating, 0)
        color = RATING_COLORS.get(rating, '#000000')
        st.markdown(f"<span style='color:{color}; font-weight:bold'>{rating}</span>: {count}", unsafe_allow_html=True)

with col2:
    st.markdown("**Defense Ratings**")
    defense_counts = ratings_df['defense_rating'].value_counts().sort_index()
    for rating in ['A', 'B', 'C', 'D', 'F']:
        count = defense_counts.get(rating, 0)
        color = RATING_COLORS.get(rating, '#000000')
        st.markdown(f"<span style='color:{color}; font-weight:bold'>{rating}</span>: {count}", unsafe_allow_html=True)

with col3:
    st.markdown("**Overall Ratings**")
    overall_counts = ratings_df['overall_rating'].value_counts().sort_index()
    for rating in ['A', 'B', 'C', 'D', 'F']:
        count = overall_counts.get(rating, 0)
        color = RATING_COLORS.get(rating, '#000000')
        st.markdown(f"<span style='color:{color}; font-weight:bold'>{rating}</span>: {count}", unsafe_allow_html=True)

st.markdown("---")

with st.expander("ℹ️ How to Use"):
    st.markdown("""
    **Viewing Ratings:**
    - Color-coded ratings make it easy to identify player strengths
    - Scores show the calculated numeric values
    - Ratings are automatically calculated from individual skills

    **Position Recommendations:**
    - Top 3 recommended positions for each player
    - Based on position-specific skill weights
    - Use these as a guide when setting eligibility

    **Setting Eligibility:**
    - Check all positions a player is capable of playing
    - This helps the lineup generator create flexible lineups
    - Players can be eligible for both offense and defense positions

    **QB Designation:**
    - Mark first and second half quarterbacks
    - These will be used as default QBs in lineup generation
    - Only one player should be marked for each half
    """)
