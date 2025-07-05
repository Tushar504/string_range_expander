from typing import List, Optional

class NumberRangeExpander:
    def __init__(self, delimiters: Optional[List[str]] = None):
        self.delimiters = delimiters if delimiters else ['-', 'to', '..', '~']
    
    def _parse_part(self, part: str):
        part = part.strip()
        if not part:
            return []
        
        for delimiter in self.delimiters:
    
            part_ = part.split(delimiter)
            
            if len(part_) > 2:
                dash_index = -1
                prev_= None
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
                    end_str = part[dash_index + 1:]
                    start = int(start_str)
                    end = int(end_str)
                    return list(range(start, end + 1))
            elif len(part_) == 2 and part_[0].strip():
                start_str, end_str = part_
                start = int(start_str.strip())
                end = int(end_str.strip())
                return list(range(start, end + 1))
        
        return [int(part)]
    
    def expand(self, input_string: str):
        if not input_string:
            return []

        parts = [part.strip() for part in input_string.split(',') if part.strip()]
        
        expanded_numbers = []
        for part in parts:
            try:
                expanded_part = self._parse_part(part)
                expanded_numbers.extend(expanded_part)
            except ValueError:
                raise ValueError(f"Invalid number or range: '{part}'")

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
    """)
    
    parser.add_argument(
        "input_string",
        help="String containing numbers and ranges to expand"
    )
    
    parser.add_argument(
        "--delimiters", "-d",
        nargs="+",
        default=["-", "..", "to", "~"],
        help="Range delimiters (default: - .. to ~)"
    )
    
    args = parser.parse_args()
    expander = NumberRangeExpander(delimiters=args.delimiters)
    expanded_numbers = expander.expand(args.input_string)
    print(expanded_numbers)