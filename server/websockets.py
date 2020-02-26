"""Provides the WebSocket class."""

from inspect import getdoc
from logging import getLogger

from mindspace_protocol import CommandNotFound
from mindspace_web import WebSocketProtocol

from .db import Player
from .exc import CommandError


class WebSocketCommands:
    """Commands that can be called on connection objects."""

    def alert(self, text):
        """Send an alert down the line."""
        self.send_command('alert', text)

    def message(self, text):
        """Send a message to this connection."""
        self.send_command('message', text)

    def confirm(
        self, message, ok_command, ok_args=None, ok_kwargs=None,
        cancel_command=None, cancel_args=None, cancel_kwargs=None
    ):
        """Send a confirmation box to the client's web browser. If they click
        "OK", cancel_command will be sent back, with attendant args and kwargs.
        If not, cancel_command will be sent back, with attendant args and
        kwargs."""
        if ok_args is None:
            ok_args = []
        if ok_kwargs is None:
            ok_kwargs = {}
        if cancel_args is None:
            cancel_args = []
        if cancel_kwargs is None:
            cancel_kwargs = {}
        self.send_command(
            'confirm', message, ok_command, ok_args, ok_kwargs, cancel_command,
            cancel_args, cancel_kwargs
        )


class WebSocket(WebSocketProtocol, WebSocketCommands):
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
            player_name = self.player.name
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

    @player.setter
    def player(self, value):
        if value is None:
            self.player_id = None
        elif isinstance(value, Player):
            self.player_id = value.id
        else:
            raise RuntimeError('Not a Player instance: %r.' % value)

    def handle_command(self, command_name, *args, **kwargs):
        """Handle a command from the other side."""
        parser = self.factory.mindspace_factory.get_parser(self)
        try:
            return parser.handle_command(command_name, self, *args, **kwargs)
        except CommandError as e:
            self.alert(getdoc(e))
        except CommandNotFound as e:
            self.alert(f'Invalid command: "{e.args[-1]}".')
