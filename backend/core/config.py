from pathlib import Path

# Root directory of the project
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Data directories
DATA_DIR = PROJECT_ROOT / "data"
DATABASE_DIR = PROJECT_ROOT / "database"
LOGS_DIR = PROJECT_ROOT / "logs"

# Automatically create folders if missing
DATA_DIR.mkdir(exist_ok=True)
DATABASE_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

APP_NAME = "LAW TRADER"
VERSION = "1.0.0"

# ==========================
# AI Decision Thresholds
# ==========================

BUY_SCORE = 6
HOLD_SCORE = -2
AVOID_SCORE = -3

# ==========================
# Confidence Score
# ==========================

MAX_AI_SCORE = 14

