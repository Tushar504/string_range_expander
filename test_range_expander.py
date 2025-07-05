import unittest
from number_range_expander import NumberRangeExpander

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
        
if __name__ == "__main__":
    unittest.main(verbosity=2)