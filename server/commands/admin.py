from ..parsers import main_parser, load_commands


@main_parser.command
def reload_commands(con):
    """Reload commands."""
    con.logger.info('Reloading commands...')
    load_commands()
