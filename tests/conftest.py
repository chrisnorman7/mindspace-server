from logging import getLogger

from attr import attrs, attrib, Factory
from pytest import fixture

from server.db import Room, Player, Base, Zone, ZoneTypes
from server.parsers import load_commands
from server.websockets import WebSocketCommands

NoneType = type(None)
password = 'TestPassword123'
logger = getLogger(__name__)


@attrs
class PretendConnection(WebSocketCommands):
    """A pretend connection object. Used for testing."""

    command_args = None
    command_kwargs = None
    player_id = attrib(default=Factory(NoneType))
    logger = attrib(default=Factory(lambda: logger))

    @property
    def player(self):
        if self.player_id is not None:
            return Player.get(self.player_id)

    def send_command(self, *args, **kwargs):
        """Set self.command."""
        self.command_args = args
        self.command_kwargs = kwargs


@fixture(scope='session', autouse=True)
def initialise():
    Base.metadata.create_all()
    Zone(name='Test Zone', type=ZoneTypes.planet).save()
    load_commands()


@fixture(name='zone')
def get_zone():
    return Zone.first()


@fixture(name='room')
def get_room(zone):
    r = Room(name='Test Room', zone=zone)
    r.save()
    return r


@fixture(name='player')
def get_player():
    p = Player.create('test', 'test123', 'Test Player')
    p.save()
    return p


@fixture(name='password')
def get_password():
    return password


@fixture(name='player')
def new_player(password):
    Player.delete_all()
    p = Player.create('test', password, 'Test Player')
    p.save()
    return p


@fixture(name='con')
def get_connection():
    return PretendConnection()
