from typing import Any

from pydantic import BaseModel
from pydantic.fields import FieldInfo


def decode(b: bytes) -> str:
    return b.decode("ascii")


class ByteField(FieldInfo):
    def __init__(
        self,
        length: int,
        strip: bool = False,
        count: int | str | None = None,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.__length = length
        self.__strip = strip
        self.__count = count

    def _get_length(self) -> int:
        return self.__length

    def _get_strip(self) -> bool:
        return self.__strip

    def _get_count(self) -> int | str | None:
        return self.__count


class ByteModel(BaseModel):
    def __init__(self, data: bytes):
        _i = 0
        _data = {}
        for field, annotation in self.__annotations__.items():
            if not hasattr(annotation, "__origin__") or not hasattr(
                annotation, "__metadata__"
            ):
                raise ValueError("Only annotated fields are supported")
            metadata = annotation.__metadata__[0]
            origin = annotation.__origin__

            if not isinstance(metadata, ByteField):
                raise ValueError("Only ByteFields are supported")
            length = metadata._get_length()
            if getattr(origin, "__origin__", None) is list:
                count = metadata._get_count()
                if count is None:
                    count = len(data) // length
                _list = []
                if isinstance(count, str):
                    count = int(_data[count].strip())
                for _ in range(count):
                    chunk = decode(data[_i : _i + length])
                    if metadata._get_strip():
                        chunk = chunk.strip()
                    _list.append(chunk)
                    _i += length
                _data[field] = _list
            else:
                if _i > len(data):
                    raise ValueError("Data is too short")
                chunk = decode(data[_i : _i + length])
                if metadata._get_strip():
                    chunk = chunk.strip()
                _data[field] = chunk
                _i += length
        return super().__init__(**_data)
