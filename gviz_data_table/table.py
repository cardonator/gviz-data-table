from collections import OrderedDict

from cell import Cell
from column import Column


class Table(object):
    """
    Tables are two-dimensional arrays with fixed schemas.

    Columns are ordered dictionaries of id, label and data type.

    Rows are ordered dictionaries mirroring columns.
    """

    def __init__(self, schema=None, options=None):
        """Sample schema
        ({'id':'name', 'type':'string', 'label':'Name', 'options':{} },
         {'id':'age', 'type':'number',}
        )

        """
        self.rows = []
        self.schema = OrderedDict()
        if schema is not None:
            for col in schema:
                self.add_column(col)
        self.options = options

    def add_column(self, description):
        """
        Add a new column

        Columns cannot be added to tables which already contain data.
        """
        column = Column(**description)
        if column.id in self.schema:
            raise ValueError("Duplicate column ids '{0}'".format(column.id))
        self.schema[column.id] = column
        if len(self.rows):
            raise ValueError("Cannot add columns to tables already containing data")

    @property
    def options(self):
        return self._options

    @options.setter
    def options(self, options):
        """
        Ensure that options are a dictionary
        """
        assert isinstance(options, dict) or options is None, "Options must be a dictionary"
        self._options = options

    def _append(self, row):
        """
        Convert incoming data into table cells
        """
        cols = self.schema.values()
        cells = OrderedDict()
        for col, value in zip(cols, row):
            if isinstance(value, tuple):
                cell = Cell(*(col.type,) + value)
            elif isinstance(value, dict):
                value['typ'] = col.type
                cell = Cell(**value)
            else:
                cell = Cell(col.type, value)
            cells[col.id] = cell
        return cells

    def append(self, row):
        """
        Add a row.

        Rows are either sequences of values,
        or sequences of (value, label, options) tuples,
        or sequences of cell dictionaries.
        Dictionaries are the most flexible but also the most verbose.
        Tuples do not have to be complete but will be exhausted in order, i.e.
        you can't have just a value and options.
        """
        assert len(row) == len(self.schema), \
               "Row length does not match number of columns"
        self.rows.append(self._append(row))

    def extend(self, rows):
        """Add multiple rows of data"""
        for row in rows:
            self.append(row)

    def __iter__(self):
        """Dictionary interface for JSON encoding"""
        rows = [{"c":r.values()} for r in self.rows]
        cols = self.schema.values()
        js = ['cols', 'rows', 'p']
        for k, v in zip(js, [cols, rows, self.options]):
            if v is not None:
                yield k, v
