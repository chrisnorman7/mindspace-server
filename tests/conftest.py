from attr import attrs, attrib, Factory
from pytest import fixture

from server.db import Map, Player, Base
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
    load_commands()


@fixture(name='map')
def get_map():
    m = Map(name='Test Map')
    m.save()
    return m


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
