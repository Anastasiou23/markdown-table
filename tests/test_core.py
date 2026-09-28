import unittest

from markdown_table import MarkdownTable


class TestMarkdownTable(unittest.TestCase):
    def test_basic_table(self):
        t = MarkdownTable(["Name", "Age"], [["Alice", "30"], ["Bob", "25"]])
        self.assertEqual(
            t.render(),
            "| Name  | Age |\n| ----- | --- |\n| Alice | 30  |\n| Bob   | 25  |",
        )

    def test_no_body_rows(self):
        t = MarkdownTable(["A", "B"])
        self.assertEqual(t.render(), "| A | B |\n| - | - |")

    def test_short_row_padded(self):
        t = MarkdownTable(["A", "B", "C"], [["x"]])
        self.assertEqual(t.render(), "| A | B | C |\n| - | - | - |\n| x |   |   |")

    def test_long_row_truncated(self):
        t = MarkdownTable(["A"], [["x", "y", "z"]])
        self.assertEqual(t.render(), "| A |\n| - |\n| x |")

    def test_empty_header_rejected(self):
        with self.assertRaises(ValueError):
            MarkdownTable([])

    def test_none_headers_rejected(self):
        with self.assertRaises(TypeError):
            MarkdownTable(None)  # type: ignore[arg-type]

    def test_newlines_in_cell_replaced(self):
        t = MarkdownTable(["X"], [["line1\nline2"]])
        self.assertEqual(t.render(), "| X           |\n| ----------- |\n| line1 line2 |")

    def test_crlf_in_cell_replaced(self):
        t = MarkdownTable(["X"], [["a\r\nb"]])
        self.assertEqual(t.render(), "| X   |\n| --- |\n| a b |")

    def test_non_string_values_coerced(self):
        t = MarkdownTable(["N"], [[42], [3.14], [True]])
        self.assertEqual(t.render(), "| N    |\n| ---- |\n| 42   |\n| 3.14 |\n| True |")

    def test_none_value_coerced_to_string(self):
        t = MarkdownTable(["X"], [[None]])
        self.assertEqual(t.render(), "| X    |\n| ---- |\n| None |")

    def test_headers_copied(self):
        h = ["A", "B"]
        t = MarkdownTable(h, [["1", "2"]])
        h.append("C")
        self.assertEqual(t.render(), "| A | B |\n| - | - |\n| 1 | 2 |")

    def test_rows_copied(self):
        data = [["1", "2"]]
        t = MarkdownTable(["A", "B"], data)
        data.append(["3", "4"])
        self.assertEqual(t.render(), "| A | B |\n| - | - |\n| 1 | 2 |")

    def test_str_returns_render(self):
        t = MarkdownTable(["A"], [["1"]])
        self.assertEqual(str(t), t.render())

    def test_headers_property_returns_copy(self):
        t = MarkdownTable(["A", "B"])
        h = t.headers
        h.append("C")
        self.assertEqual(t.headers, ["A", "B"])

    def test_rows_property_returns_copy(self):
        t = MarkdownTable(["A"], [["1"]])
        r = t.rows
        r.append(["2"])
        self.assertEqual(t.rows, [["1"]])

    def test_pipe_in_value_preserved(self):
        t = MarkdownTable(["X"], [["a|b"]])
        self.assertEqual(t.render(), "| X   |\n| --- |\n| a|b |")

    def test_wide_header_determines_width(self):
        t = MarkdownTable(["LongHeader"], [["x"]])
        self.assertEqual(t.render(), "| LongHeader |\n| ---------- |\n| x          |")


if __name__ == "__main__":
    unittest.main()
