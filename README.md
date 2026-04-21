# Flag Football Lineup Planner 🏈

A comprehensive Streamlit application for managing youth flag football rosters, player rankings, and generating fair, balanced lineups.

## Features

- **Roster Management**: Add, edit, and track players
- **Skill-Based Rankings**: Rate players on 8 offense and 8 defense skills
- **Automated Ratings**: Calculate composite scores and letter grades (A-F)
- **Position Recommendations**: AI-powered position fit analysis
- **Smart Lineup Generation**: Balance playing time while optimizing positions
- **Fairness Tracking**: Monitor playing time equity across all players
- **Live Adjustments**: Make real-time changes during games
- **Comprehensive Reports**: Export lineups, fairness reports, and game summaries

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/denegrijustin/Flag-Football.git
cd Flag-Football
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run main.py
```

The app will open in your default web browser at `http://localhost:8501`

## Usage Guide

### 1. Roster Setup
- Add players with name, number, and grade
- Edit player information as needed
- Set player availability for each game

### 2. Player Ranking Tool
- Rate each player on individual skills (1-5 scale)
- Offense skills: speed, agility, hands, ball handling, route running, awareness, confidence, effort
- Defense skills: speed, flag pulling, pursuit, awareness, positioning, aggression, reaction time, effort
- Ratings automatically calculate composite scores

### 3. Ratings and Eligibility
- View all player ratings (A, B, C, D, F)
- See position recommendations based on skills
- Set position eligibility for each player
- Designate first and second half quarterbacks

### 4. Game Setup and Attendance
- Set game date and opponent
- Configure number of series (default: 6 total, 3 offense, 3 defense)
- Select quarterbacks for each half
- Mark player availability (Available, Unavailable, Late, Leaving Early)

### 5. Series Planner
- Generate balanced lineups for all series
- View complete game plan
- Check fairness metrics
- Review warnings and issues

### 6. Live Game Adjustments
- Edit lineups during the game
- Quick player swap tool
- Regenerate future lineups
- Track real-time playing time

### 7. Postgame Summary
- Review final playing time statistics
- Analyze fairness and balance
- Export reports (CSV format)
- Get recommendations for next game

## Data Storage

The app stores data locally in the `data/` directory:
- `roster.csv`: Player roster
- `player_ratings.csv`: Skill ratings and scores
- `latest_game_state.json`: Current game configuration and lineups
- `config.json`: App configuration

## Rating System

### Skill Scale (1-5)
- **5 (Advanced)**: Elite skill level
- **4 (Strong)**: Above average
- **3 (Average)**: Adequate
- **2 (Developing)**: Below average
- **1 (Limited)**: Minimal skill

### Letter Grades
- **A**: 4.5+ (Elite)
- **B**: 3.5-4.49 (Strong)
- **C**: 2.5-3.49 (Average)
- **D**: 1.5-2.49 (Developing)
- **F**: Below 1.5 (Limited)

## Lineup Algorithm

The lineup generator:
1. Prioritizes players with less playing time
2. Assigns stronger players to key positions
3. Respects player availability
4. Enforces QB assignments
5. Balances offense and defense opportunities
6. Prevents duplicate assignments in same series

## Position Types

### Offense Positions
- Quarterback
- Running Back
- Slot 1 & 2
- Wide Receiver 1 & 2
- Center

### Defense Positions
- Linebacker 1, 2 & 3
- Cornerback 1 & 2
- Blitzer

## Technical Details

### Project Structure
```
Flag-Football/
├── main.py                 # Main entry point
├── pages/                  # Streamlit pages
│   ├── 1_Roster_Setup.py
│   ├── 2_Player_Ranking_Tool.py
│   ├── 3_Ratings_and_Eligibility.py
│   ├── 4_Game_Setup_and_Attendance.py
│   ├── 5_Series_Planner.py
│   ├── 6_Live_Game_Adjustments.py
│   └── 7_Postgame_Summary.py
├── utils/                  # Utility modules
│   ├── config.py          # Configuration constants
│   ├── models.py          # Data models
│   ├── storage.py         # File I/O operations
│   ├── ranking_engine.py  # Rating calculations
│   ├── lineup_engine.py   # Lineup generation
│   ├── fairness_engine.py # Fairness tracking
│   ├── position_fit.py    # Position recommendations
│   ├── validators.py      # Data validation
│   ├── visualizer.py      # Display utilities
│   └── exports.py         # Export functions
├── data/                   # Data storage (auto-created)
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

### Built With
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **Python**: Core programming language

## Sample Data

The app includes sample data for 10 players to help you get started. You can modify or replace this data in the Roster Setup page.

## Tips for Coaches

1. **Rate Players Honestly**: Accurate ratings lead to better lineups
2. **Update Throughout Season**: Player skills change - update ratings regularly
3. **Review Fairness**: Check playing time balance after each game
4. **Use Recommendations**: Position fit scores help optimize assignments
5. **Plan Ahead**: Generate lineups before the game for smooth execution
6. **Stay Flexible**: Use live adjustments for unexpected situations

## Troubleshooting

### App Won't Start
- Verify Python 3.8+ is installed: `python --version`
- Check all dependencies are installed: `pip install -r requirements.txt`
- Ensure no other process is using port 8501

### Data Not Saving
- Check that the `data/` directory exists and is writable
- Verify file permissions
- Look for error messages in the app

### Lineups Not Generating
- Ensure roster has at least 7 players
- Check that game setup is complete
- Verify player ratings are set
- Confirm QBs are designated

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is available for use in youth sports programs.

## Support

For issues or questions, please open an issue on GitHub.

## Version

**v1.0** - Initial release

---

Built with ❤️ for youth flag football coaches and players
