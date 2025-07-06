from typing import List, Optional


class RangeExpanderError(Exception):
    """Custom exception for range expansion errors."""

    pass


class NumberRangeExpander:
    def __init__(
        self,
        delimiters: Optional[List[str]] = None,
        step_delimeter: str = ":",
        allow_reversed: bool = True,
        allow_merged: bool = False,
        allow_deduplicate: bool = False,
    ):
        self.delimiters = delimiters or ("-", "to", "..", "~")
        self.step_delimeter = step_delimeter
        self.allow_reversed = allow_reversed
        self.allow_merged = allow_merged
        self.allow_deduplicate = allow_deduplicate

    def _parse_number(self, value: str) -> int:
        try:
            value = value.strip()
            return int(value)
        except ValueError:
            raise RangeExpanderError(f"Invalid number: '{value}'")

    def _expand_range(self, start: int, end: int, step: int = 1) -> List[int]:
        if step == 0:
            raise RangeExpanderError("Step value cannot be zero")
        elif start == end:
            return [start]
        elif start > end:
            if self.allow_reversed:
                return list(range(end, start + 1, step))[::-1]
            else:
                raise RangeExpanderError(f"Reversed range not allowed: {start}-{end}")
        return list(range(start, end + 1, step))

    def _parse_range(self, part: str) -> Optional[List[int]]:
        step = 1
        if self.step_delimeter in part:
            part = part.split(self.step_delimeter)
            if len(part) != 2:
                raise RangeExpanderError(f"Invalid step syntax: '{part}'")
            step = self._parse_number(part[-1])
            part = part[0].strip()

        for delimiter in self.delimiters:

            part_ = part.split(delimiter)

            # todo: can be improved using regex to handle multiple delimiters
            # to consider negative numbers implementation for '-' range delimiter
            if len(part_) > 2:
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
            elif len(part_) == 2 and part_[0].strip():
                start, end = map(self._parse_number, part_)
                return self._expand_range(start, end, step)

    def _parse_part(self, part: str) -> List[int]:
        range_check = self._parse_range(part)
        if range_check:
            return range_check

        return [self._parse_number(part)]

    def expand(self, input_string: str) -> List[int]:
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
                expanded_part = self._parse_part(part)
                expanded_numbers.extend(expanded_part)
            except RangeExpanderError as e:
                raise RangeExpanderError(f"Error parsing token '{part}': {e}")
        
        if self.allow_deduplicate:
            seen = set()
            unique_numbers = []
            for num in expanded_numbers:
                if num not in seen:
                    seen.add(num)
                    unique_numbers.append(num)
            expanded_numbers = unique_numbers

        if self.allow_merged:
            expanded_numbers.sort()
        
        return expanded_numbers


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
        "--input_string", "-i", help="String containing numbers and ranges to expand"
    )

    parser.add_argument(
        "--delimiters",
        "-d",
        nargs="+",
        default=["-", "..", "to", "~"],
        help="Range delimiters (default: - .. to ~)",
    )
    
    parser.add_argument(
        "--step-delimiter", "-s",
        default=":",
        help="Step delimiter (default: :)"
    )
    
    parser.add_argument(
        "--no-reversed", action="store_true", help="Disallow reversed ranges"
    )
    
    parser.add_argument(
        "--allow-merged", action="store_true", help="Allow merged ranges"
    )
    
    parser.add_argument(
        "--allow-deduplicate", action="store_true", help="Allow deduplication of numbers"
    )

    args = parser.parse_args()
    
    try:
        expander = NumberRangeExpander(
            delimiters=args.delimiters,
            allow_reversed=not args.no_reversed,
            allow_merged=args.allow_merged,
            allow_deduplicate=args.allow_deduplicate,
        )
        expanded_numbers = expander.expand(args.input_string)
        print(expanded_numbers)
    except RangeExpanderError as e:
        print(f"Error: {e}")
