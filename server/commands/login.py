"""Provides the "login" command."""

from ..db import Player
from ..parsers import parser, anonymous

from ..exc import AuthenticationError


@parser.command(name='login')
@anonymous
def login(con, username, password):
    """Try to log in with the given credentials."""
    try:
        player = Player.authenticate(username, password)
        print(player)
    except AuthenticationError:
        con.alert('Invalid login.')
        con.dropConnection()
