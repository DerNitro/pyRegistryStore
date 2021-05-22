#!/usr/bin/env python3

"""
    Утилита формирование реестра объектов
"""

import sys
import importlib
import os
import inspect
from objects import set, get, last, help as o_help

__author__ = "Sergey V. Utkin"
__version__ = "0.0.0"
__email__ = "utkins01@gmail.com"

OBJECT_FOLDER = 'objects'
REGISTRY_FOLDER = 'registry'


def form_module(fp):
    return '.' + os.path.splitext(fp)[0]


# copy-past from https://copyninja.info/blog/dynamic-module-loading.html
def load_plugins():
    files = os.listdir(os.path.join(os.path.dirname(__file__), OBJECT_FOLDER))
    pluginfiles = []
    for f in files:
        if f.endswith('.py') and not f.startswith('__'):
            pluginfiles.append(f)
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

HELP = """Help: - {file}:{version}
Usage:
  1. Получить список модулей
    {file} ls
  2. Получить информацию по модулю
    {file} <module> help

{author}, mailto:{email}, 2021""".format(
    file=__file__,
    version=__version__,
    author=__author__,
    email=__email__
)

if not os.path.isdir(REGISTRY_FOLDER):
    os.makedirs(REGISTRY_FOLDER)

args = sys.argv[1:]
# print(args)

if len(args) == 0:
    print(HELP)
elif len(args) == 1 and args[0] == 'ls':
    print('Список модулей:')
    for k, v in _plugins.items():
        print("  {name:20}{describe}".format(name=k, describe=v().describe()))
elif args[0] in [i for i in _plugins]:
    if args[1] == 'set':
        set(_plugins[args[0]], REGISTRY_FOLDER, args[2:])
    elif args[1] == 'get':
        get(_plugins[args[0]], REGISTRY_FOLDER, args[2:])
    elif args[1] == 'last':
        last(_plugins[args[0]], REGISTRY_FOLDER, args[2:])
    elif args[1] == 'help':
        o_help(_plugins[args[0]])
    else:
        print(HELP)
elif len(args) == 1 and (args[0] == '-h' or args[0] == '--help'):
    print(HELP)
else:
    print('Не корректный ввод параметров!!!\n')
    print(HELP)

sys.exit(0)
