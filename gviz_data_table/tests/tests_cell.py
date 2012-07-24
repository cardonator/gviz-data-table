from unittest import TestCase


class TestCell(TestCase):

    def make_one(self):
        from gviz_data_table.cell import Cell
        return Cell

    def test_valid_data(self):
        Cell = self.make_one()
        c = Cell(1, int)
        self.assertEqual(c.value, 1)
        self.assertEqual(c.type, int)
        c = Cell('a', str)
        self.assertEqual(c.value, "a")
        self.assertEqual(c.type, str)

    def test_empty_cell(self):
        Cell = self.make_one()
        c = Cell(None, int)
        self.assertFalse(c.value)

    def test_invalid_data(self):
        Cell = self.make_one()
        self.assertRaises(ValueError,
                          Cell,
                          1, str)

    def test_label(self):
        Cell = self.make_one()
        c = Cell(1, int)
        self.assertFalse(c.label)
        c = Cell(1, int, "Birthday")
        self.assertEqual(c.label, "Birthday")
