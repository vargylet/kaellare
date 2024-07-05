"""
Route for showing multiple beverages.
"""
from flask import Blueprint, render_template, request
from utils.beverage import get_beverages

beverages_bp = Blueprint('beverages_bp', __name__)


@beverages_bp.route("/")
def index():
    """
    Fetches beverages from the database and shows the user the list of beverages in the database.

    :return: An HTML page with some of the beverages' information.
    :rtype: str
    """

    filter_value = request.args.get('filter')

    # All beverages in the database
    if filter_value == 'all':
        beverages = get_beverages(
            ("beverageId", "beverageName", "beverageYear", "locationId", "locationName")
        )
    # Beverages currently not in storage
    elif filter_value == 'not_stored':
        beverages = get_beverages(
            ("beverageId", "beverageName", "beverageYear", "locationId", "locationName"), 
            "LEFT JOIN", 
            "beverageLocationId = 0"
        )
    # Beverages in storage
    else:
        beverages = get_beverages(
            ("beverageId", "beverageName", "beverageYear", "locationId", "locationName"), 
            "LEFT JOIN", 
            "beverageLocationId != 0"
        )

    return render_template("beverages.html", beverages=beverages)