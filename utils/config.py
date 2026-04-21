"""Configuration constants for the flag football lineup planner."""

from pathlib import Path

# Directories
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
PAGES_DIR = BASE_DIR / "pages"
UTILS_DIR = BASE_DIR / "utils"

# Data files
ROSTER_FILE = DATA_DIR / "roster.csv"
RATINGS_FILE = DATA_DIR / "player_ratings.csv"
GAME_STATE_FILE = DATA_DIR / "latest_game_state.json"
CONFIG_FILE = DATA_DIR / "config.json"

# Ensure data directory exists
DATA_DIR.mkdir(exist_ok=True)

# Position definitions
OFFENSE_POSITIONS = [
    "quarterback",
    "running back",
    "slot 1",
    "slot 2",
    "wide receiver 1",
    "wide receiver 2",
    "center"
]

DEFENSE_POSITIONS = [
    "linebacker 1",
    "linebacker 2",
    "linebacker 3",
    "cornerback 1",
    "cornerback 2",
    "blitzer"
]

ALL_POSITIONS = OFFENSE_POSITIONS + DEFENSE_POSITIONS

# Offense skill categories
OFFENSE_SKILLS = [
    "speed",
    "agility",
    "hands",
    "ball_handling",
    "route_running",
    "awareness",
    "confidence",
    "effort"
]

# Defense skill categories
DEFENSE_SKILLS = [
    "speed",
    "flag_pulling",
    "pursuit",
    "awareness",
    "positioning",
    "aggression",
    "reaction_time",
    "effort"
]

# Offense skill weights
OFFENSE_WEIGHTS = {
    "speed": 0.15,
    "agility": 0.10,
    "hands": 0.20,
    "ball_handling": 0.15,
    "route_running": 0.10,
    "awareness": 0.10,
    "confidence": 0.10,
    "effort": 0.10
}

# Defense skill weights
DEFENSE_WEIGHTS = {
    "speed": 0.15,
    "flag_pulling": 0.20,
    "pursuit": 0.15,
    "awareness": 0.15,
    "positioning": 0.10,
    "aggression": 0.10,
    "reaction_time": 0.05,
    "effort": 0.10
}

# Position fit weights
POSITION_FIT_WEIGHTS = {
    "quarterback": {
        "awareness": 0.25,
        "confidence": 0.20,
        "ball_handling": 0.20,
        "hands": 0.10,
        "agility": 0.10,
        "effort": 0.15
    },
    "running back": {
        "speed": 0.25,
        "agility": 0.25,
        "ball_handling": 0.20,
        "awareness": 0.10,
        "effort": 0.20
    },
    "wide receiver": {
        "speed": 0.25,
        "hands": 0.25,
        "route_running": 0.25,
        "awareness": 0.10,
        "effort": 0.15
    },
    "linebacker": {
        "flag_pulling": 0.25,
        "pursuit": 0.25,
        "awareness": 0.20,
        "speed": 0.15,
        "effort": 0.15
    },
    "cornerback": {
        "speed": 0.30,
        "reaction_time": 0.20,
        "positioning": 0.20,
        "flag_pulling": 0.15,
        "effort": 0.15
    },
    "blitzer": {
        "aggression": 0.25,
        "speed": 0.25,
        "pursuit": 0.20,
        "flag_pulling": 0.15,
        "effort": 0.15
    }
}

# Rating thresholds
RATING_THRESHOLDS = {
    'A': 4.5,
    'B': 3.5,
    'C': 2.5,
    'D': 1.5,
    'F': 0.0
}

# Rating colors
RATING_COLORS = {
    'A': '#006400',  # dark green
    'B': '#228B22',  # green
    'C': '#FFD700',  # yellow
    'D': '#FF8C00',  # orange
    'F': '#DC143C'   # red
}

# Game defaults
DEFAULT_TOTAL_SERIES = 6
DEFAULT_OFFENSE_SERIES = 3
DEFAULT_DEFENSE_SERIES = 3
EXPECTED_ROSTER_SIZE = 10

# Skill scale
SKILL_MIN = 1
SKILL_MAX = 5
