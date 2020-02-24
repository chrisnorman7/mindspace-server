"""Provides the Player class."""

from passlib.hash import sha512_crypt
from sqlalchemy import Column, String, Float
from twisted.internet import reactor

from .base import Base, NameMixin, LocationMixin, CoordinatesMixin, Flag
from .maps import MapOwner

from ..exc import InvalidUsername, InvalidPassword
from ..socials import factory
from ..util import pluralise

crypt = sha512_crypt.using(rounds=10000)
connections = {}


class Player(Base, NameMixin, CoordinatesMixin, LocationMixin):
    """A player."""

    __tablename__ = 'players'
    username = Column(String(25), nullable=False)
    password = Column(String(120), nullable=False)
    admin = Flag(False)
    connected = Flag(False)
    volume = Column(Float, nullable=False, default=0.05)
    code = Column(String(1000), nullable=True)

    @classmethod
    def create(cls, username, password, name):
        """Create a new user."""
        p = cls(username=username, name=name)
        p.set_password(password)
        return p

    @classmethod
    def authenticate(cls, username, password):
        """Return a Player object, or raise an exception."""
        p = cls.query(username=username).first()
        if p is None:
            raise InvalidUsername
        if p.check_password(password):
            return p
        raise InvalidPassword

    def set_password(self, password):
        """Give this player a new password."""
        self.password = crypt.hash(password)

    def check_password(self, password):
        """Check this player's password against the supplied password."""
        return crypt.verify(password, self.password)

    @property
    def connection(self):
        return connections.get(self.id, None)

    @connection.setter
    def connection(self, value):
        if value is None:
            if self.id in connections:
                del connections[self.id]
        else:
            old = self.connection
            if old is not None:
                old.message('Logging you in from somewhere else.')
                old.player_id = None
                old.send('disconnecting')
                old.dropConnection()
            self.connected = True
            connections[self.id] = value

    def message(self, string):
        """Send a message to this player's connection."""
        if self.connection is None:
            return False
        self.connection.message(string)
        return True

    @property
    def neighbours(self):
        """Return the players in the same map as this player, excluding this
        player."""
        cls = type(self)
        return cls.query(
            cls.id != self.id, cls.location_id == self.location_id
        )

    def move(self, x, y):
        """Move this player to the given coordinates."""
        self.x = x
        self.y = y
        self.save()

    def do_social(
        self, string, perspectives=None, sound=None, local=False, **kwargs
    ):
        """Perform a social in the context of this player. If perspectives is a
        list, add it to a list containing this player, to form a full
        perspectives list."""
        if perspectives is None:
            perspectives = []
        perspectives.insert(0, self)
        strings = factory.get_strings(string, perspectives, **kwargs)
        filter_args = []
        if local:
            filter_kwargs = self.same_coordinates()
        else:
            filter_kwargs = dict(location_id=self.location_id)
        cls = type(self)
        for player in cls.query(*filter_args, **filter_kwargs):
            try:
                index = perspectives.index(player)
            except (ValueError, IndexError):
                index = -1
            player.message(strings[index])
            if sound is not None:
                player.sound(sound)

    def disconnect(self):
        """Disconnect this player."""
        if self.connection is None:
            return False
        self.connection.transport.loseConnection()
        return True

    def call_later(self, time, *args, **kwargs):
        """Use reactor.callLater to schedule something, telling the player how
        long they have to wait."""
        reactor.callLater(time, *args, **kwargs)
        self.message(f'({time} {pluralise(time, "second")})')

    @classmethod
    def message_admins(cls, string, sound='admin.wav'):
        """Send all connected admins the provided string."""
        for p in cls.all(admin=True, connected=True):
            if sound is not None:
                p.sound(sound)
            p.message(string)

    def delete(self):
        """First delete all MapOwner instances."""
        MapOwner.query(player_id=self.id).delete()
        return super().delete()
