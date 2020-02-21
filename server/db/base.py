"""Provides the Base class for database tables."""

from datetime import datetime
from inspect import isclass

from sqlalchemy import (
    Column, Integer, String, ForeignKey, inspect, DateTime, Boolean
)
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base, declared_attr

from .engine import engine
from .session import session


class _Base:
    """Create a primary key and some useful methods."""

    id = Column(Integer, primary_key=True)

    def save(self):
        """Save this object."""
        session.add(self)
        try:
            session.commit()
        except DatabaseError:
            session.rollback()
            raise

    def delete(self):
        session.delete(self)
        try:
            session.commit()
        except DatabaseError:
            session.rollback()
            raise

    @classmethod
    def query(cls, *args, **kwargs):
        """Return a query object with this class."""
        return session.query(cls).filter(*args).filter_by(**kwargs)

    @classmethod
    def count(cls, *args, **kwargs):
        """Return the number of instances of this class in the database."""
        return cls.query(*args, **kwargs).count()

    @classmethod
    def delete_all(cls, *args, **kwargs):
        """Delete all rows which are matched by cls.query(*args, **kwargs).
        Each object's delete method is called."""
        for obj in cls.query(*args, **kwargs):
            obj.delete()

    @classmethod
    def first(cls, *args, **kwargs):
        """Return the first instance of this class in the database."""
        return cls.query(*args, **kwargs).first()

    @classmethod
    def get(cls, id):
        """Get an object with the given id."""
        return cls.query().get(id)

    @classmethod
    def one(cls, *args, **kwargs):
        return cls.query(*args, **kwargs).one()

    @classmethod
    def all(cls, *args, **kwargs):
        """Return all child objects."""
        return cls.query(*args, **kwargs).all()

    @classmethod
    def classes(cls):
        """Return all table classes."""
        for item in cls._decl_class_registry.values():
            if isclass(item) and issubclass(item, cls):
                yield item

    @classmethod
    def number_of_objects(cls):
        """Returns the number of objects in the database."""
        count = 0
        for base in cls.classes():
            count += base.count()
        return count

    def __repr__(self):
        name = type(self).__name__
        string = '%s (' % name
        attributes = []
        i = inspect(type(self))
        for column in i.c:
            name = column.name
            attributes.append('%s=%r' % (name, getattr(self, name)))
        string += ', '.join(attributes)
        return string + ')'

    @classmethod
    def get_class_from_table(cls, table):
        """Return the class whose __table__ attribute is the provided Table
        instance."""
        for value in cls._decl_class_registry.values():
            if getattr(value, '__table__', None) is table:
                return value


Base = declarative_base(bind=engine, cls=_Base)


class CreatedMixin:
    created = Column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow
    )


class CoordinatesMixin:
    x = Column(Integer, nullable=False, default=0)
    y = Column(Integer, nullable=False, default=0)

    @property
    def coordinates(self):
        return self.x, self.y

    @coordinates.setter
    def coordinates(self, value):
        self.x, self.y = value

    def distance_to(self, other):
        """Return the distance between this object and other."""
        dx = max(self.x, other.x) - min(self.x, other.x)
        dy = max(self.y, other.y) - min(self.y, other.y)
        return max(dx, dy)

    def directions_to(self, other):
        """Return textual directions to an object other."""
        if other.x == self.x:
            direction_x = None
        elif other.x > self.x:
            direction_x = 'east'
        else:
            direction_x = 'west'
        if other.y == self.y:
            direction_y = None
        elif other.y > self.y:
            direction_y = 'north'
        else:
            direction_y = 'south'
        if direction_y is not None:
            dy = max(self.y, other.y) - min(self.y, other.y)
            string = f'{dy} {direction_y}'
        else:
            string = ''
        if direction_x is not None:
            dx = max(self.x, other.x) - min(self.x, other.x)
            if string:
                string += ', '
            string += f'{dx} {direction_x}'
        if string:
            return string
        return 'here'


class NameMixin:
    name = Column(String(30), nullable=False)

    @classmethod
    def alphabetized(cls, *args, **kwargs):
        """Return a list of items, sorted by name."""
        return cls.query(*args, **kwargs).order_by(cls.name)


class DescriptionMixin:
    description = Column(String(1000), nullable=True)

    def get_description(self):
        return self.description or 'You see nothing special.'


class LocationMixin:
    @declared_attr
    def location_id(cls):
        return Column(Integer, ForeignKey('maps.id'), nullable=True)

    @declared_attr
    def location(cls):
        return relationship(
            'Map', backref=cls.__tablename__, foreign_keys=[cls.location_id],
            remote_side='Map.id'
        )

    def same_coordinates(self):
        """Return a set of query-ready args representing this player's current
        location and coordinates."""
        return dict(location_id=self.location_id, x=self.x, y=self.y)


class OwnerMixin:
    owned_since = Column(DateTime(timezone=True), nullable=True)

    @declared_attr
    def owner_id(cls):
        return Column(Integer, ForeignKey('players.id'), nullable=True)

    @declared_attr
    def owner(cls):
        return relationship(
            'Player', backref=backref(
                f'owned_{cls.__tablename__}', order_by=cls.owned_since
            ), foreign_keys=[cls.owner_id], remote_side='Player.id'
        )

    def set_owner(self, value):
        """Set self.owner, and update self.owned_since."""
        self.owner = value
        if value is None:
            self.owned_since = None
        else:
            self.owned_since = datetime.utcnow()


def Flag(default, nullable=False):
    """Return a Colum instance, representing a boolean."""
    return Column(Boolean, nullable=nullable, default=default)
