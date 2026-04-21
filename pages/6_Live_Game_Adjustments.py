"""Live Game Adjustments page for making real-time lineup changes."""

import streamlit as st
import pandas as pd

from utils.storage import load_roster, load_ratings, load_game_state, save_game_state
from utils.lineup_engine import regenerate_future_lineups
from utils.fairness_engine import calculate_fairness_metrics
from utils.config import OFFENSE_POSITIONS, DEFENSE_POSITIONS

st.set_page_config(page_title="Live Game Adjustments", page_icon="🎮", layout="wide")

st.title("🎮 Live Game Adjustments")
st.markdown("Make real-time changes to lineups during the game.")

# Load data
roster_df = load_roster()
ratings_df = load_ratings()
game_state = load_game_state()

if 'game_state' not in st.session_state:
    st.session_state.game_state = game_state
else:
    game_state = st.session_state.game_state

all_series = game_state.get('all_series', [])

if not all_series:
    st.warning("⚠️ No lineups generated yet. Go to Series Planner to generate lineups first.")
    st.stop()

# Select series to edit
st.markdown("### Select Series to Edit")

series_options = [f"Series {s['series_number']} - {s['series_type']} (Half {s['half']})" for s in all_series]
selected_series_idx = st.selectbox("Series", range(len(series_options)), format_func=lambda x: series_options[x])

selected_series = all_series[selected_series_idx]
series_num = selected_series['series_number']
series_type = selected_series['series_type']
lineup = selected_series['lineup']

st.markdown("---")

# Display current lineup
st.markdown(f"### Current Lineup - Series {series_num}")

positions = OFFENSE_POSITIONS if series_type == 'Offense' else DEFENSE_POSITIONS

# Create editable lineup
st.markdown("**Edit lineup by selecting players for each position:**")

player_names = [''] + roster_df['name'].tolist()

edited_lineup = {}

col_count = 2
cols = st.columns(col_count)

for idx, position in enumerate(positions):
    col = cols[idx % col_count]

    with col:
        current_player = lineup.get(position, '')

        # Find index of current player
        if current_player in player_names:
            default_idx = player_names.index(current_player)
        else:
            default_idx = 0

        selected_player = st.selectbox(
            position.title(),
            options=player_names,
            index=default_idx,
            key=f"lineup_{series_num}_{position}"
        )

        edited_lineup[position] = selected_player if selected_player else ""

st.markdown("---")

# Save lineup changes
col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    if st.button("💾 Save Changes", type="primary"):
        # Update lineup
        all_series[selected_series_idx]['lineup'] = edited_lineup
        all_series[selected_series_idx]['manually_edited'] = True

        # Update game state
        st.session_state.game_state['all_series'] = all_series
        save_game_state(st.session_state.game_state)

        st.success(f"✅ Series {series_num} updated!")
        st.rerun()

with col2:
    if st.button("🔄 Regenerate Future"):
        with st.spinner("Regenerating future lineups..."):
            # Regenerate lineups after current series
            updated_series = regenerate_future_lineups(
                all_series=all_series,
                current_series=selected_series_idx + 1,
                roster_df=roster_df,
                ratings_df=ratings_df,
                first_half_qb=game_state.get('first_half_qb'),
                second_half_qb=game_state.get('second_half_qb')
            )

            st.session_state.game_state['all_series'] = updated_series
            save_game_state(st.session_state.game_state)

            st.success("✅ Future lineups regenerated!")
            st.rerun()

st.markdown("---")

# Quick swap tool
st.markdown("### Quick Player Swap")

st.info("💡 Swap two players across the current lineup.")

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    player1 = st.selectbox("Player 1", roster_df['name'].tolist(), key="swap_player1")

with col2:
    player2 = st.selectbox("Player 2", roster_df['name'].tolist(), key="swap_player2")

with col3:
    st.markdown("")  # Spacer
    st.markdown("")  # Spacer
    if st.button("🔄 Swap Players"):
        if player1 == player2:
            st.error("Cannot swap a player with themselves!")
        else:
            # Find positions of both players
            pos1 = None
            pos2 = None

            for pos, player in lineup.items():
                if player == player1:
                    pos1 = pos
                elif player == player2:
                    pos2 = pos

            # Perform swap
            new_lineup = lineup.copy()

            if pos1:
                new_lineup[pos1] = player2 if player2 else ""
            if pos2:
                new_lineup[pos2] = player1 if player1 else ""

            # Update lineup
            all_series[selected_series_idx]['lineup'] = new_lineup
            all_series[selected_series_idx]['manually_edited'] = True

            st.session_state.game_state['all_series'] = all_series
            save_game_state(st.session_state.game_state)

            st.success(f"✅ Swapped {player1} and {player2}!")
            st.rerun()

st.markdown("---")

# Current game status
st.markdown("### Current Game Status")

fairness_df = calculate_fairness_metrics(roster_df, all_series[:selected_series_idx + 1])

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Series Played", selected_series_idx + 1)

with col2:
    st.metric("Series Remaining", len(all_series) - selected_series_idx - 1)

with col3:
    if not fairness_df.empty:
        avg_series = fairness_df['total_series_played'].mean()
        st.metric("Avg Series/Player", f"{avg_series:.1f}")

with col4:
    if not fairness_df.empty:
        min_series = fairness_df['total_series_played'].min()
        max_series = fairness_df['total_series_played'].max()
        st.metric("Series Range", f"{min_series}-{max_series}")

# Playing time table
st.markdown("### Playing Time So Far")

if not fairness_df.empty:
    display_df = fairness_df[['name', 'total_series_played', 'offense_series_played', 'defense_series_played', 'bench_count']].copy()
    display_df = display_df.sort_values('total_series_played', ascending=False)

    st.dataframe(display_df, use_container_width=True)

    # Highlight players who need more playing time
    min_series = fairness_df['total_series_played'].min()
    players_needing_time = fairness_df[fairness_df['total_series_played'] == min_series]['name'].tolist()

    if players_needing_time:
        st.info(f"💡 Players with least playing time: {', '.join(players_needing_time)}")
else:
    st.info("No playing time data yet.")

st.markdown("---")

with st.expander("ℹ️ How to Use"):
    st.markdown("""
    **Making Adjustments:**
    - Select the series you want to edit
    - Use dropdowns to change player assignments
    - Click "Save Changes" to update the lineup

    **Regenerate Future Lineups:**
    - After making changes, regenerate future series
    - This re-balances playing time for remaining series
    - Past series and the current series remain unchanged

    **Quick Player Swap:**
    - Quickly swap two players in the current lineup
    - Useful for last-minute substitutions
    - Automatically updates positions

    **Playing Time Tracking:**
    - View real-time playing time statistics
    - See who needs more opportunities
    - Balance playing time as the game progresses

    **Tips:**
    - Make adjustments between series, not during play
    - Keep an eye on fairness metrics
    - Use regenerate to rebalance after major changes
    - Manual edits are marked and preserved
    """)
