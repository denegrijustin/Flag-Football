"""Data models for the flag football lineup planner."""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime


@dataclass
class Player:
    """Represents a player on the roster."""
    name: str
    number: int
    grade: str  # "4th" or "5th"

    # Offense skills (1-5)
    offense_speed: float = 3.0
    offense_agility: float = 3.0
    offense_hands: float = 3.0
    offense_ball_handling: float = 3.0
    offense_route_running: float = 3.0
    offense_awareness: float = 3.0
    offense_confidence: float = 3.0
    offense_effort: float = 3.0

    # Defense skills (1-5)
    defense_speed: float = 3.0
    defense_flag_pulling: float = 3.0
    defense_pursuit: float = 3.0
    defense_awareness: float = 3.0
    defense_positioning: float = 3.0
    defense_aggression: float = 3.0
    defense_reaction_time: float = 3.0
    defense_effort: float = 3.0

    # Computed ratings
    offense_score: float = 0.0
    defense_score: float = 0.0
    overall_score: float = 0.0
    offense_rating: str = "C"
    defense_rating: str = "C"
    overall_rating: str = "C"

    # Position eligibility
    eligible_positions: List[str] = field(default_factory=list)

    # QB designation
    is_first_half_qb: bool = False
    is_second_half_qb: bool = False

    # Availability
    availability: str = "Available"  # Available, Unavailable, Late, Leaving Early

    # Stats tracking
    total_series_played: int = 0
    offense_series_played: int = 0
    defense_series_played: int = 0
    bench_count: int = 0


@dataclass
class Series:
    """Represents a single series (offense or defense)."""
    series_number: int
    series_type: str  # "Offense" or "Defense"
    half: int  # 1 or 2

    # Position assignments
    lineup: Dict[str, Optional[str]] = field(default_factory=dict)

    # Metadata
    is_locked: bool = False
    manually_edited: bool = False
    warnings: List[str] = field(default_factory=list)


@dataclass
class Game:
    """Represents a game configuration."""
    game_date: str = ""
    opponent: str = ""
    first_half_qb: Optional[str] = None
    second_half_qb: Optional[str] = None
    total_series: int = 6
    offense_series: int = 3
    defense_series: int = 3

    # Series data
    all_series: List[Series] = field(default_factory=list)

    # State
    lineup_is_stale: bool = True
    last_rating_update: Optional[datetime] = None


@dataclass
class FairnessMetrics:
    """Tracks fairness metrics for lineup generation."""
    player_name: str
    total_series_played: int
    offense_series_played: int
    defense_series_played: int
    bench_count: int
    consecutive_series: int
    fairness_score: float = 0.0
