from server.db import Map, MapOwner


def test_init(map):
    assert isinstance(map, Map)
    assert map.name is not None
    assert map.owners == []


def test_add_owner(map, player):
    assert map.owners == []
    o = map.add_owner(player)
    o.save()
    assert isinstance(o, MapOwner)
    assert o.player is player
    assert o.map is map
    assert o in map.owners
    assert o in player.maps


def test_remove_owner(map, player):
    map.add_owner(player).save()
    assert len(map.owners) == 1
    assert map.remove_owner(player) == 1
    assert len(map.owners) == 0
