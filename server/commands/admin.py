"""Provides administrator commands."""

from twisted.internet import reactor

from ..parsers import main_parser, load_commands, admin_required


@main_parser.command
def reload_commands(con):
    """Reload commands."""
    admin_required(con.player)
    con.logger.info('Reloading commands...')
    load_commands()


@main_parser.command
def shutdown(con):
    """Shutdown the server."""
    admin_required(con.player)
    reactor.stop()
