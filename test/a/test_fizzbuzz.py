import pytest

from tasks.a.fizzbuzz import fizzbuzz

from test.common.mockit import mock_print

TEST_CASES = [
    (11, 16, ['11', 'fizz', '13', '14', 'fizzbuzz']),
    (1, 10, ['1', '2', 'fizz', '4', 'buzz', 'fizz', '7', '8', 'fizz']),
    (-3, 4, ['fizz', '-2', '-1', 'fizzbuzz', '1', '2', 'fizz']),
    (132979829, 132979850,
     [132979829, 'fizzbuzz', 132979831, 132979832, 'fizz', 132979834, 'buzz', 'fizz',
      132979837, 132979838, 'fizz', 'buzz', 132979841, 'fizz', 132979843, 132979844,
      'fizzbuzz', 132979846, 132979847, 'fizz', 132979849])
]


@pytest.mark.parametrize(
    ['a', 'b', 'answers'],
    TEST_CASES
)
def test_fizzbuzz(a, b, answers):
    with mock_print() as output:
        fizzbuzz(a, b)
        results = [line for line in output.getvalue().split('\n') if line.strip() != '']

    if len(results) != len(answers):
        pytest.fail(f'Выведено {len(results)} строк, ожидалось {len(answers)}')
    for i, (x, y) in enumerate(zip(results, answers)):
        if x != str(y):
            pytest.fail(f'Неверный ответ на позиции {i + 1}:'
                        f'\n\t>ожидалось: {y}'
                        f'\n\t>выведено:  {x}')
