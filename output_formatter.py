from abc import ABC, abstractmethod
from typing import List

class OutputFormatter(ABC):
    @abstractmethod
    def format(self, data: List[int]) -> str:
        """Format the expanded range data into a string."""
        pass

class CsvStringFormatter(OutputFormatter):
    def format(self, data: List[int]) -> str:
        """Format the expanded range data as a CSV string."""
        return ','.join(map(str, data))
    
class PythonListFormatter(OutputFormatter):
    def format(self, data: List[int]) -> List[int]:
        """Format the expanded range data as a Python list string."""
        return data
    
class PythonSetFormatter(OutputFormatter):
    def format(self, data: List[int]) -> str:
        """Format the expanded range data as a Python set string."""
        return set(data)