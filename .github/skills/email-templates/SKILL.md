---
name: email-templates
description: "Email template management skill. Use when: creating email templates, implementing template inheritance, variable substitution, HTML/plain text variants, or template testing."
topics:
  - email
  - templates
  - jinja2
  - text-formatting
  - html-emails
  - testing
applyTo:
  - path: "**/templates/**"
  - path: "**/*email*.html"
  - path: "**/*email*.txt"
---

# Email Templates Skill

Comprehensive skill for managing, inheriting, and testing email templates in the Mailer project.

---

## Overview

Email templates are critical for consistent, professional communication. This skill covers:

- **Template Inheritance** – Base templates with reusable blocks
- **Variable Substitution** – Dynamic content injection with Jinja2
- **HTML & Plain Text** – Dual format support for compatibility
- **Template Testing** – Validation before sending
- **Real Examples** – Welcome, Confirmation, Newsletter templates

---

## Template Architecture

### Directory Structure

```
templates/
├── emails/
│   ├── base/
│   │   ├── base.html          # HTML base template
│   │   └── base.txt           # Plain text base template
│   │
│   ├── transactional/         # System emails (Welcome, Confirm, etc.)
│   │   ├── welcome.html
│   │   ├── welcome.txt
│   │   ├── confirmation.html
│   │   └── confirmation.txt
│   │
│   └── marketing/             # Newsletter, promotions
│       ├── newsletter.html
│       ├── newsletter.txt
│       ├── promotion.html
│       └── promotion.txt
│
└── email_components/
    ├── header.html
    ├── footer.html
    ├── styles.css
    └── header_plain.txt
```

---

## 1. Template Inheritance Pattern

### Base Template (HTML)

**File**: `templates/emails/base/base.html`

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Mailer{% endblock %}</title>
    <style>
        {% block styles %}
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            background-color: #007bff;
            color: white;
            padding: 20px;
            text-align: center;
        }
        .content {
            padding: 20px;
            background-color: #f9f9f9;
        }
        .footer {
            background-color: #333;
            color: white;
            padding: 20px;
            font-size: 12px;
            text-align: center;
        }
        a {
            color: #007bff;
            text-decoration: none;
        }
        {% endblock %}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{% block header_title %}Mailer{% endblock %}</h1>
        </div>
        
        <div class="content">
            {% block content %}
            <!-- Content goes here -->
            {% endblock %}
        </div>
        
        <div class="footer">
            {% block footer %}
            <p>&copy; 2026 Mailer Project. All rights reserved.</p>
            <p><a href="{{ unsubscribe_link }}">Unsubscribe</a></p>
            {% endblock %}
        </div>
    </div>
</body>
</html>
```

### Base Template (Plain Text)

**File**: `templates/emails/base/base.txt`

```
{% block header_title_text %}MAILER{% endblock %}
{% block content_text %}
Content goes here
{% endblock %}

---
{% block footer_text %}
© 2026 Mailer Project
Unsubscribe: {{ unsubscribe_link }}
{% endblock %}
```

### Child Template (Welcome Email)

**File**: `templates/emails/transactional/welcome.html`

```html
{% extends "emails/base/base.html" %}

{% block title %}Welcome to Mailer{% endblock %}

{% block header_title %}Welcome, {{ user_name }}!{% endblock %}

{% block content %}
<h2>Welcome to Mailer</h2>

<p>Hi {{ user_name }},</p>

<p>Thank you for subscribing to our mailing list. We're excited to have you on board!</p>

<h3>What's Next?</h3>
<ul>
    <li>Check our latest updates at <a href="{{ website_url }}">{{ website_url }}</a></li>
    <li>Manage your preferences: <a href="{{ preferences_link }}">Update Settings</a></li>
    <li>Need help? <a href="{{ support_link }}">Contact Support</a></li>
</ul>

<p>Best regards,<br>The Mailer Team</p>
{% endblock %}
```

**File**: `templates/emails/transactional/welcome.txt`

```
{% extends "emails/base/base.txt" %}

