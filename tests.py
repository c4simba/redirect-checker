import pytest

from exceptions import CycleRedirectException, BigRedirectException
from url_checker import check_redirect

NO_REDIRECT_URL = 'http://127.0.0.1/no_redirect_one'
REDIRECT_ONE_URL = 'http://127.0.0.1/redirect_one'
REDIRECT_TWO_URL = 'http://127.0.0.1/redirect_two'
REDIRECT_CYCLE = 'http://127.0.0.1/redirect_cycle'
REDIRECT_BIG = 'http://127.0.0.1/redirect_big'


def test_no_redirect_one():
    result = check_redirect(NO_REDIRECT_URL)
    assert result == NO_REDIRECT_URL


def test_redirect_one():
    result = check_redirect(REDIRECT_ONE_URL)
    assert result == NO_REDIRECT_URL


def test_redirect_two():
    result = check_redirect(REDIRECT_TWO_URL)
    assert result == NO_REDIRECT_URL


def test_redirect_cycle():
    with pytest.raises(CycleRedirectException) as e_info:
        check_redirect(REDIRECT_CYCLE)
    assert e_info.value.url == 'http://127.0.0.1/redirect_cycle'


def test_redirect_big():
    with pytest.raises(BigRedirectException) as e_info:
        check_redirect(REDIRECT_BIG)
    assert e_info.value.url == 'http://127.0.0.1/redirect_big2'
