"""Provides the WebSocket class."""

from inspect import getdoc
from logging import getLogger

from mindspace_protocol import CommandNotFound
from mindspace_web import WebSocketProtocol

from .db import Player
from .exc import CommandError


class WebSocket(WebSocketProtocol):
    def connectionMade(self):
        """Create a logger."""
        super().connectionMade()
        self.player_id = None
        self.set_logger()
        self.logger.info('Connected.')
        peer = self.transport.getPeer()
        Player.message_admins(f'Incoming connection from {peer.host}.')

    def connectionLost(self, reason):
        super().connectionLost(reason)
        self.logger.info(reason.getErrorMessage())
        if self.player is not None:
            self.player.connected = False
            self.player.connection = None
            player_name = self.player.get_name()
        else:
            player_name = self.transport.getPeer().host
        Player.message_admins(f'{player_name} has disconnected.')

    def set_logger(self, player=None):
        """Set self.logger to a logger with a sensible name."""
        if player is None:
            peer = self.transport.getPeer()
            name = f'{peer.host}:{peer.port}'
        else:
            name = f'{player.name} (#{player.id})'
        self.logger = getLogger(name)

    def authenticated(self, player):
        """This connection has successfully logged in as the given Player
        instance."""
        player.sound('authenticated.wav')
        self.player_id = player.id
        self.message('Welcome, %s.' % player.name)
        player.send_title()
        self.send("authenticated")
        self.set_logger(player=player)
        self.logger.info('Authenticated.')
        for p in Player.all(admin=True):
            p.message(f'{player.get_name()} has connected.')

    @property
    def player(self):
        if self.player_id is not None:
            return Player.get(self.player_id)

    def alert(self, text):
        """Send an alert down the line."""
        self.send_command('alert', text)

    def handle_command(self, command_name, *args, **kwargs):
        """Handle a command from the other side."""
        parser = self.factory.mindspace_factory.get_parser(self)
        try:
            return parser.handle_command(command_name, self, *args, **kwargs)
        except CommandError as e:
            self.alert(getdoc(e))
        except CommandNotFound as e:
            self.alert(f'Invalid command: "{e.args[-1]}".')
