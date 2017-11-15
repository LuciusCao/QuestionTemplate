import pytest

from QTemplate.parser import check_interval


def test_check_interval():
    check_interval(10, 10)
    check_interval(10, 20)
    with pytest.raises(Exception):
        check_interval(20, 10)
