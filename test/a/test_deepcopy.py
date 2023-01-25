import pytest
import inspect

import re

from tasks.a.deepcopy import deepcopy
from copy import deepcopy as true_deepcopy

from test.common.modules import unload


def pretest_noimport():
    unload('tasks.a.deepcopy')
    import tasks.a.deepcopy
    source = inspect.getsourcefile(tasks.a.deepcopy)
    with open(source, 'r', encoding='utf-8') as f:
        data = f.read()
    words = re.sub(r'\s+', ' ', data)
    if 'import copy' in words or 'from copy import' in words:
        pytest.fail('Запрещено использовать модуль copy')


TEST_CASES = [
    [],
    [1, 2, 3, 4, 5],
    [[1, 2, 3], [4], [[5]]],
    [[[[[[[[[[[]]]]]]]]]]],
    [[[[[[[1]]], [[[2]]]]]], [[[[[4], [5]]]], [6]]],
    [[], [[]], [[], []], [[[]]], [[[100]]]]
]


@pytest.mark.parametrize(
    ['array'],
    [[tc] for tc in TEST_CASES]
)
def test_deepcopy(array):
    pretest_noimport()
    from tasks.a.deepcopy import deepcopy

    origin = true_deepcopy(array)
    result = deepcopy(array)
    if result != array:
        pytest.fail(f'Скопированный массив не совпадает с исходным: '
                    f'\n\t>исходный: {array}'
                    f'\n\t>копия:    {result}')

    def _test_item(item):
        for i, subitem in enumerate(item):
            if isinstance(subitem, list):
                _test_item(subitem)
            else:
                item[i] = -1
                if result != origin:
                    pytest.fail('Копия изменяется при изменении исходного массива')

    _test_item(array)