from typing import Optional, List

from exceptions import BadRedirectException, URLException
from session import SessionChecker

TOO_LONG_RESPONSE = 1000
READ_CHUNK = 100


def check_redirect(url: str, redirected_urls: Optional[List[str]] = None) -> str:
    """
    Check url for redirect

    :param url: input url
    :param redirected_urls: list of urls for detecting redirects
    :return: output url

    can raise Exception due cycle redirect
    """
    try:
        with SessionChecker() as session:
            response = session.get(url, timeout=3, stream=True)
    except URLException as e:
        raise e
    except Exception as e:
        raise BadRedirectException('redirect with error', url)
    return response.url
