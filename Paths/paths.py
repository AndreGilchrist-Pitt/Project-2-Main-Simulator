from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Main directories
SRC_DIR = PROJECT_ROOT / "Src"
UTILS_DIR = SRC_DIR / "Utils"
CLASSES_DIR = UTILS_DIR / "Classes"
UNITTEST_DIR = PROJECT_ROOT / "UnitTest"
UNITTEST_CLASSES_DIR = UNITTEST_DIR / "Classes"
