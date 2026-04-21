"""Ranking engine for calculating player scores and ratings."""

import pandas as pd
from typing import Dict

from utils.config import (
    OFFENSE_SKILLS,
    DEFENSE_SKILLS,
    OFFENSE_WEIGHTS,
    DEFENSE_WEIGHTS,
    RATING_THRESHOLDS
)


def calculate_offense_score(skill_values: Dict[str, float]) -> float:
    """Calculate weighted offense score."""
    score = 0.0
    for skill in OFFENSE_SKILLS:
        weight = OFFENSE_WEIGHTS.get(skill, 0.0)
        value = skill_values.get(f"offense_{skill}", 3.0)
        score += weight * value
    return round(score, 2)


def calculate_defense_score(skill_values: Dict[str, float]) -> float:
    """Calculate weighted defense score."""
    score = 0.0
    for skill in DEFENSE_SKILLS:
        weight = DEFENSE_WEIGHTS.get(skill, 0.0)
        value = skill_values.get(f"defense_{skill}", 3.0)
        score += weight * value
    return round(score, 2)


def calculate_overall_score(offense_score: float, defense_score: float) -> float:
    """Calculate overall score as average of offense and defense."""
    return round((offense_score + defense_score) / 2.0, 2)


def score_to_rating(score: float) -> str:
    """Convert numeric score to letter rating."""
    if score >= RATING_THRESHOLDS['A']:
        return 'A'
    elif score >= RATING_THRESHOLDS['B']:
        return 'B'
    elif score >= RATING_THRESHOLDS['C']:
        return 'C'
    elif score >= RATING_THRESHOLDS['D']:
        return 'D'
    else:
        return 'F'


def calculate_all_ratings(ratings_df: pd.DataFrame) -> pd.DataFrame:
    """Calculate all scores and ratings for all players."""
    updated_df = ratings_df.copy()

    for idx, row in updated_df.iterrows():
        # Calculate scores
        offense_score = calculate_offense_score(row.to_dict())
        defense_score = calculate_defense_score(row.to_dict())
        overall_score = calculate_overall_score(offense_score, defense_score)

        # Convert to ratings
        offense_rating = score_to_rating(offense_score)
        defense_rating = score_to_rating(defense_score)
        overall_rating = score_to_rating(overall_score)

        # Update dataframe
        updated_df.at[idx, 'offense_score'] = offense_score
        updated_df.at[idx, 'defense_score'] = defense_score
        updated_df.at[idx, 'overall_score'] = overall_score
        updated_df.at[idx, 'offense_rating'] = offense_rating
        updated_df.at[idx, 'defense_rating'] = defense_rating
        updated_df.at[idx, 'overall_rating'] = overall_rating

    return updated_df


def recalculate_single_player(player_name: str, ratings_df: pd.DataFrame) -> pd.DataFrame:
    """Recalculate ratings for a single player."""
    updated_df = ratings_df.copy()
    player_idx = updated_df[updated_df['name'] == player_name].index

    if len(player_idx) == 0:
        return updated_df

    idx = player_idx[0]
    row = updated_df.loc[idx]

    # Calculate scores
    offense_score = calculate_offense_score(row.to_dict())
    defense_score = calculate_defense_score(row.to_dict())
    overall_score = calculate_overall_score(offense_score, defense_score)

    # Convert to ratings
    offense_rating = score_to_rating(offense_score)
    defense_rating = score_to_rating(defense_score)
    overall_rating = score_to_rating(overall_score)

    # Update dataframe
    updated_df.at[idx, 'offense_score'] = offense_score
    updated_df.at[idx, 'defense_score'] = defense_score
    updated_df.at[idx, 'overall_score'] = overall_score
    updated_df.at[idx, 'offense_rating'] = offense_rating
    updated_df.at[idx, 'defense_rating'] = defense_rating
    updated_df.at[idx, 'overall_rating'] = overall_rating

    return updated_df
