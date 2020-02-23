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


def admin_required(func):
    """If the given player is not an admin, PermissionsError is raised."""
    def inner(con, *args, **kwargs):
        if con.player_id is not None and con.player.admin:
            return func(con, *args, **kwargs)
        raise MustBeAdmin()
    return inner


def anonymous(func):
    """Must be called by a non-logged in connection."""
    def inner(con, *args, **kwargs):
        if con.player_id is None:
            return func(con, *args, **kwargs)
        raise NotWhileLoggedIn()
    return inner
