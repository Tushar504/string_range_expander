import unittest
from number_range_expander import NumberRangeExpander, RangeExpanderError
from output_formatter import CsvStringFormatter, PythonListFormatter, PythonSetFormatter

class TestStage1BasicRangeExpansion(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.expander = NumberRangeExpander()
    
    def test_empty_string(self):
        """Test expansion of an empty string."""
        result = self.expander.expand("")
        self.assertEqual(result, [])
        
    def test_single_range(self):
        """Test expansion of a single range."""
        result = self.expander.expand("1-3")
        self.assertEqual(result, [1, 2, 3])
    
    def test_single_number(self):
        """Test expansion of a single number."""
        result = self.expander.expand("5")
        self.assertEqual(result, [5])
    
    def test_mixed_ranges_and_numbers(self):
        """Test expansion of mixed ranges and numbers."""
        result = self.expander.expand("1-2,4")
        self.assertEqual(result, [1, 2, 4])
    
    def test_multiple_ranges(self):
        """Test expansion of multiple ranges."""
        result = self.expander.expand("1-3,5,7-9")
        self.assertEqual(result, [1, 2, 3, 5, 7, 8, 9])
        
    def test_negative_numbers(self):
        """Test expansion with negative numbers."""
        result = self.expander.expand("-3--1")
        self.assertEqual(result, [-3, -2, -1])


class TestStage2IgnoreWhitespaceAndEmptyParts(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.expander = NumberRangeExpander()
    
    def test_whitespace_around_tokens(self):
        """Test removal of whitespace around tokens."""
        result = self.expander.expand(" 1-3 , 5 ")
        self.assertEqual(result, [1, 2, 3, 5])
    
    def test_empty_parts(self):
        """Test ignoring empty parts."""
        result = self.expander.expand(" , 1-3 , ,5 ")
        self.assertEqual(result, [1, 2, 3, 5])
    
    def test_multiple_empty_parts(self):
        """Test handling multiple empty parts."""
        result = self.expander.expand("1,  ,  ,2,3")
        self.assertEqual(result, [1, 2, 3])
    
    def test_empty_string(self):
        """Test handling empty string input."""
        result = self.expander.expand("")
        self.assertEqual(result, [])
    
    def test_only_whitespace_and_commas(self):
        """Test handling string with only whitespace and commas."""
        result = self.expander.expand("  , , , ")
        self.assertEqual(result, [])
    
    def test_whitespace_around_negative_numbers_range(self):
        """Test expansion with negative numbers."""
        result = self.expander.expand(" -3--1")
        self.assertEqual(result, [-3, -2, -1])
    
    def test_whitespace_around_mixed_ranges_and_numbers(self):
        """Test empty part around negative numbers."""
        result = self.expander.expand(" -2   , 4 ")
        self.assertEqual(result, [-2, 4])


class TestStage3CustomRangeDelimiters(unittest.TestCase):
    """Test Stage 3: Custom Range Delimiters functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.expander = NumberRangeExpander()
    
    def test_dot_dot_delimiter(self):
        """Test '..' delimiter."""
        result = self.expander.expand("1..3")
        self.assertEqual(result, [1, 2, 3])
    
    def test_tilde_delimiter(self):
        """Test '~' delimiter."""
        result = self.expander.expand("4~6")
        self.assertEqual(result, [4, 5, 6])
    
    def test_to_delimiter(self):
        """Test 'to' delimiter."""
        result = self.expander.expand("10 to 12")
        self.assertEqual(result, [10, 11, 12])
    
    def test_mixed_delimiters(self):
        """Test mixed range delimiters in one string."""
        result = self.expander.expand("1-3,4..6,7~9")
        self.assertEqual(result, [1, 2, 3, 4, 5, 6, 7, 8, 9])
    
    def test_custom_delimiters(self):
        """Test custom delimiter configuration."""
        custom_expander = NumberRangeExpander(delimiters=["->", "until"])
        result = custom_expander.expand("1 -> 3,5 until 7")
        self.assertEqual(result, [1, 2, 3, 5, 6, 7])
    
    def test_delimiter_precedence(self):
        """Test that longer delimiters take precedence."""
        result = self.expander.expand("1..5")
        self.assertEqual(result, [1, 2, 3, 4, 5])

class TestStage4HandleReversedorInvalidRangesGracefully(unittest.TestCase):
    """Test Stage 4: Error Handling functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.expander = NumberRangeExpander()
    
    def test_reverse_order_range(self):
        """Test handling of invalid ranges."""
        result = self.expander.expand("5..1")
        self.assertEqual(result, [5, 4, 3, 2, 1])
    
    def test_reverse_negative_numbers_range(self):
        """Test handling of reversed negative number ranges."""
        result = self.expander.expand("-5--1")
        self.assertEqual(result, [-5, -4, -3, -2, -1])

    def test_non_numeric_input(self):
        """Test handling of non-numeric input."""
        with self.assertRaises(RangeExpanderError):
            self.expander.expand("a-b")
    
    def test_mixed_valid_and_invalid_ranges(self):
        """Test handling of mixed valid and invalid ranges."""
        with self.assertRaises(RangeExpanderError):
            self.expander.expand("1-3,5,a-7")
            
class TestStage5SupportStepValues(unittest.TestCase):
    """Test Stage 5: Support Step Values functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.expander = NumberRangeExpander()
    
    def test_basic_step_syntax(self):
        """Test basic step syntax."""
        result = self.expander.expand("1-10:2")
        self.assertEqual(result, [1, 3, 5, 7, 9])
    
    def test_descending_step(self):
        """Test descending step syntax."""
        result = self.expander.expand("10-1:3")
        self.assertEqual(result, [10, 7, 4, 1])
    
    def test_step_with_different_delimiters(self):
        """Test step syntax with different range delimiters."""
        result = self.expander.expand("1..10:2")
        self.assertEqual(result, [1, 3, 5, 7, 9])
    
    def test_mixed_step_and_regular_ranges(self):
        """Test mixing step and regular ranges."""
        result = self.expander.expand("1-5:1,10-20:2")
        self.assertEqual(result, [1, 2, 3, 4, 5, 10, 12, 14, 16, 18, 20])
    
    def test_step_larger_than_range(self):
        """Test step larger than range."""
        result = self.expander.expand("1-3:5")
        self.assertEqual(result, [1])
    
    def test_invalid_step_syntax(self):
        """Test invalid step syntax."""
        with self.assertRaises(RangeExpanderError):
            self.expander.expand("1-10:2:3")
    
    def test_zero_step(self):
        """Test zero step value."""
        with self.assertRaises(RangeExpanderError):
            self.expander.expand("1-10:0")
    
    def test_step_with_single_number(self):
        """Test step syntax with single number (should error)."""
        with self.assertRaises(RangeExpanderError):
            self.expander.expand("5:2")
            
            
class TestStage6DuplicateAndOverlappingRangeHandling(unittest.TestCase):
    """Test Stage 6: Duplicate and Overlapping Range Handling functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.expander = NumberRangeExpander(allow_deduplicate=True, allow_merged=False)
        self.expander_no_dedup = NumberRangeExpander(allow_deduplicate=False, allow_merged=False)
        
        
    def test_overlapping_ranges_deduplicated(self):
        """Test overlapping ranges with deduplication."""
        result = self.expander.expand("1-3,2-5")
        self.assertEqual(result, [1, 2, 3, 4, 5])
    
    def test_overlapping_ranges_not_deduplicated(self):
        """Test overlapping ranges without deduplication."""
        result = self.expander_no_dedup.expand("1-3,2-5")
        self.assertEqual(result, [1, 2, 3, 2, 3, 4, 5])
    
    def test_duplicate_numbers_deduplicated(self):
        """Test duplicate numbers with deduplication."""
        result = self.expander.expand("1,2,3,2,1")
        self.assertEqual(result, [1, 2, 3])
    
    def test_duplicate_numbers_not_deduplicated(self):
        """Test duplicate numbers without deduplication."""
        result = self.expander_no_dedup.expand("1,2,3,2,1")
        self.assertEqual(result, [1, 2, 3, 2, 1])
    
    def test_complex_overlapping_pattern(self):
        """Test complex overlapping pattern."""
        result = self.expander.expand("1-5,3-7,6-10")
        self.assertEqual(result, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    
    def test_order_preservation_with_deduplication(self):
        """Test that order is preserved when deduplicating."""
        result = self.expander.expand("5,1-3,2,7")
        self.assertEqual(result, [5, 1, 2, 3, 7])
        
    def test_order_with_merged_with_deduplication(self):
        """Test that order is preserved when merging and deduplicating."""
        expander_merged = NumberRangeExpander(allow_deduplicate=True, allow_merged=True)
        result = expander_merged.expand("4-7,1-3,2-5,4-6")
        self.assertEqual(result, [1, 2, 3, 4, 5, 6, 7])
        
        
class TestStage7OutputFormatControl(unittest.TestCase):
    """Test Stage 7: Output Format Control functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.expander = NumberRangeExpander()
        self.test_string = "1-3,5,7-9"
    
    def test_list_output_format(self):
        """Test list output format."""
        result = self.expander.expand(self.test_string)
        self.assertIsInstance(result, list)
        self.assertEqual(result, [1, 2, 3, 5, 7, 8, 9])
    
    def test_csv_output_format(self):
        """Test CSV output format."""
        self.expander.output_formatter = CsvStringFormatter()
        result = self.expander.expand(self.test_string)
        self.assertIsInstance(result, str)
        self.assertEqual(result, "1,2,3,5,7,8,9")
    
    def test_set_output_format(self):
        """Test set output format."""
        self.expander.output_formatter = PythonSetFormatter()
        result = self.expander.expand(self.test_string)
        self.assertIsInstance(result, set)
        self.assertEqual(result, {1, 2, 3, 5, 7, 8, 9})
    
    def test_invalid_output_format(self):
        """Test invalid output format."""
        with self.assertRaises(RangeExpanderError):
            self.expander.output_formatter = "invalid_format"
            self.expander.expand(self.test_string)

if __name__ == "__main__":
    # Create a test suite with all test cases
    test_suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestStage1BasicRangeExpansion,
        TestStage2IgnoreWhitespaceAndEmptyParts,
        TestStage3CustomRangeDelimiters,
        TestStage4HandleReversedorInvalidRangesGracefully,
        TestStage5SupportStepValues,
        TestStage6DuplicateAndOverlappingRangeHandling,
        TestStage7OutputFormatControl  
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"Test Summary:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print(f"{'='*50}")