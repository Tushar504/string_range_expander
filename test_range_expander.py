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
