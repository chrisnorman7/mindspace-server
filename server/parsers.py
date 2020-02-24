"""Provides the various parsers used by the game."""

from sys import modules as _sys_modules
from logging import getLogger
from importlib import import_module, invalidate_caches
from os import listdir
from os.path import dirname, join, relpath, splitext

from mindspace_protocol import MindspaceParser

from .exc import MustBeAdmin, NotWhileLoggedIn

logger = getLogger(__name__)
_module_names = []

parser = MindspaceParser()


def load_commands():
    """Import all files from server/commands."""
    invalidate_caches()
    parser.commands.clear()
    for name in _module_names:
        if name in _sys_modules:
            del _sys_modules[name]
    path = relpath(dirname(__file__))
    path = join(path, 'commands')
    logger.info('Importing command files from "%s".', path)
    for filename in sorted(listdir(path)):
        if filename.startswith('_'):
            continue
        name = splitext(filename)[0]
        package = f'{__package__}.commands.{name}'
        logger.info('Loading file %s as %s.', filename, package)
        module = import_module(package, package='.commands')
        assert _sys_modules[module.__name__] is module
        _module_names.append(module.__name__)


def parser_decorator(decorated):
    """Decorate a function so that it can be used as a decorator after the
    parser.command decorator."""

    def outer(func):
        def inner(con, *args, **kwargs):
            """Give decorated(con) chance to raise something."""
            decorated(con)
            return func(con, *args, **kwargs)
        return inner
    return outer


@parser_decorator
def admin_required(con):
    """If the given player is not an admin, PermissionsError is raised."""
    if con.player_id is None or not con.player.admin:
        raise MustBeAdmin()


@parser_decorator
def anonymous(con):
    """Must be called by a non-logged in connection."""
    if con.player_id is not None:
        raise NotWhileLoggedIn()
