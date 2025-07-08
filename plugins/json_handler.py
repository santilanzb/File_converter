"""
Concrete implementation of FileHandler for JSON files.

This module uses Python's built-in 'json' library to handle the reading
and writing of data in JavaScript Object Notation format.
"""

import json
from typing import List, Dict, Any

# Try to import from project structure, fall back to dummy classes
try:
    from ..core.exceptions import FileProcessingError
    from .base_handler import FileHandler
except ImportError:
    try:
        # Try absolute imports for installed package
        from core.exceptions import FileProcessingError
        from plugins.base_handler import FileHandler
    except ImportError:
        # For standalone testing, we'll define dummy classes.
        class FileProcessingError(Exception):
            def __init__(self, path, msg):
                super().__init__(f"{msg}: {path}")

        class FileHandler:
            def read(self, file_path: str) -> List[Dict[str, Any]]: pass
            def write(self, file_path: str, data: List[Dict[str, Any]]): pass


class JsonHandler(FileHandler):
    """
    Handles reading and writing of JSON files.

    The handler expects the JSON file to contain a list of objects,
    which maps directly to our intermediate format.
    """

    def read(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Reads a JSON file and returns its content as a list of dictionaries.

        Args:
            file_path (str): The path to the input JSON file.

        Returns:
            List[Dict[str, Any]]: The content of the JSON file.

        Raises:
            FileProcessingError: If the file is not found, cannot be read,
                                 or is not valid JSON.
        """
        try:
            with open(file_path, mode='r', encoding='utf-8') as jsonfile:
                data = json.load(jsonfile)
                # We enforce that the root of the JSON is a list.
                if not isinstance(data, list):
                    raise TypeError("JSON content must be a list of objects.")
                return data
        except FileNotFoundError:
            raise FileProcessingError(file_path, "JSON file not found")
        except json.JSONDecodeError:
            raise FileProcessingError(file_path, "Invalid JSON format")
        except TypeError as e:
            raise FileProcessingError(file_path, f"JSON content has wrong structure: {e}")
        except Exception as e:
            raise FileProcessingError(file_path, f"An error occurred while reading the JSON: {e}")

    def write(self, file_path: str, data: List[Dict[str, Any]]) -> None:
        """
        Writes a list of dictionaries to a JSON file.

        Args:
            file_path (str): The path to the output JSON file.
            data (List[Dict[str, Any]]): The data to be written.

        Raises:
            FileProcessingError: If the file cannot be written.
        """
        try:
            with open(file_path, mode='w', encoding='utf-8') as jsonfile:
                # indent=4 makes the output human-readable.
                json.dump(data, jsonfile, indent=4)
        except IOError as e:
            raise FileProcessingError(file_path, f"Could not write to JSON file: {e}")
        except Exception as e:
            raise FileProcessingError(file_path, f"An unexpected error occurred during JSON writing: {e}")

