from pathlib import Path


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]


# ============================================================
# MAIN DIRECTORIES
# ============================================================

SRC_DIR = PROJECT_ROOT / "src"

DATASETS_DIR = PROJECT_ROOT / "datasets"
DOCUMENTATION_DIR = PROJECT_ROOT / "documentation"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
DATABASE_DIR = PROJECT_ROOT / "database"
TESTS_DIR = PROJECT_ROOT / "tests"
LOGS_DIR = PROJECT_ROOT / "logs"
REPORTS_DIR = PROJECT_ROOT / "reports"
POWERBI_DIR = PROJECT_ROOT / "powerbi"
IMAGES_DIR = PROJECT_ROOT / "images"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"


# ============================================================
# DATA DIRECTORIES
# ============================================================

RAW_DATA_DIR = DATASETS_DIR / "raw"
INTERIM_DATA_DIR = DATASETS_DIR / "interim"
PROCESSED_DATA_DIR = DATASETS_DIR / "processed"
VALIDATION_DATA_DIR = DATASETS_DIR / "validation"
SAMPLE_DATA_DIR = DATASETS_DIR / "sample"


# ============================================================
# POWER BI DIRECTORIES
# ============================================================

POWERBI_SCREENSHOTS_DIR = POWERBI_DIR / "screenshots"
POWERBI_DOCUMENTATION_DIR = POWERBI_DIR / "documentation"


# ============================================================
# IMAGE DIRECTORIES
# ============================================================

ER_DIAGRAM_DIR = IMAGES_DIR / "er_diagram"
SCREENSHOTS_DIR = IMAGES_DIR / "screenshots"


# ============================================================
# LOG FILES
# ============================================================

PIPELINE_LOG_FILE = LOGS_DIR / "pipeline.log"
ERROR_LOG_FILE = LOGS_DIR / "errors.log"