"""Postgame Summary page for reviewing results and exporting reports."""

import streamlit as st
import pandas as pd

from utils.storage import load_roster, load_ratings, load_game_state
from utils.fairness_engine import calculate_fairness_metrics, balance_score
from utils.exports import export_lineups_to_csv, export_fairness_report, export_game_summary
from utils.visualizer import display_fairness_summary
from utils.config import RATING_COLORS

st.set_page_config(page_title="Postgame Summary", page_icon="📈", layout="wide")

st.title("📈 Postgame Summary")
st.markdown("Review playing time, fairness, and export reports.")

# Load data
roster_df = load_roster()
ratings_df = load_ratings()
game_state = load_game_state()

all_series = game_state.get('all_series', [])

if not all_series:
    st.warning("⚠️ No game data available. Generate lineups in Series Planner first.")
    st.stop()

# Game summary
st.markdown("### Game Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.info(f"**Date:** {game_state.get('game_date', 'Not set')}")

with col2:
    st.info(f"**Opponent:** {game_state.get('opponent', 'Not set')}")

with col3:
    st.info(f"**Total Series:** {len(all_series)}")

with col4:
    offense_count = len([s for s in all_series if s['series_type'] == 'Offense'])
    defense_count = len([s for s in all_series if s['series_type'] == 'Defense'])
    st.info(f"**O/D Split:** {offense_count}/{defense_count}")

st.markdown("---")

# Calculate fairness metrics
fairness_df = calculate_fairness_metrics(roster_df, all_series)

# Fairness summary
st.markdown("### Playing Time Analysis")

display_fairness_summary(fairness_df)

# Balance score
balance = balance_score(fairness_df)

st.markdown("#### Overall Balance Score")

if balance >= 80:
    st.success(f"✅ Excellent balance: {balance:.1f}/100")
elif balance >= 60:
    st.info(f"ℹ️ Good balance: {balance:.1f}/100")
else:
    st.warning(f"⚠️ Could be improved: {balance:.1f}/100")

st.markdown("---")

# Player performance summary
st.markdown("### Player Participation Summary")

# Merge roster, ratings, and fairness
summary_df = pd.merge(roster_df, ratings_df, on='name', how='inner')
summary_df = pd.merge(summary_df, fairness_df, on='name', how='inner')

# Select relevant columns
display_columns = [
    'name', 'number', 'overall_rating',
    'total_series_played', 'offense_series_played', 'defense_series_played',
    'bench_count', 'fairness_score'
]

summary_display = summary_df[display_columns].copy()
summary_display = summary_display.sort_values('total_series_played', ascending=False)

st.dataframe(summary_display, use_container_width=True)

st.markdown("---")

# Warnings summary
st.markdown("### Warnings and Issues")

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

    st.info(f"Total warnings: {len(all_warnings)}")
else:
    st.success("✅ No warnings throughout the game!")

st.markdown("---")

# Export section
st.markdown("### Export Reports")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📄 Export Lineups", type="primary"):
        try:
            filepath = export_lineups_to_csv(all_series)
            st.success(f"✅ Lineups exported to: {filepath}")
        except Exception as e:
            st.error(f"Error exporting lineups: {str(e)}")

with col2:
    if st.button("📊 Export Fairness Report", type="primary"):
        try:
            filepath = export_fairness_report(fairness_df)
            st.success(f"✅ Fairness report exported to: {filepath}")
        except Exception as e:
            st.error(f"Error exporting fairness report: {str(e)}")

with col3:
    if st.button("📈 Export Game Summary", type="primary"):
        try:
            filepath = export_game_summary(all_series, fairness_df, game_state)
            st.success(f"✅ Game summary exported to: {filepath}")
        except Exception as e:
            st.error(f"Error exporting game summary: {str(e)}")

st.markdown("---")

# Key insights
st.markdown("### Key Insights")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Most Active Players")

    if not fairness_df.empty:
        top_players = fairness_df.nlargest(3, 'total_series_played')

        for idx, player in top_players.iterrows():
            st.write(f"**{player['name']}** - {player['total_series_played']} series")

with col2:
    st.markdown("#### Players Needing More Time")

    if not fairness_df.empty:
        bottom_players = fairness_df.nsmallest(3, 'total_series_played')

        for idx, player in bottom_players.iterrows():
            st.write(f"**{player['name']}** - {player['total_series_played']} series")

st.markdown("---")

# Recommendations
st.markdown("### Recommendations for Next Game")

if not fairness_df.empty:
    avg_series = fairness_df['total_series_played'].mean()
    std_series = fairness_df['total_series_played'].std()

    if std_series > 1.5:
        st.warning("⚠️ Large variation in playing time detected. Consider:")
        st.markdown("- Prioritize less-used players in early series next game")
        st.markdown("- Review position assignments for better balance")
        st.markdown("- Check for availability issues that affected assignments")
    else:
        st.success("✅ Playing time was well-balanced!")

    # Check offense/defense balance
    for idx, player in fairness_df.iterrows():
        o_series = player['offense_series_played']
        d_series = player['defense_series_played']

        if o_series == 0 and d_series > 0:
            st.info(f"💡 {player['name']} played only defense - consider offense opportunities next game")
        elif d_series == 0 and o_series > 0:
            st.info(f"💡 {player['name']} played only offense - consider defense opportunities next game")

st.markdown("---")

with st.expander("ℹ️ How to Use"):
    st.markdown("""
    **Reviewing the Game:**
    - Check overall balance score to assess fairness
    - Review individual player statistics
    - Identify players who need more opportunities

    **Exporting Reports:**
    - **Lineups CSV:** Complete lineup for each series
    - **Fairness Report:** Playing time statistics for all players
    - **Game Summary:** Overall game info and metrics

    **Key Insights:**
    - See who played the most and least
    - Identify patterns in playing time
    - Get recommendations for next game

    **Using Reports:**
    - Share with parents to show playing time
    - Keep records for season analysis
    - Use data to improve future lineup generation

    **Next Steps:**
    - Review recommendations for next game
    - Update player ratings based on performance
    - Adjust availability for next game in Game Setup
    """)
