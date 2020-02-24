"""Provides the Zone class, and ZoneType enumeration."""

from enum import Enum as _Enum

from sqlalchemy import Column, Enum

from .base import Base, NameDescriptionMixin, CoordinatesMixin, OwnerMixin


class ZoneTypes(_Enum):
    """The possible types for zones."""

    star = 0
    planet = 1
    moon = 2
    asteroid = 3
    station = 4
    starship = 5
    blackhole = 6


class Zone(Base, NameDescriptionMixin, CoordinatesMixin, OwnerMixin):
    """A planet, star, ship, or something else spaceborn."""

    __tablename__ = 'zones'
    type = Column(Enum(ZoneTypes), nullable=False)
