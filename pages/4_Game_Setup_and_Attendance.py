"""Game Setup and Attendance page for configuring game details."""

import streamlit as st
from datetime import date

from utils.storage import load_roster, save_roster, load_game_state, save_game_state, load_ratings
from utils.config import DEFAULT_TOTAL_SERIES, DEFAULT_OFFENSE_SERIES, DEFAULT_DEFENSE_SERIES

st.set_page_config(page_title="Game Setup", page_icon="🏟️", layout="wide")

st.title("🏟️ Game Setup and Attendance")
st.markdown("Configure game details and mark player availability.")

# Load data
roster_df = load_roster()
ratings_df = load_ratings()
game_state = load_game_state()

if 'game_state' not in st.session_state:
    st.session_state.game_state = game_state
else:
    game_state = st.session_state.game_state

# Game configuration
st.markdown("### Game Configuration")

col1, col2 = st.columns(2)

with col1:
    game_date = st.date_input(
        "Game Date",
        value=date.today(),
        key="game_date"
    )

with col2:
    opponent = st.text_input(
        "Opponent",
        value=game_state.get('opponent', ''),
        key="opponent"
    )

st.markdown("### Series Configuration")

col1, col2, col3 = st.columns(3)

with col1:
    total_series = st.number_input(
        "Total Series",
        min_value=1,
        max_value=20,
        value=game_state.get('total_series', DEFAULT_TOTAL_SERIES),
        key="total_series"
    )

with col2:
    offense_series = st.number_input(
        "Offense Series",
        min_value=1,
        max_value=total_series,
        value=min(game_state.get('offense_series', DEFAULT_OFFENSE_SERIES), total_series),
        key="offense_series"
    )

with col3:
    defense_series = total_series - offense_series
    st.metric("Defense Series", defense_series)

# Validate series total
if offense_series + defense_series != total_series:
    st.error("⚠️ Offense + Defense series must equal Total series")

st.markdown("---")

# Quarterback selection
st.markdown("### Quarterback Selection")

# Get QB candidates
qb_candidates = ratings_df[
    (ratings_df['is_first_half_qb'] == True) | (ratings_df['is_second_half_qb'] == True)
]['name'].tolist()

# If no designated QBs, show all players
if not qb_candidates:
    qb_candidates = ratings_df['name'].tolist()

col1, col2 = st.columns(2)

with col1:
    first_half_qb = st.selectbox(
        "First Half QB",
        options=['None'] + qb_candidates,
        index=0 if not game_state.get('first_half_qb') else (
            qb_candidates.index(game_state['first_half_qb']) + 1
            if game_state['first_half_qb'] in qb_candidates else 0
        ),
        key="first_half_qb_select"
    )

with col2:
    second_half_qb = st.selectbox(
        "Second Half QB",
        options=['None'] + qb_candidates,
        index=0 if not game_state.get('second_half_qb') else (
            qb_candidates.index(game_state['second_half_qb']) + 1
            if game_state['second_half_qb'] in qb_candidates else 0
        ),
        key="second_half_qb_select"
    )

# Convert 'None' to None
first_half_qb = None if first_half_qb == 'None' else first_half_qb
second_half_qb = None if second_half_qb == 'None' else second_half_qb

st.markdown("---")

# Player availability
st.markdown("### Player Availability")

st.info("💡 Mark each player's availability for this game. This affects lineup generation.")

# Create editable availability table
availability_df = roster_df[['name', 'number', 'availability']].copy()

edited_availability = st.data_editor(
    availability_df,
    disabled=['name', 'number'],
    use_container_width=True,
    column_config={
        "name": "Player Name",
        "number": "Number",
        "availability": st.column_config.SelectboxColumn(
            "Availability",
            options=["Available", "Unavailable", "Late", "Leaving Early"],
            required=True
        )
    },
    key="availability_editor"
)

st.markdown("---")

# Save button
col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    if st.button("💾 Save Game Setup", type="primary"):
        # Update game state
        st.session_state.game_state.update({
            'game_date': str(game_date),
            'opponent': opponent,
            'total_series': total_series,
            'offense_series': offense_series,
            'defense_series': defense_series,
            'first_half_qb': first_half_qb,
            'second_half_qb': second_half_qb
        })

        save_game_state(st.session_state.game_state)

        # Update roster with availability
        for idx, row in edited_availability.iterrows():
            roster_idx = roster_df[roster_df['name'] == row['name']].index
            if len(roster_idx) > 0:
                roster_df.at[roster_idx[0], 'availability'] = row['availability']

        save_roster(roster_df)
        st.session_state.roster_df = roster_df

        st.success("✅ Game setup saved successfully!")
        st.rerun()

with col2:
    if st.button("🔄 Reset to Defaults"):
        st.session_state.game_state = {
            'game_date': str(date.today()),
            'opponent': '',
            'total_series': DEFAULT_TOTAL_SERIES,
            'offense_series': DEFAULT_OFFENSE_SERIES,
            'defense_series': DEFAULT_DEFENSE_SERIES,
            'first_half_qb': None,
            'second_half_qb': None,
            'all_series': [],
            'lineup_is_stale': True
        }
        save_game_state(st.session_state.game_state)
        st.success("✅ Reset to defaults!")
        st.rerun()

st.markdown("---")

# Current status summary
st.markdown("### Current Status")

col1, col2, col3, col4 = st.columns(4)

with col1:
    available_count = len(edited_availability[edited_availability['availability'] == 'Available'])
    st.metric("Available", available_count)

with col2:
    unavailable_count = len(edited_availability[edited_availability['availability'] == 'Unavailable'])
    st.metric("Unavailable", unavailable_count)

with col3:
    late_count = len(edited_availability[edited_availability['availability'] == 'Late'])
    st.metric("Late", late_count)

with col4:
    leaving_count = len(edited_availability[edited_availability['availability'] == 'Leaving Early'])
    st.metric("Leaving Early", leaving_count)

st.markdown("---")

with st.expander("ℹ️ How to Use"):
    st.markdown("""
    **Game Configuration:**
    - Set the game date and opponent name
    - Configure total number of series for the game
    - Typically 6 series total (3 offense, 3 defense)

    **Quarterback Selection:**
    - Choose a QB for first half and second half
    - QBs are automatically assigned to offense series
    - Make sure to designate QBs in Ratings & Eligibility page first

    **Player Availability:**
    - **Available:** Player is ready for the entire game
    - **Unavailable:** Player will not be at the game
    - **Late:** Player will arrive after game starts
    - **Leaving Early:** Player must leave before game ends

    **Important:**
    - Save game setup before generating lineups
    - Unavailable players will not be assigned to any series
    - Late/Leaving Early warnings will appear in lineup generation
    """)
