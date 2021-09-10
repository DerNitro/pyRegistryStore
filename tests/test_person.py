"""
    Тестирование объекта Person
"""

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
    """
    test_obj = _plugins['person']()

    assert test_obj.desc == 'Module Person'
    assert test_obj.first_name == 'Foo'
    assert test_obj.last_name == 'Bar'
