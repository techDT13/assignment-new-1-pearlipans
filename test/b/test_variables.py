import pytest

from test.common.context import get_integer

from test.common.mockit import mock_print


def test_variables():
    with mock_print() as output:
        import tasks.b.variables
        from tasks.b.variables import int_var, float_var, str_var
        from tasks.b.variables import p1, p2, p3, p4
        results = [line for line in output.getvalue().split('\n') if line.strip() != '']

    assert int_var == 4
    assert float_var * float_var == 67
    assert str_var == '#just_a_hashtag'

    result = list(map(str.strip, results))
    ps = [p1, p2, p3, p4]
    values = [int_var, float_var, str_var]
    prods = []
    for i in range(len(values)):
        for j in range(i + 1):
            try:
                prods.append(values[i] * values[j])
            except (ValueError, TypeError):
                pass

    assert set(prods) == set(ps), 'Значения переменных p1, p2, p3, p4 неверные'
    assert set(result) == set(map(str, ps)), 'Выведены неверные значения'
