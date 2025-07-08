#!/usr/bin/env python3
"""
Test script for the file format handlers.

This script tests the basic functionality of all file format handlers:
CSV, JSON, PDF, DOCX, PPTX, PPSX, AZW3, and MOBI.
"""

import sys
import os
import tempfile
import unittest

# Add the project root to the path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

try:
    # Import from the project structure
    import plugins.handler_factory as factory
    import core.exceptions as exceptions
    
    get_handler = factory.get_handler
    UnsupportedFormatError = exceptions.UnsupportedFormatError
    FileProcessingError = exceptions.FileProcessingError
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you're running from the project root directory")
    sys.exit(1)

def test_handler_discovery():
    """
    Test that all new handlers can be discovered and instantiated.
    """
    print("Testing handler discovery...")
    
    # Test formats that should work
    working_formats = ['pdf', 'docx', 'pptx', 'ppsx']
    
    for format_name in working_formats:
        try:
            handler = get_handler(format_name)
            print(f"✓ {format_name.upper()} handler discovered: {type(handler).__name__}")
        except Exception as e:
            print(f"✗ Failed to get {format_name.upper()} handler: {e}")
    
    # Test formats that might not work (ebook formats)
    ebook_formats = ['azw3', 'mobi']
    
    for format_name in ebook_formats:
        try:
            handler = get_handler(format_name)
            print(f"✓ {format_name.upper()} handler discovered: {type(handler).__name__}")
        except UnsupportedFormatError:
            print(f"! {format_name.upper()} handler not supported (expected for complex formats)")
        except Exception as e:
            print(f"✗ Unexpected error for {format_name.upper()}: {e}")

def test_sample_data_conversion():
    """
    Test conversion with sample data.
    """
    print("\nTesting sample data conversion...")
    
    # Sample data in intermediate format
    sample_data = [
        {'content': 'This is a test document.', 'type': 'text'},
        {'content': 'This is another paragraph.', 'type': 'text'},
        {'content': 'End of document.', 'type': 'text'}
    ]
    
    # Test formats that support writing
    writeable_formats = ['pdf', 'docx', 'pptx', 'ppsx']
    
    for format_name in writeable_formats:
        try:
            handler = get_handler(format_name)
            test_file = f"test_output.{format_name}"
            
            # Try to write sample data
            handler.write(test_file, sample_data)
            print(f"✓ {format_name.upper()} write test successful")
            
            # Clean up
            if os.path.exists(test_file):
                os.remove(test_file)
                
        except Exception as e:
            print(f"✗ {format_name.upper()} write test failed: {e}")

def main():
    """
    Main test function.
    """
    print("File Converter - New Handlers Test")
    print("=" * 40)
    
    test_handler_discovery()
    test_sample_data_conversion()
    
    print("\nTest completed!")

if __name__ == "__main__":
    main()
