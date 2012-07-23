import datetime
import json
from unittest import TestCase


class TestCell(TestCase):

    def make_one(self):
        from data_table import Cell
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


class TestTable(TestCase):

    valid_schema = (
        {'id':'age', 'type':int, 'label':'Age'},
        {'id':'name', 'type':str, 'label':'Name'}
    )

    schema_missing_id = (
        {'type':int},
        {'name':'age', 'type':int}
    )

    bob = (18, 'Bob')
    sally = (20, 'Sally')

    def make_one(self):
        from data_table import Table
        return Table

    def test_constructor(self):
        Table = self.make_one()
        table = Table()
        self.assertEqual(table.schema.keys(), [])
        self.assertEqual(table.rows, [])

    def test_missing_id(self):
        Table = self.make_one()
        self.assertRaises(
            TypeError,
            Table,
            self.schema_missing_id
            )

    def test_duplicate_column(self):
        Table = self.make_one()
        table = Table(self.valid_schema)
        self.assertRaises(ValueError,
                          table.add_column,
                          dict(id='age', type=str))

    def test_add_column(self):
        Table = self.make_one()
        table = Table()
        table.add_column(self.valid_schema[0])
        table.add_column(self.valid_schema[1])
        self.assertEqual(table.schema['age'].id, "age")
        self.assertEqual(table.schema['name'].type, str)
        table.append(self.bob)
        self.assertRaises(ValueError,
                          table.add_column,
                          dict(id='height', type=int)
                          )

    def test_insert_row_no_columns(self):
        Table = self.make_one()
        table = Table()
        self.assertRaises(AssertionError,
                          table.append,
                          ('Bob', )
                          )

    def test_insert_row(self):
        Table = self.make_one()
        table = Table(self.valid_schema)
        table.append(self.bob)
        row = table.rows.pop()
        self.assertEqual(row['age'].value, 18)
        self.assertEqual(row['name'].value, 'Bob')

    def test_with_label(self):
        Table = self.make_one()
        table = Table(self.valid_schema)
        table.append(self.bob)
        rows = table.rows
        row = rows.pop()
        self.assertFalse(row['name'].label)

        harry = (17, ('Harry', 'Big Man'))
        table.append(harry)
        row = rows.pop()
        self.assertEqual(row['age'].value, 17)
        self.assertEqual(row['name'].value, 'Harry')
        self.assertEqual(row['name'].label, 'Big Man')

    def test_cell_options(self):
        Table = self.make_one()
        table = Table(self.valid_schema)

        jack = [17, ('Jack', 'Beanstalk', dict(key='value'))]
        table.append(jack)
        row = table.rows.pop()
        self.assertEqual(row['name'].options, {'key':'value'})

        kate = [26, dict(value='Kate', options={'hair':'long'})]
        table.append(kate)
        row = table.rows.pop()
        self.assertEqual(row['name'].value, 'Kate')
        self.assertEqual(row['name'].label, None)
        self.assertEqual(row['name'].options, {'hair':'long'})

    def test_insert_rows(self):
        Table = self.make_one()
        table = Table(self.valid_schema)
        table.extend([self.bob, (20, 'Sally')])
        rows = table.rows
        bob = rows.pop()
        self.assertEqual(bob['name'].value, 'Sally')

        sally = rows.pop()
        self.assertEqual(sally['age'].value, 18)

    def test_invalid_row(self):
        Table = self.make_one()
        table = Table(self.valid_schema)
        self.assertRaises(AssertionError,
                          table.append,
                          [1, 2, 3]
                          )


class TestDataTableEncoder(TestCase):

    def make_one(self):
        from data_table import DataTableEncoder
        return DataTableEncoder

    def test_encode_time(self):
        time = datetime.time(10, 30, 45)
        encoder = self.make_one()
        js = encoder().encode(time)
        python = json.loads(js)
        self.assertEqual(python, [10, 30, 45])

    def test_encode_date(self):
        today = datetime.date(2012, 1, 31)
        encoder = self.make_one()
        js = encoder().encode(today)
        python = json.loads(js)
        self.assertEqual(python, "Date(2012, 0, 31)")

    def test_encode_datetime(self):
        today = datetime.datetime(2012, 1, 31, 12, 30, 45)
        encoder = self.make_one()
        js = encoder().encode(today)
        python = json.loads(js)
        self.assertEqual(python, u"Date(2012, 0, 31, 12, 30, 45)")

    def test_encode_cell(self):
        from data_table import Cell
        c = Cell(1, int)
        encoder = self.make_one()
        js = encoder().encode(c)
        python = json.loads(js)
        self.assertEqual(python, {"v": 1})

    def test_encode_column(self):
        from data_table import Column
        schema = Column(id='age', type=int)
        encoder = self.make_one()
        js = encoder().encode(schema)
        python = json.loads(js)
        self.assertEqual(python,
                         {"type": "number", "id": "age", "label": "age"})

    def test_encode_table(self):
        from data_table import Table
        table = Table()
        encoder = self.make_one()
        js = encoder().encode(table)
        python = json.loads(js)
        self.assertEqual(python,
                         {'rows':[], 'cols':[]})

    def test_encode_unknown(self):
        encoder = self.make_one()
        self.assertRaises(TypeError,
                          encoder.encode,
                          object)


class TestColumn(TestCase):

    minimal_schema = dict(id='age', type=int)
    valid_schema = {'id':'age', 'type':int, 'label':'Age', 'options':{}}

    def make_one(self):
        from data_table import Column
        return Column

    def test_constructor(self):
        Column = self.make_one()

        col = Column(**self.minimal_schema)
        self.assertEqual(col.id, 'age')
        self.assertEqual(col.type, int)

        schema = self.minimal_schema.copy()
        schema['options'] = dict(width=100)
        col = Column(**schema)
        self.assertEqual(col.options, {'width':100})

        schema = self.valid_schema.copy()
        col = Column(**schema)
        self.assertEqual(col.id, 'age')
        self.assertEqual(col.type, int)
        self.assertEqual(col.label, 'Age')
        self.assertEqual(col.options, {})

    def test_validate_type(self):
        Column = self.make_one()
        schema = self.minimal_schema
        schema['type'] = dict
        self.assertRaises(AssertionError,
                          Column,
                          **schema)

    def test_invalid_options(self):
        Column = self.make_one()
        schema = self.minimal_schema.copy()
        schema['options'] = 'Age'
        self.assertRaises(AssertionError,
                          Column,
                          **schema)

    def test_dictionary_interface(self):
        Column = self.make_one()
        col = Column(**self.minimal_schema.copy())
        self.assertEqual(dict(col),
                         {'id':'age', 'type':'number', 'label':'age'})
        schema = self.valid_schema.copy()
        col = Column(**schema)
        self.assertEqual(dict(col),
                         {'id':'age', 'type':'number', 'label':'Age'})
        schema['options'] = {'style':'bold', 'width':100, 'color':'red'}
        col = Column(**schema)
        self.assertEqual(dict(col),
                         {'id':'age', 'type':'number', 'label':'Age',
                          'options':{'style':'bold', 'width':100, 'color':'red'}
                          }
                         )
