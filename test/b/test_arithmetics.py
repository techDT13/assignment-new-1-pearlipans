import pytest
import inspect

import re

from test.common.context import get_integer, get_float

from test.common.basic import check_printable
from test.common.mockit import mock, mock_print
from test.common.modules import unload


def pretest_noimport():
    with mock_print():
        import tasks.b.arithmetics
    source = inspect.getsourcefile(tasks.b.arithmetics)
    with open(source, 'r', encoding='utf-8') as f:
        data = f.read()
    words = re.sub(r'\s+', ' ', data)
    if 'import math' in words or 'from math import' in words:
        pytest.fail('Запрещено использовать модуль math')


TEST_CASES = [
    (
        10, 3, 0.5,
        ['10 3 0.5', 13.5, 15.0, 5, 20.0, 20.0, 1, 1.7320508075688772, 109044078.609375, '0.50000']
    ),
    (
        0, 19, 2.0,
        ['0 19 2.0', 21.0, 0.0, 0, 0.0, 0.0, 0, 361.0, 508169592.0, '2.00000']
    ),
    (
        974, 146, 13.127684636,
        ['974 146 13.127684636', 1133.127684636, 1866809.265977744, 12787, 74.19434782345422, 74.0,
         98, 2.587865684206011e+28, 5.445168149350603e+24, '13.12768']
    ),
    (
        15, 4, 4.111119,
        ['15 4 4.111119', 23.111119000000002, 246.66714000000002, 62, 3.648641647201163, 3.0,
         3, 298.6347000789221, 25548268533.895233, '4.11112']
    )
]


@pytest.mark.parametrize(
    ['x', 'y', 'z', 'answers'],
    TEST_CASES
)
def test_arithmetics(x, y, z, answers, line):
    pretest_noimport()
    unload('tasks.b.arithmetics')

    with mock(get_integer).returns_many(x, y), mock(get_float).returns(z), \
            mock_print() as output:
        import tasks.b.arithmetics
        results = [line for line in output.getvalue().split('\n') if line.strip() != '']

    check_printable(answers, results, line)


@pytest.mark.parametrize(
    ['x', 'y', 'z'],
    [tc[0:3] for tc in TEST_CASES]
)
def test_floats_count(x, y, z):
    unload('tasks.b.arithmetics')
    with mock(get_integer).returns_many(x, y), mock(get_float).returns(z), \
            mock_print() as output:
        import tasks.b.arithmetics
        results = [line for line in output.getvalue().split('\n') if line.strip() != '']

    def _is_type(s, typ):
        try:
            typ(s)
            return True
        except ValueError:
            return False

    cnt = -1
    for line in results:
        if _is_type(line, float) and not _is_type(line, int):
            cnt += 1
    if tasks.b.arithmetics.FLOATS != cnt:
        pytest.fail('Неверное число float\'ов')
