"""
    Тестирование объекта Person
"""

import time
import importlib
import inspect
import os

OBJECT_FOLDER = '../objects'

def form_module(file_path: str) -> str:
    """
    Формирует путь до плагина

    Args:
        file_path (str): Путь до файла

    Returns:
        str: Путь до плагина
    """
    return '.' + os.path.splitext(file_path)[0]


# copy-past from https://copyninja.info/blog/dynamic-module-loading.html
def load_plugins() -> list:
    """
    Поиск и загрузка модулей из директории OBJECT_FOLDER

    Returns:
        list: список модулей
    """
    files = os.listdir(os.path.join(os.path.dirname(__file__), OBJECT_FOLDER))
    pluginfiles = []
    for file in files:
        if file.endswith('.py') and not file.startswith('__'):
            pluginfiles.append(file)
    plugins = map(form_module, pluginfiles)
    importlib.import_module('objects')
    modules = []
    for plugin in plugins:
        if not plugin.startswith('__'):
            modules.append(importlib.import_module(plugin, package="objects"))

    return modules


_modules = load_plugins()
_plugins = {}

for module in _modules:
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj):
            _plugins[str(obj.__name__).lower()] = obj

def test_person():
    """
        Тестирование объекта Person
          * Проверка заполнения полей по умолчанию
          * Сравнение по уникальным полям
          * Сравнение по времени создания
    """
    test_obj1 = _plugins['person']()
    time.sleep(0.1)
    test_obj2 = _plugins['person']()

    assert test_obj1.desc == test_obj2.desc == 'Module Person'
    assert test_obj1.first_name == test_obj2.first_name == 'Foo'
    assert test_obj1.last_name == test_obj2.last_name == 'Bar'
    assert test_obj1 == test_obj2
    assert test_obj2 > test_obj1
