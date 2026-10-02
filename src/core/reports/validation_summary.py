import csv
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]

INPUT_FILE = (
    PROJECT_ROOT
    / "reports"
    / "comparison"
    / "store_sales_data_(2)_validation_comparison.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "reports"
    / "comparison"
    / "data_validation_summary.svg"
)


def load_validation_data():

    with INPUT_FILE.open(
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        return list(csv.DictReader(file))


def get_value(rows, category, check, column):

    for row in rows:

        if (
            row["Category"] == category
            and row["Check"] == check
        ):
            return row[column]

    return "N/A"


def build_svg():

    rows = load_validation_data()

    before_rows = get_value(
        rows,
        "StructuralValidator",
        "row_count",
        "Before"
    )

    after_rows = get_value(
        rows,
        "StructuralValidator",
        "row_count",
        "After"
    )

    checks = [
        (
            "STRUCTURAL CHECKS",
            [
                ("Blank Strings", "StructuralValidator", "blank_strings"),
                ("Duplicate Rows", "StructuralValidator", "duplicate_rows"),
                ("Missing Values", "StructuralValidator", "total_missing_values"),
            ],
        ),
        (
            "CONSISTENCY CHECKS",
            [
                (
                    "Customer ID → Name",
                    "ConsistencyValidator",
                    "customer_id_name_inconsistencies",
                ),
                (
                    "Product ID → Name",
                    "ConsistencyValidator",
                    "product_id_name_inconsistencies",
                ),
                (
                    "Product ID → Sub-Category",
                    "ConsistencyValidator",
                    "product_id_subcategory_inconsistencies",
                ),
                (
                    "Order Date > Ship Date",
                    "ConsistencyValidator",
                    "order_date_after_ship_date",
                ),
            ],
        ),
        (
            "BUSINESS RULE CHECKS",
            [
                (
                    "Invalid Discount",
                    "BusinessValidator",
                    "discount_outside_valid_range",
                ),
                (
                    "Invalid Quantity",
                    "BusinessValidator",
                    "quantity_less_than_or_equal_zero",
                ),
                (
                    "Invalid Sales",
                    "BusinessValidator",
                    "sales_less_than_or_equal_zero",
                ),
                (
                    "Negative Profit",
                    "BusinessValidator",
                    "negative_profit",
                ),
            ],
        ),
    ]

    validation_rows = []

    for section_name, section_checks in checks:

        validation_rows.append(
            f'<text x="70" y="{120 + len(validation_rows) * 0}" '
            f'class="section">{section_name}</text>'
        )

        for display_name, category, check in section_checks:

            value = get_value(
                rows,
                category,
                check,
                "After"
            )

            status = get_value(
                rows,
                category,
                check,
                "Status"
            )

            validation_rows.append(
                (
                    f'<text x="90" y="{0}" '
                    f'class="item">{display_name}</text>'
                )
            )

    failed = any(
        row["Status"] == "FAIL"
        for row in rows
        if row["Check"] not in {"row_count", "column_count"}
    )

    final_result = (
        "DATA VALIDATION REQUIRES ATTENTION"
        if failed
        else
        "DATA VALIDATION PASSED"
    )

    # --------------------------------------------------------
    # Build SVG manually
    # --------------------------------------------------------

    width = 1200
    height = 900

    svg = f'''<svg
        xmlns="http://www.w3.org/2000/svg"
        width="{width}"
        height="{height}"
        viewBox="0 0 {width} {height}">

        <rect width="1200" height="900" fill="#f7f9fc"/>

        <rect
            x="40"
            y="40"
            width="1120"
            height="820"
            rx="20"
            fill="white"
            stroke="#d9dee8"
            stroke-width="2"/>

        <text
            x="70"
            y="90"
            font-family="Arial"
            font-size="30"
            font-weight="bold">
            DATA VALIDATION SUMMARY
        </text>

        <text
            x="70"
            y="120"
            font-family="Arial"
            font-size="16">
            Consumer &amp; Product Analytics Platform
        </text>

        <line
            x1="70"
            y1="145"
            x2="1130"
            y2="145"
            stroke="#d9dee8"/>

        <text
            x="70"
            y="185"
            font-family="Arial"
            font-size="18"
            font-weight="bold">
            RECORDS
        </text>

        <text
            x="70"
            y="220"
            font-family="Arial"
            font-size="16">
            Before
        </text>

        <text
            x="250"
            y="220"
            font-family="Arial"
            font-size="16"
            font-weight="bold">
            {before_rows}
        </text>

        <text
            x="450"
            y="220"
            font-family="Arial"
            font-size="16">
            After
        </text>

        <text
            x="620"
            y="220"
            font-family="Arial"
            font-size="16"
            font-weight="bold">
            {after_rows}
        </text>

        <text
            x="70"
            y="270"
            font-family="Arial"
            font-size="18"
            font-weight="bold">
            VALIDATION RESULTS
        </text>
'''

    y = 310

    for section_name, section_checks in checks:

        svg += f'''
        <text
            x="70"
            y="{y}"
            font-family="Arial"
            font-size="17"
            font-weight="bold">
            {section_name}
        </text>
        '''

        y += 35

        for display_name, category, check in section_checks:

            value = get_value(
                rows,
                category,
                check,
                "After"
            )

            status = get_value(
                rows,
                category,
                check,
                "Status"
            )

            svg += f'''
            <text
                x="100"
                y="{y}"
                font-family="Arial"
                font-size="15">
                {display_name}
            </text>

            <text
                x="650"
                y="{y}"
                font-family="Arial"
                font-size="15">
                {value}
            </text>

            <text
                x="760"
                y="{y}"
                font-family="Arial"
                font-size="15"
                font-weight="bold">
                {status}
            </text>
            '''

            y += 30

        y += 20

    svg += f'''
        <line
            x1="70"
            y1="{y}"
            x2="1130"
            y2="{y}"
            stroke="#d9dee8"/>

        <text
            x="70"
            y="{y + 45}"
            font-family="Arial"
            font-size="18"
            font-weight="bold">
            Result: {final_result}
        </text>

    </svg>
    '''

    OUTPUT_FILE.write_text(
        svg,
        encoding="utf-8"
    )

    print(
        f"Validation summary created:\n{OUTPUT_FILE}"
    )


if __name__ == "__main__":
    build_svg()