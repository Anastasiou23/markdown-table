"""Build valid Markdown tables from rows of data.

The implementation targets GitHub-Flavored Markdown table syntax, which is the
most widely supported dialect. The grammar is fixed: a header row, a separator
row of dashes, then zero or more body rows. Every row has the same number of
columns. We pad short rows with empty strings and ignore extra cells in long
rows so callers never have to pre-validate their data shape.
"""

from __future__ import annotations

from typing import Iterable, List, Sequence


class MarkdownTable:
    """Render a list of rows as a GFM Markdown table.

    The table is constructed once from a header and an optional body. Rendering
    is a pure function of the data given at construction time, so the same
    instance can be rendered to a string multiple times cheaply.

    Cell values are coerced with ``str()``. This deliberately keeps the library
    dependency-free: if you need custom formatting for dates or decimals, format
    them to strings before passing them in.
    """

    def __init__(
        self,
        headers: Sequence[object],
        rows: Iterable[Sequence[object]] | None = None,
    ) -> None:
        if headers is None:
            raise TypeError("headers must not be None")
        # Copy so later mutation of the caller's list cannot corrupt the table.
        self._headers: List[str] = [self._cell(h) for h in headers]
        if not self._headers:
            raise ValueError("headers must contain at least one column")
        self._rows: List[List[str]] = [
            [self._cell(c) for c in row] for row in (rows or ())
        ]

    @staticmethod
    def _cell(value: object) -> str:
        """Coerce a value to a string and strip newlines.

        A literal newline inside a cell breaks the row in every Markdown parser,
        so we replace it with a space. Tabs are kept as-is; they render as a
        single space in most renderers and are legal in the source.
        """
        text = str(value)
        return text.replace("\r\n", " ").replace("\n", " ").replace("\r", " ")

    @property
    def headers(self) -> List[str]:
        return list(self._headers)

    @property
    def rows(self) -> List[List[str]]:
        return [list(r) for r in self._rows]

    def _normalized_rows(self) -> List[List[str]]:
        width = len(self._headers)
        out: List[List[str]] = []
        for row in self._rows:
            if len(row) < width:
                out.append(row + [""] * (width - len(row)))
            else:
                out.append(list(row[:width]))
        return out

    def render(self) -> str:
        """Return the table as a Markdown string.

        Columns are sized to the widest cell in any row, including the header.
        Padding is one space on each side, matching the GFM spec's canonical
        form. The separator row uses dashes only (no colons), which renders as
        left-aligned columns everywhere that matters.
        """
        width = len(self._headers)
        body = self._normalized_rows()

        widths = [len(h) for h in self._headers]
        for row in body:
            for i in range(width):
                if len(row[i]) > widths[i]:
                    widths[i] = len(row[i])

        def fmt(cells: Sequence[str]) -> str:
            return (
                "| "
                + " | ".join(cell.ljust(widths[i]) for i, cell in enumerate(cells))
                + " |"
            )

        lines = [fmt(self._headers)]
        lines.append("| " + " | ".join("-" * w for w in widths) + " |")
        lines.extend(fmt(row) for row in body)
        return "\n".join(lines)

    def __str__(self) -> str:
        return self.render()
