#!/usr/bin/python3
"""
Showing a states list from db
"""


from flask import Flask, render_template
from models import storage
from models.state import State
from operator import getitem

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def list_states():
    """Listing all the states"""
    states = storage.all(State).values()
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def close_db(db):
    """Method to close the session"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
