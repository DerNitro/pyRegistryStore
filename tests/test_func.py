"""
    Тестирование
"""

import sys
sys.path.append('.')
from objects import auto_type, equal_object, RegistryStore


def test_auto_type():
    """
        Проверка преобразования значений
    """
    assert auto_type('test') == str('test')
    assert auto_type('5') == 5
    for i in ['true', 'y', 'yes']:
        assert auto_type(i)
    for i in ['false', 'f', 'no']:
        assert not auto_type(i)


def test_equal_object():
    """
    Проверка функции идентификации объекта по атрибутам
    """
    test_object = RegistryStore()
    test_object.test1 = True
    test_object.test2 = 'foo'
    test_object.test3 = 5

    assert equal_object(test_object, ['test1=true', 'test2=foo', 'test3=5'])
    assert not equal_object(test_object, ['test1=false', 'test2=foo', 'test3=5'])
