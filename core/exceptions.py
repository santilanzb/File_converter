"""
This module defines custom exceptions for the file converter application.
Using custom exceptions allows for more specific error handling and clearer
intent than relying solely on built-in Python exceptions.
"""

class ConverterError(Exception):
    """Base exception class for all application-specific errors."""
    pass

class UnsupportedFormatError(ConverterError):
    """
    Raised when a file format is not supported for reading or writing.
    
    Attributes:
        format (str): The unsupported file format/extension.
        message (str): Explanation of the error.
    """
    def __init__(self, format, message="The file format is not supported."):
        self.format = format
        self.message = f"{message}: '{self.format}'"
        super().__init__(self.message)

class ConversionError(ConverterError):
    """
    Raised when an error occurs during the file conversion process.
    This can wrap other exceptions to provide more context.

    Attributes:
        from_format (str): The source format.
        to_format (str): The target format.
        message (str): Explanation of the error.
    """
    def __init__(self, from_format, to_format, message="An error occurred during conversion."):
        self.from_format = from_format
        self.to_format = to_format
        self.message = f"{message} (from {from_format} to {to_format})"
        super().__init__(self.message)

class FileProcessingError(ConverterError):
    """
    Raised for general errors during file reading or writing, such as
    permission errors or corrupted files.
    """
    def __init__(self, file_path, message="Failed to process file."):
        self.file_path = file_path
        self.message = f"{message}: {self.file_path}"
        super().__init__(self.message)

