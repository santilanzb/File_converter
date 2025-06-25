"""
The main command-line interface (CLI) for the file converter.

This script uses argparse to parse command-line arguments and invokes the
core orchestrator to perform the file conversion.

Usage:
    python main.py <input_file_path> <output_file_path>

Example:
    python main.py data/my_data.csv data/converted_data.json
"""

import argparse
import sys
from core.orchestrator import convert_file
from core.exceptions import ConverterError

# For standalone testing, we'll use the dummy versions from the orchestrator.
from orchestrator import convert_file, ConversionError, UnsupportedFormatError

def main():
    """
    Main function to parse arguments and trigger the conversion.
    """
    parser = argparse.ArgumentParser(
        description="A versatile file converter.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Examples:
  python main.py input.csv output.json
  python main.py users.json report.csv
"""
    )
    
    parser.add_argument(
        "input_path",
        help="The path to the source file to be converted."
    )
    
    parser.add_argument(
        "output_path",
        help="The path where the new converted file will be saved."
    )
    
    args = parser.parse_args()

    try:
        # Call the core logic from the orchestrator
        convert_file(args.input_path, args.output_path)
        print(f"\nSuccess! File '{args.input_path}' was converted to '{args.output_path}'.")

    except (ConversionError, UnsupportedFormatError) as e:
        # Catch our custom application errors and display them nicely.
        print(f"\n[ERROR] Conversion failed: {e}", file=sys.stderr)
        sys.exit(1) # Exit with a non-zero status code to indicate failure
    except FileNotFoundError:
        print(f"\n[ERROR] Input file not found at '{args.input_path}'", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        # Catch any other unexpected errors.
        print(f"\n[ERROR] An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    # To run this standalone, ensure 'orchestrator.py' is in the same directory.
    main()
