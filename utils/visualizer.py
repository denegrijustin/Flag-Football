"""Visualization utilities for displaying data."""

import streamlit as st
import pandas as pd
from typing import Dict, List

from utils.config import RATING_COLORS, OFFENSE_POSITIONS, DEFENSE_POSITIONS


def color_rating(rating: str) -> str:
    """Return color for a rating."""
    return RATING_COLORS.get(rating, '#000000')


def display_player_card(player_data: Dict):
    """Display a player information card."""
    st.markdown(f"### {player_data['name']} (#{player_data.get('number', 0)})")

    col1, col2, col3 = st.columns(3)

    with col1:
        offense_rating = player_data.get('offense_rating', 'C')
        offense_color = color_rating(offense_rating)
        st.markdown(f"**Offense:** <span style='color:{offense_color}; font-weight:bold'>{offense_rating}</span>",
                   unsafe_allow_html=True)

    with col2:
        defense_rating = player_data.get('defense_rating', 'C')
        defense_color = color_rating(defense_rating)
        st.markdown(f"**Defense:** <span style='color:{defense_color}; font-weight:bold'>{defense_rating}</span>",
                   unsafe_allow_html=True)

    with col3:
        overall_rating = player_data.get('overall_rating', 'C')
        overall_color = color_rating(overall_rating)
        st.markdown(f"**Overall:** <span style='color:{overall_color}; font-weight:bold'>{overall_rating}</span>",
                   unsafe_allow_html=True)


def display_lineup_table(all_series: List[Dict], show_warnings: bool = True):
    """Display lineup table for all series."""

    for series in all_series:
        series_num = series['series_number']
        series_type = series['series_type']
        half = series['half']
        lineup = series['lineup']
        warnings = series.get('warnings', [])

        st.markdown(f"### Series {series_num} - {series_type} (Half {half})")

        if show_warnings and warnings:
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


def display_fairness_summary(fairness_df: pd.DataFrame):
    """Display fairness summary."""
    st.markdown("### Playing Time Summary")

    if fairness_df.empty:
        st.info("No playing time data available yet.")
        return

    # Sort by total series
    fairness_df_sorted = fairness_df.sort_values('total_series_played', ascending=False)

    st.dataframe(
        fairness_df_sorted[[
            'name',
            'total_series_played',
            'offense_series_played',
            'defense_series_played',
            'bench_count',
            'fairness_score'
        ]],
        use_container_width=True
    )

    # Show statistics
    col1, col2, col3 = st.columns(3)

    with col1:
        avg_series = fairness_df['total_series_played'].mean()
        st.metric("Average Series", f"{avg_series:.1f}")

    with col2:
        min_series = fairness_df['total_series_played'].min()
        max_series = fairness_df['total_series_played'].max()
        st.metric("Series Range", f"{min_series} - {max_series}")

    with col3:
        avg_fairness = fairness_df['fairness_score'].mean()
        st.metric("Avg Fairness Score", f"{avg_fairness:.1f}")


def display_ratings_table(ratings_df: pd.DataFrame):
    """Display player ratings table with color coding."""

    display_df = ratings_df[['name', 'offense_rating', 'defense_rating', 'overall_rating',
                             'offense_score', 'defense_score', 'overall_score']].copy()

    st.dataframe(display_df, use_container_width=True)


def display_series_field(series_type: str, lineup: Dict[str, str]):
    """Display a simple field diagram for a series."""

    st.markdown(f"**{series_type} Formation**")

    if series_type == "Offense":
        # Simple offense formation display
        st.text("                WR1: " + lineup.get('wide receiver 1', '---'))
        st.text("    Slot1: " + lineup.get('slot 1', '---') + "        Slot2: " + lineup.get('slot 2', '---'))
        st.text("        QB: " + lineup.get('quarterback', '---'))
        st.text("    RB: " + lineup.get('running back', '---') + "    Center: " + lineup.get('center', '---'))
        st.text("                WR2: " + lineup.get('wide receiver 2', '---'))
    else:
        # Simple defense formation display
        st.text("    CB1: " + lineup.get('cornerback 1', '---') + "        CB2: " + lineup.get('cornerback 2', '---'))
        st.text("LB1: " + lineup.get('linebacker 1', '---') + "  LB2: " + lineup.get('linebacker 2', '---') + "  LB3: " + lineup.get('linebacker 3', '---'))
        st.text("        Blitzer: " + lineup.get('blitzer', '---'))
