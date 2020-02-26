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
        con.player = player
        player.connection = con
        con.message(f'Welcome back, {player.name}.')
        con.send_command('authenticated', player.name)
    except AuthenticationError:
        con.confirm(
            'Invalid login.\n\nWould you like to create a new character?',
            'urlopen', ok_args=['/register/'], cancel_command='quit'
        )


@parser.command
def quit(con):
    """Drop the connection."""
    con.dropConnection()


@parser.command
def urlopen(con, url):
    """Send the same command back to the client."""
    con.urlopen(url)
