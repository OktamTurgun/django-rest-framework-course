"""
PDF Generation with ReportLab
Bu misolda:
- PDF document yaratish
- Text va tables qo'shish
- Styling va formatting
- Headers va footers
- Multi-page reports
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.platypus import Image as RLImage
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from datetime import datetime

print("=" * 70)
print("PDF GENERATION WITH REPORTLAB")
print("=" * 70)

# ============================================================================
# EXAMPLE 1: Simple PDF with Text
# ============================================================================
print("\nEXAMPLE 1: Creating Simple PDF")
print("-" * 70)

# Create PDF
doc = SimpleDocTemplate("book_report.pdf", pagesize=letter)
story = []

# Get styles
styles = getSampleStyleSheet()

# Title
title = Paragraph("Library Books Report", styles['Title'])
story.append(title)
story.append(Spacer(1, 0.2*inch))

# Subtitle with custom style
subtitle_style = ParagraphStyle(
    'CustomSubtitle',
    parent=styles['Normal'],
    fontSize=14,
    textColor=colors.HexColor('#366092'),
    alignment=TA_CENTER,
    spaceAfter=20
)
subtitle = Paragraph(f"Generated on {datetime.now().strftime('%Y-%m-%d')}", subtitle_style)
story.append(subtitle)
story.append(Spacer(1, 0.3*inch))

print("Added title and subtitle")

# ============================================================================
# EXAMPLE 2: Tables with Styling
# ============================================================================
print("\nEXAMPLE 2: Creating Styled Table")
print("-" * 70)

# Sample book data
data = [
    ['Title', 'Author', 'Price', 'Stock'],
    ['Python Programming', 'John Doe', '$45.99', '10'],
    ['Django for Beginners', 'Jane Smith', '$39.99', '5'],
    ['Clean Code', 'Robert Martin', '$49.99', '8'],
    ['Design Patterns', 'Gang of Four', '$54.99', '3'],
    ['Refactoring', 'Martin Fowler', '$44.99', '7'],
]

# Create table
table = Table(data, colWidths=[3*inch, 2*inch, 1*inch, 1*inch])

# Style table
table.setStyle(TableStyle([
    # Header styling
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#366092')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 12),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    
    # Data styling
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
    ('ALIGN', (0, 1), (0, -1), 'LEFT'),  # Title left-aligned
    ('ALIGN', (1, 1), (-1, -1), 'CENTER'),  # Others centered
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 1), (-1, -1), 10),
    ('TOPPADDING', (0, 1), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
    
    # Grid
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
    
    # Alternate row colors
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
]))

story.append(table)
story.append(Spacer(1, 0.3*inch))

print("Created styled table with books")

# ============================================================================
# EXAMPLE 3: Summary Statistics
# ============================================================================
print("\nEXAMPLE 3: Adding Summary Statistics")
print("-" * 70)

# Calculate totals
total_books = len(data) - 1
total_stock = sum(int(row[3]) for row in data[1:])
avg_price = sum(float(row[2].replace('$', '')) for row in data[1:]) / total_books

# Summary paragraph
summary_style = ParagraphStyle(
    'Summary',
    parent=styles['Normal'],
    fontSize=11,
    leading=16,
    spaceBefore=10,
    spaceAfter=10,
    leftIndent=20
)

summary_text = f"""
<b>Summary Statistics:</b><br/>
• Total Books: {total_books}<br/>
• Total Stock: {total_stock} items<br/>
• Average Price: ${avg_price:.2f}<br/>
• Report Date: {datetime.now().strftime('%B %d, %Y')}
"""

summary = Paragraph(summary_text, summary_style)
story.append(summary)

print("Added summary statistics")

# Build PDF
doc.build(story)
print(f"PDF saved: book_report.pdf")

# ============================================================================
# EXAMPLE 4: Invoice Generation
# ============================================================================
print("\nEXAMPLE 4: Creating Invoice PDF")
print("-" * 70)

def create_invoice():
    """Generate a professional invoice"""
    doc = SimpleDocTemplate("invoice.pdf", pagesize=A4)
    story = []
    styles = getSampleStyleSheet()
    
    # Header
    header_style = ParagraphStyle(
        'InvoiceHeader',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#366092'),
        alignment=TA_CENTER,
        spaceAfter=30
    )
    header = Paragraph("LIBRARY INVOICE", header_style)
    story.append(header)
    
    # Invoice details
    invoice_data = [
        ['Invoice #:', 'INV-2024-001'],
        ['Date:', datetime.now().strftime('%Y-%m-%d')],
        ['Due Date:', '2024-02-15'],
        ['', ''],
        ['Bill To:', ''],
        ['Name:', 'John Doe'],
        ['Email:', 'john@example.com'],
        ['Member ID:', 'LIB-12345'],
    ]
    
    details_table = Table(invoice_data, colWidths=[2*inch, 4*inch])
    details_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    
    story.append(details_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Items table
    items_data = [
        ['Book Title', 'Borrow Date', 'Due Date', 'Fee'],
        ['Python Programming', '2024-01-01', '2024-01-15', '$5.00'],
        ['Django for Beginners', '2024-01-05', '2024-01-19', '$5.00'],
        ['Clean Code', '2024-01-10', '2024-01-24', '$5.00'],
        ['', '', 'Subtotal:', '$15.00'],
        ['', '', 'Tax (10%):', '$1.50'],
        ['', '', 'Total:', '$16.50'],
    ]
    
    items_table = Table(items_data, colWidths=[3*inch, 1.5*inch, 1.5*inch, 1*inch])
    items_table.setStyle(TableStyle([
        # Header
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#366092')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        
        # Data
        ('FONTNAME', (0, 1), (-1, -4), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -4), 10),
        ('ALIGN', (0, 1), (-1, -4), 'LEFT'),
        ('GRID', (0, 0), (-1, -4), 1, colors.black),
        
        # Totals
        ('FONTNAME', (2, -3), (-1, -1), 'Helvetica-Bold'),
        ('ALIGN', (2, -3), (2, -1), 'RIGHT'),
        ('ALIGN', (3, -3), (3, -1), 'RIGHT'),
        ('LINEABOVE', (2, -3), (-1, -3), 2, colors.black),
        ('LINEABOVE', (2, -1), (-1, -1), 2, colors.black),
        ('BACKGROUND', (2, -1), (-1, -1), colors.lightgrey),
    ]))
    
    story.append(items_table)
    story.append(Spacer(1, 0.5*inch))
    
    # Footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    footer = Paragraph(
        "Thank you for using our library services!<br/>For questions, contact: library@example.com",
        footer_style
    )
    story.append(footer)
    
    # Build
    doc.build(story)
    print(" Invoice PDF created: invoice.pdf")

create_invoice()

# ============================================================================
# EXAMPLE 5: Multi-Page Report with Page Numbers
# ============================================================================
print("\nEXAMPLE 5: Multi-Page Report")
print("-" * 70)

def add_page_number(canvas, doc):
    """Add page numbers to footer"""
    page_num = canvas.getPageNumber()
    text = f"Page {page_num}"
    canvas.saveState()
    canvas.setFont('Helvetica', 9)
    canvas.drawRightString(200, 20, text)
    canvas.restoreState()

# Create multi-page document
doc = SimpleDocTemplate("multi_page_report.pdf", pagesize=letter)
story = []
styles = getSampleStyleSheet()

# Add title
title = Paragraph("Complete Library Report", styles['Title'])
story.append(title)
story.append(Spacer(1, 0.5*inch))

# Add multiple sections
for i in range(3):
    section_title = Paragraph(f"Section {i+1}: Book Category", styles['Heading2'])
    story.append(section_title)
    story.append(Spacer(1, 0.2*inch))
    
    # Add table for each section
    section_data = [
        ['Title', 'Author', 'Price', 'Stock'],
        [f'Book {i*3+1}', 'Author A', '$45.99', '10'],
        [f'Book {i*3+2}', 'Author B', '$39.99', '5'],
        [f'Book {i*3+3}', 'Author C', '$49.99', '8'],
    ]
    
    section_table = Table(section_data)
    section_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    story.append(section_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Page break after each section
    if i < 2:
        story.append(PageBreak())

# Build with page numbers
doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
print(" Multi-page report created: multi_page_report.pdf")

# ============================================================================
# Summary
# ============================================================================
print("\n" + "=" * 70)
print("PDF GENERATION SUMMARY")
print("=" * 70)
print("Generated PDFs:")
print("  1. book_report.pdf - Simple report with table")
print("  2. invoice.pdf - Professional invoice")
print("  3. multi_page_report.pdf - Multi-page with page numbers")
print("\nFeatures demonstrated:")
print("  1. Text styling and paragraphs")
print("  2. Tables with custom styles")
print("  3. Headers and footers")
print("  4. Page breaks")
print("  5. Page numbers")
print("  6. Color and formatting")
print("  7. Professional layouts")
print("=" * 70)