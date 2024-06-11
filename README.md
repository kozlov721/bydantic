# Bydantic

Built on top of Pydantic, Bydantic is a library that provides a way to parse and validate data provided in a form of a byte string.

## Example

The following is a model representing the header of an EDF file.

```python
from bydantic import ByteModel, ByteField
from typing import Annotated, Any


class EDF(ByteModel):
    version: Annotated[str, ByteField(8, strip=True)]
    patient_id: Annotated[str, ByteField(80, strip=True)]
    record_id: Annotated[str, ByteField(80, strip=True)]
    start_date: Annotated[str, ByteField(8)]
    start_time: Annotated[str, ByteField(8)]
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


with open("eeg_data.edf", "rb") as f:
    edf = EDF(f.read())

print(edf)
```
