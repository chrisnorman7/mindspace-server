from pytest import fixture

from server.db import Map, Player, Base


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
