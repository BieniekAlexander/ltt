from dataclasses import dataclass
from enforce_typing import enforce_types

@enforce_types
@dataclass
class A:
    field: str

    def __post_init__(self):
        print("oh")

@enforce_types
@dataclass
class B(A):
    field: int

    def __post_init__(self):
        print("wow")
        super().__post_init__()

b = B(1)
print(b.field)