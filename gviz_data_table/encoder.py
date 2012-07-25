import datetime
import json

from cell import Cell
from column import Column
from table import Table

class Encoder(json.JSONEncoder):
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

encoder = Encoder()
