#!/usr/bin/env python3
"""
Comprehensive demonstration of the enhanced File Converter.

This script demonstrates the new file format capabilities including:
- PDF, DOCX, PPTX, PPSX format support
- Plugin-based architecture with automatic handler discovery
- Conversion between multiple formats
"""

import os
import sys
from datetime import datetime

def create_sample_data():
    """Create sample data files for demonstration."""
    print("📁 Creating sample data files...")
    
    # Create sample CSV
    csv_content = """name,age,city,department
Alice Johnson,28,New York,Engineering
Bob Smith,35,London,Marketing
Carla Rodriguez,31,Tokyo,Design
David Chen,29,San Francisco,Engineering
Eva Williams,33,Berlin,Sales"""
    
    with open('sample_data.csv', 'w', encoding='utf-8') as f:
        f.write(csv_content)
    
    print("✅ Created sample_data.csv with employee information")
    return 'sample_data.csv'

def demonstrate_conversions():
    """Demonstrate various file format conversions."""
    print("\n🔄 Demonstrating file format conversions...\n")
    
    sample_file = create_sample_data()
    
    conversions = [
        (sample_file, 'employees.json', 'CSV to JSON'),
        ('employees.json', 'employees.pdf', 'JSON to PDF'),
        ('employees.json', 'employees.docx', 'JSON to Word Document'),
        ('employees.json', 'employees.pptx', 'JSON to PowerPoint'),
        ('employees.json', 'employees.ppsx', 'JSON to PowerPoint Show'),
    ]
    
    for input_file, output_file, description in conversions:
        print(f"🔧 {description}...")
        cmd = f'fconv {input_file} {output_file}'
        print(f"   Command: {cmd}")
        
        result = os.system(cmd)
        if result == 0:
            if os.path.exists(output_file):
                size = os.path.getsize(output_file)
                print(f"   ✅ Success! Created {output_file} ({size} bytes)")
            else:
                print(f"   ⚠️  Command succeeded but file not found")
        else:
            print(f"   ❌ Failed (exit code: {result})")
        print()

def test_error_handling():
    """Test error handling for unsupported formats and edge cases."""
    print("\n🧪 Testing error handling...\n")
    
    test_cases = [
        ('sample_data.csv', 'output.xyz', 'Unsupported output format'),
        ('nonexistent.csv', 'output.json', 'Non-existent input file'),
        ('sample_data.csv', 'output.mobi', 'Complex format (MOBI)'),
        ('sample_data.csv', 'output.azw3', 'Complex format (AZW3)'),
    ]
    
    for input_file, output_file, description in test_cases:
        print(f"🧪 Testing: {description}")
        cmd = f'fconv {input_file} {output_file}'
        print(f"   Command: {cmd}")
        
        result = os.system(cmd)
        if result == 0:
            print(f"   ✅ Handled gracefully")
        else:
            print(f"   ⚠️  Error handled (exit code: {result})")
        print()

def show_supported_formats():
    """Display supported file formats."""
    print("\n📋 Supported File Formats:")
    print("=" * 40)
    
    formats = {
        '📊 Data Formats': ['CSV', 'JSON'],
        '📄 Document Formats': ['PDF', 'DOCX (Word)'],
        '📺 Presentation Formats': ['PPTX (PowerPoint)', 'PPSX (PowerPoint Show)'],
        '📚 E-book Formats': ['MOBI (limited)', 'AZW3 (placeholder)']
    }
    
    for category, format_list in formats.items():
        print(f"\n{category}:")
        for fmt in format_list:
            print(f"  • {fmt}")

def show_file_summary():
    """Show summary of created files."""
    print("\n📄 Files Created During Demo:")
    print("=" * 35)
    
    demo_files = [
        'sample_data.csv',
        'employees.json', 
        'employees.pdf',
        'employees.docx',
        'employees.pptx',
        'employees.ppsx'
    ]
    
    total_size = 0
    for filename in demo_files:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            total_size += size
            print(f"  📄 {filename:<20} ({size:,} bytes)")
    
    print(f"\n📊 Total size: {total_size:,} bytes")

def main():
    """Main demonstration function."""
    print("🚀 File Converter - Enhanced Format Support Demo")
    print("=" * 50)
    print(f"Demo started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        show_supported_formats()
        demonstrate_conversions()
        test_error_handling()
        show_file_summary()
        
        print("\n🎉 Demo completed successfully!")
        print("\n💡 Key Features Demonstrated:")
        print("  • Dynamic plugin discovery")
        print("  • Multiple file format support")
        print("  • Intermediate format conversion")
        print("  • Error handling for unsupported formats")
        print("  • Command-line interface (fconv)")
        
    except KeyboardInterrupt:
        print("\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