{% block header_title_text %}WELCOME TO MAILER{% endblock %}

{% block content_text %}
Welcome, {{ user_name }}!

Thank you for subscribing. We're excited to have you.

What's Next?
- Visit us: {{ website_url }}
- Manage preferences: {{ preferences_link }}
- Need help? {{ support_link }}

Best regards,
The Mailer Team
{% endblock %}
```

---

## 2. Variable Substitution

### Template Context Dictionary

```python
# email_sender.py - Template context definition

def prepare_template_context(user, additional_data=None):
    """Prepare context dictionary for template rendering."""
    context = {
        # User information
        'user_name': user.name,
        'user_email': user.email,
        'user_id': user.id,
        
        # System URLs
        'website_url': 'https://mailer.example.com',
        'support_link': 'https://mailer.example.com/support',
        'preferences_link': f'https://mailer.example.com/preferences/{user.id}',
        'unsubscribe_link': f'https://mailer.example.com/unsubscribe/{user.id}',
        
        # Metadata
        'company_name': 'Mailer Project',
        'current_year': datetime.now().year,
    }
    
    # Merge additional data
    if additional_data:
        context.update(additional_data)
    
    return context
```

### Rendering Templates

```python
from jinja2 import Environment, FileSystemLoader

class TemplateManager:
    """Manage email template rendering."""
    
    def __init__(self, template_dir='templates'):
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=True  # Prevent XSS
        )
    
    def render(self, template_name: str, context: dict) -> str:
        """Render template with context."""
        template = self.env.get_template(template_name)
        return template.render(**context)
    
    def render_both(self, template_name: str, context: dict) -> tuple:
        """Render both HTML and plain text versions."""
        html_template = f"{template_name}.html"
        txt_template = f"{template_name}.txt"
        
        html_content = self.render(html_template, context)
        txt_content = self.render(txt_template, context)
        
        return html_content, txt_content
```

### Usage Example

```python
# Prepare context
context = prepare_template_context(
    user=subscriber,
    additional_data={
        'confirmation_code': generate_token(),
        'action_link': f'https://mailer.example.com/confirm/{token}'
    }
)

# Render both versions
manager = TemplateManager()
html, txt = manager.render_both('emails/transactional/welcome', context)

# Send email
sender.send_email(
    to=subscriber.email,
    subject='Welcome to Mailer',
    html_body=html,
    plain_text=txt
)
```

---

## 3. HTML vs Plain Text Templates

### HTML Email Best Practices

```html
<!-- ✅ DO: Inline styles for compatibility -->
<table style="width: 100%; border-collapse: collapse;">
    <tr>
        <td style="padding: 10px; border: 1px solid #ddd;">
            Content
        </td>
    </tr>
</table>

<!-- ❌ DON'T: External stylesheets -->
<link rel="stylesheet" href="style.css">

<!-- ✅ DO: Use tables for layout -->
<table><tr><td>Layout</td></tr></table>

<!-- ❌ DON'T: Use CSS Grid/Flexbox for layout -->
<div style="display: grid;">Layout</div>
```

### Plain Text Best Practices

```
✅ DO: Use clear structure
---
Section 1
- Point 1
- Point 2

Section 2
Important: {{ important_info }}
---

❌ DON'T: Special characters or formatting
™ ® © § ¶
```

### Email Client Compatibility

| Feature | Outlook | Gmail | Apple Mail | Others |
|---------|---------|-------|-----------|--------|
| Tables | ✅ | ✅ | ✅ | ✅ |
| CSS Grid | ❌ | ❌ | ❌ | ❌ |
| Flexbox | ❌ | ⚠️ | ⚠️ | ⚠️ |
| Inline Styles | ✅ | ✅ | ✅ | ✅ |
| Media Queries | ✅ | ✅ | ⚠️ | ⚠️ |

---

## 4. Template Testing

### Test Fixtures

```python
import pytest
from jinja2 import TemplateNotFound
from email_templates import TemplateManager

