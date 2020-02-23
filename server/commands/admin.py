"""Provides administrator commands."""

from twisted.internet import reactor

from ..parsers import main_parser, load_commands, admin_required


@main_parser.command(name='reload_commands')
@admin_required
def reload_commands(con):
    """Reload commands."""
    con.logger.info('Reloading commands...')
    load_commands()


@main_parser.command(name='shutdown')
@admin_required
def shutdown(con):
    """Shutdown the server."""
    reactor.stop()
