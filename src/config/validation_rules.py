# ============================================================
# DATA QUALITY VALIDATION RULES
# ============================================================

# Maximum acceptable percentage of missing values
MAX_NULL_PERCENT = 5.0


# Duplicate policy
ALLOW_DUPLICATES = False


# Numeric validation
ALLOW_NEGATIVE_SALES = False
ALLOW_NEGATIVE_QUANTITY = False


# Date validation
ALLOW_INVALID_DATES = False


# String validation
ALLOW_EMPTY_STRINGS = False


# ============================================================
# VALIDATION SEVERITY
# ============================================================

SEVERITY_INFO = "INFO"
SEVERITY_WARNING = "WARNING"
SEVERITY_ERROR = "ERROR"
CRITICAL = "CRITICAL"