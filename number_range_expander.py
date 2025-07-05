
class NumberRangeExpander:
    
    def expand(self, input_string: str):
        if not input_string:
            return []

        parts = input_string.split(',')
        expanded_numbers = []

        for part in parts:
            if '-' in part:
                start, end = map(int, part.split('-'))
                expanded_numbers.extend(range(start, end + 1))
            else:
                expanded_numbers.append(int(part))

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