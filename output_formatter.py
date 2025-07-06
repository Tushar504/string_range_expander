from abc import ABC, abstractmethod
from typing import List, Set, Union

class OutputFormatter(ABC):
    @abstractmethod
    def format(self, data: List[int]) -> Union[List[int], Set[int], str]:
        """Format the expanded range data into the appropriate format."""
        pass

class CsvStringFormatter(OutputFormatter):
    def format(self, data: List[int]) -> str:
        """Format the expanded range data as a CSV string."""
        return ','.join(map(str, data))
    
class PythonListFormatter(OutputFormatter):
    def format(self, data: List[int]) -> List[int]:
        """Format the expanded range data as a Python list."""
        return data
    
class PythonSetFormatter(OutputFormatter):
    def format(self, data: List[int]) -> Set[int]:
        """Format the expanded range data as a Python set."""
        return set(data)