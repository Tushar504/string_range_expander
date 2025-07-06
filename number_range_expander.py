import logging
from typing import List, Optional, Union, Set
from output_formatter import (
    OutputFormatter,
    CsvStringFormatter,
    PythonListFormatter,
    PythonSetFormatter,
)
from constants import DefaultValues, ErrorMessages

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

class RangeExpanderError(Exception):
    """Custom exception for range expansion errors."""

    pass


class NumberRangeExpander:
    def __init__(
        self,
        delimiters: List[str] = DefaultValues.DELIMITER,
        step_delimeter: str = DefaultValues.STEP_DELIMITER,
        allow_reversed: bool = DefaultValues.ALLOW_REVERSED,
        allow_merged: bool = DefaultValues.ALLOW_MERGED,
        allow_deduplicate: bool = DefaultValues.ALLOW_DEDUPLICATE,
        output_formatter: OutputFormatter = DefaultValues.OUTPUT_FORMATTER,
    ):
        self.delimiters = delimiters
        self.step_delimeter = step_delimeter
        self.allow_reversed = allow_reversed
        self.allow_merged = allow_merged
        self.allow_deduplicate = allow_deduplicate
        self.output_formatter = output_formatter
        logging.info(
            f"Initialized NumberRangeExpander with delimiters: {self.delimiters}, "
            f"step_delimiter: '{self.step_delimeter}', allow_reversed: {self.allow_reversed}, "
            f"allow_merged: {self.allow_merged}, allow_deduplicate: {self.allow_deduplicate}, "
            f"output_formatter: {type(self.output_formatter).__name__}"
        )

    def _parse_number(self, value: str) -> int:
        """Parse a string to an integer, raising an error if invalid."""
        try:
            value = value.strip()
            return int(value)
        except ValueError:
            message = ErrorMessages.format_message(
                ErrorMessages.INVALID_NUMBER, value=value
            )
            raise RangeExpanderError(message)

    def _expand_range(self, start: int, end: int, step: int = 1) -> List[int]:
        """Expand a range from start to end with a given step."""
        if step == 0:
            message = ErrorMessages.format_message(
                ErrorMessages.ZERO_STEP_VALUE
            )
            raise RangeExpanderError(message)
        elif start == end:
            return [start]
        elif start > end:
            if self.allow_reversed:
                # For reversed ranges, we need to handle step correctly
                if step > 0:
                    # If step is positive but range is reversed, we need to go backwards
                    return list(range(start, end - 1, -step))
                else:
                    # If step is negative, we can use it directly
                    return list(range(start, end - 1, step))
            else:
                message = ErrorMessages.format_message(
                    ErrorMessages.REVERSED_RANGE_NOT_ALLOWED, start=start, end=end
                )
                raise RangeExpanderError(message)
        return list(range(start, end + 1, step))

    def _parse_range(self, part: str) -> Optional[List[int]]:
        """Parse a part of the input string to extract a range or single number."""
        step = 1
        if self.step_delimeter in part:
            part_split = part.split(self.step_delimeter)
            if len(part_split) != 2 or len(part) == 2:
                message = ErrorMessages.format_message(
                    ErrorMessages.STEP_WITH_SINGLE_NUMBER, value=part
                )
                raise RangeExpanderError(message)
            
            step = self._parse_number(part_split[-1])
            if step == 0:
                message = ErrorMessages.format_message(
                    ErrorMessages.ZERO_STEP_VALUE
                )
                raise RangeExpanderError(message)
            part = part_split[0].strip()
    
        exception = None
        for index, delimiter in enumerate(self.delimiters):
            # Check if delimiter is in the part
            if delimiter not in part:
                continue
            
            try:
                # Split by delimiter
                parts_split = part.split(delimiter)

                # todo: can be improved using regex to handle multiple delimiters
                # to consider negative numbers implementation for '-' range delimiter
                if len(parts_split) > 2:
                    dash_index = -1
                    prev_ = None
                    for i, char in enumerate(part):

                        if char == delimiter:

                            if i == 0:
                                # If this is the first character, it's a negative number
                                if i + 1 < len(part) and part[i + 1].isdigit():
                                    continue

                            elif prev_:
                                dash_index = i
                                break
                        elif char.isdigit():
                            prev_ = char
                        elif not char.isspace():
                            prev_ = None

                    if dash_index != -1:
                        start_str = part[:dash_index]
                        end_str = part[dash_index + 1 :]
                        start, end = map(self._parse_number, [start_str, end_str])
                        return self._expand_range(start, end, step)
                elif len(parts_split) == 2 and parts_split[0].strip():
                    start, end = map(self._parse_number, parts_split)
                    return self._expand_range(start, end, step)
            except Exception as e:
                exception = e
                if index < len(self.delimiters) - 1:
                    logging.debug(f"Delimiter '{delimiter}' failed: {e}")
                    continue
                
                logging.error(f"Error parsing range '{part}': {e}")
                raise exception
        if exception:
            raise exception
    
    def _parse_part(self, part: str) -> List[int]:
        """Parse a part of the input string to extract numbers or ranges."""
        range_check = self._parse_range(part)
        if range_check != None:
            return range_check

        return [self._parse_number(part)]

    def _format_output(
        self, expanded_numbers: List[int]
    ) -> Union[List[int], Set[int], str]:
        """Format the expanded numbers using the specified output formatter."""
        logging.debug(f"Formatting output: {expanded_numbers}")
        if isinstance(self.output_formatter, OutputFormatter):
            return self.output_formatter.format(expanded_numbers)
        else:
            message = ErrorMessages.format_message(
                ErrorMessages.INVALID_OUTPUT_FORMATTER
            )
            raise RangeExpanderError(message)

    def expand(self, input_string: str) -> Union[List[int], Set[int], str]:
        """Expand a string containing numbers and ranges into a list of integers."""
        if not input_string:
            return []

        # generator expression for lazy loading
        input_string = (
            part.strip() for part in input_string.split(",") if part.strip()
        )

        expanded_numbers = []
        for part in input_string:
            try:
                logging.debug(f"Processing part: {part}")
                expanded_part = self._parse_part(part)
                expanded_numbers.extend(expanded_part)
                
            except RangeExpanderError as e:
                raise e
        
        # Remove duplicates if allowed
        if self.allow_deduplicate:
            seen = set()
            unique_numbers = []
            for num in expanded_numbers:
                if num not in seen:
                    seen.add(num)
                    unique_numbers.append(num)
            expanded_numbers = unique_numbers
        
        # Sort the numbers if merged ranges are allowed
        if self.allow_merged:
            expanded_numbers.sort()

        return self._format_output(expanded_numbers)


