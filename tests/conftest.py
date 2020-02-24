from attr import attrs, attrib, Factory
from pytest import fixture

from server.db import Room, Player, Base, Zone, ZoneTypes
from server.parsers import load_commands

NoneType = type(None)
password = 'TestPassword123'


@attrs
class PretendConnection:
    player_id = attrib(default=Factory(NoneType))

    @property
    def player(self):
        if self.player_id is not None:
            return Player.get(self.player_id)


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
