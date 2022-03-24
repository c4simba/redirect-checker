"""Exceptions for url detector"""


class URLException(Exception):
    """Exception with url as additional info"""

    url = None

    def __init__(self, message, url):
        super().__init__(message)
        self.url = url


class CycleRedirectException(URLException):
    """Exception with cycle redirect url"""
    pass


class BigRedirectException(URLException):
    """Exception with big data redirect url"""
    pass


class BadRedirectException(URLException):
    """Any other exception"""
    pass
