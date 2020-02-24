from server.db import Room, RoomOwner


def test_init(room):
    assert isinstance(room, Room)
    assert room.name is not None
    assert room.owners == []


def test_add_owner(room, player):
    assert room.owners == []
    o = room.add_owner(player)
    o.save()
    assert isinstance(o, RoomOwner)
    assert o.player is player
    assert o.room is room
    assert o in room.owners
    assert o in player.rooms


def test_remove_owner(room, player):
    room.add_owner(player).save()
    assert len(room.owners) == 1
    assert room.remove_owner(player) == 1
    assert len(room.owners) == 0
