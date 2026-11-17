"""Keep a section or a compact signature/remission/history unit together when it fits a page and the page is not left mostly empty."""
import re

from reportlab.platypus import CondPageBreak, KeepTogether, PageBreak, Spacer


SECTION_MAX_BLANK = .4  # share of the page a section may leave blank when it moves whole to the next one


class KeepSection(Spacer):
    """Zero-height marker before a section. A section that would be cut, fits on one page and leaves no more than
    ``max_blank`` of the page empty if it moves, goes whole to the next page."""
    locChanger = 1

    def __init__(self, unit, page_height, max_blank=SECTION_MAX_BLANK):
        Spacer.__init__(self, 0, 0)
        self.unit, self.page_height, self.max_blank = unit, page_height, max_blank * page_height
        self.needed = None

    def measure(self, width):
        total, previous_after = 0, 0
        canvas = self._doctemplateAttr("canv")
        for index, item in enumerate(self.unit):
            _, height = item.wrapOn(canvas, width, self.page_height)
            if isinstance(item, KeepTogether):
                height = item._H  # KeepTogether reports a huge height to force a split; its content height is stored apart
            before = item.getSpaceBefore()
            total += height + (0 if index == 0 else max(before, previous_after))
            previous_after = item.getSpaceAfter()
        return total

    def wrap(self, availWidth, availHeight):
        if self.needed is None:
            self.needed = self.measure(availWidth)
        if self.needed > availHeight and self.needed <= self.page_height and availHeight <= self.max_blank:
            frame = self._doctemplateAttr("frame")
            if frame:
                from reportlab.platypus.doctemplate import FrameBreak
                frame.add_generated_content(FrameBreak)
        return 0, 0


class FlexKeepTogether(KeepTogether):
    """A keepWithNext group that moves whole to the next page only when little room is left: with more than
    ``limit`` points still free, its content flows and splits where it must."""

    def __init__(self, flowables, maxHeight=None, limit=0):
        KeepTogether.__init__(self, flowables, maxHeight=maxHeight)
        self.limit = limit

    def split(self, aW, aH):
        if self.limit and aH > self.limit:
            return self._content[:]
        return KeepTogether.split(self, aW, aH)


def scale_figure(figure, factor):
    """Scale an Image (draw size) or an SVG Drawing in place."""
    if hasattr(figure, "drawWidth"):
        figure.drawWidth *= factor
        figure.drawHeight *= factor
    else:
        figure.scale(factor, factor)
        figure.width *= factor
        figure.height *= factor


class FitFigure(KeepTogether):
    """Caption, figure and notes kept whole. When the block overshoots the room left on a page that is still mostly
    empty by a little, the figure shrinks (never below ``min_scale``) so it fits instead of leaving the gap."""

    def __init__(self, flowables, figure, limit, min_scale=.88):
        KeepTogether.__init__(self, flowables)
        self.figure, self.limit, self.min_scale = figure, limit, min_scale

    def split(self, aW, aH):
        if getattr(self, "_wrapInfo", None) != (aW, aH):
            self.wrap(aW, aH)
        if self._H > aH and aH > self.limit:
            height = getattr(self.figure, "drawHeight", None) or self.figure.height
            scale = (aH - (self._H - height) - 1) / height
            if self.min_scale <= scale < 1:
                scale_figure(self.figure, scale)
                self.wrap(aW, aH)
        return KeepTogether.split(self, aW, aH)


def keep_sections(story, starts, page_height):
    """Put a KeepSection before every section start, unless the section holds an authored page break."""
    ends = starts[1:] + [len(story)]
    for start, end in reversed(list(zip(starts, ends))):
        unit = story[start:end]
        while unit and isinstance(unit[-1], PageBreak):
            unit.pop()  # the break that opens the next section (new_page) is not part of this one
        if not any(isinstance(item, (PageBreak, CondPageBreak)) for item in unit):
            story.insert(start, KeepSection(unit, page_height))


def signature_rows(headers, rows):
    """Recognize the forms' signature labels, the elaboration/review/approval triad and legacy underscore lines."""
    labels = list(headers) + [row[0] for row in rows if row]
    triad = {'elaboración', 'revisión', 'aprobación'} <= {str(label).strip().casefold() for label in headers}
    return (any(str(label).strip().casefold() in ('firma', 'firmas') for label in labels) or triad
            or any(re.search(r'_{3,}', str(cell)) for row in rows for cell in row))


def append_closing(story, closing, width, page_height, flexible=False):
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
                if flexible:
                    return story[:start] + [KeepSection(group, page_height)] + group
                return story[:start] + [KeepTogether(group)]
        break
    return story + closing
