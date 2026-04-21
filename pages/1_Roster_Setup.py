"""Roster Setup page for managing team roster."""

import streamlit as st
import pandas as pd

from utils.storage import load_roster, save_roster, load_ratings, save_ratings
from utils.ranking_engine import calculate_all_ratings

st.set_page_config(page_title="Roster Setup", page_icon="📋", layout="wide")

st.title("📋 Roster Setup")
st.markdown("Add, edit, and manage your team roster.")

# Load roster
if 'roster_df' not in st.session_state or st.session_state.roster_df is None:
    st.session_state.roster_df = load_roster()

roster_df = st.session_state.roster_df

# Display current roster
st.markdown("### Current Roster")

# Editable roster table
edited_roster = st.data_editor(
    roster_df,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "name": st.column_config.TextColumn("Player Name", required=True),
        "number": st.column_config.NumberColumn("Number", min_value=0, max_value=99, required=True),
        "grade": st.column_config.SelectboxColumn("Grade", options=["4th", "5th"], required=True),
        "availability": st.column_config.SelectboxColumn(
            "Availability",
            options=["Available", "Unavailable", "Late", "Leaving Early"],
            default="Available"
        )
    },
    key="roster_editor"
)

# Save button
col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    if st.button("💾 Save Roster", type="primary"):
        # Update session state
        st.session_state.roster_df = edited_roster

        # Save to file
        save_roster(edited_roster)

        # Update ratings file if needed (add new players)
        ratings_df = load_ratings()
        existing_names = set(ratings_df['name'].tolist())
        new_names = set(edited_roster['name'].tolist())

        # Add new players to ratings
        new_players = new_names - existing_names
        if new_players:
            new_ratings = []
            for name in new_players:
                new_ratings.append({
                    'name': name,
                    'offense_speed': 3.0,
                    'offense_agility': 3.0,
                    'offense_hands': 3.0,
                    'offense_ball_handling': 3.0,
                    'offense_route_running': 3.0,
                    'offense_awareness': 3.0,
                    'offense_confidence': 3.0,
                    'offense_effort': 3.0,
                    'defense_speed': 3.0,
                    'defense_flag_pulling': 3.0,
                    'defense_pursuit': 3.0,
                    'defense_awareness': 3.0,
                    'defense_positioning': 3.0,
                    'defense_aggression': 3.0,
                    'defense_reaction_time': 3.0,
                    'defense_effort': 3.0,
                    'offense_score': 3.0,
                    'defense_score': 3.0,
                    'overall_score': 3.0,
                    'offense_rating': 'C',
                    'defense_rating': 'C',
                    'overall_rating': 'C',
                    'eligible_positions': '',
                    'is_first_half_qb': False,
                    'is_second_half_qb': False
                })

            new_ratings_df = pd.DataFrame(new_ratings)
            ratings_df = pd.concat([ratings_df, new_ratings_df], ignore_index=True)

        # Remove deleted players from ratings
        deleted_players = existing_names - new_names
        if deleted_players:
            ratings_df = ratings_df[~ratings_df['name'].isin(deleted_players)]

        # Save updated ratings
        save_ratings(ratings_df)
        st.session_state.ratings_df = ratings_df

        st.success("✅ Roster saved successfully!")
        st.rerun()

with col2:
    if st.button("🔄 Reload from File"):
        st.session_state.roster_df = load_roster()
        st.success("✅ Roster reloaded!")
        st.rerun()

st.markdown("---")

# Roster statistics
st.markdown("### Roster Statistics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_players = len(roster_df)
    st.metric("Total Players", total_players)

with col2:
    fourth_grade = len(roster_df[roster_df['grade'] == '4th'])
    st.metric("4th Graders", fourth_grade)

with col3:
    fifth_grade = len(roster_df[roster_df['grade'] == '5th'])
    st.metric("5th Graders", fifth_grade)

with col4:
    available = len(roster_df[roster_df['availability'] == 'Available'])
    st.metric("Available", available)

st.markdown("---")

# Instructions
with st.expander("ℹ️ How to Use"):
    st.markdown("""
    **Adding Players:**
    - Click the "+" button at the bottom of the table to add a new row
    - Fill in the player's name, number, and grade
    - Click "Save Roster" to save changes

    **Editing Players:**
    - Click any cell to edit the value
    - Use the dropdown for grade and availability
    - Click "Save Roster" to save changes

    **Deleting Players:**
    - Click the checkbox on the left of the row
    - Press Delete key or click the delete button
    - Click "Save Roster" to save changes

    **Notes:**
    - Player numbers should be unique
    - Grade should be "4th" or "5th"
    - Availability affects lineup generation
    - Changes are automatically synced with ratings
    """)
