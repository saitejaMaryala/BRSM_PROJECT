import sys
import os

# Try different PDF libraries
pdf_path = r"c:\Users\choud\OneDrive\Desktop\NewCollegeDocs\3-2\BRSM\project\Repo\BRSM_PROJECT\Movie memory Experiment  (2).pdf"

# Check if file exists
if not os.path.exists(pdf_path):
    print(f"Error: PDF file not found at {pdf_path}")
    sys.exit(1)

print(f"File found: {pdf_path}")
print(f"File size: {os.path.getsize(pdf_path)} bytes")

# Try PyPDF2 first
try:
    import PyPDF2
    print("\n=== Using PyPDF2 ===\n")
    
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)
        print(f"Number of pages: {num_pages}\n")
        print("="*80)
        print("EXTRACTED TEXT CONTENT")
        print("="*80)
        
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            print(f"\n--- PAGE {page_num + 1} ---\n")
            print(text)
            print("\n")
    
except ImportError:
    print("PyPDF2 not installed. Trying pdfplumber...")
    
    try:
        import pdfplumber
        print("\n=== Using pdfplumber ===\n")
        
        with pdfplumber.open(pdf_path) as pdf:
            num_pages = len(pdf.pages)
            print(f"Number of pages: {num_pages}\n")
            print("="*80)
            print("EXTRACTED TEXT CONTENT")
            print("="*80)
            
            for page_num, page in enumerate(pdf.pages):
                text = page.extract_text()
                print(f"\n--- PAGE {page_num + 1} ---\n")
                print(text)
                print("\n")
                
                # Also extract tables if any
                tables = page.extract_tables()
                if tables:
                    print(f"Tables found on page {page_num + 1}:")
                    for i, table in enumerate(tables):
                        print(f"\nTable {i + 1}:")
                        for row in table:
                            print(row)
                        print()
        
    except ImportError:
        print("pdfplumber not installed. Trying pypdf...")
        
        try:
            from pypdf import PdfReader
            print("\n=== Using pypdf ===\n")
            
            reader = PdfReader(pdf_path)
            num_pages = len(reader.pages)
            print(f"Number of pages: {num_pages}\n")
            print("="*80)
            print("EXTRACTED TEXT CONTENT")
            print("="*80)
            
            for page_num in range(num_pages):
                page = reader.pages[page_num]
                text = page.extract_text()
                print(f"\n--- PAGE {page_num + 1} ---\n")
                print(text)
                print("\n")
        
        except ImportError:
            print("\nError: No PDF libraries found!")
            print("Please install one of the following:")
            print("  pip install PyPDF2")
            print("  pip install pdfplumber")
            print("  pip install pypdf")
            sys.exit(1)
