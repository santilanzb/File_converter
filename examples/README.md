# Examples

This directory contains sample files to demonstrate the file converter functionality.

## Sample Files

- **sample_data.csv** - Example CSV file with employee data

## Usage Examples

```bash
# Convert CSV to JSON
fconv examples/sample_data.csv output.json

# Convert CSV to PDF
fconv examples/sample_data.csv report.pdf

# Convert CSV to Word document
fconv examples/sample_data.csv document.docx

# Convert CSV to PowerPoint
fconv examples/sample_data.csv presentation.pptx
```

## Chain Conversions

You can also chain conversions:

```bash
# CSV → JSON → PDF
fconv examples/sample_data.csv temp.json
fconv temp.json final_report.pdf
```
