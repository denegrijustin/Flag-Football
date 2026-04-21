"""Storage utilities for saving and loading data."""

import pandas as pd
import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

from utils.config import ROSTER_FILE, RATINGS_FILE, GAME_STATE_FILE, CONFIG_FILE, DATA_DIR


def ensure_data_dir():
    """Ensure data directory exists."""
    DATA_DIR.mkdir(exist_ok=True)


def save_roster(roster_df: pd.DataFrame):
    """Save roster to CSV."""
    ensure_data_dir()
    roster_df.to_csv(ROSTER_FILE, index=False)


def load_roster() -> pd.DataFrame:
    """Load roster from CSV or create sample data."""
    ensure_data_dir()

    if ROSTER_FILE.exists():
        return pd.read_csv(ROSTER_FILE)

    # Create sample roster
    sample_roster = pd.DataFrame({
        'name': [
            'Emma Johnson', 'Sophia Williams', 'Olivia Brown', 'Ava Davis',
            'Isabella Miller', 'Mia Wilson', 'Charlotte Moore', 'Amelia Taylor',
            'Harper Anderson', 'Evelyn Thomas'
        ],
        'number': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'grade': ['4th', '5th', '4th', '5th', '4th', '5th', '4th', '5th', '4th', '5th'],
        'availability': ['Available'] * 10
    })

    save_roster(sample_roster)
    return sample_roster


def save_ratings(ratings_df: pd.DataFrame):
    """Save player ratings to CSV."""
    ensure_data_dir()
    ratings_df.to_csv(RATINGS_FILE, index=False)


def load_ratings() -> pd.DataFrame:
    """Load player ratings from CSV or create default."""
    ensure_data_dir()

    if RATINGS_FILE.exists():
        return pd.read_csv(RATINGS_FILE)

    # Create default ratings for sample roster
    roster_df = load_roster()

    ratings_data = []
    for _, player in roster_df.iterrows():
        ratings_data.append({
            'name': player['name'],
            # Offense skills
            'offense_speed': 3.0,
            'offense_agility': 3.0,
            'offense_hands': 3.0,
            'offense_ball_handling': 3.0,
            'offense_route_running': 3.0,
            'offense_awareness': 3.0,
            'offense_confidence': 3.0,
            'offense_effort': 3.0,
            # Defense skills
            'defense_speed': 3.0,
            'defense_flag_pulling': 3.0,
            'defense_pursuit': 3.0,
            'defense_awareness': 3.0,
            'defense_positioning': 3.0,
            'defense_aggression': 3.0,
            'defense_reaction_time': 3.0,
            'defense_effort': 3.0,
            # Computed scores
            'offense_score': 3.0,
            'defense_score': 3.0,
            'overall_score': 3.0,
            'offense_rating': 'C',
            'defense_rating': 'C',
            'overall_rating': 'C',
            # Position eligibility (empty for now)
            'eligible_positions': '',
            # QB designation
            'is_first_half_qb': False,
            'is_second_half_qb': False
        })

    ratings_df = pd.DataFrame(ratings_data)
    save_ratings(ratings_df)
    return ratings_df


def save_game_state(game_state: Dict):
    """Save game state to JSON."""
    ensure_data_dir()

    # Convert datetime objects to strings
    if 'last_rating_update' in game_state and game_state['last_rating_update']:
        if isinstance(game_state['last_rating_update'], datetime):
            game_state['last_rating_update'] = game_state['last_rating_update'].isoformat()

    with open(GAME_STATE_FILE, 'w') as f:
        json.dump(game_state, f, indent=2)


def load_game_state() -> Dict:
    """Load game state from JSON or create default."""
    ensure_data_dir()

    if GAME_STATE_FILE.exists():
        with open(GAME_STATE_FILE, 'r') as f:
            state = json.load(f)

            # Convert string back to datetime if present
            if 'last_rating_update' in state and state['last_rating_update']:
                state['last_rating_update'] = datetime.fromisoformat(state['last_rating_update'])

            return state

    # Create default game state
    default_state = {
        'game_date': '',
        'opponent': '',
        'first_half_qb': None,
        'second_half_qb': None,
        'total_series': 6,
        'offense_series': 3,
        'defense_series': 3,
        'all_series': [],
        'lineup_is_stale': True,
        'last_rating_update': None
    }

    save_game_state(default_state)
    return default_state


def save_config(config: Dict):
    """Save configuration to JSON."""
    ensure_data_dir()
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)


def load_config() -> Dict:
    """Load configuration from JSON or create default."""
    ensure_data_dir()

    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)

    # Create default config
    default_config = {
        'app_title': 'Flag Football Lineup Planner',
        'team_name': '4th/5th Grade Girls Flag Football',
        'default_series': 6,
        'enable_warnings': True
    }

    save_config(default_config)
    return default_config


def get_player_data(player_name: str, roster_df: pd.DataFrame, ratings_df: pd.DataFrame) -> Optional[Dict]:
    """Get combined player data from roster and ratings."""
    roster_row = roster_df[roster_df['name'] == player_name]
    ratings_row = ratings_df[ratings_df['name'] == player_name]

    if roster_row.empty or ratings_row.empty:
        return None

    player_data = {**roster_row.iloc[0].to_dict(), **ratings_row.iloc[0].to_dict()}
    return player_data
