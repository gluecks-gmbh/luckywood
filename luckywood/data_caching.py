"""
Objekt für die Nutzung einer MySQL-Datenbank
"""

__author__ = "Frederik Glücks"
__email__ = "frederik@gluecks-gmbh.de"
__copyright__ = ""


class DataCaching:
    __cache: dict = {}

    @staticmethod
    def clear() -> int:
        """
        Leert den internen Cache vollständig und gibt die Anzahl
        der gelöschten Einträge zurück

        :return: int
        """
        number_of_cached_entries = len(DataCaching.__cache)
        DataCaching.__cache = {}
        return number_of_cached_entries

    @staticmethod
    def get_statistic() -> dict:
        statistic: dict = {}

        for cache_name in DataCaching.__cache:
            statistic[cache_name] = {}

            for cache_id in DataCaching.__cache[cache_name]:
                statistic[cache_name][cache_id] = len(DataCaching.__cache[cache_name][cache_id])

        return statistic

    @staticmethod
    def get(cache_name: str, key: str) -> dict:
        """

        :param cache_name: str
        :param key: str
        :return: dict
        """

        if cache_name in DataCaching.__cache:
            if key in DataCaching.__cache[cache_name]:
                return DataCaching.__cache[cache_name][key]
            else:
                return {}
        else:
            return {}

    @staticmethod
    def set(cache_name: str, key: str, value: dict):
        """

        :param cache_name: str
        :param key: str
        :param value: dict
        :return:
        """

        if cache_name not in DataCaching.__cache:
            DataCaching.__cache[cache_name] = {}

        DataCaching.__cache[cache_name][key] = value
