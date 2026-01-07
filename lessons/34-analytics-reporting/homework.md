# Homework: Analytics & Reporting - Lesson 34

## Objective
Implement comprehensive analytics and reporting features for the Library Management System.

---

## Requirements

### **Part 1: Excel Export (30 points)**

#### Task 1.1: Basic Book Export (10 points)
Create an endpoint to export all books to Excel with the following features:
- All book fields (title, author, ISBN, price, stock, etc.)
- Proper header styling (bold, colored background)
- Auto-sized columns
- Number formatting for price
- **Endpoint:** `GET /api/books/export/excel/`

#### Task 1.2: Filtered Export (10 points)
Extend the export to support filters:
- Filter by author
- Filter by genre
- Filter by price range
- Filter by stock availability
- **Example:** `GET /api/books/export/excel/?author=John Doe&price_min=20`

#### Task 1.3: Advanced Excel Features (10 points)
Add advanced features:
- Multiple sheets (Books, Summary, Statistics)
- Formulas (totals, averages)
- Conditional formatting (low stock highlighting)
- Charts (optional, +5 bonus points)

---

### **Part 2: PDF Reports (30 points)**

#### Task 2.1: Single Book Report (10 points)
Generate a PDF report for a single book:
- Book details (title, author, description, etc.)
- Book cover image (if available)
- Review statistics
- Borrowing history
- **Endpoint:** `GET /api/books/{id}/export/pdf/`

#### Task 2.2: Books List PDF (10 points)
Generate a PDF with all books:
- Table format with key information
- Page numbers
- Header and footer
- Professional styling
- **Endpoint:** `GET /api/books/export/pdf/`

#### Task 2.3: Invoice/Receipt Generation (10 points)
Create a PDF invoice when a book is borrowed:
- User information
- Book details
- Borrow date and due date
- Late fees calculation (if applicable)
- **Endpoint:** `GET /api/borrows/{id}/invoice/`

---

### **Part 3: Dashboard Analytics (40 points)**

#### Task 3.1: Overview Statistics (10 points)
Create a dashboard endpoint with:
- Total books count
- Total authors count
- Total genres count
- Average book price
- Total stock value
- **Endpoint:** `GET /api/analytics/dashboard/`

**Expected Response:**
```json
{
  "overview": {
    "total_books": 130,
    "total_authors": 25,
    "total_genres": 10,
    "avg_price": 42.50,
    "total_stock_value": 5525.00
  }
}
```

#### Task 3.2: Books by Genre (10 points)
Analyze books grouped by genre:
- Count of books per genre
- Average price per genre
- Total stock per genre
- **Endpoint:** `GET /api/analytics/by-genre/`

**Expected Response:**
```json
{
  "by_genre": [
    {
      "genre": "Programming",
      "count": 45,
      "avg_price": 48.50,
      "total_stock": 230
    },
    ...
  ]
}
```

#### Task 3.3: Books by Author (10 points)
Analyze books grouped by author:
- Count of books per author
- Average price per author
- Most popular author
- **Endpoint:** `GET /api/analytics/by-author/`

#### Task 3.4: Popular Books (10 points)
Find most borrowed/reviewed books:
- Top 10 most borrowed books
- Top 10 highest rated books
- Most searched books (if search tracking exists)
- **Endpoint:** `GET /api/analytics/popular/`

---

## Testing Requirements

### Test Cases
Create comprehensive tests for:
- [ ] Excel export with no filters
- [ ] Excel export with multiple filters
- [ ] PDF generation for valid book ID
- [ ] PDF generation for invalid book ID (404)
- [ ] Dashboard statistics accuracy
- [ ] Analytics aggregations correctness
- [ ] Large dataset performance (1000+ books)
- [ ] Memory usage for exports

### Postman Collection
Create a Postman collection with:
- All export endpoints
- All analytics endpoints
- Example requests with different filters
- Documentation for each request

---

## Bonus Tasks (+30 points)

### Bonus 1: Email Reports (+10 points)
Send generated reports via email:
- Send Excel reports to admin
- Email invoices to users
- Scheduled weekly reports

### Bonus 2: Charts & Visualizations (+10 points)
Add data visualization:
- Sales trends (line chart)
- Genre distribution (pie chart)
- Price distribution (histogram)
- Export charts to Excel/PDF

