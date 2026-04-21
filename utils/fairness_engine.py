"""Fairness engine for tracking and balancing playing time."""

import pandas as pd
from typing import List, Dict


def calculate_fairness_metrics(roster_df: pd.DataFrame, all_series: List[Dict]) -> pd.DataFrame:
    """Calculate fairness metrics for all players."""
    metrics = []

    for _, player in roster_df.iterrows():
        player_name = player['name']

        total_series = 0
        offense_series = 0
        defense_series = 0
        bench_count = 0
        consecutive = 0
        last_played = -999

        for idx, series in enumerate(all_series):
            lineup = series.get('lineup', {})
            series_type = series.get('series_type', 'Offense')

            if player_name in lineup.values():
                total_series += 1
                if series_type == 'Offense':
                    offense_series += 1
                else:
                    defense_series += 1

                if last_played == idx - 1:
                    consecutive += 1
                else:
                    consecutive = 1

                last_played = idx
            else:
                bench_count += 1

        fairness_score = calculate_player_fairness_score(total_series, bench_count, consecutive)

        metrics.append({
            'name': player_name,
            'total_series_played': total_series,
            'offense_series_played': offense_series,
            'defense_series_played': defense_series,
            'bench_count': bench_count,
            'consecutive_series': consecutive,
            'fairness_score': fairness_score
        })

    return pd.DataFrame(metrics)


def calculate_player_fairness_score(total_series: int, bench_count: int, consecutive: int) -> float:
    """Calculate a fairness score for a player (higher is more fair)."""
    # Penalize for low total series
    series_penalty = max(0, 6 - total_series) * 2

    # Penalize for high bench count
    bench_penalty = bench_count * 0.5

    # Penalize for high consecutive series
    consecutive_penalty = max(0, consecutive - 2) * 1.5

    fairness_score = 100 - series_penalty - bench_penalty - consecutive_penalty
    return round(max(0, fairness_score), 1)


def get_players_needing_playtime(fairness_df: pd.DataFrame, roster_df: pd.DataFrame, top_n: int = 5) -> List[str]:
    """Get list of players who need more playing time."""
    # Filter out unavailable players
    available_players = roster_df[roster_df['availability'] == 'Available']['name'].tolist()

    fairness_df_available = fairness_df[fairness_df['name'].isin(available_players)].copy()

    # Sort by total series played (ascending)
    fairness_df_available = fairness_df_available.sort_values('total_series_played')

    return fairness_df_available.head(top_n)['name'].tolist()


def get_players_with_most_playtime(fairness_df: pd.DataFrame, top_n: int = 5) -> List[str]:
    """Get list of players with most playing time."""
    # Sort by total series played (descending)
    fairness_df_sorted = fairness_df.sort_values('total_series_played', ascending=False)

    return fairness_df_sorted.head(top_n)['name'].tolist()


def balance_score(fairness_df: pd.DataFrame) -> float:
    """Calculate overall balance score (0-100, higher is better)."""
    if fairness_df.empty:
        return 100.0

    total_series = fairness_df['total_series_played']

    # Calculate standard deviation
    std_dev = total_series.std()

    # Lower std dev = better balance
    # Scale to 0-100 score
    balance = max(0, 100 - (std_dev * 20))

    return round(balance, 1)
