"""
Add branded variables to a CSV of variable information

I expect we're going to get lots of different data formats,
so I have kept this as simple as posssible.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from cmip_branded_variable_mapper.mapper import map_to_cmip_branded_variable


def main():
    """Add branded variables to the input"""
    INPUT_FILE = Path(
        "raw-spreadsheets/v1_2-Variables-Spreadsheet-KT-review-041525.xlsx"
    )
    VARIABLE_ROOT_COLUMN_NAME = "variableRootDD"
    DIMENSIONS_COLUMN_NAME = "dimensions for determining branding suffix"
    CELL_METHODS_COLUMN_NAME = "cell_methods for determining branding suffix"
    BRANDED_VARIABLE_COLUMN_NAME = "branded variable name"

    raw = pd.read_excel(INPUT_FILE)
    for col in [
        VARIABLE_ROOT_COLUMN_NAME,
        DIMENSIONS_COLUMN_NAME,
        CELL_METHODS_COLUMN_NAME,
        BRANDED_VARIABLE_COLUMN_NAME,
    ]:
        if col not in raw:
            raise KeyError(col)

    OUTPUT_SUFFIX = "_plus-branded-variables"
    output_file = Path("processed-csvs") / f"{INPUT_FILE.stem}{OUTPUT_SUFFIX}.csv"

    # Only want to operate on rows that have a variable
    res = raw.loc[~raw[VARIABLE_ROOT_COLUMN_NAME].isnull()].copy()
    # Slow way to do this, whatever (speed isn't an issue, clarity is more important)
    for idx, row in res.iterrows():
        dimensions = [v.strip() for v in row.loc[DIMENSIONS_COLUMN_NAME].split(",")]
        res.loc[idx, BRANDED_VARIABLE_COLUMN_NAME] = map_to_cmip_branded_variable(
            variable_name=row.loc[VARIABLE_ROOT_COLUMN_NAME],
            cell_methods=row.loc[CELL_METHODS_COLUMN_NAME],
            dimensions=dimensions,
        )

    output_file.parent.mkdir(exist_ok=True, parents=True)
    res.to_csv(output_file, index=False)

    print(f"Wrote output to {output_file}")


if __name__ == "__main__":
    main()
