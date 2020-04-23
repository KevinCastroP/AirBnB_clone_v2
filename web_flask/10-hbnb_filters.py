#!/usr/bin/python3
"""
Showing a cities list by states from db
"""


from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity
from operator import getitem

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def list_states():
    """Listing all the states"""
    states = storage.all(State).values()
    return render_template('7-states_list.html', states=states)


@app.route('/cities_by_states', strict_slashes=False)
def list_states_cities():
    """Listing all the cities by states"""
    states = storage.all(State).values()
    return render_template('8-cities_by_states.html', states=states)


@app.route('/states', strict_slashes=False)
def states():
    """Listing all the states"""
    states = storage.all(State).values()
    return render_template('7-states_list.html', states=states)


@app.route('/states/<id>', strict_slashes=False)
def states_id(id):
    """Listing all the states for id"""
    flag = 0
    states = None
    states_all = storage.all(State).values()

    for state in states_all:
        if id in state.id:
            flag = 1
            states = state
            break
    return render_template('9-states.html', states=states, flag=flag)


@app.route('/hbnb_filters', strict_slashes=False)
def filters():
    """Listing all states and cities"""
    states = storage.all(State).values()
    amen = storage.all(Amenity).values()
    return render_template('10-hbnb_filters.html', states=states, amenities=amen)


@app.teardown_appcontext
def close_db(db):
    """Method to close the session"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