@pytest.fixture
def template_manager():
    """Create TemplateManager for testing."""
    return TemplateManager('tests/fixtures/templates')

@pytest.fixture
def sample_context():
    """Sample context for template rendering."""
    return {
        'user_name': 'John Doe',
        'user_email': 'john@example.com',
        'website_url': 'https://example.com',
        'support_link': 'https://example.com/support',
        'preferences_link': 'https://example.com/prefs/123',
        'unsubscribe_link': 'https://example.com/unsub/123',
        'company_name': 'Test Company',
    }
```

### Test Cases

```python
class TestTemplateRendering:
    """Test email template rendering."""
    
    def test_render_welcome_template(self, template_manager, sample_context):
        """Test rendering welcome email template."""
        html = template_manager.render('emails/transactional/welcome.html', sample_context)
        
        assert 'Welcome, John Doe!' in html
        assert 'john@example.com' not in html  # Email not in greeting
        assert sample_context['website_url'] in html
    
    def test_render_both_versions(self, template_manager, sample_context):
        """Test rendering HTML and plain text versions."""
        html, txt = template_manager.render_both('emails/transactional/welcome', sample_context)
        
        # Both should contain key info
        assert 'John Doe' in html and 'John Doe' in txt
        assert 'example.com' in html and 'example.com' in txt
        
        # HTML should have HTML tags
        assert '<' in html and '>' in html
        # Plain text should not
        assert '<' not in txt or txt.count('<') < 5
    
    def test_template_variable_injection(self, template_manager):
        """Test that all required variables are injected."""
        context = {
            'user_name': 'Test',
            'user_email': 'test@example.com',
            'website_url': 'https://test.com',
            'support_link': 'https://test.com/support',
            'preferences_link': 'https://test.com/prefs',
            'unsubscribe_link': 'https://test.com/unsub',
            'company_name': 'Test Co',
        }
        
        html = template_manager.render('emails/transactional/welcome.html', context)
        
        # All variables should be rendered
        assert context['user_name'] in html
        assert context['website_url'] in html
        assert context['support_link'] in html
    
    def test_template_inheritance(self, template_manager, sample_context):
        """Test that child templates inherit from base."""
        html = template_manager.render('emails/transactional/welcome.html', sample_context)
        
        # Base template elements should be present
        assert '<html>' in html or '<!DOCTYPE' in html
        assert 'Mailer' in html  # From base template header
        assert '2026' in html or 'reserved' in html  # From footer
    
    def test_template_not_found(self, template_manager, sample_context):
        """Test handling of missing templates."""
        with pytest.raises(TemplateNotFound):
            template_manager.render('emails/nonexistent.html', sample_context)
    
    def test_template_escaping_prevents_xss(self, template_manager):
        """Test that templates escape user input to prevent XSS."""
        malicious_context = {
            'user_name': '<script>alert("XSS")</script>',
            'user_email': 'test@example.com',
            'website_url': 'https://test.com',
            'support_link': 'https://test.com/support',
            'preferences_link': 'https://test.com/prefs',
            'unsubscribe_link': 'https://test.com/unsub',
            'company_name': 'Test Co',
        }
        
        html = template_manager.render('emails/transactional/welcome.html', malicious_context)
        
        # Script tags should be escaped, not executed
        assert '<script>' not in html
        assert '&lt;script&gt;' in html or 'alert' in html
```

---

## 5. Real Examples

### Example 1: Welcome Email

**Use Case**: New subscriber onboarding

```jinja2
{% extends "emails/base/base.html" %}

{% block title %}Welcome to {{ company_name }}{% endblock %}
{% block header_title %}Welcome, {{ user_name }}!{% endblock %}

{% block content %}
<h2>You're In!</h2>
<p>Thanks for joining {{ company_name }}. We can't wait to share great content with you.</p>

