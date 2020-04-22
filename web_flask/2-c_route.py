#!/usr/bin/python3
"""
Starting a flassk web application
"""


from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_world():
    """Printing a message"""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def first_tab():
    """First tab"""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def second_tab(text):
    """Second tab"""
    return 'C {}'.format(text.replace('_'' '))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
