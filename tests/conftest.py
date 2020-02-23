from pytest import fixture

from server.db import Map, Player, Base

password = 'TestPassword123'


@fixture(scope='session', autouse=True)
def create_stuff():
    Base.metadata.create_all()


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
