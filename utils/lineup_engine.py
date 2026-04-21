"""Lineup generation engine for creating balanced lineups."""

import pandas as pd
from typing import List, Dict, Optional
import random

from utils.config import OFFENSE_POSITIONS, DEFENSE_POSITIONS
from utils.validators import validate_lineup, validate_qb_assignment


def generate_all_lineups(
    roster_df: pd.DataFrame,
    ratings_df: pd.DataFrame,
    total_series: int,
    offense_series: int,
    defense_series: int,
    first_half_qb: Optional[str],
    second_half_qb: Optional[str]
) -> List[Dict]:
    """Generate lineups for all series."""

    all_series = []
    series_num = 1

    # Generate offense series
    for i in range(offense_series):
        half = 1 if i < offense_series // 2 else 2
        qb = first_half_qb if half == 1 else second_half_qb

        lineup = generate_offense_lineup(
            roster_df=roster_df,
            ratings_df=ratings_df,
            assigned_qb=qb,
            series_number=series_num,
            all_series=all_series
        )

        warnings = validate_lineup('Offense', lineup, roster_df)
        if qb:
            warnings.extend(validate_qb_assignment(qb, ratings_df))

        all_series.append({
            'series_number': series_num,
            'series_type': 'Offense',
            'half': half,
            'lineup': lineup,
            'is_locked': False,
            'manually_edited': False,
            'warnings': warnings
        })

        series_num += 1

    # Generate defense series
    for i in range(defense_series):
        half = 1 if i < defense_series // 2 else 2

        lineup = generate_defense_lineup(
            roster_df=roster_df,
            ratings_df=ratings_df,
            series_number=series_num,
            all_series=all_series
        )

        warnings = validate_lineup('Defense', lineup, roster_df)

        all_series.append({
            'series_number': series_num,
            'series_type': 'Defense',
            'half': half,
            'lineup': lineup,
            'is_locked': False,
            'manually_edited': False,
            'warnings': warnings
        })

        series_num += 1

    return all_series


def generate_offense_lineup(
    roster_df: pd.DataFrame,
    ratings_df: pd.DataFrame,
    assigned_qb: Optional[str],
    series_number: int,
    all_series: List[Dict]
) -> Dict[str, str]:
    """Generate a single offense lineup."""

    lineup = {}

    # Get available players
    available_players = get_available_players(roster_df, ratings_df, all_series, series_number)

    # Assign QB first
    if assigned_qb and assigned_qb in available_players['name'].values:
        lineup['quarterback'] = assigned_qb
        available_players = available_players[available_players['name'] != assigned_qb]
    else:
        # Pick best available QB
        best_qb = available_players.nlargest(1, 'offense_score')
        if not best_qb.empty:
            lineup['quarterback'] = best_qb.iloc[0]['name']
            available_players = available_players[available_players['name'] != lineup['quarterback']]

    # Assign other positions by offense score
    remaining_positions = [p for p in OFFENSE_POSITIONS if p != 'quarterback']

    for position in remaining_positions:
        if available_players.empty:
            lineup[position] = ""
            continue

        # Pick best available player
        best_player = available_players.nlargest(1, 'offense_score')
        if not best_player.empty:
            lineup[position] = best_player.iloc[0]['name']
            available_players = available_players[available_players['name'] != lineup[position]]
        else:
            lineup[position] = ""

    return lineup


def generate_defense_lineup(
    roster_df: pd.DataFrame,
    ratings_df: pd.DataFrame,
    series_number: int,
    all_series: List[Dict]
) -> Dict[str, str]:
    """Generate a single defense lineup."""

    lineup = {}

    # Get available players
    available_players = get_available_players(roster_df, ratings_df, all_series, series_number)

    # Assign positions by defense score
    for position in DEFENSE_POSITIONS:
        if available_players.empty:
            lineup[position] = ""
            continue

        # Pick best available player
        best_player = available_players.nlargest(1, 'defense_score')
        if not best_player.empty:
            lineup[position] = best_player.iloc[0]['name']
            available_players = available_players[available_players['name'] != lineup[position]]
        else:
            lineup[position] = ""

    return lineup


def get_available_players(
    roster_df: pd.DataFrame,
    ratings_df: pd.DataFrame,
    all_series: List[Dict],
    current_series: int
) -> pd.DataFrame:
    """Get players available for assignment, prioritizing those with less playing time."""

    # Merge roster and ratings
    merged = pd.merge(roster_df, ratings_df, on='name', how='inner')

    # Filter out unavailable players
    merged = merged[merged['availability'] == 'Available']

    # Calculate playing time for each player
    playing_time = calculate_playing_time(merged['name'].tolist(), all_series[:current_series - 1])

    # Add playing time to dataframe
    merged['_total_series'] = merged['name'].map(playing_time)
    merged['_total_series'] = merged['_total_series'].fillna(0)

    # Sort by playing time (ascending) then by score (descending)
    # This prioritizes players with less playing time
    merged = merged.sort_values(['_total_series', 'overall_score'], ascending=[True, False])

    return merged


def calculate_playing_time(player_names: List[str], series_list: List[Dict]) -> Dict[str, int]:
    """Calculate total series played for each player."""
    playing_time = {name: 0 for name in player_names}

    for series in series_list:
        lineup = series.get('lineup', {})
        for player_name in lineup.values():
            if player_name in playing_time:
                playing_time[player_name] += 1

    return playing_time


def regenerate_future_lineups(
    all_series: List[Dict],
    current_series: int,
    roster_df: pd.DataFrame,
    ratings_df: pd.DataFrame,
    first_half_qb: Optional[str],
    second_half_qb: Optional[str]
) -> List[Dict]:
    """Regenerate lineups for series after current_series."""

    updated_series = all_series[:current_series].copy()

    for series in all_series[current_series:]:
        series_type = series['series_type']
        half = series['half']
        series_number = series['series_number']

        if series_type == 'Offense':
            qb = first_half_qb if half == 1 else second_half_qb
            lineup = generate_offense_lineup(
                roster_df=roster_df,
                ratings_df=ratings_df,
                assigned_qb=qb,
                series_number=series_number,
                all_series=updated_series
            )
            warnings = validate_lineup('Offense', lineup, roster_df)
            if qb:
                warnings.extend(validate_qb_assignment(qb, ratings_df))
        else:
            lineup = generate_defense_lineup(
                roster_df=roster_df,
                ratings_df=ratings_df,
                series_number=series_number,
                all_series=updated_series
            )
            warnings = validate_lineup('Defense', lineup, roster_df)

        updated_series.append({
            'series_number': series_number,
            'series_type': series_type,
            'half': half,
            'lineup': lineup,
            'is_locked': series.get('is_locked', False),
            'manually_edited': False,
            'warnings': warnings
        })

    return updated_series
