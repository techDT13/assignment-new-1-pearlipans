import pytest

from test.common.context import get_integer, get_string

from test.common.basic import check_printable
from test.common.mockit import mock, mock_print
from test.common.modules import unload

TEST_CASES = [
    (
        10, 3, 'abacaba',
        ['10 3 abacaba', 6, 6, 4]
    ),
    (
        145, 91763, 'london is the capital of great britain',
        ['145 91763 london is the capital of great britain', 91617, 116, 13]
    ),
    (
        127633654, -2657253, 'you\'re not the sharpest tool in the shed [some random #$%09 symbols]',
        ['127633654 -2657253 you\'re not the sharpest tool in the shed [some random #$%09 symbols]',
         130290906, 221, 19]
    ),
]


@pytest.mark.parametrize(
    ['x', 'y', 's', 'answers'],
    TEST_CASES
)
def test_controls(x, y, s, answers, line):
    unload('tasks.b.controls')

    with mock(get_integer).returns_many(x, y), mock(get_string).returns(s), \
            mock_print() as output:
        import tasks.b.controls
        results = [line for line in output.getvalue().split('\n') if line.strip() != '']

    check_printable(answers, results, line)
