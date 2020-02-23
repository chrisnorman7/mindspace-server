"""Provides the various parsers used by the game."""

from sys import modules as _sys_modules
from logging import getLogger
from importlib import import_module, invalidate_caches
from os import listdir
from os.path import dirname, join, relpath, splitext

from attr import attrs, attrib
from mindspace_protocol import MindspaceParser

from .exc import MustBeAdmin

logger = getLogger(__name__)
_module_names = []


@attrs
class _Parser:
    """Add a name argument."""
    name = attrib()


@attrs
class Parser(_Parser, MindspaceParser):
    pass


login_parser = Parser('Login')
main_menu_parser = Parser('Main Menu')
main_parser = Parser('Main')


def load_commands():
    """Import all files from server/commands."""
    invalidate_caches()
    for parser in (login_parser, main_menu_parser, main_parser):
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


def admin_required(player):
    """If the given player is not an admin, PermissionsError is raised."""
    if player is None or not player.admin:
        raise MustBeAdmin()
