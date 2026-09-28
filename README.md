# markdown-table

Build valid GitHub-Flavored Markdown tables from rows of data. Standard library only, no dependencies.

```python
from markdown_table import MarkdownTable

table = MarkdownTable(
    ["Name", "Role"],
    [["Alice", "Engineer"], ["Bob", "Designer"]],
)
print(table.render())
```

Output:

```
| Name  | Role      |
| ----- | --------- |
| Alice | Engineer  |
| Bob   | Designer  |
```

## Why this exists

Generating Markdown tables by hand is fiddly: you have to count columns, pad cells so the source stays readable, and remember the separator row. This library does exactly that and nothing else. The trade-off is that it only supports GFM-style tables with left-aligned columns. If you need column alignment controls, HTML cells, or caption syntax, this is not the right tool.

## Edge cases

- Short rows are padded with empty cells; long rows are truncated to the header width. You do not have to pre-shape your data.
- Newlines inside a cell are replaced with a space, because a literal newline breaks the row in every Markdown parser.
- Cell values are coerced with `str()`. Format dates and numbers yourself before passing them in.
- Pipe characters (`|`) in cell text are left as-is. Most renderers handle them fine, but if you target a strict parser you should escape them yourself.

## Running the tests

```
PYTHONPATH=src python -m unittest discover -s tests
```
