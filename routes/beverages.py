"""
Route for showing multiple beverages.
"""
from flask import Blueprint, render_template
from utils.beverage import get_beverages

beverages_bp = Blueprint('beverages_bp', __name__)


@beverages_bp.route('/')
def index():
    """
    Fetches beverages from the database and shows the user the list of beverages in the database.

    :return: An HTML page with some of the beverages' information.
    :rtype: str
    """

    # Beverages in storage
    beverages = get_beverages(finished=False)

    return render_template('beverages.html', beverages=beverages)

@beverages_bp.route('stored')
def stored():
    return index()


@beverages_bp.route('finished')
def finished():
    beverages = get_beverages(finished=True)
    
    return render_template('beverages.html', beverages=beverages)


@beverages_bp.route('all')
def all():
    beverages = get_beverages()
    
    return render_template('beverages.html', beverages=beverages)
