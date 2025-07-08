"""
Concrete implementation of FileHandler for MOBI format.

This module attempts to use ebooklib to read MOBI files, though MOBI support
might be limited without additional tools.
"""

import os
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




class MobiHandler(FileHandler):
    """
    Handles reading and writing of MOBI files.
    
    Note: MOBI is a complex format. For full functionality,
    consider using Calibre's command-line tools.
    """

    def read(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Reads a MOBI file and extracts text content.

        Args:
            file_path (str): The path to the input MOBI file.

        Returns:
            List[Dict[str, Any]]: Extracted content from the MOBI file.

        Raises:
            FileProcessingError: If the file cannot be read or processed.
        """
        try:
            import ebooklib
            from ebooklib import epub
            from bs4 import BeautifulSoup
            import tempfile
            import subprocess
            import re
            
            # First try to convert MOBI to EPUB using ebook-convert if available
            # This requires Calibre to be installed on the system
            try:
                with tempfile.NamedTemporaryFile(suffix='.epub', delete=False) as tmp_epub:
                    temp_epub_path = tmp_epub.name
                
                # Try using ebook-convert command from Calibre
                ebook_convert_cmd = 'ebook-convert'
                # Check if Calibre is installed in the typical Windows location
                import os
                calibre_path = r'C:\Program Files\Calibre2\ebook-convert.exe'
                if os.path.exists(calibre_path):
                    ebook_convert_cmd = calibre_path
                
                result = subprocess.run(
                    [ebook_convert_cmd, file_path, temp_epub_path],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode == 0:
                    # Successfully converted, now read the EPUB
                    book = epub.read_epub(temp_epub_path)
                    content_data = []
                    
                    # Extract metadata
                    title = book.get_metadata('DC', 'title')
                    author = book.get_metadata('DC', 'creator')
                    
                    content_data.append({
                        'type': 'metadata',
                        'title': title[0][0] if title else 'Unknown',
                        'author': author[0][0] if author else 'Unknown',
                        'content': f"Title: {title[0][0] if title else 'Unknown'}\nAuthor: {author[0][0] if author else 'Unknown'}"
                    })
                    
                    # Extract text content from chapters
                    for item in book.get_items():
                        if item.get_type() == ebooklib.ITEM_DOCUMENT:
                            soup = BeautifulSoup(item.get_content(), 'html.parser')
                            text = soup.get_text().strip()
                            if text:
                                content_data.append({
                                    'type': 'chapter',
                                    'title': getattr(item, 'title', 'Chapter'),
                                    'content': text
                                })
                    
                    # Clean up temp file
                    import os
                    try:
                        os.unlink(temp_epub_path)
                    except:
                        pass
                    
                    return content_data if content_data else [{
                        'type': 'text',
                        'content': 'No readable content found in MOBI file'
                    }]
                
            except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
                # Calibre not available, fall back to basic file reading
                pass
            
            # Fallback: try to extract basic information by reading the file directly
            # MOBI files have some readable metadata at the beginning
            with open(file_path, 'rb') as f:
                data = f.read(1024)  # Read first 1KB
                
                # Try to extract title from the MOBI header
                try:
                    # MOBI files often have readable text in the header
                    text_data = data.decode('utf-8', errors='ignore')
                    
                    # Look for common metadata patterns
                    title_match = re.search(r'<title>(.*?)</title>', text_data, re.IGNORECASE)
                    author_match = re.search(r'<author>(.*?)</author>', text_data, re.IGNORECASE)
                    
                    content_data = []
                    
                    if title_match or author_match:
                        content_data.append({
                            'type': 'metadata',
                            'title': title_match.group(1) if title_match else 'Unknown',
                            'author': author_match.group(1) if author_match else 'Unknown',
                            'content': f"Title: {title_match.group(1) if title_match else 'Unknown'}\nAuthor: {author_match.group(1) if author_match else 'Unknown'}"
                        })
                    
                    content_data.append({
                        'type': 'note',
                        'content': 'MOBI file detected. For full text extraction, install Calibre (ebook-convert command).'
                    })
                    
                    return content_data
                    
                except UnicodeDecodeError:
                    pass
            
            # If all else fails, return a basic response
            return [{
                'type': 'info',
                'content': 'MOBI file format detected. Install Calibre for full content extraction.',
                'note': 'File exists and appears to be a valid MOBI file'
            }]
            
        except FileNotFoundError:
            raise FileProcessingError(file_path, "MOBI file not found")
        except Exception as e:
            raise FileProcessingError(file_path, f"An error occurred while reading the MOBI file: {e}")

    def write(self, file_path: str, data: List[Dict[str, Any]]) -> None:
        """
        Creates a MOBI file from the provided data.
        
        This method creates an EPUB first and then converts it to MOBI using Calibre.
        If Calibre is not available, it will create an HTML file instead.

        Args:
            file_path (str): The path to the output MOBI file.
            data (List[Dict[str, Any]]): The data to be written.

        Raises:
            FileProcessingError: If the file cannot be written.
            ValueError: If the data is invalid.
        """
        if not data:
            raise ValueError("Input data for MOBI writing cannot be empty.")
        
        try:
            import ebooklib
            from ebooklib import epub
            import tempfile
            import subprocess
            import html
            
            # Create an EPUB first
            book = epub.EpubBook()
            
            # Set metadata
            title = "Converted Document"
            author = "File Converter"
            
            # Extract metadata if available
            for item in data:
                if isinstance(item, dict) and item.get('type') == 'metadata':
                    title = item.get('title', title)
                    author = item.get('author', author)
                    break
            
            book.set_identifier('converted_doc')
            book.set_title(title)
            book.set_language('en')
            book.add_author(author)
            
            # Create chapters from content
            chapters = []
            chapter_num = 1
            
            for item in data:
                if isinstance(item, dict):
                    content = ''
                    chapter_title = f'Chapter {chapter_num}'
                    
                    if item.get('type') == 'chapter' and 'content' in item:
                        content = item['content']
                        chapter_title = item.get('title', chapter_title)
                    elif item.get('type') in ['text', 'paragraph'] and 'content' in item:
                        content = item['content']
                    elif 'content' in item:
                        content = str(item['content'])
                    elif 'text' in item:
                        content = str(item['text'])
                    else:
                        content = str(item)
                    
                    if content and content.strip():
                        # Create HTML content
                        html_content = f'<html><head><title>{html.escape(chapter_title)}</title></head><body>'
                        html_content += f'<h1>{html.escape(chapter_title)}</h1>'
                        
                        # Convert content to HTML paragraphs
                        paragraphs = content.split('\n')
                        for para in paragraphs:
                            if para.strip():
                                html_content += f'<p>{html.escape(para.strip())}</p>'
                        
                        html_content += '</body></html>'
                        
                        # Create chapter
                        chapter = epub.EpubHtml(
                            title=chapter_title,
                            file_name=f'chapter_{chapter_num}.xhtml',
                            lang='en'
                        )
                        chapter.content = html_content
                        
                        book.add_item(chapter)
                        chapters.append(chapter)
                        chapter_num += 1
                
                else:
                    # Handle non-dict items
                    content = str(item)
                    if content.strip():
                        chapter_title = f'Chapter {chapter_num}'
                        html_content = f'<html><head><title>{html.escape(chapter_title)}</title></head><body>'
                        html_content += f'<h1>{html.escape(chapter_title)}</h1>'
                        html_content += f'<p>{html.escape(content)}</p>'
                        html_content += '</body></html>'
                        
                        chapter = epub.EpubHtml(
                            title=chapter_title,
                            file_name=f'chapter_{chapter_num}.xhtml',
                            lang='en'
                        )
                        chapter.content = html_content
                        
                        book.add_item(chapter)
                        chapters.append(chapter)
                        chapter_num += 1
            
            # If no chapters were created, create a default one
            if not chapters:
                default_content = '<html><head><title>Document</title></head><body><h1>Document</h1><p>No content available</p></body></html>'
                chapter = epub.EpubHtml(title='Document', file_name='chapter_1.xhtml', lang='en')
                chapter.content = default_content
                book.add_item(chapter)
                chapters.append(chapter)
            
            # Define table of contents and spine
            book.toc = chapters
            book.add_item(epub.EpubNcx())
            book.add_item(epub.EpubNav())
            book.spine = ['nav'] + chapters
            
            # First try to create MOBI directly using Calibre
            try:
                with tempfile.NamedTemporaryFile(suffix='.epub', delete=False) as tmp_epub:
                    temp_epub_path = tmp_epub.name
                
                # Write EPUB to temp file
                epub.write_epub(temp_epub_path, book)
                
                # Convert EPUB to MOBI using ebook-convert
                ebook_convert_cmd = 'ebook-convert'
                # Check if Calibre is installed in the typical Windows location
                import os
                calibre_path = r'C:\Program Files\Calibre2\ebook-convert.exe'
                if os.path.exists(calibre_path):
                    ebook_convert_cmd = calibre_path
                
                result = subprocess.run(
                    [ebook_convert_cmd, temp_epub_path, file_path],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                
                # Clean up temp file
                import os
                try:
                    os.unlink(temp_epub_path)
                except:
                    pass
                
                if result.returncode == 0:
                    return  # Success!
                else:
                    raise subprocess.CalledProcessError(result.returncode, 'ebook-convert')
            
            except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
                # Calibre not available, create an HTML file instead
                html_file_path = file_path.replace('.mobi', '.html')
                
                # Create a single HTML file with all content
                html_content = f'<html><head><title>{html.escape(title)}</title></head><body>'
                html_content += f'<h1>{html.escape(title)}</h1>'
                html_content += f'<p><em>Author: {html.escape(author)}</em></p>'
                
                for chapter in chapters:
                    # Extract content from each chapter
                    chapter_content = chapter.content
                    if '<body>' in chapter_content:
                        body_start = chapter_content.find('<body>') + 6
                        body_end = chapter_content.find('</body>')
                        if body_end > body_start:
                            html_content += chapter_content[body_start:body_end]
                
                html_content += '</body></html>'
                
                with open(html_file_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                raise FileProcessingError(
                    file_path,
                    f"Calibre not found. Created HTML file instead: {html_file_path}. Install Calibre for MOBI support."
                )
            
        except ValueError as e:
            raise e
        except Exception as e:
            raise FileProcessingError(file_path, f"An error occurred while writing the MOBI file: {e}")
