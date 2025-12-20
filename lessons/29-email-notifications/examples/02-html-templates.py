"""
Example 2: HTML Email Templates

Demonstrates:
- Django template rendering for emails
- HTML email best practices
- Responsive email design
- Template context and variables
- Inline CSS (required for emails)

Use cases:
- Welcome emails with branding
- Order confirmations with details
- Newsletters with rich content
- Password reset with buttons
"""

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

# ============================================================================
# EXAMPLE 1: BASIC TEMPLATE EMAIL
# ============================================================================

def example_1_basic_template():
    """
    Send email using Django template
    
    Template: templates/emails/welcome_basic.html
    """
    
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic Template Email")
    print("="*60)
    
    # Context data for template
    context = {
        'username': 'John Doe',
        'site_name': 'Library System',
        'site_url': 'https://library.com',
    }
    
    # Render HTML template
    html_message = render_to_string('emails/welcome_basic.html', context)
    
    # Create plain text version
    plain_message = strip_tags(html_message)
    
    # Send email
    email = EmailMultiAlternatives(
        subject='Welcome to Library System',
        body=plain_message,
        from_email='noreply@library.com',
        to=['user@example.com']
    )
    email.attach_alternative(html_message, "text/html")
    email.send()
    
    print("✅ Template email sent")
    print(f"   Template: welcome_basic.html")
    print(f"   Context: {context}")


# ============================================================================
# EXAMPLE 2: TEMPLATE WITH BASE
# ============================================================================

