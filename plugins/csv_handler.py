"""
Concrete implementation of FileHandler for CSV files.

This module uses Python's built-in 'csv' library to handle the reading
and writing of data in Comma-Separated Values format.
"""

import csv
from typing import List, Dict, Any

# Assuming a project structure where these imports are valid.
# from ..core.exceptions import FileProcessingError
# from .base_handler import FileHandler
# For standalone testing, we'll define dummy classes.
class FileProcessingError(Exception):
    def __init__(self, path, msg):
        super().__init__(f"{msg}: {path}")

class FileHandler:
    def read(self, file_path: str) -> List[Dict[str, Any]]: pass
    def write(self, file_path: str, data: List[Dict[str, Any]]): pass


class CsvHandler(FileHandler):
    """
    Handles reading and writing of CSV files.
    
    The handler assumes the first row of the CSV is the header.
    """

    def read(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Reads a CSV file and converts it into a list of dictionaries.

        Args:
            file_path (str): The path to the input CSV file.

        Returns:
            List[Dict[str, Any]]: A list where each dictionary represents a row.

        Raises:
            FileProcessingError: If the file cannot be found, read, or is malformed.
        """
        try:
            with open(file_path, mode='r', encoding='utf-8', newline='') as csvfile:
                # DictReader uses the first row as keys, which is what we want.
                reader = csv.DictReader(csvfile)
                return list(reader)
        except FileNotFoundError:
            raise FileProcessingError(file_path, "CSV file not found")
        except Exception as e:
            # Catch other potential errors like permission denied, or csv.Error
            raise FileProcessingError(file_path, f"An error occurred while reading the CSV: {e}")

    def write(self, file_path: str, data: List[Dict[str, Any]]) -> None:
        """
        Writes a list of dictionaries to a CSV file.

        Args:
            file_path (str): The path to the output CSV file.
            data (List[Dict[str, Any]]): The data to be written.

        Raises:
            FileProcessingError: If the data is invalid or file cannot be written.
            ValueError: If the data list is empty.
        """
        if not data:
            raise ValueError("Input data for CSV writing cannot be empty.")
        
        # All dictionaries in the list must have the same keys to form a valid CSV.
        # We'll use the keys from the first dictionary as the header.
        headers = list(data[0].keys())

        try:
            with open(file_path, mode='w', encoding='utf-8', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()
                writer.writerows(data)
        except IOError as e:
            raise FileProcessingError(file_path, f"Could not write to CSV file: {e}")
        except Exception as e:
            raise FileProcessingError(file_path, f"An unexpected error occurred during CSV writing: {e}")

