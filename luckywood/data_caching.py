"""
Data caching class
"""

__author__ = "Frederik Glücks"
__email__ = "frederik@gluecks-gmbh.de"
__copyright__ = "Frederik Glücks - Glücks GmbH"


class DataCaching:
    """
    Data caching class
    """
    __cache: dict = {}

    @staticmethod
    def clear() -> int:
        """
        Complete clearing the data cache and return the number of cleared objects.

        :return: int
        """
        number_of_cached_entries = len(DataCaching.__cache)
        DataCaching.__cache = {}
        return number_of_cached_entries

    @staticmethod
    def get_statistic() -> dict:
        """
        Return the number of cached object. Group by cache_group and object name

        :return: dict
        """
        statistic: dict = {}

        for group_name in DataCaching.__cache:
            statistic[group_name] = {}

            for object_id in DataCaching.__cache[group_name]:
                statistic[group_name][object_id] = len(DataCaching.__cache[group_name][object_id])

        return statistic

    @staticmethod
    def get(group_name: str, object_id: str) -> dict:
        """
        Returns the value of object_id.
        If the object doesn't exists an empty dict will returned

        :param group_name: str
        :param object_id: str
        :return: dict
        """

        if group_name not in DataCaching.__cache:
            return {}

        return DataCaching.__cache[group_name].get(object_id, {})

    @staticmethod
    def set(group_name: str, object_id: str, value: dict):
        """
        Adds the value of to the data cache

        :param group_name: str
        :param object_id: str
        :param value: dict
        :return: None
        """

        if group_name not in DataCaching.__cache:
            DataCaching.__cache[group_name] = {}

        DataCaching.__cache[group_name][object_id] = value
