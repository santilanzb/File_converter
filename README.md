# File Converter 🔄

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A versatile, extensible file converter that supports multiple formats through a plugin-based architecture.

## Features ✨

- **Multiple Format Support**: Convert between CSV, JSON, PDF, DOCX, PPTX, PPSX, and more
- **Plugin Architecture**: Easily extensible with new format handlers
- **Command Line Interface**: Simple `fconv` command for quick conversions
- **Intermediate Format**: Universal data representation for seamless conversions
- **Error Handling**: Robust error handling and informative error messages
- **Dynamic Discovery**: Automatic plugin discovery and registration

## Supported Formats 📁

### Data Formats
- **CSV** - Comma-Separated Values
- **JSON** - JavaScript Object Notation

### Document Formats
- **PDF** - Portable Document Format (with ReportLab)
- **DOCX** - Microsoft Word Document

### Presentation Formats
- **PPTX** - Microsoft PowerPoint Presentation
- **PPSX** - Microsoft PowerPoint Show

### E-book Formats
- **MOBI** - Mobipocket (limited support)
- **AZW3** - Kindle Format (placeholder)

## Installation 📦

### Prerequisites

Ensure you have Python 3.8+ installed on your system.

### Install from Source

1. Clone the repository:
```bash
git clone https://github.com/yourusername/file-converter.git
cd file-converter
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install the package:
```bash
pip install -e .
```

## Usage 🚀

### Command Line Interface

After installation, use the `fconv` command:

```bash
# Convert CSV to JSON
fconv data.csv data.json

# Convert JSON to PDF
fconv data.json report.pdf

# Convert JSON to Word document
fconv data.json document.docx

# Convert JSON to PowerPoint
fconv data.json presentation.pptx
```

### Python API

```python
from core.orchestrator import convert_file

# Convert files programmatically
convert_file('input.csv', 'output.json')
convert_file('data.json', 'report.pdf')
```

## Examples 📋

### Sample CSV to JSON Conversion

**Input (`employees.csv`):**
```csv
name,age,department
Alice Johnson,28,Engineering
Bob Smith,35,Marketing
Carla Rodriguez,31,Design
```

**Command:**
```bash
fconv employees.csv employees.json
```

**Output (`employees.json`):**
```json
[
    {
        "name": "Alice Johnson",
        "age": "28",
        "department": "Engineering"
    },
    {
        "name": "Bob Smith",
        "age": "35",
        "department": "Marketing"
    },
    {
        "name": "Carla Rodriguez",
        "age": "31",
        "department": "Design"
    }
]
```

## Project Structure 🏗️

```
file-converter/
├── core/
│   ├── __init__.py
│   ├── exceptions.py      # Custom exceptions
│   └── orchestrator.py    # Main conversion logic
├── plugins/
│   ├── __init__.py
│   ├── base_handler.py    # Abstract base class
│   ├── csv_handler.py     # CSV format support
│   ├── json_handler.py    # JSON format support
│   ├── pdf_handler.py     # PDF format support
│   ├── docx_handler.py    # Word document support
│   ├── pptx_handler.py    # PowerPoint support
│   ├── ppsx_handler.py    # PowerPoint show support
│   ├── azw3_handler.py    # Kindle format (placeholder)
│   ├── mobi_handler.py    # MOBI format (placeholder)
│   └── handler_factory.py # Plugin discovery
├── tests/
│   └── test_new_handlers.py
├── main.py               # CLI entry point
├── demo.py              # Demonstration script
├── setup.py             # Package configuration
├── requirements.txt     # Dependencies
└── README.md           # This file
```

## Development 🛠️

### Adding New Format Handlers

1. Create a new handler file in the `plugins/` directory:

```python
# plugins/new_format_handler.py
from typing import List, Dict, Any
from .base_handler import FileHandler
from ..core.exceptions import FileProcessingError

class NewFormatHandler(FileHandler):
    def read(self, file_path: str) -> List[Dict[str, Any]]:
        # Implement reading logic
        pass
    
    def write(self, file_path: str, data: List[Dict[str, Any]]) -> None:
        # Implement writing logic
        pass
```

2. The handler will be automatically discovered and registered!

### Running Tests

```bash
python -m pytest tests/
```

### Running the Demo

```bash
python demo.py
```

## Dependencies 📚

- **PyPDF2** - PDF file handling
- **python-docx** - Word document processing
- **python-pptx** - PowerPoint file handling
- **ebooklib** - E-book format support
- **reportlab** - PDF generation

## Error Handling 🚨

The converter provides comprehensive error handling:

- **UnsupportedFormatError** - When a file format is not supported
- **FileProcessingError** - When file reading/writing fails
- **ConversionError** - When conversion process encounters issues

## Contributing 🤝

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/new-format`)
3. Commit your changes (`git commit -am 'Add new format support'`)
4. Push to the branch (`git push origin feature/new-format`)
5. Create a new Pull Request

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments 🙏

- Built with Python's robust ecosystem
- Inspired by the need for seamless file format conversions
- Thanks to all the open-source libraries that make this possible

---

**Made with ❤️ for the developer community**
