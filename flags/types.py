from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto

from typing import List


class FLAG_TYPES(Enum):
    EXPIRED = auto()
    OUTZONE = auto()
    DELETE_CANDIDATE = auto()


@dataclass
class Domain:
    fqdn: str
    created_at: datetime
    expire_at: datetime
    deleted_at: datetime


@dataclass
class Flag:
    domain: Domain
    flag_type: FLAG_TYPES
    valid_from: datetime
    valid_to: datetime


@dataclass
class FlagData:
    flag_type: FLAG_TYPES
    valid_from: datetime
    valid_to: datetime


@dataclass
class DomainsData:
    fqdn: str
    created_at: datetime
    expire_at: datetime
    deleted_at: datetime
    flags: List[FlagData]
