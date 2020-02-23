"""Provides administrator commands."""

from twisted.internet import reactor

from ..parsers import parser, load_commands, admin_required


@parser.command(name='reload_commands')
@admin_required
def reload_commands(con):
    """Reload commands."""
    con.logger.info('Reloading commands...')
    load_commands()


@parser.command(name='shutdown')
@admin_required
def shutdown(con):
    """Shutdown the server."""
    reactor.stop()
