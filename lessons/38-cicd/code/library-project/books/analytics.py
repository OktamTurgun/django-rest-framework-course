"""
Analytics and Statistics Logic
"""
from decimal import Decimal

from django.db.models import (
    Count,
    Sum,
    Avg,
    Min,
    Max,
    F,
    Q,
    DecimalField,
    ExpressionWrapper,
    Value,
)
from django.db.models.functions import Coalesce

from .models import Book, Author, Genre


DECIMAL_ZERO = Value(Decimal("0.00"))


class BookAnalytics:
    """Book analytics utility class"""

    # =========================
    # DASHBOARD
    # =========================
    @staticmethod
    def get_dashboard_stats():
        """
        Get complete dashboard statistics
        """
        overview = Book.objects.aggregate(
            total_books=Count("id"),
            avg_price=Avg("price"),
            min_price=Min("price"),
            max_price=Max("price"),
            total_stock=Sum("stock"),
            total_value=ExpressionWrapper(
                Sum(F("price") * F("stock")),
                output_field=DecimalField(max_digits=14, decimal_places=2),
            ),
        )

        authors_stats = Author.objects.aggregate(
            total_authors=Count("id"),
            authors_with_books=Count(
                "id", filter=Q(books__isnull=False), distinct=True
            ),
        )

        genres_stats = Genre.objects.aggregate(
            total_genres=Count("id"),
            genres_with_books=Count(
                "id", filter=Q(books__isnull=False), distinct=True
            ),
        )

        stock_status = Book.objects.aggregate(
            out_of_stock=Count("id", filter=Q(stock=0)),
            low_stock=Count("id", filter=Q(stock__gt=0, stock__lt=5)),
            in_stock=Count("id", filter=Q(stock__gte=5)),
        )

        return {
            "overview": {
                "total_books": overview["total_books"],
                "avg_price": float(overview["avg_price"] or 0),
                "min_price": float(overview["min_price"] or 0),
                "max_price": float(overview["max_price"] or 0),
                "total_stock": overview["total_stock"] or 0,
                "total_value": float(overview["total_value"] or 0),
            },
            "authors": {
                "total": authors_stats["total_authors"],
                "with_books": authors_stats["authors_with_books"],
            },
            "genres": {
                "total": genres_stats["total_genres"],
                "with_books": genres_stats["genres_with_books"],
            },
            "stock_status": stock_status,
        }

    # =========================
    # BOOKS BY GENRE
    # =========================
    @staticmethod
    def get_books_by_genre():
        """
        Get books statistics grouped by genre
        """
        return (
            Genre.objects.annotate(
                book_count=Count("books"),
                avg_price=Coalesce(
                    Avg("books__price"),
                    DECIMAL_ZERO,
                    output_field=DecimalField(max_digits=10, decimal_places=2),
                ),
                min_price=Coalesce(
                    Min("books__price"),
                    DECIMAL_ZERO,
                    output_field=DecimalField(max_digits=10, decimal_places=2),
                ),
                max_price=Coalesce(
                    Max("books__price"),
                    DECIMAL_ZERO,
                    output_field=DecimalField(max_digits=10, decimal_places=2),
                ),
                total_stock=Coalesce(Sum("books__stock"), 0),
                total_value=Coalesce(
                    ExpressionWrapper(
                        Sum(F("books__price") * F("books__stock")),
                        output_field=DecimalField(
                            max_digits=14, decimal_places=2
                        ),
                    ),
                    DECIMAL_ZERO,
                ),
            )
            .filter(book_count__gt=0)
            .order_by("-book_count")
        )

    # =========================
    # BOOKS BY AUTHOR
    # =========================
    @staticmethod
    def get_books_by_author():
        """
        Get books statistics grouped by author
        """
        return (
            Author.objects.annotate(
                book_count=Count("books"),
                avg_price=Coalesce(
                    Avg("books__price"),
                    DECIMAL_ZERO,
                    output_field=DecimalField(max_digits=10, decimal_places=2),
                ),
                total_stock=Coalesce(Sum("books__stock"), 0),
                total_pages=Coalesce(Sum("books__pages"), 0),
                avg_pages=Coalesce(Avg("books__pages"), 0.0),
                total_value=Coalesce(
                    ExpressionWrapper(
                        Sum(F("books__price") * F("books__stock")),
                        output_field=DecimalField(
                            max_digits=14, decimal_places=2
                        ),
                    ),
                    DECIMAL_ZERO,
                ),
            )
            .filter(book_count__gt=0)
            .order_by("-book_count")
        )

    # =========================
    # POPULAR BOOKS
    # =========================
    @staticmethod
    def get_popular_books(limit=10):
        try:
            from .models import BorrowHistory

            return (
                Book.objects.annotate(
                    borrow_count=Count("borrow_history")
                )
                .filter(borrow_count__gt=0)
                .order_by("-borrow_count")[:limit]
            )
        except Exception:
            return (
                Book.objects.annotate(
                    popularity_score=ExpressionWrapper(
                        F("stock") * Value(-1),
                        output_field=DecimalField(
                            max_digits=10, decimal_places=2
                        ),
                    )
                )
                .order_by("popularity_score")[:limit]
            )

    # =========================
    # PRICE DISTRIBUTION
    # =========================
    @staticmethod
    def get_price_distribution():
        return {
            "budget": Book.objects.filter(price__lt=30).count(),
            "moderate": Book.objects.filter(
                price__gte=30, price__lt=50
            ).count(),
            "premium": Book.objects.filter(
                price__gte=50, price__lt=70
            ).count(),
            "luxury": Book.objects.filter(price__gte=70).count(),
        }

    # =========================
    # STOCK ANALYSIS
    # =========================
    @staticmethod
    def get_stock_analysis():
        return {
            "status": {
                "out_of_stock": Book.objects.filter(stock=0).count(),
                "critical": Book.objects.filter(
                    stock__gte=1, stock__lte=2
                ).count(),
                "low": Book.objects.filter(
                    stock__gte=3, stock__lte=5
                ).count(),
                "normal": Book.objects.filter(
                    stock__gte=6, stock__lte=10
                ).count(),
                "high": Book.objects.filter(stock__gt=10).count(),
            },
            "needs_restock": Book.objects.filter(stock__lt=5)
            .select_related("author")
            .order_by("stock")[:20],
            "highest_stock": Book.objects.select_related("author")
            .order_by("-stock")[:10],
        }

    # =========================
    # TOP BOOKS
    # =========================
    @staticmethod
    def get_top_expensive_books(limit=10):
        return (
            Book.objects.select_related("author")
            .order_by("-price")[:limit]
        )

    @staticmethod
    def get_top_affordable_books(limit=10):
        return (
            Book.objects.select_related("author")
            .filter(stock__gt=0)
            .order_by("price")[:limit]
        )

    @staticmethod
    def get_top_valued_books(limit=10):
        return (
            Book.objects.annotate(
                stock_value=ExpressionWrapper(
                    F("price") * F("stock"),
                    output_field=DecimalField(
                        max_digits=14, decimal_places=2
                    ),
                )
            )
            .select_related("author")
            .order_by("-stock_value")[:limit]
        )

    # =========================
    # PERFORMANCE
    # =========================
    @staticmethod
    def get_genre_performance():
        genres = BookAnalytics.get_books_by_genre()

        if not genres.exists():
            return {
                "most_books": None,
                "highest_value": None,
                "most_expensive": None,
                "most_stock": None,
            }

        return {
            "most_books": genres.order_by("-book_count").first(),
            "highest_value": genres.order_by("-total_value").first(),
            "most_expensive": genres.order_by("-avg_price").first(),
            "most_stock": genres.order_by("-total_stock").first(),
        }

    @staticmethod
    def get_author_performance():
        authors = BookAnalytics.get_books_by_author()

        if not authors.exists():
            return {
                "most_productive": None,
                "highest_value": None,
                "most_pages": None,
                "most_expensive": None,
            }

        return {
            "most_productive": authors.order_by("-book_count").first(),
            "highest_value": authors.order_by("-total_value").first(),
            "most_pages": authors.order_by("-total_pages").first(),
            "most_expensive": authors.order_by("-avg_price").first(),
        }

    # =========================
    # RECOMMENDATIONS
    # =========================
    @staticmethod
    def get_recommendations():
        recommendations = []

        out_of_stock = Book.objects.filter(stock=0).count()
        if out_of_stock > 0:
            recommendations.append(
                {
                    "type": "warning",
                    "message": f"{out_of_stock} books are out of stock",
                    "action": "Restock these books immediately",
                }
            )

        low_stock = Book.objects.filter(
            stock__gt=0, stock__lt=5
        ).count()
        if low_stock > 0:
            recommendations.append(
                {
                    "type": "info",
                    "message": f"{low_stock} books have low stock",
                    "action": "Monitor and consider restocking",
                }
            )

        expensive = Book.objects.filter(price__gte=70).count()
        total = Book.objects.count()
        if total and expensive > total * 0.3:
            recommendations.append(
                {
                    "type": "info",
                    "message": f"{expensive} premium books (>$70)",
                    "action": "Consider adding more affordable options",
                }
            )

        genre_perf = BookAnalytics.get_genre_performance()
        if genre_perf["highest_value"]:
            recommendations.append(
                {
                    "type": "success",
                    "message": (
                        f"Top performing genre: "
                        f"{genre_perf['highest_value'].name}"
                    ),
                    "action": "Focus marketing efforts on this genre",
                }
            )

        author_perf = BookAnalytics.get_author_performance()
        if author_perf["most_productive"]:
            recommendations.append(
                {
                    "type": "success",
                    "message": (
                        f"Most productive author: "
                        f"{author_perf['most_productive'].name}"
                    ),
                    "action": "Promote this author's works",
                }
            )

        return recommendations
