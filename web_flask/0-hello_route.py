#!/usr/bin/python3
"""
Starting a flask web application
"""


from flask import Flask

app = Flask(__name__)

@app.route('/', strict_slashes=False)
def hello_world():
    """Printing a message"""
    return 'Hello HBNB!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
