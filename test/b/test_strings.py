import pytest

from test.common.basic import check_printable
from test.common.mockit import mock, mock_print
from test.common.modules import unload

TEST_CASES = [
    (
        'abacaba', 'abracadabra',
        [77, 'abacaba abracadabra', 'abacaba,\tabracadabra',
         'Hello, abacaba! Just wanted to say: \'abracadabra\'', 'abacaba abracadabra', 1, -1]
    ),
    (
        'Dark Cult Leader Name', 'The world will sink into darkness and despair!',
        [966, 'Dark Cult Leader Name The world will sink into darkness and despair!',
         'Dark Cult Leader Name,\tThe world will sink into darkness and despair!',
         'Hello, Dark Cult Leader Name! Just wanted to say: \'The world will sink into darkness and despair!\'',
         'Dark The', 4, -1]
    ),
    (
        'small string', 'big string containing small string and some other #$%',
        [636, 'small string big string containing small string and some other #$%',
         'small string,\tbig string containing small string and some other #$%',
         'Hello, small string! Just wanted to say: \'big string containing small string and some other #$%\'',
         'small big', 2, 22]
    )
]


@pytest.mark.parametrize(
    ['s1', 's2', 'answers'],
    TEST_CASES
)
def test_strings(s1, s2, answers, line):
    unload('tasks.b.strings')

    with mock(input).returns_many(s1, s2), mock_print() as output:
        import tasks.b.strings
        results = [line for line in output.getvalue().split('\n') if line.strip() != '']

    check_printable(answers, results, line)
