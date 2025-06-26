"""
The main command-line interface (CLI) for the file converter.

This script uses argparse to parse command-line arguments and invokes the
core orchestrator to perform the file conversion.
"""

import argparse
import sys
import os


project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(project_root))


# Now that the path is set, we can use absolute imports from the project root.
from core.orchestrator import convert_file
from core.exceptions import ConverterError, UnsupportedFormatError
# No additional code needed at this placeholder.
def main():
    """
    Main function to parse arguments and trigger the conversion.
    """
    parser = argparse.ArgumentParser(
        description="A versatile file converter.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Examples:
  python path/to/main.py input.csv output.json
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

    except (ConverterError, UnsupportedFormatError) as e:
        print(f"\n[ERROR] Conversion failed: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"\n[ERROR] Input file not found at '{args.input_path}'", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
