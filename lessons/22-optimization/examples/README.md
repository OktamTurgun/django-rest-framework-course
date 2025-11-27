# Query Optimization Examples

Bu papkada Django ORM query optimization texnikalariga oid amaliy misollar mavjud.

## Fayllar

### 1. `01-select-related.py`
**Mavzu:** `select_related()` - ForeignKey optimization

**O'rganish:**
- ForeignKey relationships
- SQL JOIN operatsiyalari
- N+1 problem yechimi
- Nested relationships

**Ishga tushirish:**
```bash
python 01-select-related.py
```

---

### 2. `02-prefetch-related.py`
**Mavzu:** `prefetch_related()` - ManyToMany optimization

**O'rganish:**
- ManyToMany relationships
- Reverse ForeignKey
- Prefetch obyekti
- Custom queryset bilan prefetch

**Ishga tushirish:**
```bash
python 02-prefetch-related.py
```

---

### 3. `03-n-plus-one-problem.py`
**Mavzu:** N+1 Problem detection va solution

**O'rganish:**
- N+1 problem nima?
- Qanday aniqlash?
- Yechim usullari
- Before/After comparison

**Ishga tushirish:**
```bash
python 03-n-plus-one-problem.py
```

---

### 4. `04-database-indexes.py`
**Mavzu:** Database Indexes va ularning ta'siri

**O'rganish:**
- Index nima?
- Qachon ishlatiladi?
- Composite indexes
- Migration yaratish

**Ishga tushirish:**
```bash
python 04-database-indexes.py
```

---

### 5. `05-combined-optimization.py`
**Mavzu:** Barcha texnikalarni birlashtirib ishlatish

**O'rganish:**
- select_related + prefetch_related
- Indexes + optimization
- Real-world scenarios
- Performance comparison

**Ishga tushirish:**
```bash
python 05-combined-optimization.py
```

---

## Ishlatish

### 1. Virtual environment yaratish
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 2. Dependencies o'rnatish
```bash
pip install django djangorestframework
```

### 3. Misollarni ishga tushirish
```bash
cd examples
python 01-select-related.py
```

---

## Eslatmalar

1. **Standalone Scripts**: Har bir misol mustaqil ishlaydi va Django settings.py talab qilmaydi
2. **In-Memory Database**: SQLite :memory: ishlatiladi
3. **Query Logging**: Barcha SQL query'lar console'ga chiqadi
4. **Performance Metrics**: Har bir misol vaqt va query count ko'rsatadi

---

## O'rganish tartibi

1. Avval `03-n-plus-one-problem.py` - Muammoni tushunish
2. Keyin `01-select-related.py` - ForeignKey optimization
3. So'ngra `02-prefetch-related.py` - ManyToMany optimization
4. Keyingi `04-database-indexes.py` - Indexlar
5. Nihoyat `05-combined-optimization.py` - Hammasi birgalikda

---

## Qo'shimcha

Har bir faylda:
-  To'liq code
-  Detailed comments
-  SQL query output
-  Performance comparison
-  Best practices

**Happy Learning!**