__version__ = '0.2.3'
__build_stamp__ = 1602860598

from .executor import (
    BaseError,
    DeserializeError,
    InternalError,
    InvalidArguments,
    InvalidRequest,
    MethodExecutor,
    MethodNotFound,
    Result,
    method,
)
from .jsonrpc import JsonRpcError, JsonRpcExecutor

__all__ = [
    'BaseError',
    'DeserializeError',
    'InvalidRequest',
    'MethodNotFound',
    'InvalidArguments',
    'InternalError',
    'JsonRpcExecutor',
    'JsonRpcError',
    'method',
    'MethodExecutor',
    'Result',
]

try:
    __import__("iprpc.aioapp")
except ImportError:
    pass

try:
    __import__("iprpc.aiohttp")
except ImportError:
    pass
