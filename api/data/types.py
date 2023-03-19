from typing import (
    TypeVar,
    Generic,
    List,
    Dict,
    Any,
    Union,
    Optional,
    Callable,
    Awaitable,
)
from datetime import datetime
from pydantic.typing import NoneType

number = Union[int, float]
string = str
boolean = bool
null = NoneType
true = True
false = False
any = Any
undefined = Optional[Union[null, any]]
Promise = Awaitable
Scalar = Union[null, boolean, number, string]
Map = Dict
Array = List
Date = datetime
JSON = Union[Scalar, Array, Map]
