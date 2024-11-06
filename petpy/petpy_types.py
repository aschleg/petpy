from typing import Union, TypeAlias
import datetime

from pandas import DataFrame


# Parameters
AnimalTypes: TypeAlias = Union[str, list, tuple]
PetfinderID: TypeAlias = Union[int, list[int], tuple[int]]
AnimalFeatures: TypeAlias = Union[str, list[str], tuple[str]]
Date: TypeAlias = Union[str, datetime]

# Return Types
Animals: TypeAlias = Union[dict, DataFrame]
