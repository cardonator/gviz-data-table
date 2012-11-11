import pytest
from gviz_data_table.encoder import Encoder

import datetime
import json


def test_encode_time():
    time = datetime.time(10, 30, 45)
    encoder = Encoder()
    js = encoder.encode(time)
    python = json.loads(js)
    assert python == [10, 30, 45]

def test_encode_date():
    today = datetime.date(2012, 1, 31)
    encoder = Encoder()
    js = encoder.encode(today)
    python = json.loads(js)
    assert python == "Date(2012, 0, 31)"

def test_encode_datetime():
    today = datetime.datetime(2012, 1, 31, 12, 30, 45)
    encoder = Encoder()
    js = encoder.encode(today)
    python = json.loads(js)
    assert python == "Date(2012, 0, 31, 12, 30, 45)"

def test_encode_cell():
    from gviz_data_table.cell import Cell
    c = Cell(int, 1)
    encoder = Encoder()
    js = encoder.encode(c)
    python = json.loads(js)
    assert python == {"v": 1}

def test_encode_column():
    from gviz_data_table.column import Column
    schema = Column(id='age', type=int)
    encoder = Encoder()
    js = encoder.encode(schema)
    python = json.loads(js)
    assert python == {"type": "number", "id": "age", "label": "age"}

def test_encode_table():
    from gviz_data_table.table import Table
    table = Table()
    encoder = Encoder()
    js = encoder.encode(table)
    python = json.loads(js)
    assert python == {'rows':[], 'cols':[]}

def test_encode_unknown():
    encoder = Encoder()
    with pytest.raises(TypeError):
        encoder.encode(object)
