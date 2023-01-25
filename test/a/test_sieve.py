import pytest

from tasks.a.sieve import sieve

from test.common.mockit import mock_print

TEST_CASES = [
    (1, []),
    (2, [2]),
    (3, [2, 3]),
    (31, [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]),
    (100, [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97])
]


@pytest.mark.parametrize(
    ['n', 'answer'],
    TEST_CASES
)
def test_sieve(n, answer):
    primes = sieve(n)
    if len(primes) != len(answer):
        pytest.fail(f'Неверное количество простых: '
                    f'\n\t>ожидалось {len(answer)}'
                    f'\n\t>возвращено {len(primes)}')
    for i, (x, y) in enumerate(zip(primes, answer)):
        if x != y:
            pytest.fail(f'Неверное простое под номером {i + 1}: '
                        f'\n\t>ожидалось:  {x}'
                        f'\n\t>возвращено: {y}')