### Bonus 3: Scheduled Reports (+10 points)
Implement automated report generation:
- Daily summary email
- Weekly sales report
- Monthly inventory report
- Use Celery for scheduling

---

## Submission Guidelines

### What to Submit
1. **Code Repository**
   - All implementation files
   - Tests with >80% coverage
   - README with setup instructions

2. **Documentation**
   - API endpoint documentation
   - Sample reports (Excel, PDF)
   - Postman collection

3. **Screenshots/Videos**
   - Generated Excel file screenshot
   - Generated PDF screenshot
   - Dashboard statistics screenshot
   - (Optional) Video demo

### Submission Format
```
homework-submission/
├── code/
│   └── library-project/
│       ├── books/
│       │   ├── exports.py
│       │   ├── reports.py
│       │   ├── analytics.py
│       │   └── tests/
│       └── requirements.txt
├── samples/
│   ├── books_report.xlsx
│   ├── book_details.pdf
│   └── invoice_sample.pdf
├── postman/
│   └── analytics-reporting.postman_collection.json
└── README.md
```

---

## Grading Rubric

| Category | Points | Criteria |
|----------|--------|----------|
| **Excel Export** | 30 | Functionality, styling, features |
| **PDF Reports** | 30 | Layout, content, professional look |
| **Analytics** | 40 | Correctness, performance, coverage |
| **Code Quality** | 10 | Clean code, documentation, tests |
| **Bonus** | +30 | Extra features implementation |
| **Total** | 110 | (100 base + 10 quality + 30 bonus) |

### Grade Scale
- **A+ (100-110)**: Excellent work with bonus features
- **A (90-99)**: All requirements met perfectly
- **B (80-89)**: Most requirements met with minor issues
- **C (70-79)**: Basic requirements met
- **D (60-69)**: Incomplete or significant issues
- **F (<60)**: Major requirements missing

---

## Tips & Hints

### Excel Export Tips
```python
# Use generators for large datasets
def generate_rows():
    for book in Book.objects.iterator(chunk_size=1000):
        yield [book.title, book.author.name, book.price]

for row in generate_rows():
    ws.append(row)
```

### PDF Tips
```python
# Use tables for structured data
from reportlab.platypus import Table, TableStyle

data = [['Title', 'Author', 'Price'], ...]
table = Table(data)
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
]))
```

### Analytics Tips
```python
# Use aggregation efficiently
from django.db.models import Count, Avg, Sum

stats = Book.objects.aggregate(
    total=Count('id'),
    avg_price=Avg('price'),
    total_value=Sum('price')
)
```

---

## Resources

### Documentation
- [openpyxl Docs](https://openpyxl.readthedocs.io/)
- [ReportLab User Guide](https://www.reportlab.com/docs/reportlab-userguide.pdf)
- [Django Aggregation](https://docs.djangoproject.com/en/stable/topics/db/aggregation/)

### Examples
- Check `examples/` folder for reference implementations
- Review lesson code for best practices

### Common Issues
- **Memory issues**: Use `iterator()` for large querysets
- **File not found**: Check file paths and permissions
- **Slow queries**: Use `select_related()` and `prefetch_related()`

---

## Timeline

| Week | Task | Deliverable |
|------|------|-------------|
| Week 1 | Excel Export | Working endpoints with tests |
| Week 2 | PDF Reports | Sample PDFs generated |
| Week 3 | Analytics | Dashboard with all stats |
| Week 4 | Testing & Polish | Complete submission |

**Deadline:** 4 weeks from lesson completion

---

## FAQs

**Q: Can I use different libraries?**
A: Yes, but explain why (e.g., xlsxwriter instead of openpyxl)

**Q: How to handle large files?**
A: Use streaming responses and generators

**Q: Should I implement all bonus tasks?**
A: Bonus tasks are optional but recommended for A+

**Q: Can I work in groups?**
A: Individual work preferred, but pair programming allowed

---

## Support

Need help?
- Review lesson examples
- Check documentation
- Ask in course forum
- Office hours: [Schedule]

---

**Good luck!**

Remember: Focus on clean code, proper error handling, and comprehensive testing!