"""Position fit scoring for recommending best positions for each player."""

import pandas as pd
from typing import Dict, List, Tuple

from utils.config import POSITION_FIT_WEIGHTS


def calculate_position_fit_score(player_skills: Dict[str, float], position: str) -> float:
    """Calculate fit score for a player in a specific position."""
    if position not in POSITION_FIT_WEIGHTS:
        # Map generic position names to specific ones
        position_map = {
            'running back': 'running back',
            'quarterback': 'quarterback',
            'wide receiver 1': 'wide receiver',
            'wide receiver 2': 'wide receiver',
            'slot 1': 'wide receiver',
            'slot 2': 'wide receiver',
            'center': 'wide receiver',  # Center needs similar skills to receivers
            'linebacker 1': 'linebacker',
            'linebacker 2': 'linebacker',
            'linebacker 3': 'linebacker',
            'cornerback 1': 'cornerback',
            'cornerback 2': 'cornerback',
            'blitzer': 'blitzer'
        }
        position_key = position_map.get(position, position)
    else:
        position_key = position

    if position_key not in POSITION_FIT_WEIGHTS:
        return 0.0

    weights = POSITION_FIT_WEIGHTS[position_key]
    score = 0.0

    for skill, weight in weights.items():
        # Try to find the skill value (could be offense_ or defense_ prefixed)
        offense_skill = f"offense_{skill}"
        defense_skill = f"defense_{skill}"

        if offense_skill in player_skills:
            score += weight * player_skills[offense_skill]
        elif defense_skill in player_skills:
            score += weight * player_skills[defense_skill]

    return round(score, 2)


def get_best_positions_for_player(player_skills: Dict[str, float], top_n: int = 3) -> List[Tuple[str, float]]:
    """Get the top N best-fit positions for a player."""
    position_scores = []

    # Calculate score for each unique position type
    position_types = {
        'quarterback': 'quarterback',
        'running back': 'running back',
        'wide receiver': 'wide receiver',
        'linebacker': 'linebacker',
        'cornerback': 'cornerback',
        'blitzer': 'blitzer'
    }

    for position_type in position_types.keys():
        score = calculate_position_fit_score(player_skills, position_type)
        position_scores.append((position_type, score))

    # Sort by score descending
    position_scores.sort(key=lambda x: x[1], reverse=True)

    return position_scores[:top_n]


def generate_position_recommendations(ratings_df: pd.DataFrame) -> pd.DataFrame:
    """Generate position recommendations for all players."""
    recommendations = []

    for _, player in ratings_df.iterrows():
        player_skills = player.to_dict()
        top_positions = get_best_positions_for_player(player_skills, top_n=3)

        recommendations.append({
            'name': player['name'],
            'top_position_1': top_positions[0][0] if len(top_positions) > 0 else '',
            'top_position_1_score': top_positions[0][1] if len(top_positions) > 0 else 0.0,
            'top_position_2': top_positions[1][0] if len(top_positions) > 1 else '',
            'top_position_2_score': top_positions[1][1] if len(top_positions) > 1 else 0.0,
            'top_position_3': top_positions[2][0] if len(top_positions) > 2 else '',
            'top_position_3_score': top_positions[2][1] if len(top_positions) > 2 else 0.0,
        })

    return pd.DataFrame(recommendations)
