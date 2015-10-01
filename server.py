
from flask import *

app = Flask(__name__)

@app.route('/page')
def somefunc():
    return """
    <html>
        <head>
        <title>A title</title>
        </head>

        <body>
        Seni gedi findikkiran
        </body>
    </html>
    """

app.run(port=80, host="0.0.0.0", debug=True)
