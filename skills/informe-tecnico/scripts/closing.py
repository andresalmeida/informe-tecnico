"""Keep a compact signature/remission/history unit together when it fits a page."""
import re

from reportlab.platypus import KeepTogether, PageBreak


def signature_rows(headers, rows):
    """Recognize the forms' signature labels, including unfilled underscore lines."""
    labels = list(headers) + [row[0] for row in rows if row]
    return (any(str(label).strip().casefold() in ('firma', 'firmas') for label in labels)
            or any(re.search(r'_{3,}', str(cell)) for row in rows for cell in row))


def append_closing(story, closing, width, page_height):
    for start in range(len(story)-1, -1, -1):
        if not getattr(story[start], '_closing_signature', False):
            continue
        if start and getattr(story[start-1], 'entry', (None, None, None))[2] == 'section':
            start -= 1
        group = story[start:] + closing
        # An authored page break wins. Oversized units retain the usual splitting behavior.
        if not any(isinstance(item, PageBreak) for item in group):
            height = sum(item.wrap(width, page_height)[1] + item.getSpaceBefore() + item.getSpaceAfter()
                         for item in group)
            if height <= page_height:
                return story[:start] + [KeepTogether(group)]
        break
    return story + closing
