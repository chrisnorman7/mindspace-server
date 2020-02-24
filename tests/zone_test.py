from server.db import Zone, ZoneTypes


def test_init(zone):
    assert isinstance(zone, Zone)
    assert zone.type is ZoneTypes.planet


def test_zone_rooms(zone, room):
    assert room in zone.rooms
    assert room.zone_id == zone.id
    assert room.zone is zone
