# Lesson 34: Analytics & Reporting

## Overview
Learn how to implement analytics, reporting, and data export features in Django REST Framework.

---

## Learning Objectives

By the end of this lesson, you will be able to:

- ✅ Export data to Excel files using openpyxl
- ✅ Generate PDF reports using ReportLab
- ✅ Create dashboard statistics with aggregations
- ✅ Implement complex analytics queries
- ✅ Visualize data with charts and graphs

---

## Topics Covered

### 1. Excel Export (openpyxl)
- Creating workbooks and worksheets
- Writing data to cells
- Formatting and styling
- Multiple sheets
- Formulas and charts
- Auto-sizing columns
- Freezing panes

### 2. PDF Generation (ReportLab)
- Creating PDF documents
- Adding text and images
- Tables and layouts
- Custom styling
- Headers and footers
- Page breaks
- Multi-page reports

### 3. Dashboard Statistics
- Aggregation queries (Count, Sum, Avg, Min, Max)
- Group By operations
- Annotate and aggregate
- Complex filtering
- Subqueries
- Window functions

### 4. Data Visualization
- Sales analytics
- Popular books statistics
- Author performance
- Genre distribution
- Time-based analysis

---

## Technologies Used

- **openpyxl**: Excel file generation
- **ReportLab**: PDF creation
- **Pillow**: Image processing
- **Django ORM**: Aggregations
- **Matplotlib** (optional): Charts

---

## Project Structure

```
34-analytics-reporting/
├── README.md
├── examples/
│   ├── README.md
│   ├── 01-excel-basics.py
│   ├── 02-pdf-generation.py
│   ├── 03-aggregations.py
│   └── 04-dashboard-stats.py
└── code/
    └── library-project/
        ├── books/
        │   ├── exports.py       # Excel export utilities
        │   ├── reports.py       # PDF report generation
        │   ├── analytics.py     # Analytics logic
        │   └── views.py         # Export endpoints
        └── requirements.txt
```

---

## Quick Start

### 1. Install Dependencies
```bash
pip install openpyxl==3.1.2 reportlab==4.0.7 Pillow==10.1.0
```

### 2. Run Examples
```bash
cd examples
python 01-excel-basics.py
python 02-pdf-generation.py
python 03-aggregations.py
python 04-dashboard-stats.py
```

### 3. Test Django API
```bash
cd code/library-project
python manage.py runserver

# Test endpoints
GET /api/books/export/excel/
GET /api/books/export/pdf/
GET /api/books/analytics/dashboard/
```

---

## API Endpoints

### Excel Export
```http
GET /api/books/export/excel/
GET /api/books/export/excel/?author=John Doe&genre=Programming
```

### PDF Reports
```http
GET /api/books/export/pdf/
GET /api/books/export/pdf/{id}/
GET /api/books/reports/invoice/{borrow_id}/
```

### Analytics Dashboard
```http
GET /api/books/analytics/dashboard/
GET /api/books/analytics/by-genre/
GET /api/books/analytics/by-author/
GET /api/books/analytics/popular/
```

---

## Examples

### Example 1: Excel Export
Create an Excel file with book data, formatting, and formulas.

### Example 2: PDF Generation
Generate a professional PDF report with tables and styling.

### Example 3: Aggregations
Learn Django ORM aggregation functions.

### Example 4: Dashboard Statistics
Build a complete analytics dashboard.

---

## Key Concepts

### Excel Export Best Practices
- Use generators for large datasets
- Stream responses for memory efficiency
- Add proper headers and metadata
- Implement error handling

### PDF Generation Tips
- Design templates first
- Use consistent styling
- Optimize for printing
- Handle page breaks properly

### Analytics Optimization
- Use select_related and prefetch_related
- Index frequently queried fields
- Cache expensive calculations
- Use database aggregations (not Python loops)

---

## Testing Checklist

- [ ] Excel export with various filters
- [ ] PDF generation for single book
- [ ] PDF generation for list of books
- [ ] Dashboard statistics accuracy
- [ ] Performance with large datasets
- [ ] Error handling for edge cases
- [ ] File download headers correct
- [ ] Memory usage acceptable

---

## Real-World Applications

- **E-commerce**: Sales reports, invoice generation
- **Education**: Student reports, grade sheets
- **Healthcare**: Patient reports, medical records
- **Finance**: Financial statements, audit reports
- **Inventory**: Stock reports, movement analysis

---

## Resources

- [openpyxl Documentation](https://openpyxl.readthedocs.io/)
- [ReportLab Documentation](https://www.reportlab.com/docs/reportlab-userguide.pdf)
- [Django Aggregation](https://docs.djangoproject.com/en/stable/topics/db/aggregation/)
- [Django QuerySet API](https://docs.djangoproject.com/en/stable/ref/models/querysets/)

---

## Next Steps

After completing this lesson:
- Implement scheduled reports (Celery)
- Add email delivery for reports
- Create interactive dashboards
- Implement real-time analytics
- Add data visualization with charts

---

## Notes

- Always validate user input for filters
- Implement proper permissions for exports
- Consider rate limiting for export endpoints
- Add logging for report generation
- Monitor memory usage for large exports

---

**Happy Learning!**