from django import template
import markdown as md
import bleach

register = template.Library()

ALLOWED_TAGS = [
    'p', 'br', 'strong', 'em', 'a', 'ul', 'ol', 'li', 'code', 'pre', 'blockquote',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'img'
]
ALLOWED_ATTRS = {
    '*': ['class'],
    'a': ['href', 'title', 'rel', 'target'],
    'img': ['src', 'alt', 'title']
}
ALLOWED_PROTOCOLS = ['http', 'https', 'mailto']


@register.filter(name='markdown_safe')
def markdown_safe(text: str) -> str:
    if not text:
        return ''
    html = md.markdown(text, extensions=['extra', 'sane_lists', 'codehilite'])
    clean = bleach.clean(html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS, protocols=ALLOWED_PROTOCOLS, strip=True)
    # linkify plain URLs
    return bleach.linkify(clean)
