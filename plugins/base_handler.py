"""
Defines the abstract base class (ABC) for all file handlers.

Each file handler plugin must inherit from this class and implement its
abstract methods, ensuring a consistent interface for the core engine.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Tuple

class FileHandler(ABC):
    """
    Abstract Base Class for file handlers.

    This class defines the standard interface for reading from and writing to
    a specific file format. It also specifies which conversions are supported.
    """

    @abstractmethod
    def read(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Reads a file and converts its content into the standardized
        intermediate format (a list of dictionaries).

        Args:
            file_path (str): The path to the input file.

        Returns:
            List[Dict[str, Any]]: The file content as a list of dictionaries.
        
        Raises:
            FileProcessingError: If the file cannot be read or parsed.
        """
        pass

    @abstractmethod
    def write(self, file_path: str, data: List[Dict[str, Any]]) -> None:
        """
        Writes data from the standardized intermediate format to a file.

        Args:
            file_path (str): The path to the output file.
            data (List[Dict[str, Any]]): The data to write, in the intermediate format.

        Raises:
            FileProcessingError: If the file cannot be written.
        """
        pass

    @classmethod
    def get_supported_conversions(cls) -> List[Tuple[str, str]]:
        """
        Returns a list of supported conversion pairs (from_ext, to_ext).
        This allows handlers to declare what they can convert to and from.
        
        For handlers that use the intermediate format, this can often be inferred.
        For direct conversion handlers (e.g., DOCX to PDF), this is crucial.

        Returns:
            List[Tuple[str, str]]: A list of tuples, where each tuple is a
                                   (source_extension, target_extension) pair.
                                   Example: [('csv', 'json'), ('csv', 'xml')]
        """
        # Default implementation can be empty, requiring subclasses to be specific.
        return []

