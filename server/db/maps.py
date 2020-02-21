"""Provides the Map class."""

from random import randint

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base, NameMixin, CreatedMixin, Flag
from .session import session


class Map(Base, NameMixin, CreatedMixin):
    """A map for game play."""

    __tablename__ = 'maps'
    size_x = Column(Integer, nullable=False, default=25)
    size_y = Column(Integer, nullable=False, default=25)

    def broadcast(self, text, sound=None):
        """Broadcast a message to all players on this map."""
        for player in self.players:
            player.message(text)
            if sound is not None:
                player.sound(sound)

    def valid_coordinates(self, x, y):
        """Return True if the given x and y coordinates are valid."""
        return x >= 0 and x <= self.size_x and y >= 0 and y <= self.size_y

    def random_coordinates(self):
        """Return random coordinates on this map."""
        x = randint(0, self.size_x)
        y = randint(0, self.size_y)
        return x, y

    def add_owner(self, player, **kwargs):
        """Add an owner to this map."""
        return MapOwner(player_id=player.id, map_id=self.id, **kwargs)

    def remove_owner(self, player):
        """Stop the given player from having ownership over this map."""
        res = MapOwner.query(map_id=self.id, player_id=player.id).delete()
        session.commit()
        return res


class MapOwner(Base, CreatedMixin):
    """Used so that more than 1 player can edit a map."""

    __tablename__ = 'map_owners'
    player_id = Column(Integer, ForeignKey('players.id'), nullable=False)
    player = relationship('Player', backref='maps')
    map_id = Column(Integer, ForeignKey('maps.id'), nullable=False)
    map = relationship('Map', backref='owners')
    can_edit = Flag(True)
    can_add_objects = Flag(True)
    can_remove_objects = Flag(True)
    can_add_entrances = Flag(True)
    can_remove_entrances = Flag(True)
    can_add_exits = Flag(True)
    can_remove_exits = Flag(True)