<h3>Get Started</h3>
<table>
    <tr>
        <td style="padding: 10px;">
            <a href="{{ preferences_link }}" style="background: #007bff; color: white; padding: 10px 20px; text-decoration: none;">
                Set Preferences
            </a>
        </td>
        <td style="padding: 10px;">
            <a href="{{ website_url }}" style="background: #28a745; color: white; padding: 10px 20px; text-decoration: none;">
                View Updates
            </a>
        </td>
    </tr>
</table>

<h3>Questions?</h3>
<p>Check out <a href="{{ support_link }}">our help center</a> or reply to this email.</p>
{% endblock %}
```

### Example 2: Confirmation Email

**Use Case**: Email verification

```jinja2
{% extends "emails/base/base.html" %}

{% block title %}Confirm Your Email{% endblock %}
{% block header_title %}Confirm Your Email Address{% endblock %}

{% block content %}
<p>Hi {{ user_name }},</p>

<p>To activate your account, please confirm your email by clicking the button below:</p>

<div style="text-align: center; padding: 20px;">
    <a href="{{ confirmation_link }}" style="background: #007bff; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; font-weight: bold;">
        Confirm Email
    </a>
</div>

<p style="color: #999; font-size: 12px;">
    Or copy this link: {{ confirmation_link }}
</p>

<p style="color: #999;">
    This link expires in {{ expiration_hours }} hours.
</p>
{% endblock %}
```

### Example 3: Newsletter

**Use Case**: Periodic content distribution

```jinja2
{% extends "emails/base/base.html" %}

{% block title %}{{ company_name }} Newsletter - {{ month }} {{ year }}{% endblock %}
{% block header_title %}{{ month }} Newsletter{% endblock %}

{% block content %}
<p>Hi {{ user_name }},</p>

<p>Here's what's new this month:</p>

{% for article in articles %}
<div style="margin: 20px 0; padding: 15px; border-left: 4px solid #007bff;">
    <h3><a href="{{ article.url }}">{{ article.title }}</a></h3>
    <p>{{ article.summary }}</p>
    <small style="color: #999;">{{ article.date }}</small>
</div>
{% endfor %}

<div style="text-align: center; margin: 20px 0;">
    <a href="{{ website_url }}/blog" style="background: #007bff; color: white; padding: 10px 20px; text-decoration: none;">
        Read All Articles
    </a>
</div>

<p style="margin-top: 40px; color: #999; font-size: 12px;">
    You're receiving this because you subscribed. 
    <a href="{{ preferences_link }}">Update preferences</a> or 
    <a href="{{ unsubscribe_link }}">unsubscribe</a>.
</p>
{% endblock %}
```

---

## Best Practices

### DO ✅

- Use template inheritance to avoid duplication
- Escape user input (Jinja2 autoescape=True)
- Provide both HTML and plain text versions
- Use inline styles for HTML emails
- Test templates before sending
- Keep templates simple and readable
- Use semantic HTML

### DON'T ❌

- Use external CSS files
- Trust user input without escaping
- Use CSS Grid/Flexbox for layout
- Send only HTML emails
- Use animated GIFs (unreliable support)
- Hardcode URLs (use context variables)
- Use images as the only content

---

## Integration with Email Sender

```python
# email_sender.py

class EmailSender:
    def __init__(self, smtp_config, template_dir='templates'):
        self.smtp_config = smtp_config
        self.template_manager = TemplateManager(template_dir)
    
    def send_template_email(self, to_email, template_name, context, subject):
        """Send email using template."""
        # Render both versions
        html_body, txt_body = self.template_manager.render_both(
            template_name, 
            context
        )
        
        # Send with both versions
        return self.send_email(
            to=to_email,
            subject=subject,
            html_body=html_body,
            plain_text=txt_body
        )
```

---

**Skill Version**: 1.0  
**Template Engine**: Jinja2  
**Minimum Python**: 3.9  
**Status**: Production Ready  
**Last Updated**: 2026-06-21