def example_2_template_inheritance():
    """
    Use template inheritance for consistent email design
    
    Base template: emails/base_email.html
    Child template: emails/welcome_email.html
    """
    
    print("\n" + "="*60)
    print("EXAMPLE 2: Template Inheritance")
    print("="*60)
    
    context = {
        'user': {
            'username': 'Jane Smith',
            'email': 'jane@example.com',
        },
        'site_url': 'https://library.com',
        'year': 2024,
    }
    
    # Render template that extends base
    html_content = render_to_string('emails/welcome_email.html', context)
    plain_content = strip_tags(html_content)
    
    email = EmailMultiAlternatives(
        subject='Welcome to Our Library!',
        body=plain_content,
        from_email='Library Team <noreply@library.com>',
        to=[context['user']['email']]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
    
    print("✅ Email with base template sent")


# ============================================================================
# EXAMPLE 3: ORDER CONFIRMATION EMAIL
# ============================================================================

def example_3_order_confirmation():
    """
    Rich email with order details
    
    Shows:
    - Complex data structures
    - Loops in templates
    - Calculations
    - Conditional content
    """
    
    print("\n" + "="*60)
    print("EXAMPLE 3: Order Confirmation Email")
    print("="*60)
    
    context = {
        'order': {
            'id': 12345,
            'date': '2024-12-19',
            'status': 'Confirmed',
        },
        'customer': {
            'name': 'John Doe',
            'email': 'john@example.com',
        },
        'items': [
            {
                'title': 'Python Programming',
                'author': 'John Smith',
                'price': 29.99,
                'quantity': 1,
            },
            {
                'title': 'Django for Beginners',
                'author': 'Jane Doe',
                'price': 34.99,
                'quantity': 2,
            },
        ],
        'subtotal': 99.97,
        'tax': 9.00,
        'total': 108.97,
        'shipping_address': {
            'street': '123 Main St',
            'city': 'New York',
            'state': 'NY',
            'zip': '10001',
        },
    }
    
    html_content = render_to_string('emails/order_confirmation.html', context)
    plain_content = strip_tags(html_content)
    
    email = EmailMultiAlternatives(
        subject=f'Order #{context["order"]["id"]} Confirmed',
        body=plain_content,
        from_email='orders@library.com',
        to=[context['customer']['email']]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
    
    print(f"✅ Order confirmation sent: #{context['order']['id']}")
    print(f"   Items: {len(context['items'])}")
    print(f"   Total: ${context['total']}")


# ============================================================================
# EXAMPLE 4: PASSWORD RESET EMAIL
# ============================================================================

def example_4_password_reset():
    """
    Password reset email with secure token link
    
    Shows:
    - Action button (CTA)
    - Security warning
    - Expiration notice
    """
    
    print("\n" + "="*60)
    print("EXAMPLE 4: Password Reset Email")
    print("="*60)
    
    import uuid
    
    context = {
        'user': {
            'username': 'johndoe',
            'email': 'john@example.com',
        },
        'reset_token': str(uuid.uuid4()),
        'reset_url': 'https://library.com/reset-password/',
        'expiry_hours': 24,
        'site_name': 'Library System',
    }
    
    # Complete reset URL
    context['reset_link'] = f"{context['reset_url']}{context['reset_token']}/"
    
    html_content = render_to_string('emails/password_reset.html', context)
    plain_content = strip_tags(html_content)
    
    email = EmailMultiAlternatives(
        subject='Password Reset Request',
        body=plain_content,
        from_email='security@library.com',
        to=[context['user']['email']]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
    
    print("✅ Password reset email sent")
    print(f"   Token: {context['reset_token'][:16]}...")
    print(f"   Expires in: {context['expiry_hours']} hours")


# ============================================================================
# EXAMPLE 5: NOTIFICATION EMAIL
# ============================================================================

def example_5_new_book_notification():
    """
    Notification about new book available
    
    Shows:
    - Book details
    - Book cover image (external URL)
    - Call-to-action button
    """
    
    print("\n" + "="*60)
    print("EXAMPLE 5: New Book Notification")
    print("="*60)
    
    context = {
        'user': {
            'username': 'bookworm',
            'email': 'reader@example.com',
        },
        'book': {
            'title': 'Advanced Django',
            'author': 'John Developer',
            'description': 'Master Django with advanced techniques...',
            'cover_url': 'https://example.com/covers/advanced-django.jpg',
            'price': 39.99,
            'url': 'https://library.com/books/123/',
        },
        'site_name': 'Library System',
    }
    
    html_content = render_to_string('emails/book_notification.html', context)
    plain_content = strip_tags(html_content)
    
    email = EmailMultiAlternatives(
        subject=f'New Book: {context["book"]["title"]}',
        body=plain_content,
        from_email='notifications@library.com',
        to=[context['user']['email']]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
    
    print(f"✅ Book notification sent: {context['book']['title']}")


# ============================================================================
# EXAMPLE 6: REMINDER EMAIL
# ============================================================================

def example_6_book_return_reminder():
    """
    Reminder email for book return
    
    Shows:
    - Urgency indicator
    - Date formatting
    - Conditional content (overdue vs upcoming)
    """
    
    print("\n" + "="*60)
    print("EXAMPLE 6: Book Return Reminder")
    print("="*60)
    
    from datetime import datetime, timedelta
    
    due_date = datetime.now() + timedelta(days=3)
    
    context = {
        'user': {
            'username': 'reader',
            'email': 'reader@example.com',
        },
        'book': {
            'title': 'Python Basics',
            'author': 'John Coder',
        },
        'due_date': due_date,
        'days_remaining': 3,
        'is_overdue': False,
        'late_fee': 0.50,  # per day
    }
    
    html_content = render_to_string('emails/book_reminder.html', context)
    plain_content = strip_tags(html_content)
    
    subject = (
        f'Reminder: Return "{context["book"]["title"]}" in {context["days_remaining"]} days'
        if not context['is_overdue'] else
        f'OVERDUE: Please return "{context["book"]["title"]}"'
    )
    
    email = EmailMultiAlternatives(
        subject=subject,
        body=plain_content,
        from_email='reminders@library.com',
        to=[context['user']['email']]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
    
    print(f"✅ Reminder sent: {context['book']['title']}")
    print(f"   Due in: {context['days_remaining']} days")


# ============================================================================
# EXAMPLE 7: NEWSLETTER
# ============================================================================

def example_7_newsletter():
    """
    Newsletter with multiple sections
    
    Shows:
    - Rich content layout
    - Multiple CTAs
    - Unsubscribe link
    """
    
    print("\n" + "="*60)
    print("EXAMPLE 7: Newsletter")
    print("="*60)
    
    context = {
        'subscriber': {
            'name': 'Book Lover',
            'email': 'bookfan@example.com',
        },
        'newsletter': {
            'title': 'December Book Highlights',
            'month': 'December',
            'year': 2024,
        },
        'featured_books': [
            {
                'title': 'Book 1',
                'author': 'Author 1',
                'description': 'Amazing book...',
                'url': 'https://library.com/books/1/',
            },
            {
                'title': 'Book 2',
                'author': 'Author 2',
                'description': 'Must read...',
                'url': 'https://library.com/books/2/',
            },
        ],
        'statistics': {
            'new_books': 25,
            'active_readers': 1250,
            'books_borrowed': 3450,
        },
        'unsubscribe_url': 'https://library.com/unsubscribe/token123/',
    }
    
    html_content = render_to_string('emails/newsletter.html', context)
    plain_content = strip_tags(html_content)
    
    email = EmailMultiAlternatives(
        subject=f'{context["newsletter"]["title"]} - Library Newsletter',
        body=plain_content,
        from_email='newsletter@library.com',
        to=[context['subscriber']['email']]
    )
    
    # Add unsubscribe header
    email.extra_headers = {
        'List-Unsubscribe': f'<{context["unsubscribe_url"]}>',
    }
    
    email.attach_alternative(html_content, "text/html")
    email.send()
    
    print(f"✅ Newsletter sent: {context['newsletter']['title']}")
    print(f"   Featured books: {len(context['featured_books'])}")


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def create_inline_styles():
    """
    Inline CSS for email compatibility
    
    Email clients have limited CSS support:
    - Use inline styles
    - Avoid external stylesheets
    - Use tables for layout (old school but works)
    - Test in multiple clients
    """
    
    styles = {
        'body': 'font-family: Arial, sans-serif; line-height: 1.6; color: #333;',
        'container': 'max-width: 600px; margin: 0 auto; padding: 20px;',
        'header': 'background-color: #4CAF50; color: white; padding: 20px; text-align: center;',
        'content': 'background-color: #f9f9f9; padding: 20px;',
        'button': 'display: inline-block; padding: 12px 24px; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 5px;',
        'footer': 'background-color: #333; color: white; padding: 15px; text-align: center; font-size: 12px;',
    }
    
    return styles


def render_email_template(template_name, context, subject):
    """
    Helper function to render and send email
    
    Args:
        template_name: Path to template
        context: Template context dict
        subject: Email subject
    
    Returns:
        Rendered HTML and plain text
    """
    
    # Add default context
    default_context = {
        'site_name': 'Library System',
        'site_url': 'https://library.com',
        'year': 2024,
    }
    context = {**default_context, **context}
    
    # Render templates
    html_content = render_to_string(template_name, context)
    plain_content = strip_tags(html_content)
    
    return html_content, plain_content


# ============================================================================
# EMAIL DESIGN BEST PRACTICES
# ============================================================================

"""
✅ EMAIL DESIGN BEST PRACTICES:

1. Layout:
   - Max width: 600px
   - Use tables for layout (better compatibility)
   - Single column on mobile
   - Clear hierarchy

2. CSS:
   - Inline styles only
   - No external stylesheets
   - No <style> tags (limited support)
   - Avoid complex CSS (flexbox, grid)

3. Images:
   - Use absolute URLs
   - Include alt text
   - Don't rely on images for critical info
   - Optimize file sizes

4. Colors:
   - Use hex codes (#RRGGBB)
   - Ensure good contrast
   - Test in dark mode

5. Fonts:
   - Stick to web-safe fonts
   - Arial, Helvetica, Times, Georgia
   - Provide fallbacks

6. Links:
   - Use full URLs (https://...)
   - Make buttons obvious
   - Include unsubscribe link

7. Content:
   - Keep it concise
   - Clear call-to-action
   - Personalize when possible
   - Mobile-friendly

8. Testing:
   - Test in multiple clients (Gmail, Outlook, Apple Mail)
   - Test on mobile devices
   - Check spam score
   - Use Litmus or Email on Acid

❌ AVOID:

1. JavaScript (not supported)
2. Forms (limited support)
3. Videos (use thumbnail + link)
4. Background images (unreliable)
5. External CSS files
6. Excessive images
7. Too much text
8. Tiny fonts
"""

# ============================================================================
# TEMPLATE STRUCTURE EXAMPLES
# ============================================================================

"""
Basic template structure:

templates/emails/base_email.html:
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 0; font-family: Arial, sans-serif;">
    <table width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
            <td align="center" style="padding: 20px 0;">
                <table width="600" cellpadding="0" cellspacing="0" border="0">
                    <!-- Header -->
                    <tr>
                        <td style="background-color: #4CAF50; padding: 20px; text-align: center;">
                            <h1 style="color: white; margin: 0;">📚 {{ site_name }}</h1>
                        </td>
                    </tr>
                    
                    <!-- Content -->
                    <tr>
                        <td style="background-color: #f9f9f9; padding: 20px;">
                            {% block content %}{% endblock %}
                        </td>
                    </tr>
                    
                    <!-- Footer -->
                    <tr>
                        <td style="background-color: #333; color: white; padding: 15px; text-align: center; font-size: 12px;">
                            <p>&copy; {{ year }} {{ site_name }}</p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
```

Child template (templates/emails/welcome_email.html):
```html
{% extends 'emails/base_email.html' %}

{% block content %}
    <h2>Welcome, {{ user.username }}!</h2>
    <p>Thank you for joining {{ site_name }}.</p>
    <p style="text-align: center; margin: 20px 0;">
        <a href="{{ site_url }}" 
           style="display: inline-block; padding: 12px 24px; 
                  background-color: #4CAF50; color: white; 
                  text-decoration: none; border-radius: 5px;">
            Get Started
        </a>
    </p>
{% endblock %}
```
"""

# ============================================================================
# DEMO RUNNER
# ============================================================================

def run_all_examples():
    """Run all template email examples"""
    
    print("\n" + "="*70)
    print("DJANGO EMAIL TEMPLATES EXAMPLES")
    print("="*70)
    
    example_1_basic_template()
    example_2_template_inheritance()
    example_3_order_confirmation()
    example_4_password_reset()
    example_5_new_book_notification()
    example_6_book_return_reminder()
    example_7_newsletter()
    
    print("\n" + "="*70)
    print("ALL TEMPLATE EXAMPLES COMPLETED")
    print("="*70)


if __name__ == '__main__':
    run_all_examples()