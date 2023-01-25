import pytest

from test.common.context import get_integer

from test.common.basic import check_printable
from test.common.mockit import mock, mock_print
from test.common.modules import unload

TEST_CASES = [
    (
        [77],
        [[77], '77 77 77', '77 77', 77, [], 0, [77], [77]]
    ),
    (
        [10, 8, 7, 1, 6, 5, 2, 4, 3, 9],
        [[10, 8, 7, 1, 6, 5, 2, 4, 3, 9], '10 6 9', '1 10', 55, [100, 64, 36, 4, 16], 3,
         [9, 3, 4, 2, 5, 6, 1, 7, 8, 10], [10, 7, 6, 2, 3]]
    ),
    (
        [1, 2, 1, 1, 1, 0, 2, 0, 1, 2, 2],
        [[1, 2, 1, 1, 1, 0, 2, 0, 1, 2, 2], '1 0 2', '0 2', 13, [4, 0, 4, 0, 4, 4], 5,
         [2, 2, 1, 0, 2, 0, 1, 1, 1, 2, 1], [1, 1, 1, 2, 1, 2]]
    )
]


@pytest.mark.parametrize(
    ['array', 'answers'],
    TEST_CASES
)
def test_data(array, answers, line):
    unload('tasks.b.data')

    with mock(get_integer).returns(len(array)).returns_many(*array), \
            mock_print() as output:
        import tasks.b.data
        results = [line for line in output.getvalue().split('\n') if line.strip() != '']

    check_printable(answers, results, line)
