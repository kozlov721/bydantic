import builtins
from datetime import date, time
from typing import Annotated

from pydantic import field_validator
from rich import print

from bydantic import ByteField, ByteModel

builtins.print = print


class EDF(ByteModel):
    version: Annotated[str, ByteField(8, strip=True)]
    patient_id: Annotated[str, ByteField(80, strip=True)]
    record_id: Annotated[str, ByteField(80, strip=True)]
    start_date: Annotated[date, ByteField(8)]
    start_time: Annotated[time, ByteField(8)]
    n_header_bytes: Annotated[int, ByteField(8)]
    reserved: Annotated[str, ByteField(44, exclude=True)]
    n_records: Annotated[int, ByteField(8)]
    duration: Annotated[float, ByteField(8)]
    n_signals: Annotated[int, ByteField(4)]

    labels: Annotated[list[str], ByteField(16, strip=True, count="n_signals")]
    transducer_types: Annotated[
        list[str], ByteField(80, strip=True, count="n_signals")
    ]
    physical_dimensions: Annotated[
        list[str], ByteField(8, strip=True, count="n_signals")
    ]
    physical_mins: Annotated[
        list[float], ByteField(8, strip=True, count="n_signals")
    ]
    physical_maxs: Annotated[
        list[float], ByteField(8, strip=True, count="n_signals")
    ]
    digital_mins: Annotated[
        list[float], ByteField(8, strip=True, count="n_signals")
    ]
    digital_maxs: Annotated[
        list[float], ByteField(8, strip=True, count="n_signals")
    ]
    prefilterings: Annotated[
        list[str], ByteField(80, strip=True, count="n_signals")
    ]
    n_samples: Annotated[
        list[int], ByteField(8, strip=True, count="n_signals")
    ]
    samples_reserved: Annotated[
        list[str], ByteField(32, exclude=True, count="n_signals")
    ]

    @field_validator("start_date", mode="before")
    def validate_start_date(cls, v):
        return date(*map(int, v.split(".")))

    @field_validator("start_time", mode="before")
    def validate_start_time(cls, v):
        return time(*map(int, v.split(".")))  # type: ignore
