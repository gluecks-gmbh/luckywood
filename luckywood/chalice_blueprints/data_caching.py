"""
Chalice Routen für Caching
"""

__author__ = "Glücks GmbH - Frederik Glücks"
__email__ = "frederik@gluecks-gmbh.de"
__copyright__ = "Frederik Glücks - Glücks GmbH"

# Generic/Built-in Imports

# External libs/modules
from chalice import Blueprint

# Own libs/modules
from luckywood import DataCaching


data_caching_routes = Blueprint(__name__)


@data_caching_routes.route('/cache', methods=['DELETE'])
def cache_clear():
    """
    Clear the complete data cache and returns the number of
    deleted objects

    :return: json
    """

    return {
        "cleared": DataCaching.clear()
    }


@data_caching_routes.route('/cache', methods=['GET'])
def get_cache_statistic():
    """
    Returns a statistic of cached objects

    :return: json
    """
    return DataCaching.get_statistic()
