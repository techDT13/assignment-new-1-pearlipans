import pytest

from tasks.a.game import create_secret, score, validate, \
    computer_player, real_player, play

from test.common.mockit import mock, mock_print


@pytest.mark.parametrize(
    ['n'], [
        (1,),
        (2,),
        (5,),
        (10,),
        (50,)
    ]
)
def test_create_secret(n):
    s = set()
    for i in range(n):
        secret = create_secret(n)
        if len(secret) != n:
            pytest.fail(f'Секретное слово неверного размера: '
                        f'\n\t>ожидалось:  длины {n}'
                        f'\n\t>возвращено: {secret} длины {len(secret)}')
        if not secret.isnumeric():
            pytest.fail(f'Ожидалась строка из цифр, возвращена {secret}')
        s.add(secret)
    if len(s) < n // 2:
        pytest.fail('Генерируемые строки повторяются')

    for i in range(1000):
        s.add(create_secret(n))
    for pos in range(n):
        digits = {int(w[pos]) for w in s}
        if len(digits) != 10:
            pytest.fail(f'Цифры {set(range(10)) - digits} не появляются на позиции {pos + 1}')


@pytest.mark.parametrize(
    ['secret', 'guess', 'answer'],
    [
        ('1111', '1111', (4, 0)),
        ('4271', '1234', (1, 2)),
        ('0123456789', '0112233445', (2, 4)),
        ('00', '11', (0, 0)),
        ('01', '10', (0, 2)),
        ('01', '01', (2, 0)),
        ('99991111', '91913333', (2, 2)),
        ('99991333', '91912222', (2, 1))
    ]
)
def test_score(secret, guess, answer):
    result = score(secret, guess)
    if result[0] != answer[0]:
        pytest.fail(f'Неверное число быков для {secret} и {guess}:'
                    f'\n\t>ожидалось:  {answer[0]}'
                    f'\n\t>возвращено: {result[0]}')
    if result[1] != answer[1]:
        pytest.fail(f'Неверное число коров для {secret} и {guess}:'
                    f'\n\t>ожидалось:  {answer[1]}'
                    f'\n\t>возвращено: {result[1]}')


@pytest.mark.parametrize(
    ['n', 'data', 'answer'],
    [
        (1, '0', True),
        (2, '0', False),
        (10, '1112227890', True),
        (10, '111111111', False),
        (9, '111111111', True),
        (10, '0912856743', True),
        (10, '01a1293289', False),
        (1, '@', False)
    ]
)
def test_validate(n, data, answer):
    result = validate(n, data)
    if result != answer:
        if result:
            pytest.fail(f'Строка {data} для {n=} считается корректной, хотя таковой не является')
        else:
            pytest.fail(f'Строка {data} для {n=} не определена, как корректная')


@pytest.mark.parametrize(
    ['secret'],
    [
        ('1287894',),
        ('1',),
        ('0347991276832974933',),
        ('219498696822873',),
        ('9999',),
    ]
)
def test_play(secret):
    if secret[-1] == '0':
        pytest.fail('Тест некорректен')
    step = -1
    n = len(secret)

    def _player():
        nonlocal step
        step += 1
        if step == 0:
            return '@' * n
        guess = secret[:step]
        guess += (n - len(guess)) * '0'
        return guess

    with mock(create_secret).returns(secret), mock_print() as output:
        play(n, _player)
        result = [line for line in output.getvalue().split('\n') if line.strip() != '']

    if 'digits' not in result[0]:
        pytest.fail('Ожидалось сообщение о неверном формате на первую догадку')
    if len(result) != n + 1:
        pytest.fail(f'Ожидалось ровно {n + 1} строк в выводе, но выведено {len(result)}')
