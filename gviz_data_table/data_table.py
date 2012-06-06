"""
Google Visualisation for Python

Convert Python data structures to JSON suitable for the Google Visualisation
Library

https://developers.google.com/chart/interactive/docs/reference?hl=de#dataparam
"""

from collections import OrderedDict
import datetime
import json


class DataTableEncoder(json.JSONEncoder):
    """
    JSON encoder for utility classes.

    Also maps datetime/date and time
    objects to the relevant Google Visualization pseudo Date() constructor
    (month = month -1). Times are lists of [h, m, s] mapped to `timeofday`
    """

    formats = {datetime.date:"Date({0}, {1}, {2})",
               datetime.datetime:"Date({0}, {1}, {2}, {3}, {4}, {5})",
               }

    def default(self, obj):
        if isinstance(obj, Cell):
            return dict(obj)
        elif isinstance(obj, Column):
            return dict(obj)
        elif isinstance(obj, Table):
            return dict(obj)
        t = type(obj)
        if t in self.formats:
            tt = list(obj.timetuple())
            tt[1] -= 1
            return self.formats[t].format(*tt)
        elif t == datetime.time:
            return [obj.hour, obj.minute, obj.second]

        return json.JSONEncoder.default(self, obj)


class Cell(object):
    """
    Cells have values which must conform to their types. They can also have labels

    Cell attributes (python:javascript) mapping

    {'value':'v, 'label':'f', 'options':'p'}
    """

    __slots__ = ['type', '_value', 'label', 'options']

    def __init__(self, value, typ, label=None, options=None):
        self.type = typ
        self.label = label
        self.value = value
        self.options = options

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self.validate(value)
        self._value = value

    def validate(self, value):
        """
        Check that a value conforms to the column type. Or is None.
        """
        if value is None:
            return
        if not isinstance(value, self.type):
            raise ValueError("{0} expected, {1} received".format(self.type,
                                                                 type(value)))

    def __iter__(self):
        """Dictionary interface for JSON encoding"""
        python = ['value', 'label', 'options']
        js = ['v', 'f', 'p']
        for key, attr in zip(js, python):
            value = getattr(self, attr)
            if value:
                yield key, value


valid_types = {str:'string', int:'number', float:'number', bool:'boolean',
               datetime.date:'date', datetime.datetime:'datetime',
               datetime.time:'timeofday'}


class Column(object):
    """A column is a type definition"""

    __slots__ = ('_id', '_type', '_label', '_options')

    def __init__(self, id, type, label=None, options=None):
        self.id = id
        self.type = type
        self.label = label
        self.options = options

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        assert value in valid_types, "{0} Type not supported".format(value)
        self._type = value

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        assert isinstance(value, basestring), "Column ids must be strings"
        self._id = value

    @property
    def label(self):
        return self._label or self.id

    @label.setter
    def label(self, value):
        self._label = value

    @property
    def options(self):
        return self._options

    @options.setter
    def options(self, value):
        assert isinstance(value, dict) or value is None, "Options must be a dictionary"
        self._options = value

    def __iter__(self):
        for key in ['id', 'type', 'label', 'options']:
            value = getattr(self, key, None)
            if value:
                if key == 'type':
                    value = valid_types[value]
                yield key, value


class Table(object):
    """
    Tables are two-dimensional arrays with fixed schemas.

    Columns are ordered dictionaries of id, label and data type.

    Rows are ordered dictionaries mirroring columns.
    """

    encoder = DataTableEncoder()

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

    def _append(self, row):
        """
        Convert incoming data into table cells
        """
        cols = self.schema.values()
        cells = OrderedDict()
        for col, value in zip(cols, row):
            label = None
            typ = col.type
            if isinstance(value, tuple):
                value, label = value
            cells[col.id] = Cell(value, typ, label)
        return cells

    def append(self, row):
        """Add a row.

        Rows are either sequences of values or sequences of (value, label) tuples
        """
        assert len(row) == len(self.schema), "Row length does not match number of columns"
        self.rows.append(self._append(row))

    def extend(self, rows):
        """Add multiple rows of data"""
        for row in rows:
            self.append(row)

    def __iter__(self):
        """Dictionary interface for JSON encoding"""
        rows = [{"c":r.values()} for r in self.rows]
        cols = self.schema.values()
        js = ['cols', 'rows', 'rows']
        #mapping = [('cols', cols), ('rows', rows), ('options', self.options)]
        for k, v in zip(js, [cols, rows, self.options]):
            if v is not None:
                yield k, v
