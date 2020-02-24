from pytest import raises

from server.db import Player
from server.exc import InvalidUsername, InvalidPassword


def test_player_create():
    username = 'username'
    password = 'password'
    name = 'This player is a test'
    p = Player.create(username, password, name)
    p.save()
    assert p.username == username
    assert p.name == name
    assert p.check_password(password) is True


def test_player_authenticate(password, player):
    assert Player.authenticate(player.username, password) is player
    with raises(InvalidUsername):
        Player.authenticate('Not a username', 'Not a password.')
    with raises(InvalidPassword):
        Player.authenticate(player.username, 'Invalid Password.')


def test_player_check_password(password, player):
    assert player.check_password(password) is True
    assert player.check_password('Wrong') is False


def test_player_set_password():
    p = Player.create('test player', 'some password', 'test name')
    p.set_password('new')
    assert p.check_password('new') is True


def test_player_location(player, room):
    player.location_id = None
    player.save()
    assert player.location is None
    assert room.players == []
    player.location = room
    player.save()
    assert room.players == [player]
