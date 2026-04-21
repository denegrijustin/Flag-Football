"""Export utilities for generating CSV files."""

import pandas as pd
from typing import List, Dict
from datetime import datetime
import os

from utils.config import DATA_DIR


def export_lineups_to_csv(all_series: List[Dict], filename: str = None) -> str:
    """Export lineups to CSV file."""

    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"lineups_{timestamp}.csv"

    export_data = []

    for series in all_series:
        series_num = series['series_number']
        series_type = series['series_type']
        half = series['half']
        lineup = series['lineup']

        for position, player in lineup.items():
            export_data.append({
                'Series': series_num,
                'Type': series_type,
                'Half': half,
                'Position': position,
                'Player': player if player else ""
            })

    export_df = pd.DataFrame(export_data)

    filepath = DATA_DIR / filename
    export_df.to_csv(filepath, index=False)

    return str(filepath)


def export_fairness_report(fairness_df: pd.DataFrame, filename: str = None) -> str:
    """Export fairness report to CSV file."""

    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"fairness_report_{timestamp}.csv"

    filepath = DATA_DIR / filename
    fairness_df.to_csv(filepath, index=False)

    return str(filepath)


def export_player_ratings(ratings_df: pd.DataFrame, filename: str = None) -> str:
    """Export player ratings to CSV file."""

    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"player_ratings_{timestamp}.csv"

    filepath = DATA_DIR / filename
    ratings_df.to_csv(filepath, index=False)

    return str(filepath)


def export_game_summary(
    all_series: List[Dict],
    fairness_df: pd.DataFrame,
    game_info: Dict,
    filename: str = None
) -> str:
    """Export comprehensive game summary to CSV."""

    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"game_summary_{timestamp}.csv"

    # Create summary data
    summary_data = []

    # Game info section
    summary_data.append({
        'Section': 'Game Info',
        'Key': 'Date',
        'Value': game_info.get('game_date', '')
    })
    summary_data.append({
        'Section': 'Game Info',
        'Key': 'Opponent',
        'Value': game_info.get('opponent', '')
    })
    summary_data.append({
        'Section': 'Game Info',
        'Key': 'Total Series',
        'Value': game_info.get('total_series', 6)
    })

    # Fairness section
    summary_data.append({
        'Section': 'Fairness',
        'Key': 'Average Series Per Player',
        'Value': f"{fairness_df['total_series_played'].mean():.2f}" if not fairness_df.empty else "0"
    })
    summary_data.append({
        'Section': 'Fairness',
        'Key': 'Min Series',
        'Value': fairness_df['total_series_played'].min() if not fairness_df.empty else 0
    })
    summary_data.append({
        'Section': 'Fairness',
        'Key': 'Max Series',
        'Value': fairness_df['total_series_played'].max() if not fairness_df.empty else 0
    })

    summary_df = pd.DataFrame(summary_data)

    filepath = DATA_DIR / filename
    summary_df.to_csv(filepath, index=False)

    return str(filepath)
