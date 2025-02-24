import re
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def remove_images(value):
    """Removes <img> tags from CKEditor content but keeps other HTML."""
    cleaned_text = re.sub(r'<img[^>]*>', '', value)  # Remove <img> tags
    return mark_safe(cleaned_text)  # Mark as safe to keep other HTML