if __name__ == "__main__":
    """Command-line interface for the Number Range Expander."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Expand number sequences and ranges from string input",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
                Examples:
                 expand-ranges "1-3,5,7-9"
    """,
    )

    parser.add_argument(
        "--input_string", help="String containing numbers and ranges to expand"
    )

    parser.add_argument(
        "--delimiters",
        "-d",
        nargs="+",
        default=["-", "..", "to", "~"],
        help="Range delimiters (default: - .. to ~)",
    )

    parser.add_argument(
        "--step-delimiter", "-s", default=":", help="Step delimiter (default: :)"
    )

    parser.add_argument(
        "--allow-reversed", action="store_true", help="Allow reversed ranges"
    )

    parser.add_argument(
        "--allow-merged", action="store_true", help="Allow merged ranges"
    )

    parser.add_argument(
        "--allow-deduplicate",
        action="store_true",
        help="Allow deduplication of numbers",
    )

    parser.add_argument(
        "--output-formatter",
        "-f",
        choices=["csv", "list", "set"],
        default="list",
        help="Output format (default: list)",
    )

    args = parser.parse_args()

    try:
        expander = NumberRangeExpander(
            delimiters=args.delimiters,
            allow_reversed=args.allow_reversed,
            allow_merged=args.allow_merged,
            allow_deduplicate=args.allow_deduplicate,
            output_formatter=(
                CsvStringFormatter()
                if args.output_formatter == "csv"
                else (
                    PythonListFormatter()
                    if args.output_formatter == "list"
                    else PythonSetFormatter()
                )
            ),
        )
        expanded_numbers = expander.expand(args.input_string)
        print(expanded_numbers)
    except RangeExpanderError as e:
        print(f"Error: {e}")
