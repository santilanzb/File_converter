"""
Concrete implementation of FileHandler for PDF files.

This module uses PyPDF2 to extract text from PDF files and create simple
PDF files from text content.
"""

import PyPDF2
from io import BytesIO
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
            def read(self, file_path: str): pass
            def write(self, file_path: str, data): pass


class PdfHandler(FileHandler):
    """
    Handles reading and writing of PDF files.
    
    For reading: Extracts text from PDF pages
    For writing: Creates a simple text-based PDF
    """

    def read(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Reads a PDF file and extracts text from each page.

        Args:
            file_path (str): The path to the input PDF file.

        Returns:
            List[Dict[str, Any]]: A list where each dictionary represents a page
                                 with page number and extracted text.

        Raises:
            FileProcessingError: If the file cannot be found, read, or processed.
        """
        try:
            with open(file_path, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                pages_data = []
                
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    try:
                        text = page.extract_text()
                        pages_data.append({
                            'page': page_num,
                            'content': text.strip(),
                            'type': 'text'
                        })
                    except Exception as e:
                        # If text extraction fails for a page, include error info
                        pages_data.append({
                            'page': page_num,
                            'content': f"[Error extracting text: {str(e)}]",
                            'type': 'error'
                        })
                
                return pages_data
                
        except FileNotFoundError:
            raise FileProcessingError(file_path, "PDF file not found")
        except Exception as e:
            raise FileProcessingError(file_path, f"An error occurred while reading the PDF: {e}")

    def write(self, file_path: str, data: List[Dict[str, Any]]) -> None:
        """
        Writes data to a PDF file.
        
        Note: This creates a simple text-based PDF. For complex layouts,
        consider using libraries like ReportLab.

        Args:
            file_path (str): The path to the output PDF file.
            data (List[Dict[str, Any]]): The data to be written.

        Raises:
            FileProcessingError: If the file cannot be written.
            ValueError: If the data is invalid.
        """
        if not data:
            raise ValueError("Input data for PDF writing cannot be empty.")
        
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet
            
            doc = SimpleDocTemplate(file_path, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []
            
            for item in data:
                if isinstance(item, dict):
                    # Handle different data formats
                    if 'content' in item:
                        text = str(item['content'])
                    elif 'text' in item:
                        text = str(item['text'])
                    else:
                        # Convert entire dict to string
                        text = str(item)
                else:
                    text = str(item)
                
                if text.strip():  # Only add non-empty content
                    para = Paragraph(text, styles['Normal'])
                    story.append(para)
                    story.append(Spacer(1, 12))
            
            doc.build(story)
            
        except ImportError:
            # Fallback: Use PyPDF2 for basic PDF creation (limited functionality)
            self._write_simple_pdf(file_path, data)
        except Exception as e:
            raise FileProcessingError(file_path, f"An error occurred while writing the PDF: {e}")
    
    def _write_simple_pdf(self, file_path: str, data: List[Dict[str, Any]]) -> None:
        """
        Fallback method for simple PDF creation without ReportLab.
        
        Note: This method has limited functionality and creates very basic PDFs.
        """
        try:
            # Create a simple text file first, then we'll note the limitation
            text_content = ""
            for item in data:
                if isinstance(item, dict):
                    if 'content' in item:
                        text_content += str(item['content']) + "\n\n"
                    elif 'text' in item:
                        text_content += str(item['text']) + "\n\n"
                    else:
                        text_content += str(item) + "\n\n"
                else:
                    text_content += str(item) + "\n\n"
            
            # For now, we'll raise an error suggesting ReportLab installation
            raise FileProcessingError(
                file_path,
                "PDF creation requires ReportLab library. Please install it with: pip install reportlab"
            )
            
        except Exception as e:
            raise FileProcessingError(file_path, f"Failed to create PDF: {e}")
