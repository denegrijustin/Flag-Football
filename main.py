"""Main entry point for the Flag Football Lineup Planner."""

import streamlit as st
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Flag Football Lineup Planner",
    page_icon="🏈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.roster_df = None
    st.session_state.ratings_df = None
    st.session_state.game_state = None
    st.session_state.lineup_is_stale = True

# Main page
st.title("🏈 Flag Football Lineup Planner")
st.markdown("### 4th and 5th Grade Girls Flag Football")

st.markdown("""
Welcome to the Flag Football Lineup Planner! This app helps coaches manage their roster,
track player skills, and generate fair and balanced lineups for games.

### How to Use This App:

1. **Roster Setup**: Add, edit, and manage your team roster
2. **Player Ranking Tool**: Rate players on individual skills (1-5 scale)
3. **Ratings and Eligibility**: View calculated ratings and set position eligibility
4. **Game Setup and Attendance**: Configure game details and mark player availability
5. **Series Planner**: Generate balanced lineups for the entire game
6. **Live Game Adjustments**: Make real-time changes during the game
7. **Postgame Summary**: Review playing time and export reports

### Getting Started:

Use the sidebar to navigate between pages. Start with **Roster Setup** to add your players,
then move to **Player Ranking Tool** to rate their skills.

The app automatically saves your data locally, so you can close and reopen it without losing progress.
""")

st.markdown("---")

# Quick stats
col1, col2, col3 = st.columns(3)

with col1:
    st.info("📋 **Current Features**\n\n- Roster Management\n- Skill-Based Rankings\n- Auto Lineup Generation\n- Fairness Tracking")

with col2:
    st.info("🎯 **Key Goals**\n\n- Balance Playing Time\n- Position-Based Assignments\n- Real-Time Adjustments\n- Export Reports")

with col3:
    st.info("⚡ **Quick Actions**\n\n1. Setup Roster\n2. Rank Players\n3. Generate Lineups\n4. Track Fairness")

st.markdown("---")
st.caption("Built with Streamlit | Flag Football Lineup Planner v1.0")
