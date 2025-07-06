from output_formatter import PythonListFormatter

class DefaultValues:
    DELIMITER = ["-", "..", "to", "~"]
    STEP_DELIMITER = ":"
    ALLOW_REVERSED = True
    ALLOW_MERGED = False
    ALLOW_DEDUPLICATE = False
    OUTPUT_FORMATTER = PythonListFormatter()

class ErrorMessages:
    # Output formatter errors
    INVALID_OUTPUT_FORMATTER = "Invalid output formatter provided - must be an instance of OutputFormatter"
    
    # Number parsing errors
    INVALID_NUMBER = "Invalid number: '{value}' - must be a valid integer or range"
    
    # Range expansion errors
    REVERSED_RANGE_NOT_ALLOWED = "Reversed range not allowed: {start}-{end} - enable allow_reversed=True to allow descending ranges"
    STEP_WITH_SINGLE_NUMBER = "Step syntax '{value}' cannot be used with a single number - use with ranges only"
    ZERO_STEP_VALUE = "Step value cannot be zero - must be a non-zero integer"
    
    @classmethod
    def format_message(cls, message_template: str, **kwargs) -> str:
        """Format an error message with the provided parameters."""
        try:
            return message_template.format(**kwargs)
        except KeyError as e:
            # Fallback if formatting fails
            return f"Error formatting message: {message_template} (missing key: {e})"
    