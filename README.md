# string_range_expander

A flexible Python utility to expand number ranges and sequences from strings. Supports custom delimiters, step values, deduplication,merging ranges, output formatting, and robust error handling.

## Features
- Expand ranges like `1-5` to `[1, 2, 3, 4, 5]`
- Support for multiple delimiters: `-`, `..`, `to`, `~` (customizable)
- Step values: `1-10:2` → `[1, 3, 5, 7, 9]`
- Negative numbers and reversed ranges (configurable)
- Deduplication and merging of overlapping ranges
- Output as Python list, set, or CSV string
- Command-line interface (CLI) and Python API
- Centralized, descriptive error messages

## Installation

Clone the repository:
```bash
git clone <repo-url>
cd string_range_expander
```

## Requirements

- **Python 3.7 or higher**
  - All modules (`argparse`, `unittest`, etc.) used are part of the Python standard library.
- **No external dependencies required.**

**For testing:**
- The built-in `unittest` module is used for all tests.  
  (No need to install anything extra.)

## Usage

### As a CLI Tool
Run directly from the command line:
```bash
python number_range_expander.py --input_string="1-3,5,7-9"
```

#### CLI Options
- `--input_string` : String with numbers/ranges to expand (required)
- `--delimiters`, `-d`   : List of range delimiters (default: `- .. to ~`)
- `--step-delimiter`, `-s` : Step delimiter (default: `:`)
- `--allow-reversed`       : allow reversed ranges
- `--allow-merged`        : Merge and sort output
- `--allow-deduplicate`   : Remove duplicates
- `--output-formatter`, `-f` : Output format: `csv`, `list`, `set` (default: `list`)

#### CLI Examples
```bash
python number_range_expander.py --input_string="1-3,5,7-9"           # [1, 2, 3, 5, 7, 8, 9]
python number_range_expander.py --input_string="10-1"                # Error if reversed not allowed
python number_range_expander.py --input_string="1-10:2"              # [1, 3, 5, 7, 9]
python number_range_expander.py --input_string="1..5"                # [1, 2, 3, 4, 5]
python number_range_expander.py --input_string="1-3,2-5" --allow-deduplicate  # [1, 2, 3, 4, 5]
python number_range_expander.py --input_string="1-3,5" -f csv        # 1,2,3,5
```

### As a Python Module
```python
from number_range_expander import NumberRangeExpander, CsvStringFormatter

expander = NumberRangeExpander()
print(expander.expand("1-3,5,7-9"))  # [1, 2, 3, 5, 7, 8, 9]

# Custom delimiters and output format
expander = NumberRangeExpander(delimiters=["->", "until"], output_formatter=CsvStringFormatter())
print(expander.expand("1->3,5until7"))  # '1,2,3,5,6,7'
```

## Customization
- **Delimiters:** Pass a list to `delimiters` (e.g., `["-", "..", "to"]`)
- **Step delimiter:** Change with `step_delimeter` (default: `:`)
- **Allow reversed:** `allow_reversed=True/False`
- **Deduplication:** `allow_deduplicate=True/False`
- **Merged/sorted:** `allow_merged=True/False`
- **Output format:** Use `CsvStringFormatter`, `PythonListFormatter`, or `PythonSetFormatter`

## Error Handling
All errors use descriptive, centralized messages (see `constants.py: ErrorMessages`). Example:
- Invalid number: `Invalid number: 'abc' - must be a valid integer`
- Reversed range not allowed: `Reversed range not allowed: 10-1 - enable allow_reversed=True to allow descending ranges`
- Step value cannot be zero: `Step value cannot be zero - must be a non-zero integer`

## Testing
Run the test suite:
```bash
python test_range_expander.py
```

