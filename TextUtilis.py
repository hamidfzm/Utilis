"""
Some useful functions to work with text

Author: Hamid FzM
Email: hamidfzm@gmail.com
"""

def teaser(text, length=50):
    """
    Convert a long text to teaser without any word wrappings

    Example :
    >>> print teaser('hello my friend. How do you do? Do you believe this is crasy?')
    hello my friend. How do you do? Do you believe...
    """
    if len(text) <= length:
        return text
    parts = text.split(' ')
    while len(' '.join(parts)) > length:
        parts.pop()
    return ' '.join(parts) + '...'
