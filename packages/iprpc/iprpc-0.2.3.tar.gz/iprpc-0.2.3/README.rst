IPRPC
=====

Библиотека для разбора json-rpc подобных запросов, их валидации и вызова методов.

Пример использования::

    from iprpc import method, MethodExecutor

    class Handler:
        @method()
        async def sum(self, a: int, b: int) -> int:
            return a + b

    executor = MethodExecutor(Handler())
    res = await executor.call(b'{"method":"sum","params":{"a":1,"b":2}}')
    assert res.result == 3
    assert res.error is None

    res = await executor.call(b'{"method":"sum","params":{"a":"NaN","b":2}}')
    assert res.result is None
    assert res.error is not None
    print(res.error)
    >> InvalidArguments(Exception('value is not a valid integer in a',),)

iprpc.MethodExecutor видит только те методы, которые отмечены декоратором iprpc.method.
Если требуется дать сложное имя метода(например использовать спецсимволы в названии),
то в декораторную функцию необходимо передать аргумент name с названием метода::

    class Handler:
        @method(name="math.sum")
        async def sum(self, a: int, b: int) -> int:
            return a + b

При этом вызвать метод передав в него имя метода соответствующее название функции
python уже не получится. Т.е., в примере выше, вызов
`{"method":"sum","params":{"a":1,"b":2}`
завершится ошибкой.
Нужно^ `{"method":"math.sum","params":{"a":1,"b":2}`

Структура запроса
-----------------

По-умолчанию структура запроса должна соответствовать следующей JSON схеме::

    {
        "type": "object",
        "required": [ "method" ],
        "properties": {
            "method": {
                "type": "string"
            },
            "params": {
                "type": "object"
            }
        }
    }

Структура может быть изменена. Ключи объека запроса с именем метода или/и параметрами
могут иметь другие значения.
Для этого нужно в MethodExecutor передать аргумент method_key или/и params_key::

    executor = iprpc.MethodExecutor(TestHandler(), method_key='name', params_key='args')
    await executor.call(b'{"name":"sum","args":{"a":1,"b":2}}')

Также аргументы метода можно передавать в корне запроса. Для этого params_key должен
быть равен None::

    executor = iprpc.MethodExecutor(TestHandler(), params_key=None)
    await executor.call(b'{"method":"sum","a":1,"b":2}')


Валидация с помощью JSON Schema
-------------------------------

Для задания правил валидации нужно передать в декоратор список правил.
Правила представляют собой словарь, где ключ - это имя аргумента, а значение - это
json схема.
Пример::

    class Handler:

        @method(validators={"a": {"type": "integer"},"b": {"type": "integer"}})
        async def sum(self, a, b):
            return a + b



Валиация с помощью pydantinc
----------------------------

Валидация происходит автоматически если есть аннотации типов в объявлении метода.
Например::

    class Handler:
        @method()
        async def sum(self, a: int, b: int):
            return a + b

При этом в запросе можно передавать значение в виде строки или другого совместимого
типа, значение будет автоматически преобразовано(если это возможно).


Сериализация результата
-----------------------

Результат вызываемой функции будет преобразован к простым типам данных для
дальнейшей сериализация в JSON.
Например, если метод возвращает объект datetime, то он будет преобразован в строку в iso формате.
Для большей информации см. функцию `pydantic.json.pydantic_encoder`

Сложный пример::

    from pydantic import BaseModel

    class User(BaseModel):
        id: int
        name: str

    class Handler:
        @method()
        async def rename(self, model: User, name: str) -> User:
            model.name = name
            return model

    executor = MethodExecutor(Handler())
    r = await executor.call(b'{"method":"rename","params":{"model": {"id": 1, "name": "Jhon Snow"},"name": "Jon Snow"}}'
    print(r.result)
    >> {'id': 1, 'name': 'Jon Snow'}


JSON-RPC 2.0
------------

Пример::

    from iprpc import method, JsonRpcError, JsonRpcExecutor

    class Handler:
        @method()
        async def do_something(self, arg1: str):
            return arg1

    executor = JsonRpcExecutor(Handler())

    request = (
        b'{"jsonrpc": "2.0", "id": 1, '
        b'"method": "do_something", "params": {"arg1": 123}}'
    )
    resp = await executor.execute(request)

    print('<< %s' % resp)
    << b'{"jsonrpc": "2.0", "id": 1, "result": "123"}'
