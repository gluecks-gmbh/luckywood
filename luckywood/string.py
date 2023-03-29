"""
String class for string operations
"""

__author__ = "Glücks GmbH - Frederik Glücks"
__email__ = "frederik@gluecks-gmbh.de"
__copyright__ = "Copyright 2020, Glücks GmbH"


# Generic/Built-in Imports
import re
from typing import Dict


class String:
    """String class for string operations"""

    @staticmethod
    def decode_to_url(raw_string: str) -> str:
        """Decode a string to a url string

        :param raw_string: String to decode
        :return: Decoded string
        """

        url_string = raw_string.lower()

        decode_chars: Dict[str, str] = {
            ", ": "_",
            "+": "_",
            "/": "_",
            " ": "_",
            "ä": "ae",
            "ü": "ue",
            "ö": "oe",
            "ß": "ss",
            ",": ".",
            "é": "e",
            "&amp;": "",
            "(": "",
            ")": ""
        }

        for char in decode_chars:
            url_string = url_string.replace(char, decode_chars[char])

        url_string = re.sub(r"([^a-z0-9_\-.]*)", "", url_string)
        url_string = re.sub(r"([_]+)", "_", url_string)

        return url_string
