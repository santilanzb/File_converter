"""
Dynamically discovers and provides file handlers.

This factory is responsible for finding all available FileHandler subclasses
within the 'plugins' package and providing an instance of the correct handler
based on a given file extension. This approach makes the application
extensible by default.
"""

import os
import pkgutil
import inspect
from typing import Dict, Type
from ..core.exceptions import UnsupportedFormatError
from .base_handler import FileHandler

# For standalone testing, we'll define dummy classes and a mock package structure.
class UnsupportedFormatError(Exception):
    def __init__(self, format, message="Unsupported format"):
        super().__init__(f"{message}: {format}")

class FileHandler:
    pass

# ---- Handler Factory Implementation ----

_HANDLERS: Dict[str, Type[FileHandler]] = {}

def _discover_handlers():
    """
    Dynamically imports all modules in the 'plugins' package and registers
    any FileHandler subclasses found.
    """
    if _HANDLERS:  # Discover only once
        return

    # This dynamically finds the path to the 'plugins' package.
    # Replace 'plugins' with the actual package name if different.
    package_path = os.path.dirname(__file__)
    package_name = os.path.basename(package_path)

    for _, module_name, _ in pkgutil.iter_modules([package_path]):
        # Import the module dynamically
        module = __import__(f"{package_name}.{module_name}", fromlist=["*"])

        # Look for classes within the imported module
        for name, obj in inspect.getmembers(module, inspect.isclass):
            # Check if it's a subclass of FileHandler but not FileHandler itself
            if issubclass(obj, FileHandler) and obj is not FileHandler:
                # Infer the format from the class name (e.g., "CsvHandler" -> "csv")
                format_name = name.replace("Handler", "").lower()
                _HANDLERS[format_name] = obj
                print(f"Discovered and registered handler for '{format_name}'")


def get_handler(file_extension: str) -> FileHandler:
    """
    Returns an instantiated file handler for the given file extension.

    The file extension should be provided without the leading dot.
    e.g., 'csv', 'json'

    Args:
        file_extension (str): The file extension to get a handler for.

    Returns:
        FileHandler: An instance of the appropriate handler.

    Raises:
        UnsupportedFormatError: If no handler is found for the extension.
    """
    _discover_handlers() # Ensure handlers are loaded
    
    handler_class = _HANDLERS.get(file_extension.lower())
    
    if not handler_class:
        raise UnsupportedFormatError(file_extension, "No handler registered for this file type")
        
    return handler_class()


# Example Usage (for demonstration):
if __name__ == '__main__':
    # To run this standalone, we need dummy handler files like
    # csv_handler.py and json_handler.py in the same directory.
    class CsvHandler(FileHandler): pass
    class JsonHandler(FileHandler): pass

    try:
        csv_handler_instance = get_handler('csv')
        json_handler_instance = get_handler('json')
        print(f"Successfully got CSV handler: {type(csv_handler_instance).__name__}")
        print(f"Successfully got JSON handler: {type(json_handler_instance).__name__}")

        # This should fail
        get_handler('xml')
    except UnsupportedFormatError as e:
        print(e)
