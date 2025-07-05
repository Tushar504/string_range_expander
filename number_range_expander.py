class NumberRangeExpander:
    
    def _parse_part(self, part: str):
        part = part.strip()
        
        if not part:
            return []
        
        dash_index = -1
        for i, char in enumerate(part):
    
            if char == '-':
                
                if i == 0:
                    # If this is the first character, it's a negative number
                    if i + 1 < len(part) and part[i + 1].isdigit():
                        continue
                    else:
                        raise ValueError(f"Invalid range format: '{part}'")
        
                elif part[i-1].isdigit() and i + 1 < len(part) and not part[i + 1].isspace():
                    dash_index = i
                    break

        if dash_index != -1:
            start_str = part[:dash_index]
            end_str = part[dash_index + 1:]
            start = int(start_str)
            end = int(end_str)
            return list(range(start, end + 1))
        else:
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
    expander = NumberRangeExpander()
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
    args = parser.parse_args()
    expanded_numbers = expander.expand(args.input_string)
    print(expanded_numbers)