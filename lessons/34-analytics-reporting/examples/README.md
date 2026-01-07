# Analytics & Reporting Examples - Lesson 34

## 📚 Overview
Bu papkada Analytics & Reporting'ni tushunish uchun 4 ta amaliy Python misollar mavjud.

---

## 📁 Examples

### 1. `01-excel-basics.py` ⭐
**Mavzu:** Excel file generation with openpyxl

**O'rganiladigan narsalar:**
- Workbook va worksheet yaratish
- Ma'lumotlarni yozish
- Header va data styling
- Auto-sizing columns
- Formulas (SUM, AVG)
- Multiple sheets
- Freezing panes
- Conditional formatting

**Output:** `books_report.xlsx`

**Run:**
```bash
python 01-excel-basics.py
```

---

### 2. `02-pdf-generation.py` 📄
**Mavzu:** PDF report generation with ReportLab

**O'rganiladigan narsalar:**
- PDF document yaratish
- Text va paragraph qo'shish
- Tables yaratish
- Styling va colors
- Headers va footers
- Page breaks
- Images qo'shish
- Multi-page reports

**Output:** `book_report.pdf`, `invoice.pdf`

**Run:**
```bash
python 02-pdf-generation.py
```

---

### 3. `03-aggregations.py` 📊
**Mavzu:** Django ORM Aggregations

**O'rganiladigan narsalar:**
- Count, Sum, Avg, Min, Max
- Group By with annotate()
- Filter + Aggregate
- Subqueries
- Complex aggregations
- Performance optimization

**Note:** Django setup kerak (manage.py shell)

**Run:**
```bash
cd ../code/library-project
python manage.py shell < ../../examples/03-aggregations.py
```

---

### 4. `04-dashboard-stats.py` 📈
**Mavzu:** Complete Analytics Dashboard

**O'rganiladigan narsalar:**
- Multiple aggregations
- Complex filtering
- Data grouping
- Statistics calculation
- Real-world analytics
- Dashboard design

**Note:** Django setup kerak

**Run:**
```bash
cd ../code/library-project
python manage.py shell < ../../examples/04-dashboard-stats.py
```

---

## Learning Path

Recommended order:

1. **Start:** `01-excel-basics.py`
   - Learn Excel export basics
   - No Django required
   - Immediate visual results

2. **Next:** `02-pdf-generation.py`
   - Learn PDF generation
   - No Django required
   - See professional reports

3. **Then:** `03-aggregations.py`
   - Django ORM aggregations
   - Foundation for analytics
   - Requires Django project

4. **Finally:** `04-dashboard-stats.py`
   - Complete dashboard
   - Combine everything learned
   - Real-world application

---

## Dependencies

### For Examples 1-2 (Standalone):
```bash
pip install openpyxl==3.1.2
pip install reportlab==4.0.7
pip install Pillow==10.1.0
```

### For Examples 3-4 (Django required):
```bash
cd ../code/library-project
pip install -r requirements.txt
```

---

## Expected Outputs

### Example 1: Excel File
```
books_report.xlsx
├── Sheet: "Books Report"
│   ├── Styled headers
│   ├── Formatted data
│   ├── Formulas (totals)
│   └── Conditional formatting
└── Sheet: "Summary"
    └── Report metadata
```

### Example 2: PDF Files
```
book_report.pdf
├── Title page
├── Books table
├── Page numbers
└── Footer with date

invoice.pdf
├── Header with logo
├── Invoice details
├── Items table
└── Total calculation
```

### Example 3: Console Output
```
AGGREGATION QUERIES
===================
Total books: 130
Average price: $42.50
Most expensive: $59.99

BY GENRE:
- Programming: 45 books, $48.50 avg
- Fiction: 30 books, $35.20 avg
...
```

### Example 4: Dashboard Data
```
DASHBOARD STATISTICS
====================
Overview:
  Total books: 130
  Total authors: 25
  Total stock value: $5,525.00

Popular Books:
  1. Python Programming (15 borrows)
  2. Clean Code (12 borrows)
...
```

---

## Key Concepts

### Excel Export
- **Workbook**: Container for worksheets
- **Worksheet**: Individual sheet with cells
- **Cell**: Single data point with styling
- **Formula**: Dynamic calculation

### PDF Generation
- **Canvas**: Drawing surface
- **Flowable**: Content elements (paragraphs, tables)
- **Style**: Visual formatting
- **PageTemplate**: Page layout structure

### Aggregations
- **aggregate()**: Single result across queryset
- **annotate()**: Add calculated field to each row
- **Group By**: Group and calculate per group
- **F expressions**: Reference field values in DB

### Analytics
- **Metrics**: Numerical measurements (count, sum, avg)
- **Dimensions**: Categories for grouping (genre, author)
- **KPIs**: Key Performance Indicators
- **Dashboard**: Visual representation of metrics

---

## Troubleshooting

### Issue: "No module named 'openpyxl'"
**Solution:**
```bash
pip install openpyxl
```

### Issue: "Django not found"
**Solution:**
```bash
cd ../code/library-project
pip install -r requirements.txt
```

### Issue: Excel file won't open
**Solution:**
- Close existing Excel files
- Check file permissions
- Try different filename

### Issue: PDF fonts not found
**Solution:**
- Install Pillow: `pip install Pillow`
- Use standard fonts (Helvetica, Times-Roman)

### Issue: Aggregation returns None
**Solution:**
- Check if data exists in database
- Verify filter conditions
- Use `Count('id')` instead of `Count('*')`

---

## Data Requirements

### For Examples 1-2:
- No database needed
- Uses sample data in code

### For Examples 3-4:
- Django project must be set up
- Database must have:
  - Books with author and genres
  - At least 10+ books for meaningful stats
  - Optional: BorrowHistory for popularity stats

---

## What You'll Learn

After completing these examples:

**Excel Skills:**
- Create professional spreadsheets
- Apply formatting and styling
- Use formulas for calculations
- Handle multiple sheets

**PDF Skills:**
- Generate reports programmatically
- Create invoices and documents
- Design professional layouts
- Handle multi-page content

**Analytics Skills:**
- Write complex ORM queries
- Perform aggregations efficiently
- Group and filter data
- Calculate business metrics

**Integration Skills:**
- Combine Django with reporting
- Export database data
- Create dashboards
- Build real-world features

---

## Next Steps

After running examples:

1. **Modify examples:**
   - Change styling
   - Add more data
   - Try different calculations

2. **Integrate into Django:**
   - Create API endpoints
   - Add to views
   - Test with real data

3. **Extend functionality:**
   - Add charts to Excel
   - Add images to PDFs
   - Create more metrics

4. **Complete homework:**
   - Implement full features
   - Add tests
   - Deploy to production

---

## Resources

- [openpyxl Tutorial](https://openpyxl.readthedocs.io/en/stable/tutorial.html)
- [ReportLab Quickstart](https://www.reportlab.com/docs/reportlab-userguide.pdf)
- [Django Aggregation Guide](https://docs.djangoproject.com/en/stable/topics/db/aggregation/)
- [Python Excel Libraries Comparison](https://www.python-excel.org/)

---

**Happy Learning!**

Run examples in order and experiment with the code!