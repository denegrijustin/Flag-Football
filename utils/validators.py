"""Validators for lineup and player data."""

from typing import List, Dict, Tuple
import pandas as pd

from utils.config import OFFENSE_POSITIONS, DEFENSE_POSITIONS


def validate_lineup(series_type: str, lineup: Dict[str, str], roster_df: pd.DataFrame) -> List[str]:
    """Validate a lineup and return list of warnings."""
    warnings = []

    # Check for duplicate players
    players_in_lineup = [p for p in lineup.values() if p and p != ""]
    if len(players_in_lineup) != len(set(players_in_lineup)):
        warnings.append("⚠️ Duplicate player in lineup")

    # Check position coverage
    positions = OFFENSE_POSITIONS if series_type == "Offense" else DEFENSE_POSITIONS
    missing_positions = [pos for pos in positions if not lineup.get(pos)]

    if missing_positions:
        warnings.append(f"⚠️ Missing positions: {', '.join(missing_positions)}")

    # Check player availability
    for position, player_name in lineup.items():
        if not player_name or player_name == "":
            continue

        player_row = roster_df[roster_df['name'] == player_name]
        if player_row.empty:
            warnings.append(f"⚠️ Player {player_name} not found in roster")
            continue

        availability = player_row.iloc[0].get('availability', 'Available')
        if availability == 'Unavailable':
            warnings.append(f"⚠️ {player_name} is marked unavailable")
        elif availability == 'Late':
            warnings.append(f"⚠️ {player_name} is arriving late")
        elif availability == 'Leaving Early':
            warnings.append(f"⚠️ {player_name} is leaving early")

    return warnings


def validate_qb_assignment(qb_name: str, ratings_df: pd.DataFrame) -> List[str]:
    """Validate QB assignment and return warnings."""
    warnings = []

    if not qb_name:
        warnings.append("⚠️ No QB assigned")
        return warnings

    qb_row = ratings_df[ratings_df['name'] == qb_name]
    if qb_row.empty:
        warnings.append(f"⚠️ QB {qb_name} not found in ratings")
        return warnings

    qb_rating = qb_row.iloc[0].get('offense_rating', 'C')
    if qb_rating in ['D', 'F']:
        warnings.append(f"⚠️ QB {qb_name} has low rating: {qb_rating}")

    return warnings


def validate_center_assignment(center_name: str, ratings_df: pd.DataFrame) -> List[str]:
    """Validate center assignment and return warnings."""
    warnings = []

    if not center_name:
        return warnings

    center_row = ratings_df[ratings_df['name'] == center_name]
    if center_row.empty:
        return warnings

    center_rating = center_row.iloc[0].get('offense_rating', 'C')
    if center_rating in ['D', 'F']:
        warnings.append(f"⚠️ Center {center_name} has low rating: {center_rating}")

    return warnings


def check_fairness_balance(fairness_metrics: pd.DataFrame, threshold: int = 2) -> List[str]:
    """Check if playing time is balanced and return warnings."""
    warnings = []

    if fairness_metrics.empty:
        return warnings

    total_series = fairness_metrics['total_series_played']
    min_series = total_series.min()
    max_series = total_series.max()

    if max_series - min_series > threshold:
        warnings.append(f"⚠️ Large playing time imbalance: {min_series} to {max_series} series")

    return warnings


def check_consecutive_series(player_name: str, series_list: List[Dict], current_series: int) -> int:
    """Count consecutive series for a player up to current series."""
    consecutive = 0

    for i in range(current_series - 1, -1, -1):
        series = series_list[i]
        lineup = series.get('lineup', {})

        if player_name in lineup.values():
            consecutive += 1
        else:
            break

    return consecutive


def validate_consecutive_series(consecutive_count: int, threshold: int = 3) -> List[str]:
    """Validate consecutive series count and return warnings."""
    warnings = []

    if consecutive_count >= threshold:
        warnings.append(f"⚠️ Player has {consecutive_count} consecutive series")

    return warnings
