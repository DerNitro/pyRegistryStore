# pyRegistryStore

`Внимание проект находится на стадии разработки!!!`

Скрипт по созданию и работе с реестром объектов.

## Создание объекта реестра

Объект описывается в произвольном файле с расширением **.py** директории **objects**, и представляет собой **python class**.

Название модуля будет соответствовать имени класса в нижнем регистре.

    class Person(objects.RegistryStore):
        """
            Person Object

            Parameters
            ----------
            first_name: str
                First Name
            last_name: str
                Last Name
        """
        _protection = False
        
        _uniq_key = ['first_name', 'last_name']
        _desc = 'Module Person'

        first_name:     str = 'Foo'
        last_name:      str = 'Bar'
        sex:            str = ''
        create_date:    datetime = now()

### Атрибуты класса

* `_desc` - Краткое описание модуля, применяется при выводе списка модулей через параметр ls
* `_uniq_key` - список атрибутов класса, которые считают уникальными для объектов в реестре
* [`__doc__`](https://www.python.org/dev/peps/pep-0257/) - описание объекта, используется для получения справки по объекту.
* `_protection` - Установка защиты на класс, если значение True, то добавление новых атрибутов объекта будет запрещено, по умолчанию защита установлена

### Функции определения типов данных для объекта

* `now(format)` - возвращает текущую дату и время в заданном формате [`format`](https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior), по умолчанию формат **'%d/%m/%Y %H:%M:%S'**

## Использование

### Получение справки

Используется ключ **--help**

    ./pyRegistryStore.py --help
    Help: - ./pyRegistryStore.py
    Usage:
    1. get modules list
        ./pyRegistryStore.py ls
    2. get information of module
        ./pyRegistryStore.py <module> help
    3. write record to registry
        ./pyRegistryStore.py <module> set [key=value]...
    4. get records from registry, key=value as filter, return json list of object
        ./pyRegistryStore.py <module> get [key=value]...
    5. last record from registry, key=value as filter, return json object
        ./pyRegistryStore.py <module> last [key=value]...
    6. delete record from registry, key=value as filter
        ./pyRegistryStore.py <module> delete [key=value]...
    7. get markdown table
        ./pyRegistryStore.py <module> markdown [key=value]...

    Sergei V. Utkin, mailto:utkins01@gmail.com, 2021

### Получить список объектов

Используется ключ **ls**

    ./pyRegistryStore.py ls
    List of modules:
    person              Module Person

### Получение справки по модулю

Для получения справки по модулю требуется указать название модуля и передать параметр **help**

    ./pyRegistryStore.py person help

        Person Object

        Parameters
        ----------
        first_name: str
            First Name
        last_name: str
            Last Name

### Создание объекта

Для создания объекта требуется указать название модуля и передать параметр **set**.

Последующие аргументы будут считать атрибутами объекта, и будут добавлены к объекту.

Если если объект уже существует в реестре, атрибуты будут перезаписаны, и обновлена META информация

    ./pyRegistryStore.py person set first_name=Foo last_name=Bar

### Получение объекта

Для получения объекта требуется указать название модуля и передать параметр **get**.

Последующие аргументы будут считаться фильтром через **"И"**. В качестве результата будет передан **список объектов в JSON**

    ./pyRegistryStore.py person get last_name=Bar

### Получение последнего объекта

Для получения объекта требуется указать название модуля и передать параметр **last**.

Последующие аргументы будут считаться фильтром через **"И"**. В качестве результата будет передан последний **объект в JSON**

    ./pyRegistryStore.py person last last_name=Bar

### Удаление объекта

Для удаления объекта требуется указать название модуля и передать параметр **delete**

Последующие аргументы будут считаться фильтром через **"И"**.

    ./pyRegistryStore.py person delete first_name=Foo last_name=Bar

### Формирование таблицы в формате Markdown

Объекты можно вывести в формате **Markdown**, представлены будут в виде таблицы

    ./pyRegistryStore.py person markdown
