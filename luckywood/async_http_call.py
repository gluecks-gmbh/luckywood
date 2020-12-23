"""
Class to create an http call without waiting of a response.
"""

__author__ = "Frederik Glücks"
__email__ = "frederik@gluecks-gmbh.de"
__copyright__ = "Frederik Glücks - Glücks GmbH"

# Generic/Built-in Imports
import threading
from typing import Dict

# External libs/modules
import requests


class AsyncHttpCall:
    """
    Class to create an http call without waiting of a response.
    """

    @staticmethod
    def start(url: str, method: str = "GET", payload: str = "", bearer_token: str = ""):
        """
        Starts a thread that calls a http call without waiting for a response

        :param url: str
        :param method: str
        :param payload: json
        :param bearer_token: str
        :return: None
        """
        threading.Thread(target=AsyncHttpCall.thread_call,
                         args=(url, method.upper(), payload, bearer_token)
                         ).start()

    @staticmethod
    def thread_call(url: str, method: str, payload: str, bearer_token: str):
        """
        Runs the http call by http method

        :param url: str
        :param method: str
        :param payload: str
        :param bearer_token: str
        :return: None
        """

        if bearer_token != "":
            headers: Dict[str, str] = {"Authorization": "Bearer " + bearer_token}
        else:
            headers: Dict[str, str] = {}

        if method == 'GET':
            requests.get(url, data=payload, headers=headers)

            if payload != {}:
                raise Warning("HTTP method get should not have a payload!")
        elif method == 'PUT':
            requests.put(url, data=payload, headers=headers)
        elif method == 'POST':
            requests.post(url, data=payload, headers=headers)
        elif method == 'DELETE':
            requests.delete(url, headers=headers)
        elif method == 'OPTIONS':
            requests.options(url, headers=headers)
        else:
            raise RuntimeError("unknown http method {}".format(method))
