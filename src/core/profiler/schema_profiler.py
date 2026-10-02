"""
Schema profiling.

Checks:
    - Column names
    - Data types
    - Non-null counts
    - Duplicate column names
    - Special characters
    - Object columns
"""

from .base_profiler import BaseProfiler


class SchemaProfiler(BaseProfiler):

    def column_name_check(self):
        result = list(self.df.columns)

        self.log_check("column_names")

        return result

    def data_type(self):
        result = {
            column: str(dtype)
            for column, dtype
            in self.df.dtypes.items()
        }

        self.log_check("data_types")

        return result

    def non_null_count(self):
        result = {
            column: int(count)
            for column, count
            in self.df.notna().sum().items()
        }

        self.log_check("non_null_count")

        return result

    def duplicate_column_name(self):
        columns = list(self.df.columns)

        duplicates = [
            column
            for column in set(columns)
            if columns.count(column) > 1
        ]

        self.log_check("duplicate_column_names")

        return duplicates

    def special_character_columns(self):
        result = [
            column
            for column in self.df.columns
            if not str(column)
            .replace("_", "")
            .replace("-", "")
            .isalnum()
        ]

        self.log_check("special_character_columns")

        return result

    def object_column_detection(self):
        result = [
            column
            for column in self.df.select_dtypes(
                include=["object", "string"]
            ).columns
        ]

        self.log_check("object_columns")

        return result

    def run(self):

        self.report = {
            "column_names": self.column_name_check(),
            "data_types": self.data_type(),
            "non_null_count": self.non_null_count(),
            "duplicate_column_names":
                self.duplicate_column_name(),
            "special_character_columns":
                self.special_character_columns(),
            "object_columns":
                self.object_column_detection()
        }

        return self.report