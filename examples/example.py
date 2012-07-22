import os
import sqlite3
from string import Template

from gviz_data_table.data_table import Table, DataTableEncoder


def data():
    folder = os.path.split(__file__)[0]
    db = sqlite3.connect(os.path.join(folder, "sample.db"))
    c = db.cursor()
    c.execute("SELECT name, salary FROM employees")
    cols = [dict(id=col[0].capitalize(), type=col[1]) for col in c.description]
    # sqlite3 unfortunately does not provide type information
    cols[0]['type'] = unicode
    cols[1]['type'] = float

    t = Table(cols)
    for r in c.fetchall():
        t.append(r)

    encoder = DataTableEncoder()
    return encoder.encode(t)


template = Template("""
<html>

<head>
<script src="http://www.google.com/jsapi" type="text/javascript"></script>
</head>

<body>
<script>
      google.load("visualization", "1", {packages:["corechart", "table"]});


      google.setOnLoadCallback(drawChart);
      function drawChart() {

      var data = new google.visualization.DataTable($data);
      var chart = new google.visualization.BarChart(document.getElementById('chart'));
      chart.draw(data);
      }
</script>
<div id="chart"></div>

</body>

</html>
""")

def save():
    with open("result.html", "wb") as f:
        f.write(template.safe_substitute(data=data()))

if __name__ == "__main__":
    save()