"""
Coordinates the file conversion process.

This module acts as the main entry point for the conversion logic.
It uses the handler_factory to get the appropriate reader and writer
and manages the data flow between them.
"""

import os
from ..plugins.handler_factory import get_handler
from .exceptions import ConversionError, UnsupportedFormatError

# For standalone testing, we'll define dummy versions.
class UnsupportedFormatError(Exception): pass
class ConversionError(Exception): pass
class FileProcessingError(Exception): pass

class FileHandler:
    def read(self, file_path):
        print(f"Reading from {file_path} using {type(self).__name__}")
        return [{"id": 1, "data": "sample"}, {"id": 2, "data": "demo"}]

    def write(self, file_path, data):
        print(f"Writing to {file_path} using {type(self).__name__}")
        print(f"Data received: {data}")

def get_handler(ext):
    if ext in ['csv', 'json']:
        # In a real scenario, this returns CsvHandler() or JsonHandler()
        return FileHandler()
    raise UnsupportedFormatError(f"No handler for {ext}")


def convert_file(input_path: str, output_path: str):
    """
    Orchestrates the conversion of a file from one format to another.

    Args:
        input_path (str): The full path to the source file.
        output_path (str): The full path where the converted file will be saved.

    Raises:
        ConversionError: If any step in the conversion process fails.
        UnsupportedFormatError: If the input or output format is not supported.
    """
    print(f"Starting conversion from '{input_path}' to '{output_path}'...")

    try:
        # 1. Determine file formats from extensions
        _, input_ext = os.path.splitext(input_path)
        _, output_ext = os.path.splitext(output_path)
        input_format = input_ext.lstrip('.').lower()
        output_format = output_ext.lstrip('.').lower()

        if not input_format or not output_format:
            raise ConversionError(input_format, output_format, "Could not determine file formats from paths.")

        print(f"Source format: '{input_format}', Target format: '{output_format}'")

        # 2. Get the appropriate handlers from the factory
        reader_handler = get_handler(input_format)
        writer_handler = get_handler(output_format)
        
        print(f"Using reader: {type(reader_handler).__name__}, writer: {type(writer_handler).__name__}")

        # 3. Read the data into the intermediate format
        intermediate_data = reader_handler.read(input_path)

        # 4. Write the data from the intermediate format to the new file
        writer_handler.write(output_path, intermediate_data)

    except (UnsupportedFormatError, FileProcessingError) as e:
        # Re-raise specific errors from lower levels with more context
        raise ConversionError(
            from_format=input_format,
            to_format=output_format,
            message=f"A handler error occurred: {e}"
        ) from e
    except Exception as e:
        # Catch any other unexpected errors
        raise ConversionError(
            from_format=input_format,
            to_format=output_format,
            message=f"An unexpected error occurred: {e}"
        ) from e

    print("Conversion completed successfully!")


# Example Usage (for demonstration):
if __name__ == '__main__':
    # Create dummy files for the example
    with open("input.csv", "w") as f:
        f.write("id,data\n1,sample\n2,demo")

    try:
        # Simulate a successful conversion
        convert_file("input.csv", "output.json")
    except (ConversionError, UnsupportedFormatError) as e:
        print(f"ERROR: {e}")
    
    print("\n" + "="*20 + "\n")

    try:
        # Simulate a failed conversion (unsupported format)
        convert_file("input.csv", "output.xml")
    except (ConversionError, UnsupportedFormatError) as e:
        print(f"CAUGHT EXPECTED ERROR: {e}")

    # Clean up dummy file
    os.remove("input.csv")
