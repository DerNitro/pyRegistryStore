"""
       Copyright 2021 Sergey "DerNitro" Utkin

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import os
from datetime import datetime
import uuid
import json
from typing import List, Union
import yaml

try:
    from mdutils.tools.Table import Table as md_table
    MARKDOWN_MODULE = True
except ModuleNotFoundError:
    MARKDOWN_MODULE = False


class Meta(yaml.YAMLObject):
    """
    Объект хранения meta информации
    """

    def __init__(self):
        self.create_time = datetime.now()
        self.update_time = datetime.now()
        self.uuid = uuid.uuid4()

    def __repr__(self):
        return str(
            {
                "create_time": str(self.create_time),
                "update_time": str(self.update_time),
                "uuid": str(self.uuid)
            }
        )

    def __str__(self) -> str:
        return str(self.__dict__)

    def to_dict(self) -> dict:
        """
        Формирование справочника объекта, для представления в формате JSON

        Returns:
            dict: Справочник
        """
        return dict(
            {
                "create_time": str(self.create_time),
                "update_time": str(self.update_time),
                "uuid": str(self.uuid)
            }
        )

    def update(self):
        """
        Обновление данных объекта
        """
        self.update_time = datetime.now()


class RegistryStore(yaml.YAMLObject):
    """
    Объект RegistryStore.
    """
    _meta = None
    _protection = True

    _file_name = None
    _uniq_key = []
    _desc = None

    def __init__(self):
        self._meta = Meta()
        for key in self.__class__.__dict__:
            if not key.startswith('_'):
                setattr(self, key, getattr(self, key))

    def protection(self, state: bool):
        """
        Устанавливает защиту на добавление атрибутов объекту

        Args:
            state (bool): Статус True - Включить.
        """
        self._protection = state

    def meta_update(self):
        """
            Вызов метода update объекта Meta
        """
        self._meta.update()

    def describe(self) -> str:
        """
        Возвращает значение desc объекта RegistryStore

        Returns:
            str: Значение RegistryStore.desc
        """
        return self._desc

    def uniq_key(self) -> list:
        """
        Возвращает список уникальных атрибутов

        Returns:
            list: Атрибуты
        """
        return self._uniq_key

    def help(self) -> str:
        """
        Возвращает описание объекта docstring

        Returns:
            str: Описание объекта
        """
        return str(self.__class__.__doc__)

    def add_attr(self, key: str, value: str):
        """
        Создает произвольный атрибут объекта RegistryStore

        Args:
            key (str): Название атрибута
            value (str): Значение атрибута
        """
        if not self._protection or hasattr(self, key):
            setattr(self, key, value)
            self.meta_update()

    def get_filename(self) -> str:
        """
        Возвращает имя файла для хранения объектов

        Returns:
            str: Имя файла
        """
        if self._file_name:
            return self._file_name
        return str(self.__class__.__name__).lower() + '.yml'

    def to_dict(self):
        """
        Формирование справочника атрибутов объекта

        Returns:
            dict: Справочник объекта
        """
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, Meta):
                result[key] = value.to_dict()
            else:
                result[key] = value
        return result

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self) -> str:
        return str(self.__dict__)

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            for uniq_key in self._uniq_key:
                if getattr(self, uniq_key) != getattr(other, uniq_key):
                    return False
            return True

        return False

    def __lt__(self, other):
        return self._meta.update_time < other._meta.update_time


def auto_type(value: str) -> Union[int, str, bool]:
    """
    Преобразование строки в INT или BOOL

    Args:
        value (str): Значение

    Returns:
        Преобразованое значение
    """
    if str(value).isdigit():
        return int(value)

    if str(value).lower() in ['true', 'y', 'yes']:
        return True

    if str(value).lower() in ['false', 'f', 'no']:
        return False

    return value


def equal_object(obj: RegistryStore, args: list) -> bool:
    """
    Проверка наличия атрибутов объекта

    Args:
        obj (RegistryStore): Объект
        args (list): список атрибутов

    Returns:
        bool: Истина если все атрибуты присутствуют у объекта
    """
    for arg in args:
        key, value = str(arg).split('=')
        if getattr(obj, key, None) != auto_type(value):
            return False
    return True


def get_list_objects(data: RegistryStore, folder: str, args: list) -> list:
    """
    Загрузка списка объектов по модулю

    Args:
        data (RegistryStore): Класс объекта
        folder (str): Директория хранения данных
        args (list): Список аргументов

    Returns:
        list: Список объектов
    """
    rs_object = data()
    result = []
    file_name = os.path.join(folder, rs_object.get_filename())
    if os.path.isfile(file_name):
        with open(file_name, 'r', encoding='UTF-8') as stream:
            obj_list = yaml.load(stream, Loader=yaml.CLoader)
        for obj in obj_list:
            if equal_object(obj, args):
                result.append(obj)
    return result


def print_json(data: Union[list, RegistryStore]):
    """
    Печать информации об объектах в формате JSON

    Args:
        data (list or RegistryStore): Объект или список объектов
    """
    if isinstance(data, list):
        results = []
        for obj in data:
            results.append(obj.to_dict())
        print(json.dumps(results))
    if isinstance(data, RegistryStore):
        print(json.dumps(data.to_dict()))


def print_markdown(data: list):
    """
    Вывод списка объектов в виде таблицы в формате MArkdown

    Args:
        data (list): Список объектов
    """
    header = set()
    body = []
    for obj in data:
        header |= set([*obj.__dict__]).difference(set(obj.uniq_key()))
    header = list(header.difference(set(['_meta'])))
    header.insert(0, 'name')
    for obj in data:
        for h in header:
            if h == 'name':
                name = []
                for uk in obj.uniq_key():
                    name.append(getattr(obj, uk))
                body.append(' '.join(name))
            else:
                body.append(str(getattr(obj, h, "")))
    result = header + body
    table = md_table().create_table(columns=len(header), rows=len(data) + 1, text=result)

    print(table)


def set_object(data: RegistryStore, folder: str, args: list):
    """
    Запись объекта в реестр, если объект существует, то обновляется его информация

    Args:
        data (RegistryStore): Класс объекта
        folder (str): Директория хранения реестра
        args (list): Список аргументов
    """
    obj_list = []
    rs_object = data()
    for arg in args:
        key, value = str(arg).split('=')
        rs_object.add_attr(key, auto_type(value))

    file_name = os.path.join(folder, rs_object.get_filename())
    if os.path.isfile(file_name):
        with open(file_name, 'r', encoding='UTF-8') as stream:
            obj_list = yaml.load(stream, Loader=yaml.CLoader)
        if rs_object in obj_list:
            indx = obj_list.index(rs_object)
            rs_object = obj_list.pop(indx)
            for arg in args:
                key, value = str(arg).split('=')
                rs_object.add_attr(key, auto_type(value))
            obj_list.append(rs_object)
        else:
            obj_list.append(rs_object)
    else:
        obj_list.append(rs_object)

    with open(file_name, 'w', encoding='UTF-8') as stream:
        stream.write(yaml.dump(obj_list, Dumper=yaml.CDumper))

    print_json(rs_object)


def get_object(data: RegistryStore, folder: str, args: list):
    """
    Получение объектов из реестра

    Args:
        data (RegistryStore): Класс объекта
        folder (str): Директория расположения реестра
        args (list): Список аргументов
    """
    print_json(get_list_objects(data, folder, args))


def last_object(data: RegistryStore, folder: str, args: list):
    """
    Получение последнего объекта по дате обновления элемента

    Args:
        data (RegistryStore): Класс объекта
        folder (str): Директория расположения реестра
        args (list): Список аргументов
    """
    print_json(sorted(get_list_objects(data, folder, args), reverse=True)[0])


def help_object(data: RegistryStore):
    """
    Вывод справочной информации

    Args:
        data (RegistryStore): Класс объекта
    """
    rs_object = data()
    print(rs_object.help())


def markdown(data: RegistryStore, folder: str, args: list):
    """
    Формирование таблицы объекта в формите Markdown

    Args:
        data (RegistryStore): Класс объекта
    """
    if MARKDOWN_MODULE:
        print_markdown(get_list_objects(data, folder, args))
    else:
        print("Don't find python module 'mdutils'")


def now(frm: str = '%d/%m/%Y %H:%M:%S') -> str:
    """
    Функция возвращает текущее время и дату

    Args:
        frm (str): Формат времени и даты

    Returns:
        str: Текущее время и дата
    """
    return datetime.now().strftime(frm)


def del_object_list(data: RegistryStore, obj_list: List[RegistryStore]) -> List[RegistryStore]:
    """
    Функция удаляет объект из списка и возвращает получившийся список

    Args:
        data (RegistryStore): Объект
        obj_list (list): Список объектов

    Returns:
        list: Результат
    """
    result = obj_list[:]
    indx = result.index(data)
    result.pop(indx)

    return result


def delete_object(data: RegistryStore, folder: str, args: list):
    """
    Удаление объекта из реестра

    Args:
        data (RegistryStore): Класс объекта
        folder (str): Директория расположения объекта
        args (list): Список аргументов
    """
    obj_list = []
    rs_object = data()
    for arg in args:
        key, value = str(arg).split('=')
        rs_object.add_attr(key, auto_type(value))
    file_name = os.path.join(folder, rs_object.get_filename())
    if os.path.isfile(file_name):
        with open(file_name, 'r', encoding='UTF-8') as stream:
            obj_list = yaml.load(stream, Loader=yaml.CLoader)
        if rs_object in obj_list:
            indx = obj_list.index(rs_object)
            rs_object = obj_list.pop(indx)

    with open(file_name, 'w', encoding='UTF-8') as stream:
        stream.write(yaml.dump(obj_list, Dumper=yaml.CDumper))
