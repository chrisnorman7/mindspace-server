"""Provides the room class."""

from random import randint

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base, NameMixin, CreatedMixin, Flag
from .session import session


class Room(Base, NameMixin, CreatedMixin):
    """A room for game play."""

    __tablename__ = 'rooms'
    size_x = Column(Integer, nullable=False, default=25)
    size_y = Column(Integer, nullable=False, default=25)
    zone_id = Column(Integer, ForeignKey('zones.id'), nullable=False)
    zone = relationship('Zone', backref='rooms')

    def broadcast(self, text, sound=None):
        """Broadcast a message to all players on this room."""
        for player in self.players:
            player.message(text)
            if sound is not None:
                player.sound(sound)

    def valid_coordinates(self, x, y):
        """Return True if the given x and y coordinates are valid."""
        return x >= 0 and x <= self.size_x and y >= 0 and y <= self.size_y

    def random_coordinates(self):
        """Return random coordinates on this room."""
        x = randint(0, self.size_x)
        y = randint(0, self.size_y)
        return x, y

    def add_owner(self, player, **kwargs):
        """Add an owner to this room."""
        return RoomOwner(player_id=player.id, room_id=self.id, **kwargs)

    def remove_owner(self, player):
        """Stop the given player from having ownership over this room."""
        res = RoomOwner.query(room_id=self.id, player_id=player.id).delete()
        session.commit()
        return res


class RoomOwner(Base, CreatedMixin):
    """Used so that more than 1 player can edit a room."""

    __tablename__ = 'room_owners'
    player_id = Column(Integer, ForeignKey('players.id'), nullable=False)
    player = relationship('Player', backref='rooms')
    room_id = Column(Integer, ForeignKey('rooms.id'), nullable=False)
    room = relationship('Room', backref='owners')
    can_edit = Flag(True)
    can_add_objects = Flag(True)
    can_remove_objects = Flag(True)
    can_add_entrances = Flag(True)
    can_remove_entrances = Flag(True)
    can_add_exits = Flag(True)
    can_remove_exits = Flag(True)
