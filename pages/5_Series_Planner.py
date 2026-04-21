"""Series Planner page for generating balanced lineups."""

import streamlit as st
import pandas as pd
from datetime import datetime

from utils.storage import load_roster, load_ratings, load_game_state, save_game_state
from utils.lineup_engine import generate_all_lineups
from utils.fairness_engine import calculate_fairness_metrics, balance_score
from utils.visualizer import display_lineup_table, display_fairness_summary
from utils.config import OFFENSE_POSITIONS, DEFENSE_POSITIONS

st.set_page_config(page_title="Series Planner", page_icon="📋", layout="wide")

st.title("📋 Series Planner")
st.markdown("Generate balanced lineups for all series.")

# Load data
roster_df = load_roster()
ratings_df = load_ratings()
game_state = load_game_state()

if 'game_state' not in st.session_state:
    st.session_state.game_state = game_state
else:
    game_state = st.session_state.game_state

# Check if lineups are stale
lineup_is_stale = game_state.get('lineup_is_stale', True)

if lineup_is_stale:
    st.warning("⚠️ Lineups need to be regenerated. Player ratings or game setup have changed.")

# Display game info
st.markdown("### Game Information")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.info(f"**Date:** {game_state.get('game_date', 'Not set')}")

with col2:
    st.info(f"**Opponent:** {game_state.get('opponent', 'Not set')}")

with col3:
    st.info(f"**Total Series:** {game_state.get('total_series', 6)}")

with col4:
    available_count = len(roster_df[roster_df['availability'] == 'Available'])
    st.info(f"**Available Players:** {available_count}")

st.markdown("---")

# Generate lineups section
st.markdown("### Generate Lineups")

col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    if st.button("⚡ Generate All Lineups", type="primary"):
        with st.spinner("Generating lineups..."):
            all_series = generate_all_lineups(
                roster_df=roster_df,
                ratings_df=ratings_df,
                total_series=game_state.get('total_series', 6),
                offense_series=game_state.get('offense_series', 3),
                defense_series=game_state.get('defense_series', 3),
                first_half_qb=game_state.get('first_half_qb'),
                second_half_qb=game_state.get('second_half_qb')
            )

            # Update game state
            st.session_state.game_state['all_series'] = all_series
            st.session_state.game_state['lineup_is_stale'] = False
            st.session_state.game_state['last_rating_update'] = datetime.now()

            save_game_state(st.session_state.game_state)

            st.success("✅ Lineups generated successfully!")
            st.rerun()

with col2:
    if st.button("🔄 Regenerate All"):
        with st.spinner("Regenerating lineups..."):
            all_series = generate_all_lineups(
                roster_df=roster_df,
                ratings_df=ratings_df,
                total_series=game_state.get('total_series', 6),
                offense_series=game_state.get('offense_series', 3),
                defense_series=game_state.get('defense_series', 3),
                first_half_qb=game_state.get('first_half_qb'),
                second_half_qb=game_state.get('second_half_qb')
            )

            st.session_state.game_state['all_series'] = all_series
            st.session_state.game_state['lineup_is_stale'] = False

            save_game_state(st.session_state.game_state)

            st.success("✅ All lineups regenerated!")
            st.rerun()

st.markdown("---")

# Display lineups if they exist
all_series = game_state.get('all_series', [])

if not all_series:
    st.info("👆 Click 'Generate All Lineups' to create lineups for the game.")
else:
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["📋 All Lineups", "📊 Fairness Summary", "⚠️ Warnings"])

    with tab1:
        st.markdown("### All Series Lineups")

        for series in all_series:
            series_num = series['series_number']
            series_type = series['series_type']
            half = series['half']
            lineup = series['lineup']
            warnings = series.get('warnings', [])

            with st.expander(f"Series {series_num} - {series_type} (Half {half})", expanded=False):
                # Show warnings
                if warnings:
                    for warning in warnings:
                        st.warning(warning)

                # Display lineup
                positions = OFFENSE_POSITIONS if series_type == 'Offense' else DEFENSE_POSITIONS

                lineup_data = []
                for position in positions:
                    player_name = lineup.get(position, "")
                    lineup_data.append({
                        'Position': position.title(),
                        'Player': player_name if player_name else "---"
                    })

                lineup_df = pd.DataFrame(lineup_data)
                st.table(lineup_df)

    with tab2:
        st.markdown("### Fairness Summary")

        # Calculate fairness metrics
        fairness_df = calculate_fairness_metrics(roster_df, all_series)

        # Display summary
        display_fairness_summary(fairness_df)

        # Balance score
        balance = balance_score(fairness_df)

        if balance >= 80:
            st.success(f"✅ Excellent balance score: {balance:.1f}/100")
        elif balance >= 60:
            st.info(f"ℹ️ Good balance score: {balance:.1f}/100")
        else:
            st.warning(f"⚠️ Balance could be improved: {balance:.1f}/100")

    with tab3:
        st.markdown("### All Warnings")

        all_warnings = []
        for series in all_series:
            series_num = series['series_number']
            series_type = series['series_type']
            warnings = series.get('warnings', [])

            for warning in warnings:
                all_warnings.append({
                    'Series': series_num,
                    'Type': series_type,
                    'Warning': warning
                })

        if all_warnings:
            warnings_df = pd.DataFrame(all_warnings)
            st.dataframe(warnings_df, use_container_width=True)

            # Warning summary
            st.markdown("#### Warning Summary")
            st.info(f"Total warnings: {len(all_warnings)}")
        else:
            st.success("✅ No warnings! All lineups look good.")

st.markdown("---")

with st.expander("ℹ️ How to Use"):
    st.markdown("""
    **Generating Lineups:**
    - Click "Generate All Lineups" to create lineups for all series
    - The algorithm balances playing time and positions players by skill
    - QBs are automatically assigned based on game setup

    **Lineup Algorithm:**
    - Prioritizes players with less playing time
    - Assigns stronger players to key positions
    - Respects player availability
    - Balances offense and defense opportunities

    **Fairness Tracking:**
    - Shows total series played for each player
    - Tracks offense vs defense balance
    - Calculates fairness score (higher is better)
    - Identifies playing time imbalances

    **Warnings:**
    - Low-rated QB or center assignments
    - Unavailable players in lineup
    - Large fairness imbalances
    - Consecutive series concerns

    **Next Steps:**
    - Review lineups in each series
    - Check fairness summary for balance
    - Address any warnings if needed
    - Use Live Game Adjustments for changes during game
    """)
